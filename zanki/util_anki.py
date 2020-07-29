import sys
import os
import time
import requests
import json
from requests.exceptions import ConnectionError, Timeout
import platform

WINDOWS_CANDIDATES = [
    r"%APPDATA%\Anki2"
]
LINUX_CANDIDATES = [
    "~/.local/share/Anki2",
    "~/Anki",
    "~/Documents/Anki"
]
MAC_CANDIDATES = [
    "~/Library/Application Support/Anki2"
]
DEFAULT_USERNAME = "用户1"

def look_for_existing_dir(dirs):
    for dir in dirs:
        dir = os.path.expandvars(dir)
        dir = os.path.expanduser(dir)
        if os.path.exists(dir) and os.path.isdir(dir):
            return dir
    return None

def get_anki_dir():
    if is_windows():
        return look_for_existing_dir(WINDOWS_CANDIDATES)
    elif is_linux():
        return look_for_existing_dir(LINUX_CANDIDATES)
    elif is_mac():
        return look_for_existing_dir(MAC_CANDIDATES)
    return None

def get_user_dir(user=DEFAULT_USERNAME):
    anki_dir = get_anki_dir()
    if anki_dir is not None:
        dst_dir = os.path.join(anki_dir, user)
        if os.path.exists(dst_dir) and os.path.isdir(dst_dir):
            return dst_dir
    return None

def get_default_collection(user=DEFAULT_USERNAME):
    user_dir = get_user_dir(user)
    if user_dir is not None:
        dst_file = os.path.join(user_dir, "collection.anki2")
        return dst_file
    raise Exception("Anki was not installed or user (%s) was not created." %(user))

def is_windows():
    return platform.system() == "Windows"

def is_linux():
    return platform.system() == "Linux"

def is_mac():
    return platform.system() == "Darwin"
