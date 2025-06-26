from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# Local Imports
#from .database import account_engine, player_engine, BaseSaveAccountModel, BaseSavePlayerModel
from .api.routes import account, player, guild

# Crear las tablas en la base de datos
#BaseSaveAccountModel.metadata.create_all(bind=account_engine)
#BaseSavePlayerModel.metadata.create_all(bind=player_engine)

app = FastAPI(
    title="Mi API con FastAPI",
    description="Una API construida con FastAPI y SQLAlchemy",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(account.router, prefix="/api")
app.include_router(player.router, prefix="/api")
app.include_router(guild.router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "¡Bienvenido a mi API con FastAPI y SQLAlchemy!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
