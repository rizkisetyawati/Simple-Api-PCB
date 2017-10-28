from flask_restful import Resource, reqparse
from models.megazine import Megazine


class NewMegazine(Resource):
    parse = reqparse.RequestParser()
    parse.add_argument('id_author',
                       type=str,
                       required=True,
                       help='This field cannot be blank.')
    parse.add_argument('title',
                       type=str,
                       required=True,
                       help='This field cannot be blank.')
    parse.add_argument('about',
                       type=str,
                       required=True,
                       help='This field cannot be blank.')

    def post(self):

        data = NewMegazine.parse.parse_args()

        megazine_data = Megazine(data['id_author'],
                             data['title'],
                             data['about'])

        try:
            megazine_data.save_to_db()
        except:
            return {"message": "An error occurred creating the megazine."}, 500

        return {"message": "New megazine created successfully."}, 201


class Megazines(Resource):
    parse = reqparse.RequestParser()
    parse.add_argument('title',
                       type=str,
                       required=True,
                       help='This field cannot be blank.')
    parse.add_argument('about',
                       type=str,
                       required=True,
                       help='This field cannot be blank.')

    def get(self, id_all):

        megazine_data = Megazine.find_by_id(id_all) or Megazine.find_by_author(id_all)

        if megazine_data:
            return megazine_data.json()
        else:
            return {'message': 'Megazine not found'}, 404

    def put(self, id_all):

        data = Megazines.parse.parse_args()
        megazine_data = Megazine.find_by_id(id_all)

        if megazine_data:
            megazine_data.title = data['title']
            megazine_data.about = data['about']

            try:
                megazine_data.save_to_db()
            except:
                return {"message": "An error occurred update the megazine."}, 500

            return {'message': 'Megazine succes update'}, 200
        else:
            return {'message': 'Megazine not found'}, 404

    def delete(self, id_all):

        megazine_data = Megazine.find_by_id(id_all)

        if megazine_data:
            try:
                megazine_data.delete_to_db()
            except:
                return {"message": "An error occurred update the megazine."}, 500

            return {'message': 'Megazine succes delete'}, 200
        else:
            return {'message': 'Megazine succes delete'}, 404


class MegazineList(Resource):
    def get(self):
        return {'megazine': list(map(lambda megazine: megazine.json(), Megazine.query.all())),
                'total': len(list(map(lambda megazine: megazine.json(), Megazine.query.all())))}


class MegazineListpage(Resource):
    # def get(self, count):
    #     def countx():
    #         return count * 10
    #
    #     data = Megazine.query.all()
    #     megazines = []
    #     megazines_page = []
    #
    #     if not data:
    #         return {"message": "Megazine not found."}, 200
    #     else:
    #         for megazine in data:
    #             megazine_data = {}
    #             megazine_data['id_pub'] = megazine.id_pub
    #             megazine_data['id_author'] = megazine.id_author
    #             megazine_data['title'] = megazine.title
    #             megazine_data['about'] = megazine.about
    #             megazine_data['timestamp'] = str(megazine.timestamp)
    #             megazines.append(megazine_data)
    #
    #         if countx() > len(megazines) and len(megazines) < countx():
    #             for s in range((countx() - 10), len(megazines)):
    #                 megazines_page.append(megazines[s])
    #         else:
    #             for s in range((countx() - 10), countx()):
    #                 megazines_page.append(megazines[s])
    #
    #         if len(megazines_page) > 0:
    #             return {'megazines': megazines_page,
    #                     'total': len(megazines_page)}
    #         else:
    #             return {"message": "Megazine not found."}, 200

        def get(self, id_all):
            def countx():
                return int(id_all) * 10

            data = Megazine.query.filter_by(id_author=id_all).first()

            if data:
                data = Megazine.query.filter_by(id_author=id_all).all()
                megazines = []

                if not data:
                    return {"message": "Megazine not found."}, 200
                else:
                    for megazine in data:
                        megazine_data = {}
                        megazine_data['id_pub'] = megazine.id_pub
                        megazine_data['id_author'] = megazine.id_author
                        megazine_data['title'] = megazine.title
                        megazine_data['about'] = megazine.about
                        megazine_data['timestamp'] = str(megazine.timetamp)
                        megazines.append(megazine_data)

                return {'id_author': id_all,
                        'megazines': megazines,
                        'total': len(megazines)}
            else:
                data = Megazine.query.all()
                megazines = []
                megazines_page = []

                if not data:
                    return {"message": "Megazine not found."}, 200
                else:
                    for megazine in data:
                        megazine_data = {}
                        megazine_data['id_pub'] = megazine.id_pub
                        megazine_data['id_author'] = megazine.id_author
                        megazine_data['title'] = megazine.title
                        megazine_data['about'] = megazine.about
                        megazine_data['timestamp'] = str(megazine.timestamp)
                        megazines.append(megazine_data)

                    if countx() > len(megazines) and len(megazines) < countx():
                        for s in range((countx() - 10), len(megazines)):
                            megazines_page.append(megazines[s])
                    else:
                        for s in range((countx() - 10), countx()):
                            megazines_page.append(megazines[s])

                    return {'megazines': megazines_page,
                            'total': len(megazines_page)}
