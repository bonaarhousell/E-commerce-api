from fastapi import FastAPI

from app.routers import auth
from app.routers import order
from app.routers import product
from app.routers import cart
from app.routers import checkout

app = FastAPI()

app.include_router(auth.router, tags=["Auth"])
app.include_router(product.router, tags=["Product"])
app.include_router(order.router, tags=["Order"])
app.include_router(cart.router, tags=["Cart"])
app.include_router(checkout.router, tags=["Checkout"])