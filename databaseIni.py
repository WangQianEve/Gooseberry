#!/usr/bin/python
# -*- coding: UTF-8 -*-
# BY EVELYN WANG
import MySQLdb
userPage = "users"
invitationPage = "invitations"
contactPage = "contacts"
timePage = "times"
optionPage = "options"

def cleanDb():
    pages=[userPage,invitationPage,contactPage,timePage]
    for page in pages:
        sql = "DROP TABLE IF EXISTS "+page
        exe(sql)

def createPages():
	sql ="CREATE TABLE IF NOT EXISTS "+userPage+"""(
	id VARCHAR(40) NOT NULL,
	psw VARCHAR(15) NOT NULL,
	name VARCHAR(20) NOT NULL,
	timezone INT DEFAULT 0,
	invitations VARCHAR(6000) DEFAULT '[]',
	PRIMARY KEY ( id )
	)ENGINE=InnoDB DEFAULT CHARSET=utf8;"""
	exe(sql)
    sql ="CREATE TABLE IF NOT EXISTS "+invitationPage+"""(
    id VARCHAR(10) NOT NULL,
    title VARCHAR(40) NOT NULL,
    status VARCHAR(1) default 'v',
    creator VARCHAR(40) NOT NULL,
    members varchar(4000) DEFAULT '[]',
    options VARCHAR(100) default '[]',
    description varchar(100) default '',
    startdate varchar(6) NOT NULL,
    final varchar(100) default '',
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
    sql ="CREATE TABLE IF NOT EXISTS "+optionPage+"""(
        uid VARCHAR(40) NOT NULL,
        iid VARCHAR(10) NOT NULL,
        op VARCHAR(100) default '[]',
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
    db = MySQLdb.connect(host='127.0.0.1',port = 3306,user='root', passwd='',db ='gooseberry')
    cursor = db.cursor()
    results = []
    print "-------SQL COMMAND------"
    print sql
    try:
       cursor.execute(sql)
       results = cursor.fetchall()
       db.commit()
    except:
       db.rollback()
    db.close()
    print "-------SQL RESULT------"
    print results
    return results
