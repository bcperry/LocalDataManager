'''A sample data management module'''

import os
import sqlite3
import hashlib
import logging
from sqlite3 import Error

class FileManager: 
    """
    A class to represent a the File Manager.
    ...

    Attributes
    ----------
    :connection: the database connection object

    Methods
    -------
    :create_management_table: 
    :create_management_folders:
    :hash_file:
    :check_hash:
    :manage_file:

    """

    def __init__(self, base_path, db_file):
        """
        Constructs all the necessary attributes for the file manager object.

        Parameters
        ----------
        :base_path: the path to the data management system
        :db_file: the name of the sqlite database used to manage the files
        """

        self.base_path = base_path

        try:
            self.create_management_folders()
            connection = sqlite3.connect(os.path.join(base_path,db_file))
            self.connection = connection
            self.create_management_table()
        except Error as e:
            logging.info(e)

    
    def create_management_table(self, SQL=None):
        """ create a file management table in the SQLite database
        :param SQL: SQL command to create the table
        :param connection: a database connection

        :return: Boolean
        """
        if SQL is None:
            SQL = """ CREATE TABLE IF NOT EXISTS files (
                                                name text NOT NULL,
                                                hash text PRIMARY KEY,
                                                location text NOT NULL
                                            ); """


        try:
            c = self.connection.cursor()
            c.execute(SQL)
        except Error as e:
            logging.info(e)
            return False

        return True

    def create_management_folders(self, base_path=r'data/managed_data', data_arch='medallion'):
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
            logging.info(f'{base_path} exists')
        
        for level in levels:
            if os.path.exists(os.path.join(base_path,level)):
                logging.info(f'{os.path.join(base_path,level)} exists')
            else:
                try:
                    os.makedirs(os.path.join(base_path,level))
                except:
                    logging.error(f'Failed to create {os.path.join(base_path,level)}')
                    return False
        return True

    def insert_file_into_files(self, name, hash, location):
        """
        Create a new file into the files table
        :param file:
        :return: file id
        """
        sql = ''' INSERT INTO files(name,hash,location)
                VALUES(?,?,?) '''
        cur = self.connection.cursor()
        cur.execute(sql, (name, hash, location))
        self.connection.commit()
        return cur.lastrowid

    def hash_file(self, file):
        """
        Provides hashing functionality.

        Parameters:
            file:

        Returns:
            The sha256 hash in hex format 

        """

        # A arbitrary (but fixed) buffer size
        # 65536 = 65536 bytes = 64 kilobytes
        BUF_SIZE = 65536

        # Initializing the sha256() method
        sha256 = hashlib.sha256()

        # Opening the file provided
        while True:
            data = file.read()

            # True if eof = 1
            if not data:
                break

            # Passing that data to that sh256 hash 
            # function (updating the function with that data)
            sha256.update(data)

        # sha256.hexdigest() hashes all the input data passed
        # to the sha256() via sha256.update()
        # Acts as a finalize method, after which 
        # all the input data gets hashed
        # hexdigest() hashes the data, and returns 
        # the output in hexadecimal format
        return sha256.hexdigest()

    def check_hashes(self, hash):
        """
        Provides functionality to check if a file has been hashed previously.

        Parameters:
            hash:

        Returns:
            boolean 

        """
        # Creating cursor object using connection object
        cursor = self.connection.cursor()
            
        # executing our sql query
        cursor.execute("""SELECT hash FROM files;""")
            
        # create a list of all hashes
        hashlist = [i[0] for i in cursor.fetchall()]

        if hash in hashlist:
            return True
        else:
            return False

    def check_names(self, name):
        pass

    def save_uploadedfile(self, uploadedfile, data_management, level):
        """
        Provides functionality to save documents per the medallion data management
        system.

        Parameters:
            file:
            data_management:
            level:

        Returns:
            true or error
        """

        # check the management system for the file
        hash = self.hash_file(uploadedfile)
        file_managed = self.check_hashes(hash)
        if file_managed:
            return f"{uploadedfile.name} already managed."

        # check if a file with this name already exists, if the hash is different
        file_name = self.check_names(uploadedfile.name)

        try:
            path = data_management['base_filepath'] + "/" + medallion

        except:
            return {"data_management": data_management, 
                    "message": "Failed to parse management json"}


        try:
            with open(os.path.join(path, file_name),"wb") as f:
                f.write(uploadedfile.getbuffer())

            return True
        except Exception as err:
            logging.error(err)
            return err


if __name__ == '__main__':
    pass