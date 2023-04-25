import peewee

DIRECTORY = "data/"
DATA_SAVE = "all_objects.db"

db = peewee.SqliteDatabase(DIRECTORY + DATA_SAVE)


class PhysicalObject(peewee.Model):
    name = peewee.CharField()
    is_save = peewee.BooleanField()

    class Meta:
        database = db


db.connect()
db.create_tables([PhysicalObject])
