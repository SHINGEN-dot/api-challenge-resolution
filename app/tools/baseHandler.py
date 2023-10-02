from abc import ABC
import tornado.web


class BaseHandler(tornado.web.RequestHandler, ABC):

    def set_default_headers(self: tornado.web.RequestHandler):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "Authorization,Content-type,Accept,X-Access-Token,X-Access,X-Key")
        self.set_header("Access-Control-Allow-Methods", "GET,POST")

    def options(self: tornado.web.RequestHandler):
        # to save CORS on development
        self.set_status(204)
        self.finish()
