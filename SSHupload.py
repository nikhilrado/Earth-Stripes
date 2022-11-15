import paramiko, sys
from es_secrets import SSH as SSHkeys

host = SSHkeys.host
port = SSHkeys.port
password = SSHkeys.password
username = SSHkeys.username

# uploads a file to the server
def upload(path, local_path):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, port, username, password)

    sftp = ssh.open_sftp()

    #path = "/public_html/result-sitemap.xml"
    #local_path = "SEO/result-sitemap.xml"
    sftp.put(local_path, path)

    sftp.close()
    ssh.close()