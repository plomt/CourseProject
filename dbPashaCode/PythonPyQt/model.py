from peewee import *

database = PostgresqlDatabase('postgres', **{'user': 'postgres', 'password': '0000'})

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class Seance(BaseModel):
    id_seance = IntegerField(constraints=[SQL("DEFAULT nextval('project_pyqt.seance_id_seance_seq'::regclass)")], unique=True)
    name_user = CharField(null=True)

    class Meta:
        table_name = 'seance'
        schema = 'project_pyqt'
        primary_key = False

class Message(BaseModel):
    answer_to_command = CharField(null=True)
    command = CharField(null=True)
    date_time = DateTimeField(null=True)
    flag = CharField(null=True)
    id_seance = ForeignKeyField(column_name='id_seance', constraints=[SQL("DEFAULT nextval('project_pyqt.message_id_seance_seq'::regclass)")], field='id_seance', model=Seance)

    class Meta:
        table_name = 'message'
        schema = 'project_pyqt'
        primary_key = False

