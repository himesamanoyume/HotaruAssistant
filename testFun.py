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

def get_single_mp4_file(directory):
    mp4_files = [f for f in os.listdir(directory) if f.endswith('.mp4')]
    if len(mp4_files) == 1:
        return mp4_files[0]
    else:
        return None
    
def test():
    sendHostEmail = smtplib.SMTP(config.notify_smtp_host, config.notify_smtp_port)
    sendHostEmail.login(config.notify_smtp_user, config.notify_smtp_password)
    
    emailObject = MIMEMultipart()
    themeObject = Header("测试", 'utf-8').encode()

    emailObject['subject'] = themeObject
    emailObject['From'] = config.notify_smtp_From

    html = "<html></html>"
    emailObject.attach(MIMEText(html,'html','utf-8'))
    emailObject['To'] = '285835609@qq.com'

    directory = './records/temp'  # 你的文件夹路径
    mp4_file = get_single_mp4_file(directory)
    # print(mp4_file)
    mp4_file_path = f"{directory}/{mp4_file}"
    if mp4_file is not None:
        att = open(mp4_file_path, 'rb')
        part = MIMEBase('application','octet-stream')
        part.set_payload((att).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % mp4_file)
        emailObject.attach(part)

    import threading
    try:
        t = threading.Thread(target=send_mail(config.notify_smtp_From, '285835609@qq.com', sendHostEmail, str(emailObject)))
        t.start()
        t.join()
        t = threading.Thread(target=send_mail(config.notify_smtp_From, 'himeproducer@qq.com', sendHostEmail, str(emailObject)))
        t.start()
        t.join()
        sendHostEmail.quit()
        att.close()
        if os.path.isfile(mp4_file_path):
            os.remove(mp4_file_path)
    except Exception as e:
        print(e)
    # sendHostEmail.sendmail(config.notify_smtp_From, '285835609@qq.com', str(emailObject))
    # sendHostEmail.sendmail(config.notify_smtp_From, 'himeproducer@qq.com', str(emailObject))
    

def send_mail(smtp_from, smtp_to, send_host, email_object):
    send_host.sendmail(smtp_from, smtp_to, email_object)

if __name__ == '__main__':
    test()