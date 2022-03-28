@echo off

source venv\bin\activate
pip install -r requirements.txt
DEL  log.log
python3 client.py

@echo on
echo "Le client discord ce lance"
deactivate