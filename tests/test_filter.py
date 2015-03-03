import os
import unittest
import datetime
os.environ["CONFIG_PATH"] = "blog.config.TestingConfig"
import blog
from blog.filters import *
import logging
logging.basicConfig(filename="blog.log", level=logging.DEBUG)

class Test_filter(unittest.TestCase):
  def testing1(self):
    date = datetime.date(1999, 12, 31)
    formatted = dateformat(date,"%y/%m/%d")
    self.assertEqual(formatted, "99/12/31")
    
if __name__ == "__main__":
  unittest.main()
