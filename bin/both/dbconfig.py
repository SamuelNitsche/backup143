from bin.both.dbcon import dbmanager

def dbconf(value):
    db = dbmanager()
    qry = db.query("SELECT value FROM '143_options' WHERE option = '"+ value +"' LIMIT 1;")
    result = qry.fetchone()
    return result[0]
    