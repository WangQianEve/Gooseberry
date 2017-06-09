#!/usr/bin/python
# -*- coding: UTF-8 -*-
# BY EVELYN WANG
import MySQLdb, random, string, json

userPage = "users"
invitationPage = "invitations"
contactPage = "contacts"
timePage = "times"
optionPage = "options"

InvIdLength = 10
calendarW = 7

def ranchar(i):
    return ''.join(random.sample(string.ascii_letters + string.digits, i))
#Users
def addUser(uid, psw, name, timezone):
    sql = "insert into %s (id, psw, name, timezone) values ('%s','%s','%s',%d)"% (userPage, uid, psw, name, timezone)
    return exe(sql)

def findUser(goal,uid):
    sql = "select %s from %s where id='%s'" % (goal,userPage,uid)
    return exe(sql)

def updateUser(goal,val,uid):
    sql = "update %s set %s=\"%s\" where id='%s'" % (userPage,goal,val,uid)
    return exe(sql)

def userAddInv(inv,uid):
    sql = "select invitations from %s where id='%s'" % (userPage,uid)
    exe(sql)
    invs = json.loads(exe(sql)[0][0])
    invs.append(inv)
    sql = "update %s set invitations='%s' where id='%s'" % (userPage,json.dumps(invs),uid)
    exe(sql)

def userDelInv(inv,uid):
    sql = "select invitations from %s where id='%s'" % (userPage,uid)
    exe(sql)
    invs = json.loads(exe(sql)[0][0])
    if inv in invs:
        invs.remove(inv)
        sql = "update %s set invitations='%s' where id='%s'" % (userPage,json.dumps(invs),uid)
        exe(sql)

    # more: modify name or psw or timezone

# contacts
def addCon(uid, fid, fname, fnickname):
    sql = "insert into %s (uid, id, name, nickname) values ('%s','%s','%s','%s' )"% (contactPage, uid, fid, fname, fnickname)
    exe(sql)

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

# options
def addOpp(inv,uid,op):
    sql = "select opt from %s where uid ='%s' and iid='%s' and opt='%s'" % (optionPage, uid, inv, op)
    t = exe(sql)
    if len(t)==0:
        sql = "insert into %s (uid, iid, opt) values ('%s','%s','%s' )"% (optionPage, uid, inv, op)
        exe(sql)

def delOpp(inv,uid=""):
    if(uid==''):
        sql = "delete from %s where iid='%s'" % (optionPage, inv)
    else:
        sql = "delete from %s where uid='%s' and iid='%s'" % (optionPage, uid, inv)
    exe(sql)

def findOpp(inv,uid):
    sql = "select opt from %s where uid ='%s' and iid='%s'" % (optionPage, uid, inv)
    return exe(sql)

def findVoters(inv,op):
    sql = "select uid from %s where opt ='%s' and iid='%s'" % (optionPage, op, inv)
    return exe(sql)

#times
def addTime(uid,title,start,end):
    sql = "insert into %s (id, title, start, end) values ('%s','%s','%s','%s' )"% (timePage,uid,title,start,end)
    exe(sql)

def deleteTime(uid, title, start, end):
    sql = "delete from %s where id='%s' and title='%s' and start='%s' and end='%s'" % (timePage,uid,title,start,end)
    exe(sql)

def findTime(uid, start):
    goal = "title,start,end"
    end = "timestampadd(day,%d,'%s')" % (calendarW,start)
    sql = "select %s from %s where id='%s' and ((start>='%s' and start<%s) or (end>'%s' and end<=%s))" % (goal,timePage,uid, start, end, start, end)
    return exe(sql)

#invitations
def addInv(goal, data):
    iid = ranchar(InvIdLength)
    sql = "select id from %s while id=%s" % (invitationPage,iid)
    while(len(exe(sql))!=0):
        iid = ranchar(InvIdLength)
        sql = "select id from %s while id=%s" % (invitationPage,iid)
    sql = "insert into %s (%s) values ('%s',%s)"% (invitationPage, goal, iid, data)
    exe(sql)

def delInv(iid):
    sql = "delete from %s where id='%s'"% (invitationPage, iid)
    exe(sql)

def findInvByCreator(goal,uid):
    sql = "select %s from %s where creator='%s'" % (goal,invitationPage,uid)
    return exe(sql)

def findInvById(goal,iid):
    sql = "select %s from %s where id='%s'" % (goal,invitationPage,iid)
    return exe(sql)

def invAddMember(inv, uid):
    sql = "select members from %s where id='%s'" % (invitationPage,inv)
    mems = json.loads(exe(sql)[0][0])
    mems.append(uid)
    sql = "update %s set members='%s' where id='%s'" % (invitationPage,json.dumps(mems),inv)
    exe(sql)

def invSettle(inv, ops):
    s='f'
    if len(ops)==0:
        s='v'
    sql = "update %s set final='%s',status='%s' where id='%s'" % (invitationPage,json.dumps(ops),s,inv)
    exe(sql)

def invDelMember(inv, uid):
    sql = "select members from %s where id='%s'" % (invitationPage,inv)
    mems = json.loads(exe(sql)[0][0])
    mems.remove(uid)
    sql = "update %s set members='%s' where id='%s'" % (invitationPage,json.dumps(mems),inv)
    exe(sql)

def exe(sql):
    db = MySQLdb.connect(host='127.0.0.1',port = 3306,user='root', passwd='',db ='gooseberry')
    print "-------SQL COMMAND------"
    print sql
    cursor = db.cursor()
    results = []
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
