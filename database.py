#!/usr/bin/python
# -*- coding: UTF-8 -*-
import MySQLdb, random, string
# uid = "evelynwang"
# uname = "evelyn"
# timezone = 8
page = "test"
invpage = "invitations"
IIDL = 20
def addUser(page, uid, name, timezone = 8):
    sql = "insert into %s (uid, uname, timezone) values ('%s','%s',%d)"% (page, uid, uname, timezone)
    print sql
    exe(sql)
    return

def deleteInv(iid):
    sql = "delete from %s where iid='%s'"% (invpage, iid)
    print sql
    exe(sql)
    return

def ranchar(i):
    return ''.join(random.sample(string.ascii_letters + string.digits, i))

def addInv(goal, data):
    iid = ranchar(IIDL)
    sql = "select iid from %s while iid=%s" % (invpage,iid)
    print(sql)
    while(len(exe(sql))!=0):
        iid = ranchar(IIDL)
    sql = "insert into %s (%s) values ('%s',%s)"% (invpage, goal, iid, data)
    print sql
    exe(sql)
    return

def findUser(goal,uid):
    sql = "select %s from %s where uid=\'%s\'" % (goal,page,uid)
    print sql
    return exe(sql)

def findInv(goal,uid):
    sql = "select %s from %s where icreator='%s'" % (goal,invpage,uid)
    print sql
    return exe(sql)

def createPage():
    sql = """
    CREATE TABLE invitations(
    iid VARCHAR(10) NOT NULL,
    ititle VARCHAR(40) NOT NULL,
    istate VARCHAR(1) NOT NULL,
    icount INT NOT NULL,
    icreator varchar(40) not null
    PRIMARY KEY ( iid )
    )ENGINE=InnoDB DEFAULT CHARSET=utf8;
    """
    sql = """
    CREATE TABLE invitations(
    uid VARCHAR(40) NOT NULL,
    uname VARCHAR(40) NOT NULL
    PRIMARY KEY ( iid )
    )ENGINE=InnoDB DEFAULT CHARSET=utf8;
    """

def changePage():
    sql = """
    alter table invitations MODIFY iid VARCHAR(20);
    alter table invitations add column creator varchar(40) not null;
    alter table invitations CHANGE creator icreator VARCHAR(40);
    """
# update page set a=1,b=2,c=3 where d=4
# delete from page where d=4

def exe(sql):
    db = MySQLdb.connect(host='127.0.0.1',port = 3306,user='root', passwd='',db ='gooseberry')
    cursor = db.cursor()
    results = []
    try:
       cursor.execute(sql)
       results = cursor.fetchall()
       db.commit()
    except:
       db.rollback()
    db.close()
    print results
    return results
#findInv("iid,ititle,istate,icount","evelynwang")
#addInv("iid,ititle,istate,icount,icreator","'soa meeting','v',0,'evelynwang'")
#deleteInv("py2wSVrsMI")
