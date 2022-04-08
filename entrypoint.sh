source  venv/bin/activate > /dev/null
pip install -r requirements.txt > /dev/null
rm -f log.log
python3 run.py > /dev/null &

echo "Le client discord ce lance"

deactivate
