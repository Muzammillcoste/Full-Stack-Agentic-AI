from server import app
from uvicorn import run

def main():
    run(app, host="127.0.0.1", port=8000)

main()