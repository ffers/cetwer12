from fastapi import FastAPI
import uvicorn, multiprocessing


app = FastAPI()
@app.get("/v2")
def read_main():
    return {"message": "Hello World"}

def main():
    uvicorn.run(
        "server_flask.flask_app:app",
        log_level="debug",
        reload=True
    )