# from flask import Flask, request, Response, json, jsonify
# from flask_restful import Api, Resource
# import time

# app = Flask(__name__)
# api = Api(app)


# class Post:
#     data = {}  # 定义一个字典用来保存网页数据，避免频繁进行http请求

#     @classmethod
#     def load(cls):  # 加载数据
#         with open(r'C:/Users/chvic/Desktop/flask_testdata/datatest.txt', 'r') as f:
#             s = f.read()
#             Post.data = json.loads(s)
#             # if s:
#             #     Post.data = json.loads(s)
#             # else:
#             #     Post.data = {
#             #         'last_id': 3,
#             #         'results': {
#             #             '0': {
#             #                 "title": "title1",
#             #                 "content": "content1",
#             #                 "date": 1604066150,
#             #             },
#             #             '1': {
#             #                 "title": "title2",
#             #                 "content": "content2",
#             #                 "date": 1604066150,
#             #             },
#             #             '2': {
#             #                 "title": "title3",
#             #                 "content": "content3",
#             #                 "date": 1604066150,
#             #             },
#             #         },
#             #     }

#     @classmethod
#     def save(cls):  # 保存数据
#         with open(r'C:/Users/chvic/Desktop/flask_testdata/datatest.txt', 'w') as f:
#             f.write(json.dumps(Post.data))
#             # try:
#             # f.write(json.dumps(Post.data))
#             # except Exception as e:
#             #     import ipdb

#             #     ipdb.set_trace()
#             #     print(123)

#     @classmethod
#     def create(cls, title, content, date):  # 创建一条新数据
#         idx = cls.data['last_id']
#         idx = str(idx)
#         cls.data['results'][idx] = {
#             'title': title,
#             'content': content,
#             'date': date,
#         }
#         cls.data['last_id'] += 1
#         cls.save()
#         # print(Post.last_id)

#     @classmethod
#     def deletePost(cls, id):  # 删除已有数据
#         # print(id)
#         id = str(id)
#         del cls.data['results'][id]
#         cls.save()

#     @classmethod
#     def loadDetail(cls, id):  # 加载特定数据
#         id = str(id)
#         with open(r'C:/Users/chvic/Desktop/flask_testdata/datatest.txt', 'r') as f:
#             s = f.read()
#             Post.data = json.loads(s)['results'][id]

#     @classmethod
#     def edit(cls, id, title, content):  # 修改特定数据
#         id = str(id)
#         cls.data['results'][id]['title'] = title
#         cls.data['results'][id]['content'] = content
#         cls.save()

#     @classmethod
#     def dictToList(cls):  # 字典转列表
#         Listdata = []
#         for key, values in cls.data['results'].items():
#             values['id'] = str(key)  # 将该字典的键名（0,1,2）作为键值，赋值给字典的新键名（id），
#             Listdata.append(values)  # 添加进数组里
#         return Listdata


# Post.load()  # 初始化时进行一次请求，将数据保存在data里


# class PostList(Resource):
#     def get(self):
#         results = Post.dictToList()
#         return {"results": results}

#     def post(self):
#         title, content, date = (
#             request.json['title'],
#             request.json['content'],
#             int(time.time()),
#         )
#         Post.create(
#             title=title,
#             content=content,
#             date=date,
#         )
#         return {'success': 'success'}


# class PostDetail(Resource):
#     def get(self, id):  # id是必须的
#         id = str(id)
#         results = Post.data['results'][id]
#         return results

#     def put(self, id):
#         id = str(id)
#         title, content, id = (
#             request.json['title'],
#             request.json['content'],
#             id,
#         )
#         print(request.json)
#         Post.edit(
#             id=id,
#             title=title,
#             content=content,
#         )
#         return {'success': 'success'}

#     def delete(self, id):
#         id = str(id)
#         Post.deletePost(id)
#         return {'success': 'success'}


# api.add_resource(PostList, '/api/post')
# api.add_resource(PostDetail, '/api/post/<id>')


# @app.after_request
# def apply_cors(response):
#     response.headers['Access-Control-Allow-Origin'] = '*'
#     response.headers['Access-Control-Allow-Headers'] = '*'
#     response.headers['Access-Control-Allow-Methods'] = '*'
#     return response


# if __name__ == '__main__':
#     app.run(debug=True)