import cjson, csv, urllib, os, time
from StringIO import StringIO
from collections import defaultdict
from difflib import get_close_matches

thisdirectory = "/".join(__file__.split("/")[:-1])
# name of tictoc database file
tictocfile = thisdirectory + "/jrss.txt"

# time tictoc database was last modifed
tictoclastmodtime = 0

# maps issn to list of records
recordsbyissn = None

def loadtictocfile(tictocfilename):
    """
        Load file with given name into issn->list(records) 
        dictionary, return dictionary
    """
    recordsbyissn = defaultdict(list)
    tictocfile = open(tictocfilename)
    for line in csv.reader(tictocfile, delimiter = '\t'):
        record = { 'title' : line[1], 'rssfeed' : line[2] }
        for issn in line[3:]:
            if issn.strip() != "":
                issn = issn.replace("-", "")
                recordsbyissn[issn].append(record)

    tictocfile.close()
    return recordsbyissn

def application(env, start_response):
    """
        Return JSON info about a ISSN + Title (Optional)
    """
    response = dict()

    global recordsbyissn, tictoclastmodtime
    lastmodtime = os.path.getmtime(tictocfile)
    if lastmodtime > tictoclastmodtime:
        tictoclastmodtime = lastmodtime
        recordsbyissn = loadtictocfile(tictocfile)

    # extract the 1234-5678 part after /tictoc/1234-5678
    issn = env['PATH_INFO'].split("/")[-1]
    response['issn'] = issn
    issn = issn.replace("-", "")
    records = recordsbyissn[issn]
    jsoncallback = None

    # if title is given, try to find the best matching title
    try:
        query = dict([map(urllib.unquote, kv.split("=")) \
                      for kv in env['QUERY_STRING'].split("&")]);

        if query.has_key('jsoncallback'):
            jsoncallback = query['jsoncallback']

        title = query['title']
        if title:
            response['title'] = title
            recordbytitle = dict([(r['title'], r) for r in records])
            match = get_close_matches(title, recordbytitle.keys())
            if len(match) != 0:
                records = [recordbytitle[match[0]]]
            
    except KeyError:
        pass
    except ValueError:
        pass

    response['records'] = records
    response['lastmod'] = time.asctime(time.localtime(tictoclastmodtime))

    encodedresponse = cjson.encode(response)
    if jsoncallback:
        encodedresponse = jsoncallback + "(" + encodedresponse + ")"

    headers = [('Content-Type', 'application/javascript;charset=utf-8'), \
               ('Cache-Control', 'max-age=1,must-revalidate')]

    start_response("200 OK", headers)
    return [encodedresponse]

