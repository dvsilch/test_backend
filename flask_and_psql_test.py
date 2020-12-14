from flask import Flask, request, Response, json, jsonify
from flask_restful import Api, Resource
import time, psqlconn, random, peewee, flask_login

app = Flask(__name__)
api = Api(app)


class Post:
    @classmethod
    def tur_to_list(cls, tur):
        ls = []
        datakey = ('id', 'title', 'timestamp', 'content')
        if len(tur) == 1:
            ls = dict(zip(datakey, tur[0]))
        else:
            for i in range(len(tur)):
                data = dict(zip(datakey, tur[i]))
                ls.append(data)
        return ls

    @classmethod
    def load(cls):
        datavalue = psqlconn.PostModel.get_db()
        # print(datavalue)
        data = cls.tur_to_list(datavalue)
        # print(data)
        return data

    @classmethod
    def create(cls, title, content, timestamp):
        psqlconn.PostModel.post_db(
            title="'" + title + "'",
            content="'" + content + "'",
            timestamp=timestamp,
        )

    @classmethod
    def deletePost(cls, id):
        psqlconn.PostModel.delete_db(
            id=int(id),
        )

    @classmethod
    def loadDetail(cls, id):
        datavalue = psqlconn.PostModel.get_single_db(id=int(id))
        data = cls.tur_to_list(datavalue)
        return data

    @classmethod
    def edit(cls, id, title, content):
        psqlconn.PostModel.put_db(
            title='%s' % title,
            content='%s' % content,
            id=int(id),
        )


class Comment:
    @classmethod
    def tur_to_list(cls, tur):
        ls = []
        datakey = ('id', 'timestamp', 'content')
        if len(tur) != 0:
            for i in range(len(tur)):
                data = dict(zip(datakey, tur[i]))
                ls.append(data)
        return ls

    @classmethod
    def get_comment(cls, id):
        commentlist = psqlconn.PostModel.get_comments(id=int(id))
        commentlist = cls.tur_to_list(commentlist)
        return commentlist


class PostList(Resource):
    def get(self):
        results = Post.load()
        if type(results) == dict:
            results = [results]
        return {"results": results}

    def post(self):
        title, content, timestamp = (
            request.json['title'],
            request.json['content'],
            int(time.time()),
        )
        Post.create(
            title=title,
            content=content,
            timestamp=timestamp,
        )
        return {'success': 'success'}


class PostDetail(Resource):
    def get(self, id):  # id是必须的
        results = Post.loadDetail(id)
        # print(results)
        return results

    def put(self, id):
        title, content, id = (
            request.json['title'],
            request.json['content'],
            id,
        )
        Post.edit(
            id=id,
            title=title,
            content=content,
        )
        return {'success': 'success'}

    def delete(self, id):
        results = Post.deletePost(id)
        return {"results": results}


class CommentDetail(Resource):
    def get(self, id):
        # results =
        results = Comment.get_comment(id)
        # print(results)
        return {"results": results}


api.add_resource(PostList, '/api/post')
api.add_resource(PostDetail, '/api/post/<id>')
api.add_resource(CommentDetail, '/api/post/comment/<id>')


@app.after_request
def apply_cors(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = '*'
    response.headers['Access-Control-Allow-Methods'] = '*'
    return response


if __name__ == '__main__':
    app.run(debug=True)