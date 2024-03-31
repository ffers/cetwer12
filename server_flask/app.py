from fastapi import FastAPI
import uvicorn, multiprocessing, logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),  # Для виведення на консоль
        logging.FileHandler("../common_asx/log/all_app.log"),  # Для запису у файл
    ]
)


app = FastAPI()
@app.get("/v2")
def read_main():
    logging.info("Обробка app на головну сторінку")
    return {"message": "Hello World"}

def main():
    uvicorn.run(
        "server_flask.flask_app:app",
        log_level="debug",
        reload=True
    )