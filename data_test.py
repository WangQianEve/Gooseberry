import time,datetime

cur_date=time.strftime('%y%m%d0000',time.localtime(time.time()))
print cur_date

t="1706081200"
lineNum = 24
time_num = 36


d1 = datetime.datetime(int('20'+cur_date[0:2]), int(cur_date[2:4]), int(cur_date[4:6]))
d2 = (d1 + datetime.timedelta(days=time_num/lineNum)).strftime('%y%m%d')  
t = d2 + '%2d' %(time_num % lineNum) + '00' 
print t