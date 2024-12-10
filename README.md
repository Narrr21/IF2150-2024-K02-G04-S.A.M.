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
