'''A local data management module'''

import os
import re
import sqlite3
import hashlib
import logging
import pandas as pd
from io import BytesIO
from sqlite3 import Error

from typing import Union, Literal


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
    insert_file_into_files:
    :hash_file:
    :get_hashes:
    :check_hash:
    :get_names:
    :check_names:
    :get_managed_files_df:
    :save_file:
    :save_dataframe:

    """

    def __init__(self, base_path: os.PathLike = None, db_file:str = 'filemanager.db', data_arch:Union[Literal['medallion'], Literal['levels']] = 'medallion'):
        """
        Constructs all the necessary attributes for the file manager object.

        Parameters
        ----------
        :base_path: the path to the data management system
        :db_file: the name of the sqlite database used to manage the files
        :data_arch: [medallion, levels] data scheme for which to create directories
        """
        if base_path == None:
            self.base_path = os.path.join('data','managed_data')
        else:
            self.base_path = base_path

        # An arbitrary (but fixed) buffer size
        # 65536 = 65536 bytes = 64 kilobytes
        self.BUF_SIZE = 65536

        self.data_arch = data_arch
        if self.data_arch == 'medallion':
            self.data_levels = ['bronze', 'silver', 'gold']
        elif self.data_arch =='levels':
            self.data_levels = ['level_1', 'level_2', 'level_3']

        try:
            self.create_management_folders()
            connection = sqlite3.connect(os.path.join(self.base_path, db_file))
            self.connection = connection
            self.create_management_table()
        except Error as e:
            logging.info(e)
 
    def close_connection(self):
        self.connection.close()

    def create_management_table(self, SQL:str=None):
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

    def create_management_folders(self):
        """ create the folders required to manage the files
        :param path: string filepath in which to create the management structure
        :param data_arch: [medallion, levels] data scheme for which to create

        :return: Boolean
        """

        if os.path.exists(self.base_path):
            logging.info(f'{self.base_path} exists')
        
        for level in self.data_levels:
            if os.path.exists(os.path.join(self.base_path,level)):
                logging.info(f'{os.path.join(self.base_path,level)} exists')
            else:
                try:
                    os.makedirs(os.path.join(self.base_path,level))
                except:
                    logging.error(f'Failed to create {os.path.join(self.base_path,level)}')
                    return False
        return True

    def insert_file_into_files(self, name: str, hash: str, location: os.PathLike):
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

    def hash_file(self, file: BytesIO):
        """
        Provides hashing functionality.

        Parameters:
            file:

        Returns:
            The sha256 hash in hex format 

        """
        # Initializing the sha256() method
        sha256 = hashlib.sha256()

        # Opening the file provided
        while True:
            data = file.read(self.BUF_SIZE)

            # True if eof = 1
            if not data:
                file.seek(0)
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

    def get_hashes(self):
        """
        Provides functionality to get all previously hashed files.

        Parameters:
            None

        Returns:
            List of all hashes 

        """
        # Creating cursor object using connection object
        cursor = self.connection.cursor()
            
        # executing our sql query
        cursor.execute("""SELECT hash FROM files;""")
            
        # create a list of all hashes
        hashlist = [i[0] for i in cursor.fetchall()]

        return hashlist

    def check_hashes(self, hash: str):
        """
        Provides functionality to check if a file has been hashed previously.

        Parameters:
            hash:

        Returns:
            boolean 

        """
        # create a list of all hashes
        hashlist = self.get_hashes()

        if hash in hashlist:
            return True
        else:
            return False

    def get_names(self):
        """
        Provides functionality to get all filenames.

        Parameters:
            None:

        Returns:
            list of all managed filenames 

        """
        # Creating cursor object using connection object
        cursor = self.connection.cursor()
            
        # executing our sql query
        cursor.execute("""SELECT name FROM files;""")
            
        # create a list of all hashes
        namelist = [i[0] for i in cursor.fetchall()]

        return namelist

    def check_names(self, filename: str):
        """
        Provides functionality to check if a file with the same name exists.

        Parameters:
            filename:

        Returns:
            boolean 

        """
        # create a list of all hashes
        namelist = self.get_names()

        if filename in namelist:
            return True
        else:
            return False

    def get_managed_files_df(self):
        """
        Provides functionality to get data on managed files.

        Parameters:
            None

        Returns:
            dataframe of all managed file information 

        """
        # Creating cursor object using connection object
        cursor = self.connection.cursor()
            
        # executing our sql query
        cursor.execute("""SELECT * FROM files;""")
            
        # create a list of all hashes
        files = cursor.fetchall()
        df = pd.DataFrame(files, columns=['filename', 'hash', 'location'])

        return df

    def save_file(self, file: BytesIO, data_level: str):
        """
        Provides functionality to save documents per the data management
        system.

        Parameters:
            file:
            data_level:

        Returns:
            true or error
        """

        if data_level not in self.data_levels:
            logging.error(f'{data_level} not in {self.data_levels}')
            return False

        filename = file.name.split('/')[-1]
        # check the management system for the file
        hash = self.hash_file(file)
        hash_managed = self.check_hashes(hash)

        # check if a file with this name already exists, if the hash is different
        file_managed = self.check_names(filename)

        if hash_managed:
            logging.info(f"{filename} already managed.")
            return f"{filename} already managed."
        
        elif file_managed and not hash_managed:
            # if the file already exists, check for a version number and increment
            pattern = re.compile(r"V[0-9]+_", re.IGNORECASE)
            
            # if the file is already versioned, increment the version
            if pattern.match(filename):
                version = "{:03d}".format(int(filename[1:4])+1)
                filename = 'V'+ version + filename[4:]
            # otherwise add a version number
            else:
                filename = 'V002_' + filename

        path = os.path.join(self.base_path, data_level)

        try:
            with open(os.path.join(path, filename),"wb") as f:
                while True:
                    data = file.read(self.BUF_SIZE)
                    if not data:
                        break
                    f.write(data)

            # with the file saved, add it to the database
            self.insert_file_into_files(name=filename, hash=hash, location=path)
            return True
        except Exception as err:
            logging.error(err)
            return err

    def save_dataframe(self, dataframe: pd.DataFrame, name: str, data_level: str):
        """
        Provides functionality to convert dataframes to csvs for storage in the data management
        system.

        Parameters:
            dataframe: a dataframe to store
            name: the name of the file
            data_level: data level at which to store the file


        Returns:
            true or error
        """
        in_memory_fp = BytesIO()
        dataframe.to_csv(in_memory_fp)
        if name.split('.')[-1] != 'csv':
            name = name + '.csv'
        in_memory_fp.name = name
        self.save_file(in_memory_fp, data_level)

if __name__ == '__main__':
    pass