from fastapi import FastAPI

from routes import cart, orders, movies, users, profiles

app = FastAPI(title="Movie Store API")

app.include_router(cart.router)
app.include_router(orders.router)
app.include_router(movies.router)
app.include_router(users.router)
app.include_router(profiles.router)

@app.get("/")
def root():
    return {"status": "ok"}

