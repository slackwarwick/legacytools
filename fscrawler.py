#! python3

import re
from pathlib import Path
import os
from crawlerscommon import Crawler, SimpleFormatter, TemplateFormatter, MECFormatter
import annotate

class FSCrawler(Crawler):

    def __init__(self, outputformatter=SimpleFormatter(uppercase=True)):
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

    def mergeLists(self, *srcfiles):
        for filename in srcfiles:
            with open(filename, 'r') as f:
                for line in f:
                    self.resultset.add(line.strip().upper())
                f.close()

    def findFilesNotInList(self, listfile, sourcedir, *filemasks):
        path = Path(sourcedir)
        print(path)
        with open(listfile, 'r') as f:
            lines = [l.lower().strip() for l in f.readlines()]
            files = []
            for mask in filemasks:
                files.extend(path.glob(mask))
            for fullpath in files:
                basename = os.path.basename(fullpath)
                if basename.lower().strip() not in lines:
                    self.resultset.add(basename)

    def inspectDfmFiles(self, sourcedir):
        srcdir = Path(sourcedir)
        for srcfile in srcdir.glob('*.dfm'):
            with srcfile.open() as srcf:
                srclines = srcf.readlines()
                for idx in range(len(srclines)):
                    srcline = srclines[idx]
                    if annotate.DFM_SQL_MARK in srcline:
                        self.resultset.add(srcfile.stem)

    def inspectPasFiles(self, sourcedir):
        srcdir = Path(sourcedir)
        for srcfile in srcdir.glob('*.pas'):
            with srcfile.open() as srcf:
                srclines = srcf.readlines()
                for idx in range(len(srclines)):
                    srcline = srclines[idx]
                    for mark in ('GetID(',):
                        if mark.lower() in srcline.lower():
                            self.resultset.add(srcfile.stem)

    def annotateFilesWithSql(self, sourcedir, destdir):
        self._annotateFiles(sourcedir, destdir, '*.dfm')
        self._annotateFiles(sourcedir, destdir, '*.pas')

    def _annotateFiles(self, sourcedir, destdir, filemask):
        if not os.path.exists(destdir):
            os.mkdir(destdir)
        srcdir = Path(sourcedir)
        dstdir = Path(destdir)
        for srcfile in srcdir.glob(filemask):
            destfile = dstdir / srcfile.name
            annotatefunc = annotate.annotateFunc(filemask)
            if annotatefunc:
                annotations = annotatefunc(srcfile, destfile)
                if annotations > 0:
                    self.resultset.add('{};{}'.format(srcfile.name, annotations))
            else:
                print('Annotation is not supported for filetype {}'.format(filemask))


if __name__ == '__main__':
    crawler = FSCrawler()
    #crawler.setOutputFormatter(TemplateFormatter('grant select on ', ' to myclient;'))
    crawler.setOutputFormatter(SimpleFormatter(sort=True))
    #crawler.findGenerators("../testdb/triggers/_ibe$finish_.sql")                
    #crawler.findAllKeywordsInSourceTree("allprocedures.txt", "D:/Work/src", "*.cpp", "codeprocedures.txt")
    #crawler.mergeLists("finalprocedures.txt", "finalprocedures2.txt", "finalprocedures3.txt", "finalprocedures4.txt", "finalprocedures5.txt")
    #crawler.findRegexpInSourceTree(r"ALTER TRIGGER (\w+)", "D:/Work/refactor_tools/testdb/triggers", "*.sql")
    #crawler.findFilesNotInList('D:/Work/modules.txt', 'D:/Work/Test', '*.pas')
    crawler.printResult()



