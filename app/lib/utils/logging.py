def get_logger_config(
    level: str = "INFO",
    *,
    handlers: list = ["default"],
    propagate: bool = False,
):
    return {
        "handlers": handlers,
        "level": level,
        "propagate": propagate,
    }
