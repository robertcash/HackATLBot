from peewee import *

database = MySQLDatabase('', **{'host': '', 'password': '', 'port': 3306, 'user': ''})

class UnknownField(object):
    pass

class BaseModel(Model):
    class Meta:
        database = database

class User(BaseModel):
    user_id = PrimaryKeyField(db_column='user_id')
    messenger_id = CharField(db_column='messenger_id', null=False)
    new_user = IntegerField(db_column='new_user', null=False)
    state = CharField(db_column='state', null=True)
    email = CharField(db_column='email', null=True)
    team_id = IntegerField(db_column='team_id', null=True)
    project_id = IntegerField(db_column='project_id', null=True)
    first_name = CharField(db_column='first_name', null=True)
    last_name = CharField(db_column='last_name', null=True)

    class Meta:
        db_table = 'User'

class Participant(BaseModel):
    email = CharField(db_column='email', null=False)
    first_name = CharField(db_column='first_name', null=False)
    last_name = CharField(db_column='last_name', null=False)

    class Meta:
        db_table = 'Participant'

class Team(BaseModel):
    team_id = PrimaryKeyField(db_column='team_id')
    team_leader_id = CharField(db_column='team_leader_id', null=True)
    code = CharField(db_column='code', null=True)

    class Meta:
        db_table = 'Team'

class Project(BaseModel):
    proj_id = PrimaryKeyField(db_column='proj_id')
    url = CharField(db_column='url', null=True)
    project_user_id = IntegerField(db_column='project_user_id', null=True)
    project_team_id = IntegerField(db_column='project_team_id', null=True)
    status = CharField(db_column='status', null=True)
    assignment = CharField(db_column='assignment', null=True)

    class Meta:
        db_table = 'Project'
