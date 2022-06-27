import random
import util
import mariadb
from fastapi import APIRouter
from typing import Optional
from pydantic import BaseModel
from database import ines_db
from users import *

router = APIRouter()

class New_user(BaseModel):
    id: Optional[int]
    name: str
    name2: Optional[str]
    name3: Optional[str]
    lastname: str
    lastname2: Optional[str]
    lastname3: Optional[str]
    email: str
    password: str
    cedula: int
    bday: Optional[str]
    is_admin : Optional[int]

@router.post('/users')
def regist_user(new_user: New_user):
    '''Registers the user in the system and saves 
    them into the database
    '''
    new_user.id = util.random_id()
    print(f'[!] Registing user with id: {new_user.id}')

    if not ines_db.users.insert(new_user):
        return {'success': False}

    return {'success': True, 'new_user': new_user}

@router.put('/users_modify') #Function to modify user
def mod_user(id : int, name : str = None, name2 : str = None, name3 : str = None,
            lastname : str = None, lastname2 : str = None, lastname3 : str = None,
            email : str = None, cedula : int = None, password : str = None):
    '''Modifies the user in the database'''
    try:
        res = ines_db.users.mod_user(id, name, name2, name3, 
                            lastname, lastname2, lastname3,
                             email, cedula, password)
        return res

    except mariadb.Error as e:
        print ('[!] There was an error during this action.\n')
        return e
@router.get('/users')
def get_user(id: str):
    '''Obtains the user from the database'''
    print(f'[!] user id: {id}')
    try:
        print ('[!] Getting user...')
        res = ines_db.users.get(id)
        return res
    
    except mariadb.Error as e:
        print ('[!] There was an error during this action.\n')
        return e

@router.delete('/users/{id}') #Function to delete user from the database
def del_user(id : int):
    '''Deletes user from the database by its ID.'''
    if not ines_db.users.delete(id):
        return {'success': False}
    
    return {'success': True}
