from fastapi import FastAPI, HTTPException
from http import HTTPStatus

from .schemas import Message, UserSchema, UserPublicSchema, UserDB, UserList

app = FastAPI(title='API PIKA DE CACHORRO')

database = []


@app.get(path='/', status_code=HTTPStatus.OK, response_model=Message)
def read_root():
    return {'message': 'ok'}


@app.post(
    path='/users/',
    status_code=HTTPStatus.CREATED,
    response_model=UserPublicSchema,
)
def create_user(user: UserSchema):
    user_with_id = UserDB(
        username=user.username,
        email=user.email,
        password=user.password,
        id=len(database) + 1,
    )

    database.append(user_with_id)

    return user_with_id


@app.get('/users/', response_model=UserList, status_code=HTTPStatus.OK)
def read_users():
    return {'users': database}


@app.put(
    '/users/{user_id}',
    status_code=HTTPStatus.OK,
    response_model=UserPublicSchema,
)
def update_user(user_id: int, user: UserSchema):
    user_with_id = UserDB(
        username=user.username,
        email=user.email,
        password=user.password,
        id=user_id,
    )

    if user_id < 1 or user_id > len(database):
        raise HTTPException(
            detail='Não existe esse usuário', status_code=HTTPStatus.NOT_FOUND
        )

    database[user_id - 1] = user_with_id

    return user_with_id


@app.delete(
    '/users/{user_id}',
    status_code=HTTPStatus.OK,
    response_model=UserPublicSchema,
)
def delete_user(user_id: int):
    if user_id < 1 or user_id > len(database):
        raise HTTPException(
            detail='Não existe esse usuário', status_code=HTTPStatus.NOT_FOUND
        )
    return database.pop(user_id - 1)
