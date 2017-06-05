#!/usr/bin/python
# -*- coding: UTF-8 -*-
import MySQLdb
userPage = "users"
invitationPage = "invitations"
contactPage = "contacts"
timePage = "times"
def cleanDb():
    pages=[userPage,invitationPage,contactPage,timePage]
    for page in pages:
        sql = "DROP TABLE IF EXISTS "+page
        exe(sql)

def createPages():
    sql ="CREATE TABLE IF NOT EXISTS "+userPage+"( \
        %s VARCHAR(40) NOT NULL, \
        %s VARCHAR(15) NOT NULL, \
        %s VARCHAR(20) NOT NULL, \
        %s INT DEFAULT 0, \
        PRIMARY KEY ( %s ) \
    )ENGINE=InnoDB DEFAULT CHARSET=utf8;" % ("id","psw","name","timezone","id")
    exe(sql)
    sql ="CREATE TABLE IF NOT EXISTS "+invitationPage+"""(
    id VARCHAR(10) NOT NULL,
    title VARCHAR(40) NOT NULL,
    state VARCHAR(1) NOT NULL,
    count INT DEFAULT 0,
    creator VARCHAR(40) NOT NULL,
    PRIMARY KEY ( id )
    )ENGINE=InnoDB DEFAULT CHARSET=utf8;
    """
    exe(sql)
    sql ="CREATE TABLE IF NOT EXISTS "+contactPage+"""(
        uid VARCHAR(40) NOT NULL,
        id VARCHAR(40) NOT NULL,
        name VARCHAR(40) NOT NULL,
        nickname VARCHAR(40),
        INDEX (uid,id)
    )ENGINE=InnoDB DEFAULT CHARSET=utf8;
    """
    exe(sql)
    sql ="CREATE TABLE IF NOT EXISTS "+timePage+"( \
        %s VARCHAR(40) NOT NULL, \
        %s VARCHAR(40) NOT NULL, \
        %s TIMESTAMP NOT NULL, \
        %s TIMESTAMP NOT NULL, \
        %s VARCHAR(10), \
        INDEX (%s) \
    )ENGINE=InnoDB DEFAULT CHARSET=utf8;" % ("id","title","start","end","iid","id,start,end")
    exe(sql)

def exe(sql):
    db = MySQLdb.connect(host='localhost',port = 3306,user='root', passwd='',db ='gooseberry')
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

createPages()
