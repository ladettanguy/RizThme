if [ -f ".env" ]; then
  poetry run source .env
fi

poetry run python3.10 run.py