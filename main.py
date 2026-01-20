from fastapi import FastAPI

from routes import cart, orders

app = FastAPI(title="Movie Store API")

app.include_router(cart.router)
app.include_router(orders.router)


@app.get("/")
def root():
    return {"status": "ok"}

