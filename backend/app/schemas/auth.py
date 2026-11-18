from pydantic import BaseModel, ConfigDict


class RegisterRequest(BaseModel):
    model_config = ConfigDict(extra="ignore")

    full_name: str
    email: str
    password: str
    confirm_password: str


class LoginRequest(BaseModel):
    model_config = ConfigDict(extra="ignore")

    email: str
    password: str


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    full_name: str
    email: str
    role: str
