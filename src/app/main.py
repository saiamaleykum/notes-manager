from fastapi import FastAPI, Depends

from src.app.notes.routers import router as notes_router
from src.app.auth.base_config import auth_backend, fastapi_users
from src.app.auth.schemas import UserCreate, UserRead
from src.app.auth.models import User
from src.app.auth.base_config import current_user


app = FastAPI(
    title="Notes"
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(notes_router)


@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.username}"


@app.get("/unprotected-route")
def unprotected_route():
    return f"Hello, anonym"