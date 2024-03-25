# main.py
"""
Este proyecto inició el día 17 de Marzo del 2024. El mismo día del fallecimiento de Laura Ortiz Castillo, mi querida abuela, que en paz descanse. 

Fuste una increíble mujer y la mejor abuela que podría pedir. Te amaré siempre y te extrañaré mucho. Este proyecto va dedicado a ti, con todo mi amor. 

Gracias por todo...
"""

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
    uvicorn.run(app, host="0.0.0.0", port=80)
