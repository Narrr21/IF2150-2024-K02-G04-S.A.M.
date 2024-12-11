# IF2150-2024-K02-G04-S.A.M

python -m venv venv

windows : venv\Scripts\activate
macOS / linux : source venv/bin/activate

pip install -r requirements.txt
pip install -e .

to exit venv : deactivate

if adding depedencies:

- set PYTHONIOENCODING=ascii
- pip freeze > requirements.txt

if adding new admin:

- add to admins.json

```json
  {
  "admin1": {
    "password_hash": "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8",
    "role": "admin"
  },
  "admin2": {
    "password_hash": "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8",
    "role": "admin"
  },
  "admin3": {
    "password_hash": "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8",
    "role": "admin"
  }
}
```

> password_hash is the hash of the password
> role is the role of the admin
