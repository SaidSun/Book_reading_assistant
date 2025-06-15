from sqlalchemy import create_engine, Column, Integer, String, Time, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base


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
        

    def make_db(self) -> None:
        __SQLConstants.__BASE.metadata.create_all(self.__ENGINE)
    
    def AllBooksList(self):
        '''
        Возвращает весь список книг, доступный на сервере
        '''
        pass
    
    def UserBooksList(self):
        '''
        Возвращяет список книг, прочитанных/в процессе чтения пользователем
        '''
        pass

    def SearchBookServer(self, arg, query):
        '''
        Возвращает список книг по определенному запросу
        '''
        pass

    


 