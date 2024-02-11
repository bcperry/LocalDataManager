'''Testing for file_manager.py'''

import unittest

class TestFileManager(unittest.TestCase):
    '''For testing the File class'''

    def test_import(self):
        """ Test that the Processing module can be imported. """
        import Data_Management

    def test_create_management_table(self):
        """ Test the database connection. """
        from Data_Management.file_manager import FileManager
        f = FileManager(r'data/testFile.db')
        table = f.create_management_table()
        self.assertTrue(table)

    def test_create_management_folders(self):
        from Data_Management.file_manager import FileManager
        f = FileManager(r'data/testFile.db')
        manager = f.create_management_folders(r'data/managed')
        self.assertTrue(manager)

if __name__ == '__main__':
    unittest.main()
