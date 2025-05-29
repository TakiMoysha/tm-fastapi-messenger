def get_logger_config(
    level: str = "INFO",
    *,
    handlers: list | None = None,
    propagate: bool = False,
):
    return {
        "handlers": handlers or ["default"],
        "level": level,
        "propagate": propagate,
    }
