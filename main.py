# main.py
from fastapi import FastAPI
from app.routes.authRoute import routerAuth
from app.routes.relationRoute import routerRelation
from app.routes.messageRoute import routerMessage
from app.routes.moviesRoute import routerMovie

app = FastAPI()

app.include_router(routerAuth)
app.include_router(routerRelation)
app.include_router(routerMessage)
app.include_router(routerMovie)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
