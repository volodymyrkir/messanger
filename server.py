import json
import os
from twisted.internet import protocol, reactor
from twisted.internet.protocol import ServerFactory as ServerFactoryImported, connectionDone
from twisted.internet.endpoints import TCP4ServerEndpoint
from sqlalchemy import create_engine
from sqlalchemy.sql import text

PG_LOGIN = os.environ.get('POSTGRES_USER')
PG_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
PG_DB = os.environ.get('POSTGRES_DB')


def get_pg_connection():
    return create_engine(f'postgresql://{PG_LOGIN}:{PG_PASSWORD}@database:5432/{PG_DB}')


class Server(protocol.Protocol):
    def __init__(self, clients: dict, my_identifier):
        self.clients = clients
        self.my_identifier = my_identifier
        self.another_client = None

    def connectionMade(self):
        self.clients[self.my_identifier] = self

    def dataReceived(self, data: bytes):
        try:
            data = json.loads(data.decode('utf-8')) #server
        except UnicodeDecodeError:
            self.send_message(value='Cannot decode, use utf-8', type='error')
            return
        except json.JSONDecodeError:
            self.send_message(value='Cannot decode, use json', type='error')
            return

        if data['value'] == "exit":
            exit(0)
        if not data.get('type') or not data.get('value'):
            self.send_message(value='Wrong data', type='error')
            return
        if data['type'] == "user_choose":
            try:
                another_client = int(data['value'])
                if another_client in self.clients.keys():
                    self.another_client = another_client
                else:
                    raise KeyError
                self.another_client = another_client
            except ValueError:
                self.send_message(value='Write id as integer',type='error')
            except KeyError:
                self.send_message(value=f'Can not find client no {another_client}',  type='error')
            else:
                self.send_message(value=f'Established connection with client #{self.another_client}',type='user_chosen')
        elif data['type'] == "new_message":
            if not self.another_client:
                self.send_message(value='Dont have a client', type='error')
            try:
                with get_pg_connection().connect() as engine:
                    self.send_message(value=data['value'], client=self.clients[self.another_client],type='new_message')
                    message_table_query = text("""CREATE TABLE IF NOT EXISTS message(
                        message_id serial primary key,
                        from_user int not null,
                        to_user int not null,
                        message_value varchar
                        );
                        INSERT INTO message(from_user, to_user, message_value) VALUES (:from_user,:to_user,:val);""")
                    engine.execute(message_table_query,
                                   from_user=self.my_identifier,
                                   to_user=self.clients[self.another_client],
                                   val=data['value'])
            except KeyError:
                self.send_message(value='try another client',type='error')
                self.another_client = None

    def disconnect(self):
        del self.clients[self.my_identifier]

    def connectionLost(self, reason=connectionDone):
        self.disconnect()

    @staticmethod
    def __encode_json(**kwargs):
        return json.dumps(kwargs)

    def send_message(self, **kwargs):
        if kwargs.get('client'):
            client = kwargs['client']
            del kwargs['client']
            client.transport.write(self.__encode_json(**kwargs).encode('utf-8'))
        else:
            self.transport.write(self.__encode_json(**kwargs).encode('utf-8'))


class ServerFactory(ServerFactoryImported):
    def __init__(self):
        self.clients = {}
        self.last_id = 0

    def buildProtocol(self, addr):
        self.last_id += 1
        with get_pg_connection().connect() as engine:
            engine.execute("ALTER TABLE user_data ADD COLUMN IF NOT EXISTS id int;")
            query = text("UPDATE user_data SET id=:x where id is null;")
            engine.execute(query, x=self.last_id)
        return Server(self.clients, self.last_id)


endpoint = TCP4ServerEndpoint(reactor, 8000)
endpoint.listen(ServerFactory())
reactor.run()
