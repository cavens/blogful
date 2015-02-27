import logging
logging.basicConfig(filename="blog.log", level=logging.DEBUG)
import os
from flask.ext.script import Manager

from blog import app

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
  
  
if __name__ == "__main__":
  manager.run()
  