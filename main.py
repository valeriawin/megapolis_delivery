from fastapi import FastAPI
import uvicorn

from routers import add_zone, add_deliveryman, deliver

app = FastAPI()

app.include_router(add_zone.router)
app.include_router(add_deliveryman.router)
app.include_router(deliver.router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
