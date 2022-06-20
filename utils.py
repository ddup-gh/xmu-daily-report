import json
import os
import requests
from log import get_log_string, logger

import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

MAIL_SERVER_URL = 'http://120.77.39.85:8080/mail/daily_report'

debug = os.getenv("ENV") == "debug"


def send_mail_ori(msg: str, title: str, to: str):
    msg += '\n\n【运行日志】\n' + get_log_string()
    if not debug:
        post = requests.post(MAIL_SERVER_URL, data=json.dumps(
            {"title": title, "body": msg, "dest": to}))
        return post
    else:
        logger.info(msg)
 
def send_mail(msg: str, title: str, to: str):
    msg += '<br/><br/>早安！'
    mymail = "cdyang0912@163.com"
    msg = MIMEText(msg, "html", "utf-8")
    msg["From"] = formataddr(["Someone", mymail])
    msg["Subject"] = title
    
    server = smtplib.SMTP_SSL("smtp.163.com")
    server.login(mymail, "UCVITBGQCCZYXKQP")
    server.sendmail(mymail, to, msg.as_string())
    server.quit()


def fail(msg: str, title: str, email: str = "", e: Exception = None, shutdown=True, run_fail=False, send=False):
    logger.error(msg)
    if e is not None:
        logger.error(e)
    if run_fail:
        raise RuntimeError(msg)
    if send:
        send_mail(msg, title, email)
    if shutdown:
        exit(0)
