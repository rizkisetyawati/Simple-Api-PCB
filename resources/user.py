from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):
    parse = reqparse.RequestParser()
    parse.add_argument('first_name',
                       type=str,
                       required=True,
                       help='This field cannot be blank.')
    parse.add_argument('last_name',
                       type=str,
                       required=True,
                       help='This field cannot be blank.')
    parse.add_argument('password',
                       type=str,
                       required=True,
                       help='This field cannot be blank.')
    parse.add_argument('email',
                       type=str,
                       required=True,
                       help='This field cannot be blank.')
    parse.add_argument('mobile_phone',
                       type=str,
                       required=True,
                       help='This field cannot be blank.')
    parse.add_argument('gender',
                       type=str,
                       required=True,
                       help='This field cannot be blank.')
    parse.add_argument('about',
                       type=str,
                       required=False,
                       help='This field cannot be blank.')
    parse.add_argument('interest',
                       type=str,
                       required=False,
                       help='This field cannot be blank.')
    parse.add_argument('semester',
                       type=str,
                       required=True,
                       help='This field cannot be blank.')

    def post(self):

        data = UserRegister.parse.parse_args()

        if UserModel.find_by_email(data['email']):
            return {"message": "A user with that email already exists"}, 400
        elif UserModel.find_by_phone(data['mobile_phone']):
            return {"message": "A user with that phone number already exists"}, 400

        user_data = UserModel(data['first_name'],
                              data['last_name'],
                              data['password'],
                              data['email'],
                              data['mobile_phone'],
                              data['gender'],
                              data['about'],
                              data['interest'],
                              data['semester'])

        try:
            user_data.save_to_db()
        except:
            return {"message": "An error occurred creating the user."}, 500

        return {"message": "User created successfully."}, 201


class Users(Resource):
    parse = reqparse.RequestParser()
    parse.add_argument('first_name',
                       type=str,
                       required=True,
                       help='This field cannot be blank.')
    parse.add_argument('last_name',
                       type=str,
                       required=True,
                       help='This field cannot be blank.')
    parse.add_argument('password',
                       type=str,
                       required=True,
                       help='This field cannot be blank.')
    parse.add_argument('email',
                       type=str,
                       required=True,
                       help='This field cannot be blank.')
    parse.add_argument('mobile_phone',
                       type=str,
                       required=True,
                       help='This field cannot be blank.')
    parse.add_argument('gender',
                       type=str,
                       required=True,
                       help='This field cannot be blank.')
    parse.add_argument('about',
                       type=str,
                       required=False,
                       help='This field cannot be blank.')
    parse.add_argument('interest',
                       type=str,
                       required=False,
                       help='This field cannot be blank.')
    parse.add_argument('semester',
                       type=str,
                       required=True,
                       help='This field cannot be blank.')

    def get(self, id_all):

        user_data = UserModel.find_by_id(id_all) or UserModel.find_by_email(id_all) or UserModel.find_by_phone(id_all)

        if user_data:
            return user_data.json()
        else:
            return {'message': 'User not found'}, 404

    def put(self, id_all):

        data = Users.parse.parse_args()
        user_data = UserModel.find_by_id(id_all) or UserModel.find_by_email(id_all)

        if user_data:
            user_data.first_name = data['first_name']
            user_data.last_name = data['last_name']
            user_data.password = data['password']
            user_data.email = data['email']
            user_data.mobile_phone = data['mobile_phone']
            user_data.gender = data['gender']
            user_data.about = data['about']
            user_data.interest = data['interest']
            user_data.semester = data['semester']

            try:
                user_data.save_to_db()
            except:
                return {"message": "An error occurred update the user."}, 500

            return {'message': 'User succes update'}, 200
        else:
            return {'message': 'User not found'}, 404

    def delete(self, id_all):

        user_data = UserModel.find_by_id(id_all) or UserModel.find_by_email(id_all)

        if user_data:
            try:
                user_data.delete_to_db()
            except:
                return {"message": "An error occurred update the user."}, 500

            return {'message': 'User succes delete'}, 200
        else:
            return {'message': 'User succes delete'}, 404


class UserList(Resource):
    def get(self):
        return {'users': list(map(lambda users: users.json(), UserModel.query.all())),
                'total': len(list(map(lambda users: users.json(), UserModel.query.all())))}


class UserListpage(Resource):
    def get(self, count):
        def countx():
            return count * 10

        data = UserModel.query.all()
        users = []
        users_page = []

        if not data:
            return {"message": "User not found."}, 200
        else:
            for user in data:
                user_data = {}
                user_data['id_pub'] = user.id_pub
                user_data['first_name'] = user.first_name
                user_data['last_name'] = user.last_name
                user_data['email'] = user.email
                user_data['mobile_phone'] = user.mobile_phone
                user_data['gender'] = user.gender
                user_data['about'] = user.about
                user_data['interest'] = user.interest
                user_data['semester'] = user.semester
                users.append(user_data)

            if countx() > len(users) and len(users) < countx():
                for s in range((countx() - 10), len(users)):
                    users_page.append(users[s])
            else:
                for s in range((countx() - 10), countx()):
                    users_page.append(users[s])

            return {'users': users_page,
                    'total': len(users_page)}
