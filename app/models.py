from django.db import models
import re
import bcrypt

class UserManager(models.Manager):
	def registerValidator(self, postData):
		EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

		errors = {}
		if len(postData['fname']) < 1:
			errors['fname'] = "You must enter first name"
		if len(postData['lname']) < 1:
			errors['lname'] = "You must enter last name"
		if len(postData['email']) < 1:
			errors['email'] = "You must enter email"
		if not EMAIL_REGEX.match(postData['email']):
			errors['email'] = ("Invalid email address!")
		else:
			emailtaken = User.objects.filter(email = postData['email'])
			if len(emailtaken) > 0:
				errors['emailtaken'] = "Email is already taken. Choose another email"
		if len(postData['password']) < 8:
			errors['password'] = "You must enter at least eight (8) characters"
		if postData['password'] != postData['confirm_password']:
			errors['passwordconfirm'] = "Password and confirm password must match"
		return errors

	def loginValidator(self, postData):
		errors = {}
		if len(postData['email']) < 1:
			errors['emaillength'] = "You must enter an email"
		userinDB = User.objects.filter(email = postData['email'])
		if len(userinDB) == 0:
			errors['emailnotregistered'] = "This email is not registered. Please register first."
		else:
			userinDB = userinDB[0]
			print(userinDB)
			if bcrypt.checkpw(postData['password'].encode(), userinDB.password.encode()):
				print("password match")
			else:
				print("failed password")
				errors['passwordwrong'] = "Incorrect password"
		print(errors)
		return errors

class groupManager(models.Manager):
	def groupValidator(self, postData):

		errors = {}
		if len(postData['org_grp_name']) < 3:
			errors['org_grp_name'] = "Organization name must consist of at least 3 characters"
		# if not group_name.match(postData['org_grp_name']):
		# 	errors['orgname'] = ("Duplicate organization name!")
		# else:
		# 	orgnametaken = User.objects.filter(orgname = postData['org_grp_name'])
		# 	if len(emailtaken) > 0:
		# 		errors['orgnametaken'] = "That name is already taken. Choose another name"
		if len(postData['desc']) < 1:
			errors['desc'] = "A description must be provided"
		if len(postData['desc']) < 3:
			errors['desclength'] = "A description must be at least 3 characters"
		return errors

class User(models.Model):
	firstname = models.CharField(max_length=255)
	lastname = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = UserManager()

class Group(models.Model):
	org_grp_name = models.TextField()
	desc = models.CharField(max_length=255)
	members = models.ManyToManyField(User, related_name="members_of_group")
	grpcreator = models.ForeignKey(User, related_name="creator_of_group", on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = groupManager()