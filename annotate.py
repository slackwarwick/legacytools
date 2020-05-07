DFM_SQL_MARK = 'SQL.Strings'

def _whitespaceSize(srcline):
    for kw in ('UpdateSQL', 'RefreshSQL', 'InsertSQL', 'DeleteSQL', 'ModifySQL', 'SelectSQL'):
        if kw in srcline:
            return srcline.index(kw) + 2
    return srcline.index(DFM_SQL_MARK) + 2

def _annotateDfmFile(sourcefile, destfile):
    annotations = 0
    srclines = None
    dstlines = list()
    with sourcefile.open() as srcf:
        srclines = srcf.readlines()
    for idx in range(len(srclines)):
        srcline = srclines[idx]
        dstlines.append(srcline)
        if DFM_SQL_MARK in srcline:
            annotation = '\'/*__SUPSQL__/{}/{}*/\''.format(sourcefile.name, idx + 2)
            whitespace = str(' '*_whitespaceSize(srcline))
            dstlines.append('{}{}\n'.format(whitespace, annotation))
            annotations += 1
    with destfile.open(mode='w') as dstf:
        dstf.writelines(dstlines)
    return annotations    

def _annotatePasFile(sourcefile, destfile):
    annotations = 0
    srclines = None
    dstlines = list()
    with sourcefile.open() as srcf:
        srclines = srcf.readlines()
    firstStatementInserted = False
    for idx in range(len(srclines)):
        srcline = srclines[idx]
        for mark in ('SQL.Add(', 'SQL.Text :=', 'GetSqlValues(', 'GetSQLValues(', 'getSQLValues(', 'ExecSQL(', 'SQLValuesToList(', 'GetID(', 'getId(', 'GetId('):
            if mark in srcline:
                annotation = '\'/*__SUPSQL__/{}/{}*/ \''.format(sourcefile.name, idx + 1)
                dstline = ''
                if mark == 'SQL.Add(' and firstStatementInserted:
                    dstline = srcline
                elif mark == 'ExecSQL(' and 'ExecSQL()' in srcline:
                    dstline = srcline
                elif mark.endswith('='):
                    dstline = srcline.replace(mark, '{} {} + '.format(mark, annotation))
                else:    
                    dstline = srcline.replace(mark, '{}{} + '.format(mark, annotation))
                dstlines.append(dstline)
                if mark == 'SQL.Add(':
                    firstStatementInserted = True
                if dstline != srcline:
                    annotations += 1
                break
        else:
            dstlines.append(srcline)
            firstStatementInserted = False
    with destfile.open(mode='w') as dstf:
        dstf.writelines(dstlines)
    return annotations    

_annotatedict = {
    '*.pas' : _annotatePasFile,
    '*.dfm' : _annotateDfmFile,
}

def annotateFunc(filemask):
    try:
        result = _annotatedict[filemask]
        return result
    except KeyError:
        return None
