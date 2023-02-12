import logging
import os
import time


class LogFormatter(logging.Formatter):
    converter = time.localtime

    def formatTime(self, record, datefmt=None):
        self.converter = time.localtime
        return super().formatTime(record, datefmt)


class GameHandler(logging.FileHandler):

    def emit(self, record):
        if record.levelno >= logging.ERROR and record.exc_info:
            tb = record.exc_info[2]
            lasttb = None
            tb_locals = ""
            while tb:
                lasttb = tb
                tb = tb.tb_next
                tb_locals += str(lasttb.tb_frame.f_locals)

            if lasttb:
                record.msg += "\nlocals: %s" % tb_locals

        super().emit(record)

        if record.levelno >= logging.ERROR and record.exc_text:
            print(record.exc_text)


def setup():
    path = "./log"
    keepsave = 20
    filename = f"log_{time.strftime('%Y-%m-%d-%H-%M-%S')}.txt"
    filepath = os.path.join(path, filename)

    if not os.path.exists(path):
        os.mkdir(path)

    if not os.path.exists(filepath):
        files = os.listdir(path)

        if len(files) > keepsave:
            delfiles = sorted(files,
                              key=lambda x: -os.path.getmtime(
                                os.path.join(path, x)))
            delfiles = delfiles[keepsave:]
            for f in delfiles:
                os.remove(os.path.join(path, f))

    logging.basicConfig(level=logging.DEBUG)

    logging.logThreads = False
    logging.logMultiprocessing = False
    logging.logProcesses = False

    logger = logging.getLogger()
    logger.handlers.clear()

    info_handler = GameHandler(filename=filepath)
    info_handler.setFormatter(LogFormatter(
                              fmt="[%(asctime)s]%(message)s",
                              datefmt="%Y-%m-%d %H:%M:%S"))
    logger.addHandler(info_handler)

    logger.setLevel(logging.DEBUG)
