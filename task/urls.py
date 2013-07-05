from django.conf.urls import patterns, include, url
from django.contrib.auth.models import User,Group
from task.views import TaskListView,TaskView

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'vulcan.views.home', name='home'),
    # url(r'^vulcan/', include('vulcan.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^tasks/$', TaskListView.as_view()),
    url(r'^task/(?P<task_id>\d+)', TaskView.as_view()),
    url(r'^task/$', TaskView.as_view()),

)
