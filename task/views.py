'''
Created on 2013-6-10

@author: wenpingliu
'''
from django.http import HttpResponse,HttpResponseRedirect
from django.views.generic.base import View
from task.models import vulcan_task,vulcan_user,vulcan_stage,vulcan_priority
from django.shortcuts import render
try: import simplejson as json
except ImportError: import json
from django.core.paginator import Paginator


class UserView(View):
    
    def get(self,request,*args,**kwargs):
        response = HttpResponse('i am book get list')
        return response;
#    
#    def handle_delete(self,request,*args,**kwargs):
#        response = HttpResponse('i am book delete list')
#        return response; 
#    
#    def handle_put(self,request,*args,**kwargs):
#        response = HttpResponse('i am book put list')
#        return response; 
#    
#    def post(self,request,*args,**kwargs):
#        method = request.POST['_method']
#        if method != None:
#            if method.lower() == 'put':
#                return self.handle_put(request,*args,**kwargs)
#            if method.lower() == 'delete':
#                return self.handle_put(request,*args,**kwargs)
#        
#        response = HttpResponse('i am book post list,%s' % method)
#        return response;
#    
#    def delete(self,request,*args,**kwargs):
#        return self.handle_delete(request,*args,**kwargs)
#    
#    def put(self,request,*args,**kwargs):
#        return self.handle_put(request,*args,**kwargs)


class Ret():
    
    SUCCESS_CODE = 200
    ERROR_CODE = 500
    ILLEDGEPARAM_CODE = 400
    NOTFOUND = 404
    
    def ret(self,code=200,msg="",data={}):
        result = dict()
        result['code']=code
        result['msg']=msg
        result['data']=data
        return json.dumps(result)
    
    def ret_with_response(self,code=200,msg="",data={}):
        return  HttpResponse(self.ret(code,msg,data))
   
class RequestUtil():
    def GET(self,request,param,default=None):
        if request.GET.has_key(param):
            return request.GET[param]
        else:
            return default
    
    def POST(self,request,param,default=None):
        if request.POST.has_key(param):
            return request.POST[param]
        else:
            return default
        
class Page():
    total = 0
    totalpage = 0
    currentpage = 0  
    pagesize = 0
    startindex = 0
    endindex = 0
    prevpage = 0
    nextpage = 0
    display = 5
    pagelist = list()
    
    def init(self,total,pagesize,current,display):
        self.display = int(display)
        self.total = int(total)
        self.pagesize = int(pagesize)
        current = int(current)
        if self.total % self.pagesize == 0:
            self.totalpage = self.total / self.pagesize
        else:
            self.totalpage = self.total / self.pagesize + 1
        if current < 1:
            current = 1;
        self.currentpage = current
        self.startindex = (self.currentpage - 1)*self.pagesize
        self.endindex = (self.currentpage)*self.pagesize
        self.prevpage = self.currentpage - 1
        self.nextpage = self.currentpage + 1
        if self.display <1:
            self.display = 1
        
        self.pagelist = list()
        if self.totalpage - 1 <= self.display:
            for i in range(1,self.totalpage+1):
                self.pagelist.append(i)
        else:
            if self.totalpage - self.currentpage >= self.display:
                for i in range(self.currentpage,self.currentpage+5+1):
                    self.pagelist.append(i)
            else:
                for i in range(self.currentpage - (self.display - (self.totalpage - self.currentpage)),self.totalpage+1):
                    self.pagelist.append(i)
            
        

