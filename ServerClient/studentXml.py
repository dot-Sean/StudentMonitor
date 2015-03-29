from collections import OrderedDict
import os
import ssl
from urllib.request import urlopen
import xml.etree.cElementTree as et
import time
import re
import urllib

class StudentXML(object):
    def __init__(self, client_ip=None, username=None):
        self.my_path = os.path.join(os.path.dirname(__file__))
        self.root = et.Element('student')
        if client_ip:
            self.root.attrib['client_ip'] = client_ip
        if username:
            self.root.attrib['username'] = username

        datetime_attrib = str(time.strftime("%d-%m-%Y %H:%M:%S"))
        self.data_element = et.SubElement(self.root, 'data', attrib={'datetime': datetime_attrib})

        self.processes_element = et.SubElement(self.data_element, 'processes')
        self.processes_to_tree()

        self.sites_element = et.SubElement(self.data_element, 'sites')
        self.sites_to_tree()

        self.tree = et.ElementTree(self.root)
        self.tree.write('filename.xml')

    def processes_to_tree(self):
        processes = self.get_processes()
        for process in processes:
            attribs = {'memusage': process[4], 'pid': process[1]}
            et.SubElement(self.processes_element, 'process', attrib=attribs).text = process[0]

    def sites_to_tree(self):
        sites = self.get_sites()
        #for site in sites:
        #    attribs = {'site_ip': site[1], 'web_browser': site[3]}  # TODO: wyszukaj po pid nazwę procesu
        #    site_name = str(os.popen("nslookup " + site[1] + " | findstr Name:").read())
        #    site_name = re.findall(r'Name:\s*(.+)', site_name)
#
        #    if site_name:
#
        #        et.SubElement(self.sites_element, 'site', attrib=attribs).text = site_name[0]

        sites = self.get_sites()
        for site in sites:
            try:
                page = urlopen(r'http://' + site[1])
                html = str(page.read())
                title = re.findall(r'<title>(\w+)', html, re.I)
                print(title)
            except urllib.error.HTTPError:
                print('HTTPError')
            except urllib.error.URLError:
                print('URLError')


    def get_processes(self):
        results = str(os.popen("tasklist /FI \"STATUS eq RUNNING\" /FI \"USERNAME eq %USERNAME%\"").read())
        results = re.findall(r'(\w+\.exe)\s*(\d+)\s*(\w+)\s*(\d+)\s*(\d+.\d+ K)', results, re.I)

        return results

    def get_sites(self):
        results = str(os.popen("netstat -nao | findstr /i \":80 :443\"").read())  # TODO: beznadziejnie działa - nie wszystko znajduje
        results = re.findall(r'\s*TCP\s*'
                             r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d+)\s*'
                             r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):\d+\s*'
                             r'(\w+)\s*'
                             r'(\d+)', results, re.I)

        return results


if __name__ == '__main__':
    s = StudentXML('127.0.0.1:123', 'tadek')
    s.get_sites()





    """                google_ips = re.findall(r'\s*(\d+\.\d+\.\d+)', str(os.popen('nslookup google.com').read()))
                google_ips += re.findall(r'\s*(\d+\.\d+\.\d+)', str(os.popen('nslookup google.pl').read()))

                gmail_ips = re.findall(r'\s*(\d+\.\d+\.\d+)', str(os.popen('nslookup mail.google.com').read()))

                youtube_ips = re.findall(r'\s*(\d+\.\d+\.\d+)', str(os.popen('nslookup youtube.com').read()))"""