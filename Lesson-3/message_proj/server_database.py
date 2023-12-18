"""1. Начать реализацию класса «Хранилище» для серверной стороны. Хранение необходимо осуществлять в базе данных. В качестве СУБД использовать sqlite.
 Для взаимодействия с БД можно применять ORM.
Опорная схема базы данных:
На стороне сервера БД содержит следующие таблицы:
"""

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from datetime import datetime
import os
from sqlalchemy.sql.functions import user


class ServerStorage:
    db_full_path = os.path.join(os.path.dirname(__file__), "server_db.db3")
    engine = create_engine(f'sqlite:///{db_full_path}', echo=True)
    Base = declarative_base()
    Session = sessionmaker(bind=engine)
    """
1 - клиенты:
    - логин;
    - дата последнего входа (last_login_time).
    """
    class User(Base):
        __tablename__ = 'users'
        id = Column(Integer, primary_key=True)
        login = Column(String)
        last_seen = Column(String)

        def __init__(self, name):
            self.login = name
            self.last_seen = datetime.now()
            self.id = None



    class UserTable():   #для таблиц с активными пользователями и их историей
        id = Column(Integer, primary_key=True)
        login_time = Column(String)
        ip_address = Column(String)
        port = Column(Integer)

        @declared_attr
        def client_id(cls):
            return Column(Integer, ForeignKey('users.id'))

        def __init__(self, client_id, ip_address, port):
            self.id = None
            self.client_id = client_id
            self.login_time = datetime.now()
            self.ip_address = ip_address
            self.port = port
    """
2 - история клиентов:
    - id-клиента;
    - login_time;
    - ip-адрес.
    - port
    """
    class UserHistory(UserTable, Base):
        __tablename__ = 'users_history'


    """
    c) список активных клиентов:
    * id_клиента;
    * ip-адрес;
    * port;
    * login_time.
    """

    class UserActive(UserTable, Base):
        __tablename__ = "users_active"

    def init_user(self, name, ip_address, port):

        result = self.sess.query(self.User).filter_by(login=name)
        if result.count() == 0:
            user = self.User(name)
            self.sess.add(user)
            self.sess.commit()
        else:
            user = result.first()
            user.last_seen = datetime.now()

        user_history = self.UserHistory(user.id, ip_address, port)
        self.sess.add(user_history)
        user_active = self.UserActive(user.id, ip_address, port)
        self.sess.add(user_active)

        self.sess.commit()

    def destroy_user_session(self, username):
        user = self.sess.query(self.User).filter_by(login = username).first()
        self.sess.query(self.UserActive).filter_by(client_id = user.id).delete()
        self.sess.commit()

    def users_list(self):
        result = self.sess.query(
            self.User.login,
            self.User.last_seen
        )
        return result.all()

    def active_users_list(self):
        result = self.sess.query(
            self.User.login,
            self.UserActive.ip_address,
            self.UserActive.port,
            self.UserActive.login_time
        ).join(self.User)

    def login_history(self, username = None):
        result = self.sess.query(
            self.User.login,
            self.UserHistory.login_time,
            self.UserHistory.ip_address,
            self.UserHistory.port
        ).join(self.User)

        if username:
            result = result.filter(self.User.login == username)
        return result.all()


    def __init__(self):

        self.Base.metadata.create_all(self.engine)
        self.sess = self.Session()



if __name__ == "__main__":
    db = ServerStorage()
    db.init_user("client23", "192.168.1.1", 7777)
    db.init_user("client777", "192.168.1.1", 7777)
    db.init_user("client-ohmygod", "192.168.1.6", 7777)
    db.destroy_user_session("client23")