from tortoise import fields
from tortoise.models import Model

class UserDB(Model):
    id = fields.IntField(pk=True)
    username= fields.CharField(unique=true, min_lenght=3, max_lenght=30)
    passwort= fields.CharField(min_lenght=3, max_lenght=50)
    mail= fields.CharField(min_lenght=3, max_lenght=100)
    year_of_birth= fields.IntField(null=True)