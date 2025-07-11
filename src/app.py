from fastapi import FastAPI

from .schemas import Message

app = FastAPI(title='API PIKA DE CACHORRO')


@app.get(path='/', response_model=Message)
def read_root():
    return {'message': 'ok'}
