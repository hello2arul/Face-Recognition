from flask import Flask, request
from flask.helpers import send_file
from flask_restful import Api, Resource
from alert import alert_user

app = Flask(__name__)
api = Api(app)

class Request(Resource):
    def get(self):
        return send_file("home.html")

    def post(self):
        postedData = request.get_data()
        postedDataInWeb = request.form.to_dict()
        res = alert_user(postedData)
        print(postedData)
        print(res)
        return f"{res}"

api.add_resource(Request, "/")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000)
