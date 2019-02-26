# Flask Git Repositories

Create Python virtual env:

Linux
```
python -m virtualenv env
```

Windows
```
python -m venv env
```

Activate vritual env:

Linux

```
source env/bin/activate
```

Windows

```
env/scripts/activate
```

Install requirements.txt
```
pip install -r requirements.txt
```

Run on Linux:
```
export FLASK_APP=manage.py
flask run
```

Run on Windows with PS:
```
$env:FLASK_APP = "manage.py"
flask run
```
