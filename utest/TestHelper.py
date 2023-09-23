import unittest


class CustomAssert(unittest.TestCase):
    def setExceptionType(self, exception_type):
        self.exceptionType = exception_type

    def assertRaisesWithMessage(self, msg, func, *args, **kwargs):
        try:
            func(*args, **kwargs)
            self.assertFail()
        except Exception as e:
            self.assertEqual(type(e), self.exceptionType)
            self.assertEqual(str(e), msg)
