set FLASK_APP=run.py
#set FLASK_ENV=development
set FLASK_ENV=development
set PREV_PYTHONPATH = %PYTHONPATH%
set PYTHONPATH=%PYTHONPATH%;.\;.
flask run
set PYTHONPATH=%PREV_PYTHONPATH%