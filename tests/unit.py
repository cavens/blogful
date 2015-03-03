import os
import unittest
import datetime
os.environ["CONFIG_PATH"] = "blog.config.TestingConfig"
import blog
from blog.filters import *
import logging
logging.basicConfig(filename="blog.log", level=logging.DEBUG)

class Unittests(unittest.TestCase):
  def unit_filter(self):
    date = datetime(1999,12,31)
    result = dateformat(date,"%y,%m,%d")
    self.assertEqual(result, "12/31/99")
    
if __name__ == "__main__":
  unittest.main()