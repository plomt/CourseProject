from peewee import *

database = PostgresqlDatabase('postgres', **{'user': 'postgres', 'password': '0000'})

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class Message(BaseModel):
    date_time = DateTimeField(null=True)
    flag = CharField(null=True)
    sentence = TextField(null=True)

    class Meta:
        table_name = 'message'
        schema = 'project_pyqt'
        primary_key = False

class Seance(BaseModel):
    name_seance = CharField(null=True)
    name_user = CharField(null=True)

    class Meta:
        table_name = 'seance'
        schema = 'project_pyqt'
        primary_key = False

