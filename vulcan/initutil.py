# coding=utf-8
'''
Created on 2013-6-12

@author: wenpingliu
'''
import time
from task.models import vulcan_task,vulcan_stage,vulcan_user,vulcan_priority

def init_stage():
    stage = vulcan_stage()
    stage.stage_name="需求"
    vulcan_stage.save(stage)
    stage = vulcan_stage()
    stage.stage_name="开发"
    vulcan_stage.save(stage)
    stage = vulcan_stage()
    stage.stage_name="测试"
    vulcan_stage.save(stage)
    stage = vulcan_stage()
    stage.stage_name="上线"
    vulcan_stage.save(stage)    
    
def init_prioirty():
    vulcan_priority_all = vulcan_priority.objects.all()
    vulcan_priority().delete(vulcan_priority_all)
    priority = vulcan_priority()
    priority.priority_name="低"
    vulcan_priority.save(priority)
    priority = vulcan_priority()
    priority.priority_name="中"
    vulcan_priority.save(priority)
    priority = vulcan_priority()
    priority.priority_name="高"
    vulcan_priority.save(priority)
    priority = vulcan_priority()
    priority.priority_name="紧急"
    vulcan_priority.save(priority)
    
def init_user():
    user = vulcan_user();
    #user.username = "wenpingliu"
    #user.nick = u"刘文平"
    #user.username = "donglaizhang"
    #user.nick = '张东来'
    #user.username = "haiyunwang"
    #user.nikc = '王海云'
    #vulcan_user.save(user);

if __name__ == '__main__':
    
    print time.time()
#    init_prioirty()
    #init_stage()
    
