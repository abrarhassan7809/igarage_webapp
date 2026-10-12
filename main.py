from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.config import STATIC_DIR
from app.routers import pages, api
from db_config.database import Base, engine
import uvicorn

app = FastAPI(title="i Garage")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
app.include_router(pages.router)
app.include_router(api.router, prefix="/api")

Base.metadata.create_all(engine)

# Run: uvicorn main:app --reload
if __name__ == "__main__":
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)