from datetime import date
from typing import List

import uvicorn
from fastapi import FastAPI
from pydantic_settings import BaseSettings
from pydantic import BaseModel

from entrymanager import EntryManager
from resources import Entry

from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost",  # адрес на котором работает фронт-энд
    "http://158.160.124.254"
]

app = FastAPI(title='Todo Backend',
              description='Бэк-энд списка дел')

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,    # Список разрешенных доменов
    allow_credentials=True,   # Разрешить Cookies и Headers
    allow_methods=["*"],      # Разрешить все HTTP методы
    allow_headers=["*"],      # Разрешить все хедеры
)

class User(BaseModel):
    first_name: str
    last_name: str
    birthdate: date

class Settings(BaseSettings):
    data_folder: str='.'

settings = Settings()

@app.get("/api/get_data_folder")
async def get_data_folder():
    return {
        'data_folder': settings.data_folder
    }

@app.get("/hello_world")
async def hello_world(name: str) -> dict:
    """
    Просто возвращаем Hello
    :return: 
    """
    return {'hello': name}

@app.get("/api/entries/")
async def get_entries():
    new_m_entry = EntryManager(settings.data_folder)
    new_m_entry.load()
    list_of_entries = list()
    for entry in new_m_entry.entries:
        list_of_entries.append(entry.json())
    return list_of_entries

@app.post('/api/save_entries/')
async def save_entries(data: List[dict]):
    entry_manager = EntryManager(settings.data_folder)
    for entry in data:
        new_entry = Entry.from_json(entry)
        entry_manager.entries.append(new_entry)
    entry_manager.save()
    return {'status': 'success'}

# if __name__ == '__main__':
#     uvicorn.run("main:app", host='localhost', port=8000, reload=True)