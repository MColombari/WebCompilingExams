from webcompilingexams import app


class Log:
    @staticmethod
    def write_debug(row):
        app.logger.debug(row)

    @staticmethod
    def write_info(row):
        app.logger.info(row)

    @staticmethod
    def write_warning(row):
        app.logger.warning(row)

    @staticmethod
    def write_error(row):
        app.logger.error(row)

    @staticmethod
    def write_critical(row):
        app.logger.critical(row)
