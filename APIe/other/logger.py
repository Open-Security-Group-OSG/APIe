import logging

from rich.logging import RichHandler


def set_logging_config(level: int, filename: str = "default.log"):
    match level:
        case 10:
            log_level = logging.DEBUG
        case 20:
            log_level = logging.INFO
        case 30:
            log_level = logging.WARNING
        case 40:
            log_level = logging.ERROR
        case 50:
            log_level = logging.CRITICAL
        case _:
            log_level = logging.NOTSET

    logging.basicConfig(level=log_level,
                format="%(asctime)s [%(levelname)s] %(message)s",
                handlers=[logging.FileHandler(filename),
                          RichHandler(show_time=False, show_level=False, omit_repeated_times=False, rich_tracebacks=True, markup=True)])


log = logging.getLogger(__name__)
