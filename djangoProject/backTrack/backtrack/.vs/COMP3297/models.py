from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

#override the User class of Django
class ManagerOrDeveloper(AbstractUser):
	pass
	# add additional fields in here
	name = models.CharField(max_length = 40, unique=True)
	post = models.CharField(max_length = 2, choices=(
		('UD', 'Unassigned Developer'),
		('AD', 'Assigned Developer'),
		('O', 'Owner'),
		('M', 'Manager'),
		), default='Unassigned Developer')

	def __str__(self):
		return "%s - %s(%s)"%(self.get_post_display(), self.username, self.name)
	class Meta:
		#abstract = True
		ordering = ['post', 'name']

class Project(models.Model):
	name = models.CharField(max_length = 40, unique=True)
	current_sprint = models.IntegerField(default=1)
	def __str__(self):
		return self.name
	class Meta:
		ordering = ['name']

class Developer(ManagerOrDeveloper):
	project = models.ForeignKey(Project , on_delete=models.CASCADE, default=None, null=True, blank=True)
	# name = models.CharField(max_length = 40, unique=True)

class Manager(ManagerOrDeveloper):
	project = models.ManyToManyField(Project)
	# name = models.CharField(max_length = 40, unique=True)

class Sprint_Backlog(models.Model):
	sprint_number = models.IntegerField()
	project = models.ForeignKey(Project , on_delete = models.CASCADE)
	capacity = models.IntegerField()
	def __str__(self):
		return '%s - %d'%(self.project, self.sprint_number)
	class Meta:
		unique_together = ('project', 'sprint_number',)
		ordering = ['project', 'sprint_number']

class PBI(models.Model):
	project = models.ForeignKey(Project , on_delete = models.CASCADE)
	PBI_name = models.CharField(max_length = 200, unique=True)
	description = models.CharField(max_length = 200)
	est_storypoint = models.IntegerField()
	priority = models.IntegerField()
	PBI_status = models.CharField(max_length = 2, choices=(
		('TD', 'To Do'),
		('IP', 'In Progress'),
		('F', 'Finished'),
		('U', 'Unfinished'),
		), default='To Do')
	sprint = models.ForeignKey(Sprint_Backlog , on_delete = models.CASCADE, default=None, null=True, blank=True)
	def __str__(self):
		return '%d. %s'%(self.priority, self.PBI_name)
	class Meta:
		unique_together = ('project', 'priority',)
		ordering = ['project', 'priority']

class Task(models.Model):
	project = models.ForeignKey(Project , on_delete = models.CASCADE)
	pbi = models.ForeignKey(PBI , on_delete = models.CASCADE)
	developer = models.ForeignKey(Developer , on_delete = models.CASCADE)
	sprint = models.ForeignKey(Sprint_Backlog , on_delete = models.CASCADE, default=None, null=True, blank=True)
	description = models.CharField(max_length = 200)
	estimated_effort = models.IntegerField()
	task_status = models.CharField(max_length = 2, choices=(
		('TD', 'To Do'),
		('IP', 'In Progress'),
		('F', 'Finished'),
		('U', 'Unfinished'),
		), default='To Do')
	def __str__(self):
		return '%s - %s - %s'%(self.project, self.pbi, self.description)
	class Meta:
		unique_together = ('pbi','description',)
		ordering = ['project', 'pbi', 'task_status']