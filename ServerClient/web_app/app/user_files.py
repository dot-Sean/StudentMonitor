import os
import xml.etree.cElementTree as et
from config import DOCS_DIR


class UserFiles(object):
    def __init__(self, username):
        self.username = username

        self.ss_names = self.list_files('.jpg')
        self.xml_names = self.list_files('.xml')

        self.processes = []
        self.sites = []
        self.get_data()

    def list_files(self, file_type):
        files_list = []
        try:
            for file in os.listdir(os.path.join(DOCS_DIR, self.username)):
                if file.endswith(file_type):
                    files_list.append(file)
            return files_list
        except FileNotFoundError:
            return []

    def get_processes(self):
        processes_name = []

        for name in self.xml_names:
            tree = et.parse(os.path.join(DOCS_DIR, self.username, name))
            root = tree.getroot()
            for process in root.iter('process'):
                processes_name.append(process.text)

        return self.delete_duplicates(processes_name)

    def get_data(self):
        sites_name = []
        processes_name = []

        for name in self.xml_names:
            tree = et.parse(os.path.join(DOCS_DIR, self.username, name))
            root = tree.getroot()
            for process in root.iter('process'):
                processes_name.append(process.text)
            for site in root.iter('site'):
                sites_name.append(site.get('url'))  # TODO: poprawić urle

        self.processes = self.delete_duplicates(processes_name)
        self.sites = self.delete_duplicates(sites_name)

    def delete_duplicates(self, l):
        seen = set()
        processes_uniq = []
        for x in l:
            if x not in seen:
                processes_uniq.append(x)
                seen.add(x)
        return processes_uniq

if __name__ == '__main__':
    u = UserFiles("BURCHARDTIST-PC")
