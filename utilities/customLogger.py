import logging

class LogGen:
    @staticmethod
    def loggen(logger_name='automation', log_file=r'logs\linkedin.log', log_level=logging.DEBUG):

        logger = logging.getLogger(logger_name)
        logger.setLevel(log_level)

        file_handler = logging.FileHandler(log_file, encoding = 'utf-8')
        file_handler.setLevel(log_level)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                                      datefmt='%Y-%m-%d %H:%M:%S')
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)


        return logger

