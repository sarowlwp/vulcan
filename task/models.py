'''
Created on 2013-6-10

@author: wenpingliu
'''
from django.db import models
import datetime
import time

class vulcan_task(models.Model):
    task_id = models.AutoField(primary_key=True)
    stage_id = models.IntegerField()
    status = models.IntegerField(default=0)
    user_id = models.IntegerField()
    task_name = models.CharField(max_length=100,default='')
    task_description = models.CharField(max_length=1000,default='')
    priority = models.IntegerField()
    create_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField()
    @property
    def user_nick(self):
        return vulcan_user.objects.get(user_id = self.user_id).nick
    @property
    def priority_zh(self):
        return vulcan_priority.objects.get(priority_id = self.priority).priority_name
    @property
    def requirement(self):
        return self.stage_id == 1
    @property
    def development(self):
        return self.stage_id == 2
    @property
    def testing(self):
        return self.stage_id == 3
    @property
    def online(self):
        return self.stage_id == 4
    
    @property
    def iswarning(self):
        endtime = self.end_time.replace(tzinfo=None)
        nowtime = datetime.datetime.now().replace(tzinfo=None)
        delaytime = datetime.timedelta (days = 2)
        try:
            datetime.datetime.now()
            #print datetime.datetime.now()
            #print type(self.end_time)
            #print type(datetime.datetime.now())
            #print self.end_time - datetime.datetime.now()
        except Exception,e:
            print e
       
        return endtime - nowtime < delaytime
    
    @property
    def iserror(self):
        endtime = self.end_time.replace(tzinfo=None)
        nowtime = datetime.datetime.now().replace(tzinfo=None)
        return endtime < nowtime


        
class vulcan_stage(models.Model):
    stage_id = models.AutoField(primary_key=True)
    stage_name =  models.CharField(max_length=100,default='')

class vulcan_priority(models.Model):
    priority_id = models.AutoField(primary_key=True)
    priority_name =  models.CharField(max_length=100,default='')
    
class vulcan_user(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100,default='')
    password = models.CharField(max_length=100,default='')
    nick = models.CharField(max_length=100,default='')

