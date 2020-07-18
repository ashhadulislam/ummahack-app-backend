# app/__init__.py

from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy

# local import
from instance.config import app_config

from flask import request, jsonify, abort, make_response

# initialize sql-alchemy
db = SQLAlchemy()


def create_app(config_name):
    from app.models import Bucketlist, User, UserProfile

    app = FlaskAPI(__name__, instance_relative_config=True)
    print("config_name = ",config_name)
    print("App_config are ",app_config)
    app.config.from_object(app_config[config_name])
    print("db uri=",app_config[config_name].SQLALCHEMY_DATABASE_URI)
    app.config.from_pyfile('config.py')
    print("State of env = ",config_name)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)


    @app.route('/bucketlists/', methods=['POST', 'GET'])
    def bucketlists():
        # Get the access token from the header
        auth_header = request.headers.get('Authorization')
        print("Auth header is ",auth_header)
        access_token = auth_header.split(" ")[1]

        if access_token:
         # Attempt to decode the token and get the User ID
            user_id = User.decode_token(access_token)
            print("user id is ",user_id)
            if not isinstance(user_id, str):
                # Go ahead and handle the request, the user is authenticated

                if request.method == "POST":
                    content=request.json
                    name=content["name"]
                    # name = str(request.data.get('name', ''))
                    if name:
                        bucketlist = Bucketlist(name=name, created_by=user_id)
                        bucketlist.save()
                        response = jsonify({
                            'id': bucketlist.id,
                            'name': bucketlist.name,
                            'date_created': bucketlist.date_created,
                            'date_modified': bucketlist.date_modified,
                            'created_by': user_id
                        })

                        return make_response(response), 201

                else:
                    # GET all the bucketlists created by this user
                    bucketlists = Bucketlist.query.filter_by(created_by=user_id)
                    results = []

                    for bucketlist in bucketlists:
                        obj = {
                            'id': bucketlist.id,
                            'name': bucketlist.name,
                            'date_created': bucketlist.date_created,
                            'date_modified': bucketlist.date_modified,
                            'created_by': bucketlist.created_by
                        }
                        results.append(obj)

                    return make_response(jsonify(results)), 200
            else:
                # user is not legit, so the payload is an error message
                message = user_id
                response = {
                    'message': message
                }
                return make_response(jsonify(response)), 401  

    @app.route('/bucketlists/', methods=['GET', 'PUT', 'DELETE'])
    def bucketlist_manipulation(id, **kwargs):
     # retrieve a buckelist using it's ID
        bucketlist = Bucketlist.query.filter_by(id=id).first()
        if not bucketlist:
            # Raise an HTTPException with a 404 not found status code
            abort(404)

        if request.method == 'DELETE':
            bucketlist.delete()
            return {
            "message": "bucketlist {} deleted successfully".format(bucketlist.id) 
         }, 200

        elif request.method == 'PUT':
            content=request.json
            # name = str(request.data.get('name', ''))
            name = str(content['name'])
            bucketlist.name = name
            bucketlist.save()
            response = jsonify({
                'id': bucketlist.id,
                'name': bucketlist.name,
                'date_created': bucketlist.date_created,
                'date_modified': bucketlist.date_modified
            })
            response.status_code = 200
            return response
        else:
            # GET
            response = jsonify({
                'id': bucketlist.id,
                'name': bucketlist.name,
                'date_created': bucketlist.date_created,
                'date_modified': bucketlist.date_modified
            })
            response.status_code = 200
            return response

