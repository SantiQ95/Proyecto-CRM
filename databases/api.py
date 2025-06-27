from fastapi import FastAPI
from dotenv import load_dotenv
import os
import threading
import webbrowser
import time

# Load environment variables
load_dotenv()

# FastAPI instance
app = FastAPI(
    title="EvolveCRM API",
    description="Public API for managing users, invoices, and reports",
    version="1.2.3"
)

# ——— Routers ———
from routes.auth_routes import router as auth_router
from routes.param_routes import router as param_router

app.include_router(auth_router)
app.include_router(param_router)

# ——— Dev Launch Enhancer ———
if __name__ == "__main__":
    def abrir_docs():
        time.sleep(1.5)
        webbrowser.open("http://127.0.0.1:8000/docs")

    threading.Thread(target=abrir_docs).start()

    import uvicorn
    uvicorn.run("databases.api:app", host="127.0.0.1", port=8000, reload=True)
