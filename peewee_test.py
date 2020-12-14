import peewee
import datetime
import time
import flask_login
from peewee import fn, JOIN

from playhouse.pool import PooledPostgresqlExtDatabase, PostgresqlExtDatabase
from flask import Flask, request, Response, json, jsonify
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

# settings = {
#     'database': 'psqltest',
#     'user': 'dvsilch',
#     'password': 'dvsilch123456788',
#     'host': '120.53.223.160',
#     'port': '7080',
# }

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

    # def create_tables():


class PostModel(BaseModel):
    id = peewee.PrimaryKeyField(
        primary_key=True,
    )

    title = peewee.CharField()

    content = peewee.CharField()

    timestamp = peewee.IntegerField()

    is_delete = peewee.BooleanField(default=False)


class CommentModel(BaseModel):
    id = peewee.PrimaryKeyField(
        primary_key=True,
    )

    content = peewee.CharField()

    timestamp = peewee.IntegerField()

    post_id = peewee.ForeignKeyField(
        PostModel,
    )

    is_delete = peewee.BooleanField(default=False)


class Post(Resource):
    def get(self):
        post = (
            PostModel.select(PostModel)
            .join(CommentModel, JOIN.LEFT_OUTER)
            .where(PostModel.is_delete == False)
            .order_by(fn.MAX(CommentModel.timestamp).desc(), PostModel.timestamp.desc())
            .group_by(PostModel)
        )
        results = []
        for i in post:
            results.append(
                {
                    'id': i.id,
                    'title': i.title,
                    'timestamp': i.timestamp,
                    'content': i.content,
                }
            )
            # print(i.is_delete)
        # print(results)
        return {"results": results}

    def post(self):
        title, content, timestamp = (
            request.json['title'],
            request.json['content'],
            int(time.time()),
        )
        post = PostModel.create(title=title, content=content, timestamp=timestamp)

        post.save()

        return {'success': 'success'}


class PostDetail(Resource):
    def get(self, id):
        post = PostModel.get(PostModel.id == id)
        results = {
            'id': post.id,
            'title': post.title,
            'timestamp': post.timestamp,
            'content': post.content,
        }
        return results

    def put(self, id):
        title, content, id = (
            request.json['title'],
            request.json['content'],
            id,
        )
        post = PostModel.get(PostModel.id == id)
        if content != '':
            post.content = content
        if title != '':
            post.title = title
        post.save()
        return {'success': 'success'}

    def delete(self, id):
        post = PostModel.get(PostModel.id == id)
        post.is_delete = True
        post.save()
        return {'success': 'success'}
        # results = Post.deletePost(id)
        # return {"results": results}


class CommentDetail(Resource):
    def get(self, id):
        comment = (
            CommentModel.select()
            .where(
                CommentModel.post_id == (int(id) - 1), CommentModel.is_delete == False
            )
            .order_by(CommentModel.id)
        )
        # print(comment)
        results = []
        for i in comment:
            results.append({'id': i.id, 'content': i.content, 'timestamp': i.timestamp})
        return {"results": results}

    def post(self, id):
        post_id, content, timestamp = (
            int(id) - 1,
            request.json['content'],
            int(time.time()),
        )
        comment = CommentModel.create(
            post_id=post_id, content=content, timestamp=timestamp
        )

        comment.save()

        return {'success': 'success'}

    def delete(self, id):
        comment = CommentModel.get(CommentModel.id == id)
        comment.is_delete = True
        comment.save()

        return {'success': 'success'}


api.add_resource(Post, '/api/post')
api.add_resource(PostDetail, '/api/post/<id>')
api.add_resource(CommentDetail, '/api/post/comment/<id>')


# @app.before_first_request
# def log():
#     print('first')


@app.before_request
def conn():
    if DATABASE.is_closed():
        DATABASE.connect()


@app.teardown_request
def close(e):
    if not DATABASE.is_closed():
        DATABASE.close()


@app.after_request
def apply_cors(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = '*'
    response.headers['Access-Control-Allow-Methods'] = '*'
    return response


if __name__ == '__main__':
    app.run(debug=True)


# PostModel.create_table()
# CommentModel.create_table()

# for i in range(1, 10):
#     post = PostModel.create(
#         title='title%s' % i, content='content%s' % i, timestamp=int(time.time())
#     )
#     post.save()

# for i in range(1, 11):
#     for j in range(0, 11):
#         comment = CommentModel.create(
#             content='comment%s' % j, timestamp=int(time.time()), post_id=i
#         )

# comment = commentlist.create(content='comment1', timestamp=int(time.time()), post_id=2)
# comment.save()

# post = postlist.get(postlist.title == 'title2')
# print(post.content)


# 查全部帖子
# post = postlist.select().order_by(postlist.id.desc())
# ls = []
# for i in post:
#     ls.append(
#         {'id': i.id, 'title': i.title, 'timestamp': i.timestamp, 'content': i.content}
#     )
# print(ls)

# # 增加帖子
# post = postlist.create(title='title10', content='content10', timestamp=int(time.time()))
# post.save()

# # 查单个帖子
# post = postlist.get(postlist.title == 'title2')
# post = {
#     'id': post.id,
#     'title': post.title,
#     'timestamp': post.timestamp,
#     'content': post.content,
# }
# print(post)

# 修改单个帖子(会修改排序)
# post = postlist.get(postlist.title == 'title2')
# post.content = 'content2'
# post.id = 2
# post.save()

# 删除单个帖子
# post = postlist.get(postlist.title == 'title3')
# post.delete_instance()


# # 拿评论
# comment = commentlist.select().order_by(commentlist.id)
# ls = []
# for i in comment:
#     ls.append({'id': i.id, 'content': i.content})
# print(ls)

# 发评论
# comment = commentlist.create(
#     content='comment2',
#     timestamp=int(time.time()),
#     post_id=5,
# )
# comment.save()
