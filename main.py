# TODO: Error Handling

from fastapi import Depends, FastAPI, HTTPException, File, UploadFile
from fastapi.responses import FileResponse
import os
from random import randint
import uuid
import uvicorn

from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import random
from backend.user import Users, BaseUser
from backend.topic import Topic
import json
from typing import Annotated

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")
IMAGEDIR = "images/"

# TODO: Move to a Database
try:
    with open("users.json", "r") as file:
        registered_users_data = json.load(file)
except FileNotFoundError:
    registered_users_data = {}

users = Users(registered_users = {})
users.register_from_json(registered_users_data)
topic = Topic()

### USER

@app.post("/login", tags = ["user"])
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    if users.exist(form_data.username):
        if users.registered_users[form_data.username].login(form_data.username, form_data.password):
            return {"access_token": form_data.username, "token_type": "bearer"}
    else:
        return HTTPException(status_code=404, detail="User not found") # redirect to registration


@app.post("/register", tags=["user"])
def register(base_user: BaseUser):
    if users.register(base_user) is True:
        users.save_users_to_json()
        return {"message": "Registration successful"}
    else:
        return {"message": f"'{base_user.username}' has been already utilized"}

@app.get("/users", tags = ["user"])
def get_users(username: Annotated[str, Depends(oauth2_scheme)]):
    return users.registered_users

@app.get("/users/me", tags = ["user"])
async def read_users_me(
    username: Annotated[str, Depends(oauth2_scheme)]
):
    return users.registered_users[username]

### APP

@api.get('/hello')
def hello():
    return "Hello World!"

@app.get("/topic", tags = ["topic"] )
def get_topic(username: Annotated[str, Depends(oauth2_scheme)], day: str):
    return topic.get_topic(day)

@app.get("/question", tags = ["topic"] )
def get_question(username: Annotated[str, Depends(oauth2_scheme)], day: str):
    return topic.get_question(day)


@app.get("/home", tags=["topic"])
def get_home(username: Annotated[str, Depends(oauth2_scheme)], day: str):
        if users.exist(username) and users.registered_users[username].enabled:
            # if the user has posted
            if day in users.registered_users[username].album.pictures:
                return dict(
                    (user, f"{IMAGEDIR}{users.registered_users[user].album.pictures[day]}")
                    for user in users.registered_users if day in users.registered_users[user].album.pictures
                )
            else:
                return None
        else:
            return HTTPException(status_code=404, detail="User not found or not logged in")

@app.get("/home/pictures", tags = ["topic"])
async def get_picture(username: Annotated[str, Depends(oauth2_scheme)], path: str):
    return FileRespnse(path)

@app.post("/picture",  tags = ["topic"])
async def upload_picture(username: Annotated[str, Depends(oauth2_scheme)], day: str, picture: UploadFile = File(...)):
    if users.exist(username) and users.registered_users[username].enabled:
        picture.filename = f"{uuid.uuid4()}.jpg" # random name
        contents = await picture.read()
        with open(f"{IMAGEDIR}{picture.filename}", "wb") as f:
            f.write(contents)

        users.registered_users[username].album.set_picture(day, picture.filename)
        users.save_users_to_json()
        return {"message": "Picture uploaded successfully"}
    else:
        return HTTPException(status_code=404, detail="User not found or not logged in")


def eligible_for_ranking(user: str, day:str) -> bool:
    return day in users.registered_users[user].album.pictures

@app.get("/rank",  tags = ["rank"])
def get_pic_to_rank(username: Annotated[str, Depends(oauth2_scheme)], day: str):
    if users.exist(username) and users.registered_users[username].enabled:
        # if the user has posted
        if day in users.registered_users[username].album.pictures:
            
            pic_to_rank = {}
            all_users = [user for user in users.registered_users if (user != username and eligible_for_ranking(user, day))]
            
            # if at least 4 other users has posted
            if len(all_users) < 4:
                return HTTPException(status_code=400, detail="Not enough users available for ranking")

            random_users = random.sample(all_users, min(4, len(all_users)))

            for user_key in random_users:
                pic_to_rank[user_key] = f"{IMAGEDIR}{users.registered_users[user_key].album.pictures[day]}"

            return pic_to_rank
    else:
        return HTTPException(status_code=404, detail="User not found or not logged in")
 
        
@app.post("/rank",  tags = ["rank"])
def set_rank(username: Annotated[str, Depends(oauth2_scheme)], rank: dict, day: str):
    if users.exist(username) and users.registered_users[username].enabled:
        for index, user in enumerate(rank):
            users.registered_users[user].album.vote(day,4-index)
            users.save_users_to_json()
            return {"message": "Rank set successfully"}
    else:
        return HTTPException(status_code=404, detail="User not found or not logged in")
 

@app.post("/rank/final", tags = ["rank"])
def get_final_rank(username: Annotated[str, Depends(oauth2_scheme)], day:str):
    if users.exist(username) and users.registered_users[username].enabled:
        final_rank = {}
        for user in users.registered_users:
            final_rank[user] = (users.registered_users[user].album.get_vote(day), f"{IMAGEDIR}{users.registered_users[user].album.pictures[day]}")
        
        final_rank = {k: v for k, v in sorted(final_rank.items(), key=lambda item: item[1][0], reverse=True)}
        return final_rank
    else:
        return HTTPException(status_code=404, detail="User not found or not logged in")


if __name__ == "__main__":
    print("Starting webserver...")
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8080)),
        debug=os.getenv("DEBUG", False),
        log_level=os.getenv('LOG_LEVEL', "info"),
        proxy_headers=True
    )
