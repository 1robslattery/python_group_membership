from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path("", views.loginreg),
    path('admin/', admin.site.urls),
    path('register', views.register),
    path('login', views.login),
    path('groups', views.groups),
    path('newgroup', views.newgroup),
    path('creategroup', views.creategroup),
    path('members/<members_id>', views.members),
    path('groups/<group_id>', views.grp_details),
    path('join_group/<group_id>', views.join_group),
    path('leave_group/<group_id>', views.leave_group),
    path('delete/<deletegroup_id>', views.deletegroup),
    path('logout', views.logout)
]