import logging
logging.basicConfig(filename="blog.log", level=logging.DEBUG)
import os
from flask.ext.script import Manager
from blog import app
from getpass import getpass
from werkzeug.security import generate_password_hash
from blog.models import User

manager = Manager(app)

@manager.command
def run():
  port = int(os.environ.get('PORT',8080))
  app.run(host='0.0.0.0', port=port)

from blog.models import Post
from blog.database import session
  
@manager.command
def seed():
  content = """Lorem ipsum dolor sit amet"""
  
  for i in range(25):
    post = Post(title="Test Post #{}".format(i),content=content)
    session.add(post)
    logging.debug(i)
  session.commit()
  
@manager.command
def adduser():
  name = raw_input("Name:")
  email = raw_input("Email:")
  if session.query(User).filter(User.email = email).first():
    print "User with that email address already exists"
    return
  
  password =""
  password_2 =""
  while not (password and password_2) or password != password_2:
    password=getpass("Password:")
    password_2=getpass("Re-enter password:")
  user = User(name=name,email=email,password=generate_password_hash(password))
  session.add(user) 
  session.commit()
  
  
  
  
if __name__ == "__main__":
  manager.run()
  