import paramiko, sys
from es_secrets import SSH as SSHkeys

host = SSHkeys.host
port = SSHkeys.port
password = SSHkeys.password
username = SSHkeys.username

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(host, port, username, password)

sftp = ssh.open_sftp()

#def upload(path,localpath):
path = "/public_html/result-sitemap.xml"
localpath = "SEO/result-sitemap.xml"
sftp.put(localpath, path)

sftp.close()
ssh.close()