from flask_restful import Resource, reqparse
from models.article import Article


class NewArticle(Resource):
    parse = reqparse.RequestParser()
    parse.add_argument('id_author',
                       type=str,
                       required=True,
                       help='This field cannot be blank.')
    parse.add_argument('title',
                       type=str,
                       required=True,
                       help='This field cannot be blank.')
    parse.add_argument('content',
                       type=str,
                       required=True,
                       help='This field cannot be blank.')

    def post(self):

        data = NewArticle.parse.parse_args()

        article_data = Article(data['id_author'],
                               data['title'],
                               data['content'])

        try:
            article_data.save_to_db()
        except:
            return {"message": "An error occurred creating the article."}, 500

        return {"message": "New article created successfully."}, 201


class Articles(Resource):
    parse = reqparse.RequestParser()
    parse.add_argument('title',
                       type=str,
                       required=True,
                       help='This field cannot be blank.')
    parse.add_argument('content',
                       type=str,
                       required=True,
                       help='This field cannot be blank.')

    def get(self, id_all):

        article_data = Article.find_by_id(id_all)

        if article_data:
            return article_data.json()
        else:
            return {'message': 'Article not found'}, 404

    def put(self, id_all):

        data = Articles.parse.parse_args()
        article_data = Article.find_by_id(id_all)

        if article_data:
            article_data.title = data['title']
            article_data.content = data['content']

            try:
                article_data.save_to_db()
            except:
                return {"message": "An error occurred update the Article."}, 500

            return {'message': 'Article succes update'}, 200
        else:
            return {'message': 'Article not found'}, 404

    def delete(self, id_all):

        article_data = Article.find_by_id(id_all)

        if article_data:
            try:
                article_data.delete_to_db()
            except:
                return {"message": "An error occurred update the Article."}, 500

            return {'message': 'Article succes delete'}, 200
        else:
            return {'message': 'Article succes delete'}, 404


class ArticleList(Resource):
    def get(self):
        return {'article': list(map(lambda article: article.json(), Article.query.all())),
                'total': len(list(map(lambda article: article.json(), Article.query.all())))}


class ArticleListpage(Resource):
    def get(self, id_all):
        def countx():
            return int(id_all) * 10

        data = Article.query.filter_by(id_author=id_all).first()

        if data:
            data = Article.query.filter_by(id_author=id_all).all()
            articles = []

            if not data:
                return {"message": "Article not found."}, 200
            else:
                for article in data:
                    article_data = {}
                    article_data['id_pub'] = article.id_pub
                    article_data['id_author'] = article.id_author
                    article_data['title'] = article.title
                    article_data['content'] = article.content
                    article_data['timestamp'] = str(article.timetamp)
                    articles.append(article_data)

            return {'id_author': id_all,
                    'articles': articles,
                    'total': len(articles)}
        else:
            data = Article.query.all()
            articles = []
            articles_page = []

            if not data:
                return {"message": "Article not found."}, 200
            else:
                for article in data:
                    article_data = {}
                    article_data['id_pub'] = article.id_pub
                    article_data['id_author'] = article.id_author
                    article_data['title'] = article.title
                    article_data['content'] = article.content
                    article_data['timestamp'] = str(article.timetamp)
                    articles.append(article_data)

                if countx() > len(articles) and len(articles) < countx():
                    for s in range((countx() - 10), len(articles)):
                        articles_page.append(articles[s])
                else:
                    for s in range((countx() - 10), countx()):
                        articles_page.append(articles[s])

                return {'articles': articles_page,
                        'total': len(articles_page)}
