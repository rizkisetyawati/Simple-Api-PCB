from flask_restful import Resource, reqparse
from models.event import Event


class NewEvent(Resource):
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

        data = NewEvent.parse.parse_args()

        event_data = Event(data['id_author'],
                              data['title'],
                              data['content'])

        try:
            event_data.save_to_db()
        except:
            return {"message": "An error occurred creating the event."}, 500

        return {"message": "New event created successfully."}, 201


class Events(Resource):
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

        event_data = Event.find_by_id(id_all) or Event.find_by_author(id_all)

        if event_data:
            return event_data.json()
        else:
            return {'message': 'Event not found'}, 404

    def put(self, id_all):

        data = Events.parse.parse_args()
        event_data = Event.find_by_id(id_all)

        if event_data:
            event_data.title = data['title']
            event_data.content = data['content']

            try:
                event_data.save_to_db()
            except:
                return {"message": "An error occurred update the event."}, 500

            return {'message': 'event succes update'}, 200
        else:
            return {'message': 'event not found'}, 404

    def delete(self, id_all):

        event_data = Event.find_by_id(id_all)

        if event_data:
            try:
                event_data.delete_to_db()
            except:
                return {"message": "An error occurred update the event."}, 500

            return {'message': 'Event succes delete'}, 200
        else:
            return {'message': 'Event succes delete'}, 404


class EventList(Resource):
    def get(self):
        return {'event': list(map(lambda event: event.json(), Event.query.all())),
                'total': len(list(map(lambda event: event.json(), Event.query.all())))}


class EventListpage(Resource):
    # def get(self, count):
    #     def countx():
    #         return count * 10
    #
    #     data = Event.query.all()
    #     events = []
    #     events_page = []
    #
    #     if not data:
    #         return {"message": "Event not found."}, 200
    #     else:
    #         for event in data:
    #             event_data = {}
    #             event_data['id_pub'] = event.id_pub
    #             event_data['id_author'] = event.id_author
    #             event_data['title'] = event.title
    #             event_data['content'] = event.content
    #             event_data['timestamp'] = str(event.timestamp)
    #             events.append(event_data)
    #
    #         if countx() > len(events) and len(events) < countx():
    #             for s in range((countx() - 10), len(events)):
    #                 events_page.append(events[s])
    #         else:
    #             for s in range((countx() - 10), countx()):
    #                 events_page.append(events[s])
    #
    #         if len(events_page) > 0:
    #             return {'events': events_page,
    #                     'total': len(events_page)}
    #         else:
    #             return {"message": "Event not found."}, 200




    def get(self, id_all):
        def countx():
            return int(id_all) * 10

        data = Event.query.filter_by(id_author=id_all).first()

        if data:
            data = Event.query.filter_by(id_author=id_all).all()
            events = []

            if not data:
                return {"message": "Event not found."}, 200
            else:
                for event in data:
                    event_data = {}
                    event_data['id_pub'] = event.id_pub
                    event_data['id_author'] = event.id_author
                    event_data['title'] = event.title
                    event_data['content'] = event.content
                    event_data['timestamp'] = str(event.timetamp)
                    events.append(event_data)

            return {'id_author': id_all,
                    'events': events,
                    'total': len(events)}
        else:
            data = Event.query.all()
            events = []
            events_page = []

            if not data:
                return {"message": "Event not found."}, 200
            else:
                for event in data:
                    event_data = {}
                    event_data['id_pub'] = event.id_pub
                    event_data['id_author'] = event.id_author
                    event_data['title'] = event.title
                    event_data['content'] = event.content
                    event_data['timestamp'] = str(event.timestamp)
                    events.append(event_data)

                if countx() > len(events) and len(events) < countx():
                    for s in range((countx() - 10), len(events)):
                        events_page.append(events[s])
                else:
                    for s in range((countx() - 10), countx()):
                        events_page.append(events[s])

                return {'events': events_page,
                        'total': len(events_page)}
