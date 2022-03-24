source  venv/bin/activate

pip install -r requirements.txt > temp.txt

rm temp.txt

rm log.txt

python3 client.py > log.txt & echo "Le client discord ce lance"

deactivate
