import json
import os
import hashlib
from typing import Tuple, Optional
from datetime import datetime, timedelta
import uuid

class LoginManager:
    def __init__(self):
        # initialize admin data and session files
        self.admins_file = "admins.json"
        self.session_file = "session.json"
        self._init_storage()

    def _init_storage(self) -> None:
        # create admins.json if it doesn't exist
        if not os.path.exists(self.admins_file):
            with open(self.admins_file, 'w') as f:
                json.dump({}, f)

    def _hash_password(self, password: str) -> str:
        # hash the password using SHA-256
        return hashlib.sha256(password.encode()).hexdigest()

    def _save_session(self, user_data: dict, session_id: str) -> None:
        # save session data to local file
        session_data = {
            "session_id": session_id,
            "username": user_data["username"],
            "role": user_data["role"],
            "expires_at": (datetime.utcnow() + timedelta(days=1)).isoformat(),
            "password_hash": user_data["password_hash"]
        }
        
        with open(self.session_file, 'w') as f:
            json.dump(session_data, f, indent=4)

    def _load_session(self) -> Optional[dict]:
        # load session data from local file
        try:
            if not os.path.exists(self.session_file):
                return None
                
            with open(self.session_file, 'r') as f:
                session_data = json.load(f)
                
            # Check if session has expired
            expires_at = datetime.fromisoformat(session_data["expires_at"])
            if datetime.utcnow() > expires_at:
                self.logout()
                return None
                
            return session_data
        except Exception:
            return None

    def _get_users(self) -> dict:
        # load admins data from JSON file
        with open(self.admins_file, 'r') as f:
            return json.load(f)

    def _save_users(self, users: dict) -> None:
        # save admins data to JSON file
        with open(self.admins_file, 'w') as f:
            json.dump(users, f, indent=4)

    def login(self, username: str, password: str) -> Tuple[bool, str]:
        """
        Authenticate user and create a new session
        return: Tuple[isLoggedIn, message]
        """
        try:
            if not username or not password:
                return False, "Username and password cannot be empty"
            
            users = self._get_users()
            password_hash = self._hash_password(password)
            
            if username not in users:
                return False, "Invalid username or password"
                
            user = users[username]
            if user["password_hash"] != password_hash:
                return False, "Invalid username or password"
            
            session_id = str(uuid.uuid4())
            user_data = {
                "username": username,
                "role": user["role"],
                "password_hash": password_hash
            }
            self._save_session(user_data, session_id)
            return True, "Login successful"
            
        except Exception as e:
            return False, f"Login failed: {str(e)}"

    def logout(self) -> Tuple[bool, str]:
        # delete the current session
        try:
            if os.path.exists(self.session_file):
                os.remove(self.session_file)
            return True, "Logout successful"
        except Exception as e:
            return False, f"Logout failed: {str(e)}"

    def verify_session(self) -> Tuple[bool, Optional[dict], str]:
        # verify if there's an active session and return user data
        try:
            session_data = self._load_session()
            if not session_data:
                return False, None, "No active session"

            users = self._get_users()
            username = session_data["username"]
            
            # verify user still exists and password hasn't changed
            if (username not in users or 
                users[username]["password_hash"] != session_data["password_hash"]):
                self.logout()
                return False, None, "Session invalid"

            return True, session_data, "Session valid"
            
        except Exception as e:
            return False, None, f"Session verification failed: {str(e)}"
