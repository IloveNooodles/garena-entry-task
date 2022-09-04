import logging

formatter = logging.Formatter(fmt='%(asctime)s [%(levelname)s][%(name)s]: %(message)s', datefmt='%m/%d/%Y %I:%M:%S%p')

class Logger:
    def __init__(self, name):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)        
        stream = logging.StreamHandler()
        stream.setLevel(logging.DEBUG)
        stream.setFormatter(formatter)
        self.logger.addHandler(stream)

    def log(self):
        return self.logger