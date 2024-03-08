from backend_server.fastapi_app import app
import uvicorn


uvicorn.run(app, host="0.0.0.0", port=8080)