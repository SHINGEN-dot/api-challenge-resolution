from concurrent.futures import ThreadPoolExecutor
from config import config

WORKER_INFO = config.WORKER

workers = int(WORKER_INFO['workers'])


aux_executor = ThreadPoolExecutor(max_workers=workers)


def get_aux_executor() -> ThreadPoolExecutor:
    """ Return ThreadPoolExecutor for execute sync tasks """
    return aux_executor
