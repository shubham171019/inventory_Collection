import csv
import time
import socket
import smtplib, ssl
import pymsteams
from email.message import EmailMessage
from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException
from paramiko.ssh_exception import SSHException
from netmiko.ssh_exception import AuthenticationException

# def send_commands(): 
#     with open("commands_to_send.txt") as f:
#         commands_to_send_router = f.read().splitlines()           
#         return commands_to_send_router              

def isOpen():
    myTeamsMessage = pymsteams.connectorcard("https://npciorg.webhook.office.com/webhookb2/bc0ed667-1971-4581-a704-3a3f92268a75@8ca9216b-1bdf-4056-9775-f5e402a48d32/IncomingWebhook/caffc2be4d75408b81ae6e804bcf837e/2fca531a-51bc-4fc2-bd2f-c1535f6f1021")
    myTeamsMessage.addLinkButton("Configure Device", "http://10.2.71.108:5000/configure_device")
    myTeamsMessage.text("hiiiiiiiiiiiii")
    # myTeamsMessage.text(mydict['IP_Address']+" being port down: "+ mydict["Port_no"])
    myTeamsMessage.send() 
    print("Please check on teams!")

# def doit(): 
#     mydict_details = call_details()
#     isOpen(mydict_details)

# def call_details():
#     mydict = {} 
#     filename = "data.csv"
#     with open(filename, 'r') as csvfile:
#         csvreader = csv.reader(csvfile)
#         fields = next(csvreader)
#         for i,j,k,l in csvreader:
#             mydict["IP_Address"] = i.strip()
#             mydict["Port_no"] = j.strip()
#             mydict["Username_ip"] = k.strip()
#             mydict["Password_ip"] = l.strip()
         
#     return mydict

if __name__ == "__main__":
    while True:
        isOpen()
        # time.sleep(120)      