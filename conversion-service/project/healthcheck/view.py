from project import Resource

class HealthcheckResource(Resource):
    def get(self):
        return {"status":"ok"}, 200