class TaskListView(View):
    template_name = 'task_list.html'
    def get(self,request,*args,**kwargs):
        status = RequestUtil().GET(request, "status", 0)
        pagesize = RequestUtil().GET(request, "pagesize", 20)
        currentpage = RequestUtil().GET(request, "page", 1)
        display = RequestUtil().GET(request, "display", 5)

        page = Page()
        
        if status == "all":
            page.init(vulcan_task.objects.count(),pagesize,currentpage,display)
            tasks = vulcan_task.objects.all()[page.startindex:page.endindex]
        else:
            page.init(vulcan_task.objects.filter(status=status).count(),pagesize,currentpage,display)
            tasks = vulcan_task.objects.filter(status=status)[page.startindex:page.endindex]
            
            
        ftasks = vulcan_task.objects.filter(status=0)
        rcount = ftasks.filter(stage_id=1).count()
        dcount = ftasks.filter(stage_id=2).count()
        tcount = ftasks.filter(stage_id=3).count()
        ocount = ftasks.filter(stage_id=4).count()
        
        users = vulcan_user.objects.all()
        stages = vulcan_stage.objects.all()
        prioritys = vulcan_priority.objects.all()
        return render(request, self.template_name,{'tasks': tasks,'users':users,
                                                   'stages':stages,'prioritys':prioritys,
                                                   'rcount':rcount,'dcount':dcount,
                                                   'tcount':tcount,'ocount':ocount,
                                                   'status':status,'page':page
                                                   })
    
    
class TaskView(View):
    def get(self,request,*args,**kwargs):
        self.template_name = 'add_task.html'
        users = vulcan_user.objects.all()
        stages = vulcan_stage.objects.all()
        prioritys = vulcan_priority.objects.all()
        return render(request, self.template_name,{'users':users,'stages':stages,'prioritys':prioritys})
    
    def handle_delete(self,request,*args,**kwargs):
        if kwargs.has_key('task_id'):
            taskid = kwargs['task_id']
            try:
                task = vulcan_task.objects.get(task_id=taskid)
            except Exception:
                task = None
            if task == None:
                return Ret().ret_with_response(Ret.NOTFOUND)
            task.delete()
            return Ret().ret_with_response(Ret.SUCCESS_CODE)
        else:
            return Ret().ret_with_response(Ret.ERROR_CODE)

    
    def handle_put(self,request,*args,**kwargs):
        taskid = RequestUtil().POST(request, 'taskid')
        taskname = RequestUtil().POST(request, 'taskname')
        endtime =  RequestUtil().POST(request, 'endtime')
        userid = RequestUtil().POST(request, 'userid')
        priority = RequestUtil().POST(request, 'priority')
        status = RequestUtil().POST(request, 'status')
        stageid = RequestUtil().POST(request, 'stageid')
        taskdescription = RequestUtil().POST(request, 'taskdescription')
        if kwargs.has_key('task_id'):
            taskid = kwargs['task_id']
            task = vulcan_task()
            try:
                task = vulcan_task.objects.get(task_id=taskid)
            except Exception:
                task = None
            if task != None:
                if taskname != None:
                    task.task_name = taskname
                if endtime != None:
                    task.end_time = endtime
                if userid != None:
                    task.user_id = userid
                if status != None:
                    task.status = status
                if priority != None:
                    task.priority = priority
                if stageid != None:
                    task.stage_id = stageid
                if taskdescription != None:
                    task.task_description = taskdescription
                task.save()
                return Ret().ret_with_response(Ret.SUCCESS_CODE)
        else:
            return Ret().ret_with_response(Ret.ILLEDGEPARAM_CODE)
        return HttpResponseRedirect('/tasks/'); 
    
    def post(self,request,*args,**kwargs):
        if request.POST.has_key('_method'):
            method = request.POST['_method']
            if method.lower() == 'put':
                return self.handle_put(request,*args,**kwargs)
            if method.lower() == 'delete':
                return self.handle_delete(request,*args,**kwargs)
        newtask = vulcan_task()
        newtask.task_name = request.POST['taskname']
        newtask.end_time = request.POST['endtime']
        newtask.user_id = request.POST['userid']
        newtask.priority = request.POST['priority']
        newtask.stage_id = request.POST['stageid']
        newtask.task_description = request.POST['taskdescription']
        vulcan_task.save(newtask)
        return Ret().ret_with_response(Ret.SUCCESS_CODE)
        #return HttpResponseRedirect('/tasks/'); 

    
    def delete(self,request,*args,**kwargs):
        return self.handle_delete(request,*args,**kwargs)
    
    def put(self,request,*args,**kwargs):
        return self.handle_put(request,*args,**kwargs)
    