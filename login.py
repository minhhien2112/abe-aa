import uuid
import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseSettings, BaseModel, UUID4

from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException


class Settings(BaseSettings):
    secret: str  # automatically taken from environment variable
class Data(BaseModel):
    user: dict

class UserCreate(BaseModel):
    email: str
    password: str


class User(UserCreate):
    id: UUID4


DEFAULT_SETTINGS = Settings(_env_file=".env")
DB = {
    "users": {}
}
TOKEN_URL = "/auth/token"

app = FastAPI()
manager = LoginManager(DEFAULT_SETTINGS.secret, TOKEN_URL)


@manager.user_loader
def get_user(email: str):
    return DB["users"].get(email)

def adduser():
    u = {'email': 'alice', 'password': 'alice'}
    db_user = {'email': 'alice', 'password': 'alice', 'id': uuid.uuid4()}
    print(db_user)
    DB["users"][db_user['email']] = db_user
@app.get("/")
def index():
    adduser()
    print(DB)
    with open("./templates/index.html", 'r') as f:
        return HTMLResponse(content=f.read())


@app.post("/auth/register")
def register(user: UserCreate):
    if user.email in DB["users"]:
        raise HTTPException(status_code=400, detail="A user with this email already exists")
    else:
        db_user = User(**user.dict(), id=uuid.uuid4())
#        print(user.dict())
#        print(db_user)
        # PLEASE hash your passwords in real world applications
        DB["users"][db_user.email] = db_user
        print(type(DB["users"]))
        return {"detail": "Successfull registered"}
@app.post("/abe")
def abe(object: dict):
    print("OK")
    print(object)

@app.post(TOKEN_URL)
def login(data: OAuth2PasswordRequestForm = Depends()):
    email = data.username
    password = data.password

    user = get_user(email)  # we are using the same function to retrieve the user
#    printu=("user", user)
    if not user:
        raise InvalidCredentialsException  # you can also use your own HTTPException
    elif password != user['password']:
        raise InvalidCredentialsException

    access_token = manager.create_access_token(
        data=dict(sub=email)
    )
    return {'access_token': access_token, 'token_type': 'bearer'}


@app.get("/private")
def private_route(user=Depends(manager)):
    return {"detail": f"Welcome {user.email}"}

