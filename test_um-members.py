import unittest

if __name__ == '__main__':
    # Discover and run all test files in the 'tests/' directory that match the pattern 'test_*.py'
    loader = unittest.TestLoader()
    suite = loader.discover('tests', pattern='test_*.py')
    runner = unittest.TextTestRunner()
    runner.run(suite)
