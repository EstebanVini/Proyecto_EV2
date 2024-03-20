# main.py
from fastapi import FastAPI
from app.routes.authRoute import routerAuth
from app.routes.relationRoute import routerRelation

app = FastAPI()

app.include_router(routerAuth)
app.include_router(routerRelation)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
