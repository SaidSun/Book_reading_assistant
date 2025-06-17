from sqlalchemy import create_engine, Column, Integer, String, Time, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import text
from sqlalchemy.ext.declarative import declarative_base
import pandas as pd
from typing import List


class __SQLConstants:
    __BASE = declarative_base()

class Model_table(__SQLConstants.__BASE):
    __tablename__ = "ModelsTable"

    id = Column(Integer, primary_key=True, index=True)
    Name = Column(String[255])
    Model_name = Column(String[255])
    Popularity = Column(Integer)

    def __repr__(self):
        return f"ModelTable(Name={self.Name}, Model_name={self.Model_name}, Popularity={self.Popularity})"
    
class Author_table(__SQLConstants.__BASE):
    __tablename__ = "AuthorsTable"

    id = Column(Integer, primary_key=True, index=True)
    Author = Column(String[255])
    BookName = Column(String[255])
    Pages = Column(Integer)
    Editor = Column(String[255])
    Origin = Column(String[255])

class General_table(__SQLConstants.__BASE):
    __tablename__ = "GeneralTable"

    id = Column(Integer, primary_key=True, index=True)
    Author = Column(Integer, ForeignKey("AuthorsTable.id"))
    Name = Column(Integer, ForeignKey("AuthorsTable.id"))
    Model = Column(Integer, ForeignKey("ModelsTable.id"))
    Filepath = Column(String[255])
    Origin = Column(Integer, ForeignKey("AuthorsTable.id"))
    Time = Column(Time)

class User_table(__SQLConstants.__BASE):
    __tablename__ = "UserTable"

    id = Column(Integer, primary_key=True, index=True)
    Author = Column(Integer, ForeignKey("AuthorsTable.id"))
    Name = Column(Integer, ForeignKey("AuthorsTable.id"))
    Model = Column(Integer, ForeignKey("ModelsTable.id"))
    Filepath = Column(String[255])
    Origin = Column(Integer, ForeignKey("AuthorsTable.id"))
    RemainingTime = Column(Time)


class Bookworm:
    def __init__(self, logi="superbookreader_user", passw="D73e55g6t08ru!", db="books_db"):
        self.__DATABASE_URL = f"postgresql://{logi}:{passw}!@localhost/{db}"
        self.__ENGINE = create_engine(self.__DATABASE_URL, echo=True)
        self.Server_view_query= f""" CREATE VIEW Server_Data AS SELECT AuthorTable.Author as Author, AuthorTable.BookName as BookName,
          ModelsTable.Name as ModelName, 
          GeneralTable.Time as Time from GeneralTable
          JOIN AuthorTable ON GeneralTable.id == AuthorTable.id
          JOIN ModelsTable ON GeneralTable.id == ModelsTable.id
        """
        self.User_view_query = f""" CREATE VIEW User_Data AS SELECT AuthorTable.Author as Author, AuthorTable.BookName as BookName,
          ModelsTable.Name as ModelName, 
          UserTable.Time as Time from UserTable
          JOIN AuthorTable ON UserTable.id == AuthorTable.id
          JOIN ModelsTable ON UserTable.id == ModelsTable.id
        """

    def make_db(self) -> None:
        __SQLConstants.__BASE.metadata.create_all(self.__ENGINE)
    
    def make_view(self, query):
        with self.__ENGINE.connect() as conn:
            result = conn.execute(text(query))
        return True
    
    def BooksList(self, origin: str):
        '''
        Возвращает весь список книг, доступный на сервере или на стороне клиента
        '''
        with self.__ENGINE.connect() as conn:
            result = conn.execute(text(f"SELECT * FROM {origin}"))
        return result

    def SearchBookServer(self, query: str):
        '''
        Возвращает список книг по определенному запросу
        '''
        with self.__ENGINE.connect() as conn:
            result = conn.execute(text(query))
        return result
    
    def req_sub(result):
        """
        Представляет результат запроса в виде таблицы Pandas
        """
        rows = result.fetchall()
        columns_names = result.keys()

        df = pd.DataFrame(rows, columns=columns_names)
        
        return df, rows, columns_names

        




 