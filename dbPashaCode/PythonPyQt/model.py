from peewee import *

database = PostgresqlDatabase('postgres', **{'user': 'postgres', 'password': 'postgres'})

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class Message(BaseModel):
    answer_to_command = TextField(null=True)
    command = TextField(null=True)
    date_time = CharField(null=True)
    flag = BooleanField(null=True)
    id_seance = CharField(null=True)

    class Meta:
        table_name = 'message'
        schema = 'project_pyqt'
        primary_key = False

class Seance(BaseModel):
    id_seance = IntegerField(constraints=[SQL("DEFAULT nextval('project_pyqt.seance_id_seance_seq'::regclass)")], unique=True)
    name_user = CharField(null=True)

    class Meta:
        table_name = 'seance'
        schema = 'project_pyqt'
        primary_key = False

