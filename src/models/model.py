from typing import List

from pydantic import BaseModel


class User(BaseModel):
    name : str
    username : str
    email : str
    password : str
    chats : List[str]