from loginManager import LoginManager

def print_menu():
    print("\nAvailable methods to test:")
    print("1. Login")
    print("2. Logout")
    print("3. Verify Session")
    print("4. Exit")
    print("\nChoose a method to test (1-4):", end=" ")

def test_login(login_manager):
    print("\n=== Testing Login ===")
    username = input("Enter username: ")
    password = input("Enter password: ")
    
    success, message = login_manager.login(username, password)
    print(f"\nResult: {message}")

def test_logout(login_manager):
    print("\n=== Testing Logout ===")
    success, message = login_manager.logout()
    print(f"\nResult: {message}")

def test_verify_session(login_manager):
    print("\n=== Testing Verify Session ===")
    is_valid, session_data, message = login_manager.verify_session()
    
    print(f"\nResult: {message}")
    if is_valid:
        print("\nSession Data:")
        print(f"Username: {session_data['username']}")
        print(f"Role: {session_data['role']}")
        print(f"Session ID: {session_data['session_id']}")
        print(f"Expires at: {session_data['expires_at']}")

def main():
    login_manager = LoginManager()
    
    while True:
        print_menu()
        
        try:
            choice = input()
            
            if choice == "1":
                test_login(login_manager)
            elif choice == "2":
                test_logout(login_manager)
            elif choice == "3":
                test_verify_session(login_manager)
            elif choice == "4":
                print("\nExiting test program. Goodbye!")
                break
            else:
                print("\nInvalid choice. Please choose 1-4.")
            
            # Ask if user wants to continue testing (default is yes)
            continue_testing = input("\nDo you want to test another method? [Y/n]: ").lower()
            if continue_testing == 'n':
                print("\nExiting test program. Goodbye!")
                break
                
        except Exception as e:
            print(f"\nAn error occurred: {str(e)}")
            continue_testing = input("\nDo you want to test another method? [Y/n]: ").lower()
            if continue_testing == 'n':
                print("\nExiting test program. Goodbye!")
                break

if __name__ == "__main__":
    main()
