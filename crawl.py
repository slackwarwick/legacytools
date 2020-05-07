from pathlib import Path

from dbcrawler import FDBCrawler
from fscrawler import FSCrawler
from hgcrawler import HGCrawler


if __name__ == '__main__':
    fs = FSCrawler()
    hg = HGCrawler()
    
    myroot = Path('D:/Work/')
    processeddir = myroot / '_processed'
    fs.annotateFilesWithSql(myroot, processeddir)

    for f in processeddir.iterdir():
        f.replace(myroot / f.name)

    hg.revertFilesInList('D:/Work/modules_not.txt', myroot)    
