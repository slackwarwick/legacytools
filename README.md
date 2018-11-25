Set of Python scripts serving as helpers at enterprise refactoring

These scripts in Python 3 are my helpers at refactoring of legacy enterprise sourcecode and DB.
They get stringlists (in form of text files) as input and produce stringlists as output.
Their goal is to answer questions like "What are the dependendencies of that specific set of tables?" or "What subset of DB stored procedures are called from that source code tree?" and others like that.
Typical usage is:

1) Edit textcrawler.py or dbcrawler.py to create specific Crawler object and call its necessary method/methods (write one if it isn't present).
2) Run the script and get the output.

Currently available Crawlers are:

- TextCrawler to search the source or text file tree.
- FDBCrawler to search Firebird Database.

Crawlers can be tuned by OutputFormatter objects to get more useful strings as output. Currently available formatters are:

- UppercaseFormatter to get the strings in upper case.
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

You can easily redirect script output to the text file:
D:\Work\>py textcrawler.py > myresults.txt


