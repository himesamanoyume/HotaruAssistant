import pyautogui
import time
from managers.config_manager import config
from managers.translate_manager import _
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
import random
from datetime import datetime
from email.mime.base import MIMEBase
import time
from email import encoders
import os


if __name__ == '__main__':
    # test()
    
    print(os.path.getsize("E:\MyDownload\\2023-11-20_12-13-55.mp4"))