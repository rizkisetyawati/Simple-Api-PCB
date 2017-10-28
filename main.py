from flask import Flask
from flask_restful import Api
from config.base import Configuration
from resources.index import Index
from resources.user import *
from resources.event import *
from resources.megazine import *
from resources.article import *

app = Flask(__name__)
app.config.from_object(Configuration)

api = Api(app)


@app.before_first_request
def req():
    db.create_all()


api.add_resource(Index, '/')

api.add_resource(UserRegister, '/user/register')
api.add_resource(Users, '/user/<string:id_all>')
api.add_resource(UserList, '/users')
api.add_resource(UserListpage, '/users/<int:count>')

api.add_resource(NewArticle, '/article/register')
api.add_resource(Articles, '/article/<string:id_all>')
api.add_resource(ArticleList, '/articles')
api.add_resource(ArticleListpage, '/articles/<string:id_all>')

api.add_resource(NewMegazine, '/megazine/register')
api.add_resource(Megazines, '/megazine/<string:id_all>')
api.add_resource(MegazineList, '/megazines')
api.add_resource(MegazineListpage, '/megazines/<string:id_all>')

api.add_resource(NewEvent, '/event/register')
api.add_resource(Events, '/event/<string:id_all>')
api.add_resource(EventList, '/events')
api.add_resource(EventListpage, '/events/<string:id_all>')

if __name__ == '__main__':
    from core.db import db

    db.init_app(app)
    app.run()
