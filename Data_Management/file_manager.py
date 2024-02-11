'''A sample data management module'''

import os
import sqlite3
from sqlite3 import Error

class FileManager: 
    """
    A class to represent a the File Manager.
    ...

    Attributes
    ----------

    Methods
    -------

    """

    def __init__(self, db_file):
        """
        Constructs all the necessary attributes for the file manager object.

        Parameters
        ----------
        :db_file: the location of the sqlite database used to manage the files
        """
        try:
            connection = sqlite3.connect(db_file)
        except Error as e:
            print(e)
        self.connection = connection
    
    def create_management_table(self, SQL=None):
        """ create a file management table in the SQLite database
        :param SQL: SQL command to create the table
        :param connection: a database connection

        :return: Boolean
        """
        if SQL is None:
            SQL = """ CREATE TABLE IF NOT EXISTS files (
                                                id integer PRIMARY KEY,
                                                name text NOT NULL,
                                                location text  NOT NULL,
                                                end_date text  NOT NULL
                                            ); """


        try:
            c = self.connection.cursor()
            c.execute(SQL)
        except Error as e:
            print(e)
            return False

        return True

    def create_management_folders(self, base_path, data_arch='medallion'):
        """ create the folders required to manage the files
        :param path: string filepath in which to create the management structure
        :param data_arch: [medallion, levels] data scheme for which to create

        :return: Boolean
        """
        if data_arch == 'medallion':
            levels = ['bronze', 'silver', 'gold']
        elif data_arch =='levels':
            levels = ['level_1', 'level_2', 'level_3']

        if os.path.exists(base_path):
            print(f'{base_path} exists')
        
        for level in levels:
            if os.path.exists(os.path.join(base_path,level)):
                print(f'{os.path.join(base_path,level)} exists')
            else:
                try:
                    os.makedirs(os.path.join(base_path,level))
                except:
                    print(f'Failed to create {os.path.join(base_path,level)}')
                    return False
        
        return True

    

if __name__ == '__main__':
    pass