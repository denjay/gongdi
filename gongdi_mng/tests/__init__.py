########################################
# create by :cxh-PC
# create time :2018-01-31 11:55:31.685293
########################################
import unittest
def test():
    """Run the unit tests."""
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
