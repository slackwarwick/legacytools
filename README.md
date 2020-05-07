Set of Python scripts serving as helpers at enterprise refactoring

These scripts in Python 3 are my helpers at refactoring of legacy enterprise sourcecode and DB.
They can get stringlists (in form of text files) as input and produce stringlists as output.
Their goal is to answer questions like "What are the dependendencies of that specific set of tables?" or "What subset of DB stored procedures are called from that source code tree?" and others like that.
Typical usage is:

1) Edit <some>crawler.py to create specific Crawler methods (if necessary).
2) Edit crawl.py to create one or more Crawler objects and call their methods.
3) Run crawl.py and get the output.

You can easily redirect script output to the text file:
D:\Work\>py textcrawler.py > myresults.txt

Currently available Crawlers are:

- FSCrawler to search the source or text file tree.
- FDBCrawler to search Firebird Database.
- HGCrawler to search and operate HG repository

Crawlers can be tuned by Formatter objects to get more useful strings as output. Currently available formatters are:

- SimpleFormatter to get just the string list ("as is" or uppercase).
...
DBOBJECTS
DBUSERS
...

- TemplateFormatter to add prefix and/or postfix text to each string in list
...
CREATE SEQUENCE GEN_DBOBJECTS_ID;
CREATE SEQUENCE GEN_DBUSERS_ID;
...

- MECFormatter is for the Extract Metadata tool config file of IBExpert.
...
Table_0=DBOBJECTS
Table_1=DBUSERS
...



