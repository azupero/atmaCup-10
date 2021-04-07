import numpy as np
import time
import logging
from contextlib import contextmanager
from typing import Optional
import random
import os


def get_logger(out_file=None):
    logger = logging.getLogger()  # loggerの呼び出し
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(message)s]"
    )  # ログ出力の際のフォーマットを定義
    logger.handlers = []  # ハンドラーを追加するためのリスト
    logger.setLevel(logging.INFO)  # ロギングのレベルを設定, 'INFO' : 想定された通りのことが起こったことの確認

    handler = logging.StreamHandler()  # StreamHandler(コンソールに出力するハンドラ)を追加
    handler.setFormatter(formatter)
    handler.setLevel(logging.INFO)
    logger.addHandler(handler)

    # ログをファイルとして出力する際のハンドラ(FileHandler)
    if out_file is not None:
        fh = logging.FileHandler(out_file)
        fh.setFormatter(formatter)
        fh.setLevel(logging.INFO)
        logger.addHandler(fh)

    logger.info("logger set up")  # "logger set up"を表示
    return logger


@contextmanager
def timer(name: str, logger: Optional[logging.Logger] = None):
    t0 = time.time()
    msg = f"<{name}> start"
    if logger is None:
        print(msg)
    else:
        logger.info(msg)
    yield

    msg = f"<{name}> done in {time.time() - t0:.2f} s"
    if logger is None:
        print(msg)
    else:
        logger.info(msg)


def set_seed(seed: int = 42):
    random.seed(seed)
    np.random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)
