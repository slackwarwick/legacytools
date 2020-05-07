#! python3

import re
from pathlib import Path
from crawlerscommon import UppercaseFormatter
from crawlerscommon import TemplateFormatter
from crawlerscommon import MECFormatter
from crawlerscommon import Crawler

class TextCrawler(Crawler):

    def __init__(self, outputformatter=UppercaseFormatter()):
        super().__init__(outputformatter)

    def findRegexpInSourceTree(self, regexp, sourcedir, filemask):
        r = re.compile(regexp)
        path = Path(sourcedir)
        for filepath in list(path.glob(filemask)):
            with open(filepath, 'r') as f:
                for line in f:
                    r_result = r.search(line)
                    if r_result is not None:
                        self.resultset.add(r_result.group(1))
            f.close()    
        self.printResult() 

    def findAllKeywordsInSourceTree(self, keywordsfile, sourcedir, filemask):
        keylist = list()
        with open(keywordsfile, 'r') as f:
            keylist = f.readlines()
            f.close()
        path = Path(sourcedir)
        for filepath in list(path.glob(filemask)):
            with open(filepath, 'r') as f:
                for line in f:
                    for key in keylist:
                        key = key.strip().upper()
                        if line.upper().find(key) != -1:
                            self.resultset.add(key)
                f.close()
        self.printResult()  

    def mergeLists(self, *srcfiles):
        self.resultset.clear()
        for filename in srcfiles:
            with open(filename, 'r') as f:
                for line in f:
                    self.resultset.add(line.strip().upper())
                f.close()
        self.printResult() 

crawler = TextCrawler()
crawler.setOutputFormatter(TemplateFormatter('grant select on ', ' to ptclient;'))
#crawler.findAllKeywordsInSourceTree("allprocedures.txt", "D:/Work/src", "*.cpp")
crawler.mergeLists("finalprocedures.txt", "finalprocedures2.txt", "finalprocedures3.txt", "finalprocedures4.txt", "finalprocedures5.txt")
#crawler.findRegexpInSourceTree(r"ALTER TRIGGER (\w+)", "D:/Work/Yolka/refactor_tools/testdb/triggers", "*.sql")



