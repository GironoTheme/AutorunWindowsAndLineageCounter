import logging

logging.basicConfig(level=logging.DEBUG,
                    filename='logs.log',
                    filemode='w',
                    format='%(asctime)s:%(lineno)s - %(levelname)s - %(funcName)s() - %(message)s')
logger = logging.getLogger(__name__)

