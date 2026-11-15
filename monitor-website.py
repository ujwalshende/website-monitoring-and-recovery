import time

import requests
import smtplib
import os
import paramiko
import linode_api4
import schedule

EMAIL_ADDRESS = os.environ.get("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
LINODE_TOKEN = os.environ.get("LINODE_TOKEN")

def send_notification(email_msg):
    print("Sending an email...")
    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.starttls()
        smtp.ehlo()
        password = EMAIL_PASSWORD or "" # 'or ""' added to supress type checking error because of None
        sender_email = EMAIL_ADDRESS or ""
        smtp.login(sender_email, password)
        message = f"Subject: SITE DOWN\n{email_msg}"
        smtp.sendmail(sender_email, sender_email, message)
     
def restart_container():
    # restart docker container
    print("Restarting the application...")
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname="172.104.137.210", username="root", key_filename=r"C:\Users\ujwal\.ssh\id_ed25519")
    stdin, stdout, stderror = ssh.exec_command("docker start 25e998e47d67")
    print(stdin)
    print(stdout.readlines())
    ssh.close()
    print("Application restarted")

def restart_server_and_container():
    print("Rebooting the server...")
    client = linode_api4.LinodeClient(LINODE_TOKEN)
    nginx_server = client.load(linode_api4.Instance, 111079235)
    nginx_server.reboot() # type: ignore
    while True:
        time.sleep(1)
        nginx_server = client.load(linode_api4.Instance, 111079235)
        if nginx_server.status == "running":
            time.sleep(20)
            restart_container()
            break

def monitor_application():

    try:
        response = requests.get("http://172-104-137-210.ip.linodeusercontent.com:8080/", timeout=5)
        if response.status_code == 200:
            print("Application running successfully")
        else:
            print("Application Down. Fix it")
            send_notification(f"Application returned {response.status_code}")
            restart_container()

        
        
    except (requests.exceptions.ConnectionError, requests.exceptions.Timeout) as ex:
        print(f"Connection error happened: {ex}")
        send_notification(f"Application not accessible at all.")

        # restart linode server
        restart_server_and_container()
    

schedule.every(5).minutes.do(monitor_application)

while True:
    time.sleep(1)
    schedule.run_pending()

