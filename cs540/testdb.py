#!/usr/bin/python
import MySQLdb


def list_files_in_dir(mypath):
    from os import listdir
    from os.path import isfile, join
    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
    return onlyfiles

def queries_on_db(query_list, filename, paths):
    db = MySQLdb.connect(host="mysql.cs.orst.edu",    # your host, usually localhost
                         user="cs340_khodadaa",         # your username
                         passwd="****",  # your password
                         db="cs340_khodadaa")        # name of the data base

    
    for i, query in enumerate(query_list):

        # you must create a Cursor object. It will let
        #  you execute all the queries you need
        cur = db.cursor()
        fw = open('{0}/{1}/{2}.txt'.format(paths[2], filename, i+1), 'w')
        try:
            # Use all the SQL you like        
            cur.execute(query)                        
        except Exception as e:            
            fw.write(str(e))
        else:
            result = cur.fetchall()
            final_result = [str(i) for i in result]
            final_result = '\n'.join(final_result)
            fw.write('{0}\n\n{1}'.format(len(result),final_result))
        finally:
            fw.close()
    db.close()    

def parse_sql_file(filename, path):
    import re    
    script = open(path[0]+'/'+filename, 'r').read()        
    script = re.sub('\/\*(\*(?!\/)|[^*])*\*\/|--.*|#.*', ';', script)
    script.strip()
    script += ';'
    
    query_list = []
    query = ''
    for ql in script.splitlines():                
        for qw in ql.split():                
            if query == '' and qw == ';':
                continue
            query += ' ' + qw
            if qw[-1] == ';':
                query_list += [query.strip()]
                query = ''
    
    fw = open(path[1] + '/sql_'+filename, 'w')    
    for i, query in enumerate(query_list):        
        fw.write('{}\n'.format(query))                
    fw.close()
    return query_list 
                
import sys
import os
if __name__ == '__main__':
    paths = ['.', './sql_queries', './outputs']
    for i,p in enumerate(sys.argv[1:]):
        paths[i] = p
    for p in paths[1:]:
        if not os.path.exists(p):
            os.makedirs(p)

    filename_list = list_files_in_dir(paths[0])     
    for i,filename in enumerate(filename_list): 
        print i+1,filename
        print '--------------------------------'
        query_list = parse_sql_file(filename, paths)
        if not os.path.exists(paths[2]+'/'+filename):
            os.makedirs(paths[2]+'/'+filename)
        queries_on_db(query_list, filename, paths)
