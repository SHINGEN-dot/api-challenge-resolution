from deployment import urls
from config import config
import tornado.httpserver
import tornado.web
import tornado.ioloop

API_INFO = config.API

port = int(API_INFO['port'])
main_processes = int(API_INFO['main_processes'])


urls_to_deploy = urls.get_urls_for_deploy()

if __name__ == "__main__":
    application = tornado.web.Application(urls_to_deploy)
    server = tornado.httpserver.HTTPServer(application)
    server.bind(port)
    server.start(main_processes)
    tornado.ioloop.IOLoop.current().start()
