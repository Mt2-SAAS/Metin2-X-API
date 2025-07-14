from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
# Local Imports
from .database import BaseSaveModel, engine
from .api.routes import account, game

# Crear las tablas en la base de datos
BaseSaveModel.metadata.create_all(bind=engine)


app = FastAPI(
    title="Mi API con FastAPI",
    description="Una API construida con FastAPI y SQLAlchemy",
    version="1.0.0"
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(account.router, prefix="/api/v1")
app.include_router(game.router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "¡Bienvenido a mi API con FastAPI y SQLAlchemy!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
