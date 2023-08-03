import time
import socket
import smtplib, ssl
import pymsteams
from email.message import EmailMessage
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException
from paramiko.ssh_exception import SSHException
from netmiko.ssh_exception import AuthenticationException

from asyncio.log import logger
import logging
logger = logging.getLogger('django')

def my_scheduled_job():

    print("##########%%%from CronTab%%%%############")
    myTeamsMessage = pymsteams.connectorcard("https://npciorg.webhook.office.com/webhookb2/bc0ed667-1971-4581-a704-3a3f92268a75@8ca9216b-1bdf-4056-9775-f5e402a48d32/IncomingWebhook/caffc2be4d75408b81ae6e804bcf837e/2fca531a-51bc-4fc2-bd2f-c1535f6f1021")
    myTeamsMessage.addLinkButton("Configure Device", "http://10.1.82.42:80/configure_device")
    myTeamsMessage.summary("Test Message")
    myTeamsMessage.send()
    print("Please check on teams!")
    return True


# while True:
# my_scheduled_job()
# time.sleep(60)

