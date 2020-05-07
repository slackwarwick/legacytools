#! python3

import fdb
import logging
from crawlerscommon import SimpleFormatter, MECFormatter
from crawlerscommon import Crawler

DEP_TABLE = 0
DEP_VIEW = 1
DEP_TRIGGER = 2
DEP_PROCEDURE = 5
DEP_EXCEPTION = 7
DEP_GENERATOR = 14

class FDBCrawler(Crawler):
    ibdsn = ''
    ibusername = ''
    ibpassword = ''
    ibconnection = None
    do_savesource = False

    def __init__(self, ibdsn, ibusername, ibpassword, outputformatter=SimpleFormatter(uppercase=True)):
        super().__init__(outputformatter)
        self.ibdsn = ibdsn
        self.ibusername = ibusername
        self.ibpassword = ibpassword
        self.connectDB()

    def __del__(self):
        self.disconnectDB()

    def setSaveSource(self, value):
        self.do_savesource = value

    def connectDB(self):
        try:
            self.ibconnection = fdb.connect(dsn=self.ibdsn, user=self.ibusername, password=self.ibpassword, charset='WIN1251')
            return True
        except Exception as e:
            logging.error('CONNECT ERROR: ' + str(e))
            return False

    def addValue(self, value, sourcevalue):
        saved_value = value.strip()
        if (self.do_savesource):
            saved_value = saved_value + " - " + sourcevalue
        self.resultset.add(saved_value)

    def findDependencies(self, keyword, deptype):
        ibcursor = self.ibconnection.cursor()
        ibcursor.execute("select RDB$DEPENDED_ON_NAME from RDB$DEPENDENCIES where upper(RDB$DEPENDENT_NAME) = upper(?) "
            "and RDB$DEPENDED_ON_TYPE = ?", [keyword,deptype])
        for dep in ibcursor.fetchall():
            if not dep[0].startswith('CHECK_'):
                self.addValue(dep[0], keyword)

    def findDependents(self, keyword, deptype):
        ibcursor = self.ibconnection.cursor()
        ibcursor.execute("select RDB$DEPENDENT_NAME from RDB$DEPENDENCIES where upper(RDB$DEPENDED_ON_NAME) = upper(?) "
            "and RDB$DEPENDENT_TYPE = ?", [keyword,deptype])
        for dep in ibcursor.fetchall():
            if not dep[0].startswith('CHECK_'):
                self.addValue(dep[0], keyword)

    def findTriggers(self, tablename):
        ibcursor = self.ibconnection.cursor()
        ibcursor.execute("select RDB$TRIGGER_NAME from RDB$TRIGGERS where upper(RDB$RELATION_NAME) = upper(?) "
            "and RDB$TRIGGER_SOURCE is not null", [tablename])
        for dep in ibcursor.fetchall():
            self.addValue(dep[0], tablename)

    def disconnectDB(self):
        try:
            self.ibconnection.close
            return True
        except Exception as e:
            logging.error('DISCONNECT ERROR: ' + str(e))
            return False

    def findAllDependents(self, sourcefile, deptype):
        self.resultset.clear()
        with open(sourcefile, "r") as src:
            for line in src:
                if len(line):
                    self.findDependents(line, deptype)
        self.printResult() 

    def findAllDependencies(self, sourcefile, deptype):
        self.resultset.clear()
        with open(sourcefile, "r") as src:
            for line in src:
                line = line.strip()
                if len(line):
                    self.findDependencies(line, deptype)
        self.printResult() 

    def findTriggersForTables(self, sourcefile):
        self.resultset.clear()
        with open(sourcefile, "r") as src:
            for line in src:
                line = line.strip()
                if len(line):
                    self.findTriggers(line)
        self.printResult() 

    def findAllProcedures(self):
        self.resultset.clear()
        ibcursor = self.ibconnection.cursor()
        ibcursor.execute("select RDB$PROCEDURE_NAME from RDB$PROCEDURES")
        for dep in ibcursor.fetchall():
            self.addValue(dep[0], '')
        self.printResult() 

if __name__ == '__main__':
    crawler = FDBCrawler('192.92.92.88:/mnt/backup/16042018.fdb', 'SYSDBA', 'testdb')
    crawler.setOutputFormatter(MECFormatter("View_"))
    #crawler.setSaveSource(True)
    #crawler.findTriggersForTables("tableswithtriggers.txt")
    crawler.findAllDependencies("finalfinalprocedures.txt", DEP_VIEW)
    #crawler.findAllProcedures("allprocedures.txt")
