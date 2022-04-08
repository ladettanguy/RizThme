@echo off

source venv\bin\activate
pip install -r requirements.txt
DEL  log.log
python3 run.py

@echo on
echo "Le client discord ce lance"
deactivate