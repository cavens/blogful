import unittest
from flask.ext.testing import TestCase
from invoice_calculator import divide_pay
import logging
logging.basicConfig(filename="blog.log", level=logging.DEBUG)

class InvoiceCalculatorTests(unittest.TestCase):
  
  def testDividedFairly(self):
    function_results = divide_pay(360, {"Alice": 3.0, "Bob": 3.0, "Carol": 6.0})
    self.assertEqual(function_results, {"Alice": 90.0, "Bob": 90.0, "Carol": 180.0})
     
  def testDividedFairly_zero(self):
    function_results = divide_pay(360, {"Alice": 0, "Bob": 3.0, "Carol": 6.0})
    self.assertEqual(function_results, {"Alice": 0, "Bob": 120.0, "Carol": 240.0})
    
  def testDividedFairly_zero_total(self):
    with self.assertRaises(ValueError):
      function_results = divide_pay(360, {"Alice": 0, "Bob": 0, "Carol": 0})

  def testDividedFairly_empty(self):
    with self.assertRaises(ValueError):
      function_results = divide_pay(360, {})

  def testDividedFairly_amountZero(self):
    function_results = divide_pay(0, {"Alice": 0, "Bob": 3.0, "Carol": 6.0})
    self.assertEqual(function_results, {"Alice": 0, "Bob": 0, "Carol": 0})
      
if __name__ == "__main__":
  unittest.main()
  
  
  
  