import datetime 
import os

from dotenv import load_dotenv

load_dotenv()

def formet_time(str):
    GMT_FORMAT = '%a %b %d %H:%M:%S +0800 %Y'
    timeArray = datetime.datetime.strptime(str, GMT_FORMAT)
    ret_time = timeArray.strftime("%Y-%m-%d %H:%M:%S")
    return ret_time

def getEnv(key):
    return os.getenv(key)
