import os


class StalkWindows(object):
    def __init__(self):
        self.my_path = os.path.join(os.path.dirname(__file__))

    def get_processes(self):
        results = str(os.system("tasklist /FI \"STATUS eq RUNNING\" /FI \"USERNAME eq %USERNAME%\""))[:-1]
        print(results)

    def get_links(self):
        results = str(os.system("netstat -nao | findstr /i \":80 :44\""))[:-1]
        print(results)

if __name__ == '__main__':
    w = StalkWindows
    w.get_processes()