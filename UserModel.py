import peewee, time
from flask_login import UserMixin
from playhouse.pool import PooledPostgresqlExtDatabase
from werkzeug.security import generate_password_hash, check_password_hash

DATABASE = PooledPostgresqlExtDatabase(
    database='psqltest',
    user='dvsilch',
    password='dvsilch123456788',
    host='120.53.223.160',
    port='7080',
)


class BaseModel(peewee.Model):
    class Meta:
        database = DATABASE


class UserModel(BaseModel):
    id = peewee.PrimaryKeyField(primary_key=True)

    username = peewee.CharField(max_length=32, help_text='用户名')
    passwdmd5 = peewee.CharField(max_length=32, help_text='密码的md5值')

    register_time = peewee.DateTimeField(default=int(time.time()), help_text='用户注册时间')

    def __str__(self):
        return self.username


# UserModel.create_table()


class User(UserMixin):
    def __init__(self, username):
        self.username = username
        # self.id = self.get_id()

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)


a = User('dvsilch')
a.password('123456788')
print(a.password_hash)