from typing import List, Optional

from pydantic import BaseModel


class GenresItems(BaseModel):
    id: str
    genre: str


class GenreItems(BaseModel):
    id: str
    title: str
    imdb_rating: Optional[float]


# Список всех жанров
class Genres(BaseModel):
    genres: List[GenresItems]


# Информация по одному жанру
class Genre(BaseModel):
    id: str
    genre: str
    films: List[GenreItems]
