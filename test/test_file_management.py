'''Testing for file_manager.py'''

import unittest
import os
import shutil

class TestFileManager(unittest.TestCase):
    '''For testing the File class'''

    @classmethod
    def tearDownClass(self) -> None:
        self.manager.connection.close()
        shutil.rmtree('data')

    @classmethod
    def setUpClass(self):

        # create the required folder
        if not os.path.exists('data'):
            try:
                os.makedirs('data')
            except:
                print(f'Failed to create data directory')
                pass
        
        # stand up the file manager
        from src.LocalDataManager.file_manager import FileManager
        self.manager = FileManager(base_path= 'data', db_file='testFile.db')
        self.manager.create_management_table()
        self.manager.insert_file_into_files('name', 'hash', 'location')


    def test_import(self):
        """ Test that the Data Management module can be imported. """
        import src.LocalDataManager

    def test_create_management_table(self):
        """ Test the database connection. """
        table = self.manager.create_management_table()
        self.manager.create_management_table()
        self.assertTrue(table)

    def test_create_management_folders(self):
        """ Test the creation of the Folder structure"""
        manager = self.manager.create_management_folders()
        self.assertTrue(manager)

    def test_hash_file(self):
        """ Test the file hashing"""

        # Reading a file 
        file = open(r'test/testfile.txt', mode='rb')
        # print(file.read())
        hash = self.manager.hash_file(file)
        self.assertEqual(hash , '9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08')

    def test_insert_file_into_files(self):
        result = self.manager.insert_file_into_files('name.txt', 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'location')
        self.assertGreaterEqual(result, 0)

    def test_check_hashes(self):
        self.assertTrue(self.manager.check_hashes('hash'))
        self.assertFalse(self.manager.check_hashes('not_here'))

    def test_check_names(self):
        self.assertTrue(self.manager.check_names('name'))
        self.assertFalse(self.manager.check_names('not_here'))
    
    def test_save_file(self):
        self.assertTrue(self.manager.save_file(file=open(r'test/testfile.txt', 'rb'),
                                               data_level='bronze'))

if __name__ == '__main__':
    unittest.main()
