import os
from threading import Thread
import xml.etree.cElementTree as et
import time
import re

from config import DOCUMENTS_PATH, XML_NAME
from packetSniffer import TCPSniffer


class StudentXML(object):
    def __init__(self, client_ip=None, username=None):
        self.url_list = []

        self.my_path = os.path.join(os.path.dirname(__file__))
        self.root = et.Element('student')
        if client_ip:
            self.root.attrib['client_ip'] = client_ip
        if username:
            self.root.attrib['username'] = username

        datetime_attrib = str(time.strftime("%d-%m-%Y %H:%M:%S"))
        self.data_element = et.SubElement(self.root, 'data', attrib={'datetime': datetime_attrib})

        self.processes_element = et.SubElement(self.data_element, 'processes')

        self.sites_element = et.SubElement(self.data_element, 'sites')

        self.tree = et.ElementTree(self.root)

    def generate_document(self, file_path=os.path.join(DOCUMENTS_PATH, XML_NAME)):
        datetime_attrib = str(time.strftime("%d-%m-%Y %H:%M:%S"))
        self.data_element.set('datetime', datetime_attrib)

        self.processes_to_tree()
        self.sites_to_tree()
        self.tree.write(file_path)

        self.data_element.remove(self.processes_element)
        self.processes_element = et.SubElement(self.data_element, 'processes')

        self.data_element.remove(self.sites_element)
        self.sites_element = et.SubElement(self.data_element, 'sites')

    def processes_to_tree(self):
        processes = self.get_processes()
        for process in processes:
            attribs = {'memusage': process[4], 'pid': process[1]}
            et.SubElement(self.processes_element, 'process', attrib=attribs).text = process[0]

    def sites_to_tree(self):
        temp_urls_list = self.url_list.copy()

        urls = []
        for i in temp_urls_list:
            if i not in urls:
                urls.append(i)
        for url in urls:
            attribs = {'url': url}
            et.SubElement(self.sites_element, 'site', attrib=attribs)

    def get_processes(self):
        results = str(os.popen("tasklist /FI \"STATUS eq RUNNING\" /FI \"USERNAME eq %USERNAME%\"").read())
        results = re.findall(r'(\w+\.exe)\s*(\d+)\s*(\w+)\s*(\d+)\s*(\d+.\d+ K)', results, re.I)

        return results

    def get_sites(self):
        """
        to nie działa jakby się chciało. Może do :443 się przyda
        """
        results = str(os.popen("netstat -nao | findstr /i \":80 :443\"").read())
        results = re.findall(r'\s*TCP\s*'
                             r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+)\s*'
                             r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):\d+\s*'
                             r'(\w+)\s*'
                             r'(\d+)', results, re.I)
        return results

    def get_urls(self):
        with TCPSniffer() as tcp_sniffer:
            site_url = tcp_sniffer.get_http_referer()
            if site_url:
                self.url_list.append(site_url[0])


if __name__ == '__main__':

    def infite_url_capturing(s):
        while True:
            s.get_urls()

    s = StudentXML('127.0.0.1:123', 'tadek')
    capturing_thread = Thread(target=infite_url_capturing, args=(s,))
    capturing_thread.start()

    while time.process_time() < 5:
        pass

    s.generate_document()