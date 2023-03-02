import logging
import sys
import os

class logger():
    def __init__(self):
        # clear log records
        with open('runtime.log','w') as log:
            pass
        self.logger = []
        

    def getLogger(self,name,level=-1):
        for logger in self.logger:
            if logger.name == name:
                return logger
        logger = logging.getLogger(name)
        logger.setLevel(level)
        file_handler = logging.FileHandler(filename='log/runtime.log', encoding='utf-8', mode='a')
        file_handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(lineno)d: %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))
        logger.addHandler(file_handler)
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(lineno)d: %(message)s', datefmt='%Y-%m-%d %H:%M:%S'))
        logger.addHandler(stream_handler)
        self.logger.append(logger)
        return logger

