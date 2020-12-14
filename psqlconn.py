# class Animal:
#     @classmethod
#     def action(cls):
#         print('起床')
#         print('刷牙')
#         cls.eat()

#     @staticmethod
#     def eat():
#         print('吃肉')


# class Cat(Animal):
#     @staticmethod
#     def eat():
#         print('吃猫粮')


# Animal.action()
# Cat.action()
import psycopg2


def abc(fuc):
    def wrapper(*args, **kwargs):
        conn = psycopg2.connect(
            database='psqltest',
            user='dvsilch',
            password='dvsilch123456788',
            host='120.53.223.160',
            port='7080',
        )
        cur = conn.cursor()
        kwargs['cur'] = cur
        kwargs['conn'] = conn
        result = fuc(*args, **kwargs)
        conn.close()
        return result

    return wrapper


class PostModel:
    @classmethod
    @abc
    def get_db(cls, cur, conn):
        cur.execute('select id, title, timestamp, content from PostModel;')
        data = cur.fetchall()
        return data
        # return cls.request_db('select id, title, timestamp, content from PostModel;')

    @classmethod
    @abc
    def post_db(cls, cur, conn, title, content, timestamp):
        cur.execute(
            'insert into PostModel (title, timestamp, content) values (%s, %s, %s);'
            % (title, timestamp, content)
        )
        conn.commit()

    @classmethod
    @abc
    def put_db(cls, cur, conn, title, content, id):
        cur.execute(
            'uptimestamp PostModel set title = %s, content = %s where id = %s;'
            % (title, content, id)
        )
        conn.commit()

    @classmethod
    @abc
    def delete_db(cls, cur, conn, id):
        cur.execute('delete from PostModel where id = %s;' % id)
        conn.commit()

    @classmethod
    @abc
    def get_single_db(cls, cur, conn, id):
        cur.execute(
            'select id, title, timestamp, content from PostModel where id = %s;' % id
        )
        data = cur.fetchall()
        return data

    @classmethod
    @abc
    def get_comments(cls, cur, conn, id):
        cur.execute(
            'select id,  timestamp, content from CommentModel where post_id = %s;' % id
        )

        data = cur.fetchall()
        return data
