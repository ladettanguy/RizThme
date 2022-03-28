source  venv/bin/activate > /dev/null
pip install -r requirements.txt > /dev/null
rm -f log.txt
python3 client.py > /dev/null &

echo "Le client discord ce lance"

deactivate
