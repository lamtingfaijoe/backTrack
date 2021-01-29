"""backtrack URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic.base import TemplateView
from COMP3297 import views

urlpatterns = [
	path('admin/', admin.site.urls),
	path('COMP3297/', include('COMP3297.urls')),
	path('COMP3297/', include('django.contrib.auth.urls')),
	path('COMP3297/home/', TemplateView.as_view(template_name='home.html'), name='home'),

    re_path(r'editpbi/(\d+)/$',views.editpbi),
    re_path(r'editpbi/(\d+)/(\w+)$',views.editpbi),
    re_path(r'deletepbi/(\d+)/$',views.deletepbi),
    re_path(r'edittask/(\d+)/$',views.edittask),
    re_path(r'edittask/(\d+)/(\w+)$',views.edittask),
    re_path(r'deletetask/(\d+)/$',views.deletetask),
    re_path(r'deleteDeveloper/(\d+)/$',views.deleteDeveloper),
    re_path(r'deleteManager/(\d+)/(\d+)$',views.deleteManager)
]
