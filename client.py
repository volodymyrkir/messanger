import json
from json import JSONDecodeError
import os
import re
from sys import stderr
from twisted.internet import protocol, reactor
from twisted.internet.protocol import ReconnectingClientFactory as ClientFactoryImported
from twisted.internet.endpoints import TCP4ClientEndpoint
from sqlalchemy.engine import create_engine
from sqlalchemy.sql import text
from sqlalchemy.exc import IntegrityError, ProgrammingError
from dotenv import load_dotenv

load_dotenv()
PG_LOGIN = os.environ.get('POSTGRES_USER')
PG_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
PG_DB = os.environ.get('POSTGRES_DB')


def get_pg_connection():
    return create_engine(f'postgresql://{PG_LOGIN}:{PG_PASSWORD}@localhost:5432/{PG_DB}')


def check_login_correctness(login, password, another_user, form_object):
    with get_pg_connection().connect() as engine:
        query = text("SELECT * FROM user_data WHERE login=:x and password=:y")
        try:
            user = engine.execute(query, x=login, y=password).first()
        except ProgrammingError:
            form_object.incorrect_data_popup()
        else:
            if not user:
                form_object.incorrect_data_popup()
            else:
                another_query = text("SELECT * FROM user_data WHERE login=:x")
                another_user = engine.execute(another_query, x=another_user).first()
                if not another_user:
                    form_object.incorrect_data_popup(True)
                else:
                    another_user_id = another_user[2]
                    form_object.login_successful(login, Client(), another_user_id)  # enter in chat


def create_new_user(new_login, new_password, form_object):
    with get_pg_connection().connect() as engine:
        engine.execute("""CREATE TABLE IF NOT EXISTS user_data(
                        login varchar(255) not null primary key,
                        password varchar(255) not null,
                        client_id serial);""")

        if not re.match(r'^\D[\d\w]{3,}$', new_login):
            form_object.incorrect_login_popup()
        else:
            try:
                query = text("""
                INSERT INTO user_data(LOGIN, PASSWORD) VALUES 
                (:x,:y);""")
                engine.execute(query, x=new_login, y=new_password)
            except IntegrityError:
                form_object.login_exists_popup()
            else:
                form_object.user_created_popup()


class Client(protocol.Protocol):
    def __init__(self):
        reactor.callInThread(self.message_input)

    @staticmethod
    def __encode_json(**kwargs):
        return json.dumps(kwargs)

    def send_message(self, **kwargs):
        self.transport.write(self.__encode_json(**kwargs).encode('utf-8'))

    def message_input(self):
        while True:
            self.send_message(value=input('value:'), type=input('type:'))

    def dataReceived(self, data):
        try:
            data = json.loads(data.decode('utf-8'))  # client
        except UnicodeDecodeError or JSONDecodeError:
            print("Something went wrong", file=stderr)
            return
        if data['type'] == 'error':
            print(data.get('value', 'Unknown error'), file=stderr)
        else:
            print(data.get('value', 'NO value in the message'))


class ClientFactory(ClientFactoryImported):
    def clientConnectionLost(self, connector, unused_reason):
        self.retry(connector)

    def clientConnectionFailed(self, connector, reason):
        self.retry(connector)

    def buildProtocol(self, addr):
        return Client()


if __name__ == "__main__":
    endpoint = TCP4ClientEndpoint(reactor, 'localhost', 8000)
    endpoint.connect(ClientFactory())
    reactor.run()
