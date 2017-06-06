#!/usr/bin/python
# -*- coding: UTF-8 -*-
import MySQLdb, random, string
# uid = "evelynwang"
# uname = "evelyn"
# timezone = 8
userPage = "users"
invitationPage = "invitations"
contactPage = "contacts"
timePage = "times"

InvIdLength = 20
calendarW = 7

def ranchar(i):
    return ''.join(random.sample(string.ascii_letters + string.digits, i))

#User
def addUser(uid, psw, name, timezone):
    sql = "insert into %s (id, psw, name, timezone) values ('%s','%s','%s',%d)"% (userPage, uid, psw, name, timezone)
    exe(sql)

def findUser(goal,uid):
    sql = "select %s from %s where id='%s'" % (goal,userPage,uid)
    return exe(sql)
# modify name or psw or timezone

# contacts
def addCon(uid, fid, fname, fnickname):
    sql = "insert into %s (uid, id, name, nickname) values ('%s','%s','%s','%s' )"% (contactPage, uid, fid, fname, fnickname)
    exe(sql)
    # sql = "select fid from %s where uid ='%s' and id='%s'" % (contactPage, uid, fid)
    # t = exe(sql)
    # if len(t)==0:
    #     sql = "insert into %s (uid, id, name, nickname) values ('%s','%s','%s','%s' )"% (contactPage, uid, fid, fname, fnickname)
    #     exe(sql)

def updateCon(uid, fid, goal, val):
    sql = "update %s set %s='%s' where uid='%s' and id='%s'" %  (contactPage, goal, val, uid, fid[4:])
    return exe(sql)

def delCon(uid,fid):
    sql = "delete from %s where uid='%s' and id='%s'" % (contactPage, uid, fid)
    exe(sql)

def findCon(uid):
    goal = "id,name,nickname"
    sql = "select %s from %s where uid='%s' " % (goal,contactPage,uid)
    return exe(sql)

def relation(uid,fid):
    goal = "id,name,nickname"
    sql = "select %s from %s where uid='%s' and id='%s' " % (goal,contactPage,uid,fid)
    return exe(sql)

#time
def addTime(uid,title,start,end):
    sql = "insert into %s (uid, title, start, end) values ('%s','%s','%s','%s' )"% (timepage,uid,title,start,end)
    print sql
    exe(sql)

def deleteTime(uid, title, start, end):
    sql = "delete from %s where uid='%s' and title='%s' and start='%s' and end='%s'" % (timepage,uid,title,start,end)
    print sql
    exe(sql)

def findTime(uid, start):
    goal = "title,start,end"
    end = "timestampadd(day,%d,'%s')" % (calendarW,start)
    sql = "select %s from %s where uid='%s' and ((start>='%s' and start<%s) or (end>'%s' and end<=%s))" % (goal,timepage,uid, start, end, start, end)
    return exe(sql)

#invitations
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

def deleteInv(iid):
    sql = "delete from %s where iid='%s'"% (invpage, iid)
    print sql
    exe(sql)
    return

def findInv(goal,uid):
    sql = "select %s from %s where icreator='%s'" % (goal,invpage,uid)
    print sql
    return exe(sql)
#others
def changePage():
    sql = """
    alter table invitations MODIFY iid VARCHAR(20);
    alter table invitations add column creator varchar(40) not null;
    alter table invitations CHANGE creator icreator VARCHAR(40);
    """
# update page set a=1,b=2,c=3 where d=4
# delete from page where d=4

def exe(sql):
    print "[sql] ",
    print sql
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
    print "[sql] ",
    print results
    return results
#findInv("iid,ititle,istate,icount","evelynwang")
#addInv("iid,ititle,istate,icount,icreator","'soa meeting','v',0,'evelynwang'")
#deleteInv("py2wSVrsMI")
# addUser(page,"wangxr","daniang")
# makeCon()
# addCon("evelynwang","wangxr","daniang","xinran")
# print(findCon("evelynwang"))
# makeTime()
# addTime("wangxr","e","1705310000","1706010000")
# deleteTime("eve","test2","1705310010","1705310111")
# findTime("wangxr","170524")
