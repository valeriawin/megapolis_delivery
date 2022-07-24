from routers import add_zone, add_deliveryman, deliver
from main import app

app.include_router(add_zone.router)
app.include_router(add_deliveryman.router)
app.include_router(deliver.router)