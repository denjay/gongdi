########################################
# create by :mis82
# create time :2018-02-26 16:13:31.389193
########################################
import unittest
def test():
    """Run the unit tests."""
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)
