import os
from client_server.config import DOCUMENTS_DIRECTORY
import xml.etree.cElementTree as et


class UserFiles(object):
    def __init__(self, username):
        self.username = username
        #tree = et.parse(os.path.join(DOCUMENTS_DIRECTORY, self.username, '.xml'))
        #root = tree.getroot()
        self.ss_names = self.list_files('.jpg')
        xml_names = self.list_files('.xml')

    def list_files(self, file_type):
        files_list = []
        for file in os.listdir(os.path.join(DOCUMENTS_DIRECTORY, self.username)):
            if file.endswith(file_type):
                files_list.append(file)
        return files_list


if __name__ == '__main__':
    u = UserFiles("BURCHARDTIST-PC")

