# main.py
from fastapi import FastAPI
from app.routes.authRoute import routerAuth

app = FastAPI()

app.include_router(routerAuth)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
