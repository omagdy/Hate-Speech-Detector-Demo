from microblog import app
import zlib
import zipfile
from flask_mail import Mail, Message

language_files= ["Hateful_Tweets.txt", "German_Hateful_Tweets.txt"]

file_names=[]

for file in language_files:
    try:
        f = open(file)
        last_line = f.read().splitlines()[-1]
        try:
            fx = open("last_saved_line_"+file,'r')
            if last_line!=fx.read():
                file_names.append(file)
                fx = open("last_saved_line_"+file,'w')
                fx.write(last_line)
            fx.close()
        except IOError:
            file_names.append(file)
            fx = open("last_saved_line_"+file,'w')
            fx.write(last_line)
            fx.close()
        f.close()            
    except IOError:
        print("File "+file+" not accessible")


def compress(file_names):
    compression = zipfile.ZIP_DEFLATED
    zf = zipfile.ZipFile("Backup.zip", mode="w")
    path_names=[]
    for file_name in file_names: 
        fp=app.open_resource("../"+file_name)
        path_names.append(fp.name)
    try:
        for file_name,path_name in zip(file_names,path_names):
            zf.write(path_name, file_name, compress_type=compression)
    except FileNotFoundError:
        pass
    finally:
        zf.close()

with app.app_context():
    mail = Mail(app)
    msg = Message("Tweets Database Backup", recipients=["hussei05@ads.uni-passau.de"])
    msg.body = "This is an automatic message. Kindly find the updated database backup attached."

    compress(file_names)

    with app.open_resource("../Backup.zip") as fp:
        msg.attach("Backup.zip", "application/zip", fp.read())

    if file_names:
        mail.send(msg)
