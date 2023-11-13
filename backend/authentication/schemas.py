from pydantic import BaseModel


class SignIn(BaseModel):
    username: str
    password: str
