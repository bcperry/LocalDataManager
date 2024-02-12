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
        from Data_Management.file_manager import FileManager
        self.manager = FileManager(base_path= 'data', db_file='testFile.db')
        self.manager.create_management_table()
        self.manager.insert_file_into_files('name', 'hash', 'location')


    def test_import(self):
        """ Test that the Data Management module can be imported. """
        import Data_Management

    def test_create_management_table(self):
        """ Test the database connection. """
        table = self.manager.create_management_table()
        self.manager.create_management_table()
        self.assertTrue(table)

    def test_create_management_folders(self):
        """ Test the creation of the Folder structure"""
        manager = self.manager.create_management_folders(r'data/managed')
        self.assertTrue(manager)

    def test_hash_file(self):
        """ Test the file hashing"""

        # Reading a file 
        file = open(r'test/testfile.txt', 'r', encoding='utf-8')
        print(file.read())
        hash = self.manager.hash_file(file)
        self.assertEquals(hash , 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855')

    def test_insert_file_into_files(self):
        result = self.manager.insert_file_into_files('name.txt', 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 'location')
        self.assertGreaterEqual(result, 0)

    def test_check_hashes(self):
        self.assertTrue(self.manager.check_hashes('hash'))
        self.assertFalse(self.manager.check_hashes('not_here'))

if __name__ == '__main__':
    unittest.main()