###############################################
    @app.route('/userprofiles/', methods=['POST', 'GET'])
    def userprofiles():
        # Get the access token from the header
        auth_header = request.headers.get('Authorization')
        print("Auth header is ",auth_header)
        access_token = auth_header.split(" ")[1]

        if access_token:
         # Attempt to decode the token and get the User ID
            user_id = User.decode_token(access_token)
            print("user id is ",user_id)
            if not isinstance(user_id, str):
                # Go ahead and handle the request, the user is authenticated

                if request.method == "POST":
                    content=request.json
                    print("Content received = ",content)
                    first_name = str(content['first_name'])
                    last_name = str(content['last_name'])
                    gender = str(content['gender'])
                    category = str(content['category'])
                    area = str(content['area'])
                    contact = str(content['contact'])
                    lat = str(content['coord']['lat'])
                    lon = str(content['coord']['lon'])
                    if first_name:
                        print("First name = ",first_name)
                        userprofile = UserProfile(first_name=first_name,                             
                            last_name=last_name, 
                            gender=gender, 
                            category=category, 
                            area=area, 
                            contact=contact,
                            lat=lat, 
                            lon=lon, 
                            created_by=user_id)
                        print("saving in db")
                        userprofile.save()
                        print("Saved")
                        response = jsonify({
                            'id': userprofile.id,
                            'first_name': userprofile.first_name,
                            'date_created': userprofile.date_created,
                            'date_modified': userprofile.date_modified,
                            'created_by': user_id
                        })

                        return make_response(response), 201

                else:
                    # GET all the bucketlists created by this user
                    userprofiles = UserProfile.query.filter_by(created_by=user_id)
                    results = []

                    for userprofile in userprofiles:
                        obj = {
                            'id': userprofile.id,
                            'first_name': userprofile.first_name,
                            'last_name': userprofile.last_name,
                            'gender': userprofile.gender,
                            'category': userprofile.category,
                            'area': userprofile.area,
                            'contact': userprofile.contact,
                            'lat': userprofile.lat,
                            'lon': userprofile.lon,

                            'date_created': userprofile.date_created,
                            'date_modified': userprofile.date_modified,
                            'created_by': userprofile.created_by
                        }
                        results.append(obj)

                    return make_response(jsonify(results)), 200
            else:
                # user is not legit, so the payload is an error message
                message = user_id
                response = {
                    'message': message
                }
                return make_response(jsonify(response)), 401 




    @app.route('/userprofiles/<id>', methods=['GET', 'PUT', 'DELETE'])
    def userprofile_manipulation(id, **kwargs):
     # retrieve a buckelist using it's ID
        print("id is ",id)
        userprofile = UserProfile.query.filter_by(id=id).first()
        if not userprofile:
            # Raise an HTTPException with a 404 not found status code
            abort(404)

        if request.method == 'DELETE':
            userprofile.delete()
            return {
            "message": "userprofile {} deleted successfully".format(userprofile.id) 
         }, 200

        elif request.method == 'PUT':
            content=request.json
            # name = str(request.data.get('name', ''))
            first_name = str(content['first_name'])
            last_name = str(content['last_name'])
            gender = str(content['gender'])
            category = str(content['category'])
            area = str(content['area'])
            contact = str(content['contact'])
            lat = str(content['coord']['lat'])
            lon = str(content['coord']['lon'])
            
            userprofile.first_name = first_name
            userprofile.last_name = last_name
            userprofile.gender = gender
            userprofile.category = category
            userprofile.area = area
            userprofile.contact = contact
            userprofile.lat = lat
            userprofile.lon = lon

            userprofile.save()

            response = jsonify({
                'id': userprofile.id,
                'name': userprofile.first_name,
                'date_created': userprofile.date_created,
                'date_modified': userprofile.date_modified
            })
            response.status_code = 200
            return response
        else:
            # GET
            response = jsonify({
                'id': userprofile.id,
                'first_name': userprofile.first_name,
                'last_name': userprofile.last_name,
                'gender': userprofile.gender,
                'category': userprofile.category,
                'area': userprofile.area,
                'contact': userprofile.contact,
                'lat': userprofile.lat,
                'lon': userprofile.lon,

                'date_created': userprofile.date_created,
                'date_modified': userprofile.date_modified,
                'created_by': userprofile.created_by
            })
            response.status_code = 200
            return response
#################################################                




    # import the authentication blueprint and register it on the app
    from .auth import auth_blueprint
    app.register_blueprint(auth_blueprint)
    return app



