import os
import sys
import tempfile
import time
from pathlib import Path

cache = Path(tempfile.gettempdir()) / "nethack_cache"
cache.mkdir(parents=True, exist_ok=True)
os.environ.setdefault("XDG_CACHE_HOME", str(cache / "xdg"))
os.environ.setdefault("NUMBA_CACHE_DIR", str(cache / "numba"))
sys.path.insert(0, "/bot")


def t(label, fn):
    t0 = time.time()
    try:
        fn()
        print(f"RESULT {label} {time.time() - t0:.2f}s ok", flush=True)
    except Exception as e:
        print(f"RESULT {label} {time.time() - t0:.2f}s FAIL {type(e).__name__}: {e}", flush=True)


t("import numpy", lambda: __import__("numpy"))
t("import cv2", lambda: __import__("cv2"))
t("import numba", lambda: __import__("numba"))
t("import scipy", lambda: __import__("scipy"))
t("import nltk", lambda: __import__("nltk"))
t("nltk.edit_distance", lambda: __import__("nltk.edit_distance", fromlist=["x"]))
t("import autoascend.agent", lambda: __import__("autoascend.agent", fromlist=["x"]))
t("import bot", lambda: __import__("bot"))
t("make_agent", lambda: __import__("bot").make_agent())
print("IMPORTS_DONE", flush=True)
