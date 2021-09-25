from flask import Flask, request
from flask_restful import Api, Resource
import traceback
app = Flask(__name__)
api = Api(app)

assets = []
tasks = []
workers = []
allocated_assets = []

class Assetlist(Resource):
    def get(self):
        return {'assets': assets}, 200

class Assetadd(Resource):
    def post(self):
        # if request.args != 2:
        #     return {'message': 'Insufficient arguments in payload %s'%str(request.args)}, 401
        try:
            request_data = request.get_json()
            _id = request_data['asset_id']
            _name = request_data['asset_name']
            asset = {
                        'asset_id': _id,
                        'asset_name': _name
                    }
            assets.append(asset)
        except Exception as exp:
            return {'message': str(traceback.format_exc())}, 400
        return {'message': 'asset added successfully'}, 201

class Assetallocate(Resource):
    def post(self):
        # if request.args != 5:
        #     return {'message': 'Insufficient arguments in payload'}, 401
        try:
            worker_id_list = []
            worker_task_list = []
            request_data = request.get_json()
            asset_id = request_data['asset_id']
            task_id = request_data['task_id']
            worker_id = request_data['worker_id']
            time_of_allocation = request_data['time_of_allocation']
            task_to_perform = request_data['task_to_perform']

            for worker in workers:
                if worker['worker_id'] == worker_id:
                    worker_task_list = worker['worker_tasks']
                    worker_task_list.append(task_to_perform)
                worker_id_list.append(worker['worker_id'])
            if worker_id not in worker_id_list:
                msg = 'Invalid worker id is provided, cannot allocate task to worker'
                return {'message': msg}, 404

            allocate = {
                        'asset_id': asset_id,
                        'task_id': task_id,
                        'worker_id': worker_id,
                        'time_of_allocation': time_of_allocation,
                        'task_to_perform': task_to_perform
                        }
            allocated_assets.append(allocate)
        except Exception as exp:
            return {'message': str(exp)}, 400
        return {'message': 'task allocated successfully'}, 201

class Task(Resource):
    def post(self):
        # if request.args != 3:
        #     return {'message': 'Insufficient arguments in payload'}, 401
        try:
            request_data = request.get_json()
            _id = request_data['task_id']
            id_asset_name = request_data['task_desc']['asset_name']
            id_description = request_data['task_desc']['description']
            id_frequency = request_data['task_desc']['frequency']
            task = {
                    'task_id': _id,
                    'task_desc':
                                {
                                    'asset_name': id_asset_name,
                                    'description': id_description,
                                    'frequency': id_frequency
                                }
                    }
            tasks.append(task)
        except Exception as exp:
            return {'message': str(exp)}, 400
        return {'message': 'task added successfully'}, 201

class Worker(Resource):
    def post(self):
        try:
            request_data = request.get_json()
            _id = request_data['worker_id']
            _name = request_data['worker_name']
            _tasks = request_data['worker_tasks']
            worker = {
                        'worker_id': _id,
                        'worker_name': _name,
                        'worker_tasks': _tasks
                    }
            workers.append(worker)
        except Exception as exp:
            return {'message': str(traceback.format_exc())}, 400
        return {'message': 'worker added successfully'}, 201

class Workertasks(Resource):
    def get(self, w_id):
        workers_id_list = []
        for worker in workers:
            if int(worker['worker_id']) == w_id:
                return {'worker_tasks': worker['worker_tasks']}, 200
            workers_id_list.append(worker['worker_id'])
        if w_id not in workers_id_list:
            return {'message': 'Entry for worker with id = {} does not exist'.format(w_id)}, 404

api.add_resource(Assetadd, '/add-asset')
api.add_resource(Task, '/add-task')
api.add_resource(Worker, '/add-worker')
api.add_resource(Assetlist, '/asset/all')
api.add_resource(Assetallocate, '/allocate-task')
api.add_resource(Workertasks, '/get-tasks-for-worker/<int:w_id>')

app.run(debug=True)
