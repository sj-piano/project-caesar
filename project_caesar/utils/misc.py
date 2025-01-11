# Imports
import json
import sys


# Components
from datetime import datetime


def iso_timestamp_to_int(iso_timestamp):
    dt_object = datetime.strptime(iso_timestamp, "%Y-%m-%dT%H:%M:%SZ")
    int_timestamp = int(dt_object.timestamp())
    return int_timestamp


def json_to_text(json_data):
    return json.dumps(json_data, indent=4)


def stop(msg=None):
    if (msg):
        print(msg)
    exit()


def exit():
    sys.exit()

