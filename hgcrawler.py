import subprocess
from pathlib import Path
import os

from crawlerscommon import Crawler, SimpleFormatter, TemplateFormatter, MECFormatter

class HGCrawler(Crawler):

    def __init__(self, outputformatter=SimpleFormatter()):
        super().__init__(outputformatter)

    def revertFilesInList(self, listfile, sourcedir):
        path = Path(sourcedir)
        with open(listfile, 'r') as f:
            lines = [l.lower().strip().split('.')[0] for l in f.readlines()]
            to_revert = [p for p in path.glob('*.*') if os.path.basename(p).lower().strip().split('.')[0] in lines]
            print(to_revert)
            os.chdir(sourcedir)
            for p in to_revert:
                pipe = subprocess.Popen(["hg", "revert", p.name])
                pipe.wait()

if __name__ == '__main__':
    crawler = HGCrawler()
    crawler.revertFilesInList('D:/Work/modules_not.txt', 'D:/Work/Test')

