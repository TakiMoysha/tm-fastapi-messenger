class LoggingLoggerConfigFactory:
    def __init__(self, formatter=None):
        self.formatter = formatter

    def get_logger_config(self, level: str = "INFO", *, handlers: list = ["default"], propagate: bool = False):
        return {"handlers": handlers, "level": level, "propagate": propagate}
