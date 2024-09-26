from fastapi import FastAPI

from src.notes.routers import router as notes_router

app = FastAPI(
    title="Notes"
)


app.include_router(notes_router)


# @app.get("/users/{user_id}")
# def get_user(user_id: int):
#     return [user for user in users if user.get("id") == user_id]


# @app.get("/test")
# def test(t1: int, t2: int = None):
#     return "hello"