import logging

def log(current_module, filename):
    
    logger = logging.getLogger(current_module)
    logger.setLevel(logging.DEBUG)
     
    formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s')
     
    file_handler = logging.FileHandler(filename)
    stream_handler = logging.StreamHandler()
     
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)
     
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger
