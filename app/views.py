from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt
from django.db.models import Q

def loginreg(request):
	return render(request, "loginreg.html")

def register(request):
	print(request.POST)
	errors = User.objects.registerValidator(request.POST)
	print(errors)
	if len(errors) > 0:
		for key, value in errors.items():
			messages.error(request, value)
		return redirect("/")
	passwordFromForm = request.POST['password']
	hashed_password = bcrypt.hashpw(passwordFromForm.encode(), bcrypt.gensalt())
	newuser = User.objects.create(firstname = request.POST['fname'], lastname = request.POST['lname'], email = request.POST['email'], password = hashed_password.decode())
	print(newuser)
	request.session['loggedinUserID'] = newuser.id
	return redirect("/groups")

def login(request):
	print(request.POST)
	errors = User.objects.loginValidator(request.POST)
	if len(errors) > 0:
		for key, value in errors.items():
			messages.error(request, value)
		return redirect("/")
	else:
		loggedinuser = User.objects.filter(email = request.POST['email'])
		loggedinuser = loggedinuser[0]
		request.session['loggedinUserID'] = loggedinuser.id
		return redirect("/groups")

def groups(request):
	loggedinUser = User.objects.get(id = request.session['loggedinUserID'])
	context = {
		"loggedinUser" : loggedinUser,
		"allGroups" : Group.objects.all(),
#		"deleteGroup" : Group.objects.get(grpcreator = loggedinUser)
	}
	return render(request, 'home.html', context)

def newgroup(request):
	context = {
		"allGroups" : Group.objects.all()
	}
	return render(request, 'home.html', context)

def creategroup(request):
	print(request.POST)
	loggedinUser = User.objects.get(id = request.session['loggedinUserID'])
	errors = Group.objects.groupValidator(request.POST)
	print(errors)
	if len(errors) > 0:
		for key, value in errors.items():
			messages.error(request, value)
		return redirect("/groups")
	newGroup = Group.objects.create(org_grp_name = request.POST['org_grp_name'], desc = request.POST['desc'], grpcreator = loggedinUser) 
	newGroup.members.add(loggedinUser)
	print(newGroup)
	return redirect("/newgroup")

def members(request, member_id):
	context = {
		"memberCount" : User.objects.get(id = member_id)
	}
	return render(request, "home.html", context)

def grp_details(request, group_id):
	group = Group.objects.get(id = group_id)
	context = {
	"groupDetails" : Group.objects.filter(id = group_id),
	"loggedinUser" : User.objects.get(id = request.session['loggedinUserID'])
	}
	print(group)
	return render(request, "groups.html", context)

def join_group(request, group_id):
	groupToJoin = Group.objects.get(id = group_id)
	loggedinUser = User.objects.get(id = request.session['loggedinUserID'])
	groupToJoin.members.add(loggedinUser)
	print(groupToJoin)
	return redirect("/groups")

def leave_group(request, group_id):
	groupToLeave = Group.objects.get(id = group_id)
	loggedinUser = User.objects.get(id = request.session['loggedinUserID'])
	groupToLeave.members.remove(loggedinUser)
	print(groupToLeave)
	return redirect("/groups")

def deletegroup(request, deletegroup_id):
	deletegroup = Group.objects.get(id = deletegroup_id)
	deletegroup.delete()
	return redirect("/groups")

def logout(request):
	request.session.clear()
	return redirect("/")