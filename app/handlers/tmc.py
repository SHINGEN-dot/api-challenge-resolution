import tools.baseHandler
import tornado.gen
from abc import ABC
from ujson import decode
from tools import worker
from tornado.concurrent import run_on_executor
from business import tmc
from logger import loggerApi


class ProductionPlan(tools.baseHandler.BaseHandler, ABC):
    """ Manage receive request on /productionplan path """

    executor = worker.get_aux_executor()

    @run_on_executor(executor='executor')
    def post_background(self, json_body):
        data = dict()
        try:
            parameters = tmc.extract_data(json_body=json_body)
            if not parameters:
                data['status_code'] = 500
                data['response'] = {'response': 'json body does not contain all need data'}
            else:
                result = tmc.found_optimal(parameters=parameters)
                if result:
                    data['status_code'] = 200
                    if result['success']:
                        data['response'] = {'resolution': 'success', 'result': result['solution']}
                    else:
                        data['response'] = {'resolution': 'not possible', 'max load possible': result['max_load']}
                else:
                    data['status_code'] = 500
                    data['response'] = {'response': 'Internal server error', 'detail': 'Not working'}

        except Exception as error:
            data['status_code'] = 500
            data['response'] = {'response': 'Internal server error',  'detail': str(error)}
        return data

    @tornado.gen.coroutine
    def post(self, **kwargs):
        data = dict()
        try:
            try:
                json_body = decode(self.request.body)
                data = yield self.post_background(json_body)
            except Exception as error:
                data['status_code'] = 400
                data['response'] = {'response': 'Invalid JSON', 'detail': str(error)}
            self.set_status(status_code=data['status_code'])
            self.write(data['response'])
            loggerApi.write_log(self)
        except Exception as error:
            data['status_code'] = 400
            data['response'] = {'response': 'Invalid JSON', 'detail': str(error)}
            self.write(data['response'])
            loggerApi.write_log(self)
