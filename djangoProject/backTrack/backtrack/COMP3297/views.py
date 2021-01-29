from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.shortcuts import render,redirect
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views import generic
from COMP3297.auth import ManagerOrDeveloperBackTrack
from COMP3297.forms import ManagerOrDeveloperCreationForm
from COMP3297.models import *
from COMP3297.newprojectform import ProjectForm
from COMP3297.newPBIform import PBIForm
from COMP3297.newtaskform import TaskForm
from COMP3297.newSprintForm import newSprintForm
from COMP3297.InviteForm import *

def inviteDeveloper(request, project):
	developer_id=tuple()
	for developer_object in Developer.objects.all():
		if developer_object.post == 'UD':
			developer_id += (str(developer_object.id), str(developer_object.name)),

	if(len(developer_id) == 0):
		messages.error(request,'No developer is available')
		return redirect('http://127.0.0.1:8000/COMP3297/' + str(project) + '/owner')

	if request.method == "POST":
		invited = InviteDeveloperForm(request.POST, project_id=project,developer_id=developer_id)
		if invited.is_valid():
			id = invited.cleaned_data['ID']
			DEVEL = Developer.objects.get(id=id)
			current = Project.objects.get(id=project)
			DEVEL.project = current
			DEVEL.post = 'AD'
			DEVEL.save()
			messages.success(request, 'Successfully included developer %s to the your project.'%request.user.name)
			sendEmail(request, project, DEVEL, 'developer')
		return redirect('http://127.0.0.1:8000/COMP3297/' + str(project) + '/owner')
	else:
		invited = InviteDeveloperForm(request.POST, project_id=project,developer_id=developer_id)
	return render(request,"inviteDeveloper.html",locals())

def inviteManager(request, project):
	manager_id=tuple()
	for manager_object in Manager.objects.all():
		manager_id += (str(manager_object.id), str(manager_object.name)),

	if(len(manager_id) == 0):
		messages.error(request,'No developer is available')
		return redirect('http://127.0.0.1:8000/COMP3297/' + str(project) + '/owner')

	if request.method == "POST":
		invited = InviteManagerForm(request.POST, project_id=project,manager_id=manager_id)
		if invited.is_valid():
			id = invited.cleaned_data['ID']
			MANA = Manager.objects.get(id=id)
			current = Project.objects.get(id=project)
			MANA.project.add(current)
			MANA.save()
			messages.success(request, 'Successfully included manager %s to the your project.'%request.user.name)
			sendEmail(request, project, MANA, 'manager')
		return redirect('http://127.0.0.1:8000/COMP3297/' + str(project) + '/owner')
	else:
		invited = InviteManagerForm(request.POST, project_id=project,manager_id=manager_id)
	return render(request,"inviteManager.html",locals())
	
def deleteDeveloper(request,id=None,mode=None):
	try:
		developer=Developer.objects.get(id=id)
		target = developer.project.pk
		developer.project = None
		developer.post = 'UD'
		developer.save()

	except Exception as e:
		messages.error(request,str(e))

	return redirect('http://127.0.0.1:8000/COMP3297/' + str(target) + '/owner')

def deleteManager(request,manager_id=None,project_id=None,mode=None):
	try:
		manager=Manager.objects.get(id=manager_id)
		project=Project.objects.get(id=project_id)
		manager.project.remove(project)
		manager.save()

	except Exception as e:
		messages.error(request,str(e))

	return redirect('http://127.0.0.1:8000/COMP3297/' + str(project.id) + '/owner')

def newproject(request):
	username = None
	if request.user.is_authenticated:
		username = request.user.name

	if request.method == "POST":
		newproject=ProjectForm(request.POST, username=username)
		if newproject.is_valid():
			P_valid, O_valid = False, False
			Pname = newproject.cleaned_data['Project_Name']
			Oname = newproject.cleaned_data['Name_of_the_owner']
			try:
				Project.objects.get(name=Pname)
			except Project.DoesNotExist as Perror:
				P_valid = True
			except Exception as e:
				messages.error(request, str(e))
			try:
				developer = Developer.objects.get(name=Oname)
			except Developer.DoesNotExist as Derror:
				messages.error(request, str(Derror))
			else:
				if developer.post == 'UD':
					O_valid = True
				else:
					messages.error(request, 'The developer has to be unassigned.')

			if P_valid and O_valid:
				NewProject = Project.objects.create(name=Pname, current_sprint=1)
				messages.success(request, 'Project \'%s\' created.' %Pname)
				developer.post = 'O'
				developer.project = NewProject
				developer.save()
				messages.success(request, 'Owner \'%s\' created.' %Oname)
				try:
					checkProductBacklogs(request, NewProject.id)
					checkSprintBacklogs(request, NewProject.id)
				except Exception as e:
					messages.error(request,str(e))
				return redirect('../' + str(NewProject.pk) + '/owner')
			else:
				if not P_valid:
					messages.error(request, '\'%s\' already exists. Please try another name.' %Pname)
				if not O_valid:
					messages.error(request, '\'%s\' already exists. Please try another name.' %Oname)
				return redirect('./')
	else:
		newproject=ProjectForm(username=username)
	return render(request,"newproject.html",locals())

def newPBI(request, project_id):
	
	project_names = tuple()
	for project_object in Project.objects.all():
		project_names += (str(project_object.id), project_object.name),

	if request.method == "POST":
		newpbi = PBIForm(request.POST, project_id=project_id, project_names=project_names)
		if newpbi.is_valid():
			P_exist, PBI_created = False, False
			Project_name = newpbi.cleaned_data['Project_name']
			PBIname = newpbi.cleaned_data['PBI_name']
			description = newpbi.cleaned_data['description']
			est_storypoint = newpbi.cleaned_data['est_storypoint']
			priority = newpbi.cleaned_data['priority']
			PBI_status = newpbi.cleaned_data['status']
			try:
				project = Project.objects.get(id=Project_name)
			except Exception as e:
				messages.error(request, str(e))
			else:
				P_exist = True
			try:
				PBI.objects.get(PBI_name=PBIname)
			except PBI.DoesNotExist as PBIerror:
				PBI_created = True
			except Exception as e:
				messages.error(request, str(e))

			if P_exist and PBI_created:
				NewPBI = PBI.objects.create(PBI_name=PBIname, description=description, est_storypoint=est_storypoint, priority=priority, PBI_status=PBI_status, project=project)
				messages.success(request, 'PBI \'%s\' created.' %PBIname)
				try:
					checkProductBacklogs(request, project_id)
					checkSprintBacklogs(request, project_id)
				except Exception as e:
					messages.error(request,str(e))
				return redirect('../../' + str(project.pk) + '/owner')
			else:
				if not P_exist:
					messages.error(request, '\'%s\' does not exist.' %Project_name)
				if not PBI_created:
					messages.error(request, '\'%s\' already exists. Please try another name.' %PBIname)
				return redirect('./')

	else:
		newpbi=PBIForm(project_id=project_id, project_names=project_names)
	return render(request,"newpbi.html",locals())
	
def newtask(request, project_id):
	username = None
	if request.user.is_authenticated:
		username = request.user.name

	# project_names = tuple()
	# for project_object in Project.objects.all():
	#     project_names += (str(project_object.id), project_object.name),
		
	PBI_names = tuple()
	for pbi in PBI.objects.all():
		PBI_names += (pbi.PBI_name, pbi.PBI_name),

	if request.method == "POST":
		# newtask = TaskForm(request.POST, username=username, project_id=project, project_names=project_names, PBI_names=PBI_names)
		newtask = TaskForm(
			request.POST, 
			username = username , 
			PBI_names = PBI_names , 
			# Description = Description , 
			# task_status = task_status ,
			# Estimated_effort = Estimated_effort ,
			# Sprint = Sprint
			)

		# After the input from user
		if newtask.is_valid():
			task_unexist, sprint_isValid, developer_isValid = False, False, False
			PBI_name = newtask.cleaned_data['PBI_name']
			Description = newtask.cleaned_data['Description']
			Estimated_effort = newtask.cleaned_data['Estimated_effort']
			task_status = newtask.cleaned_data['task_status']
			sprint_number = newtask.cleaned_data['Sprint']
			project = Project.objects.get(id=project_id)
			try:		# No same task name
				newtask = Task.objects.get(description = Description)
			except Task.DoesNotExist as e:
				task_unexist = True
			else:
				task_unexist = False
				messages.error(request, 'Task already exists')

			try:		# Check if the sprint is valid
				Sprint_Backlog.objects.get(sprint_number = sprint_number, project = project)
			except Sprint_Backlog.DoesNotExist as SprintError:
				sprint_isValid = False
				messages.error(request, 'Invalid Sprint Number')
			else:
				sprint_isValid = True
			
			try:
				developer = Developer.objects.get(name = username)
			except Exception as e:
				messages.error(request, e)
			else:
				if developer.post == 'O':
					messages.error(request, 'Owner cannot create tasks.')
				else:
					developer_isValid = True

			if task_unexist and sprint_isValid and developer_isValid:
				pbi = PBI.objects.get(PBI_name = PBI_name)
				project = pbi.project
				# Project_name = newtask.cleaned_data['Project_name']
				sprint = Sprint_Backlog.objects.get(sprint_number = sprint_number, project = project)
				newTask = Task.objects.create(developer = developer, pbi = pbi, project = project, description = Description, estimated_effort = Estimated_effort, task_status = task_status, sprint = sprint)
				messages.success(request, 'Task \'%s\' created.' %Description)
				try:
					checkProductBacklogs(request, project_id)
					checkSprintBacklogs(request, project_id)
				except Exception as e:
					messages.error(request,str(e))
				return redirect('../../' + str(project.pk) + '/developer')
			else:
				return redirect('./')

	else:
		# newtask = TaskForm(username=username, project_id=project, project_names=project_names, PBI_names=PBI_names)
		newtask = TaskForm(
			username = username , 
			PBI_names = PBI_names , 
			# Description = Description , 
			# task_status = task_status ,
			# Estimated_effort = Estimated_effort ,
			# Sprint = Sprint
			)
	return render(request,"newtask.html",locals())

def newSprint(request,project):
	total_sprint = 0
	try:
		last_sprint = Sprint_Backlog.objects.filter(project__id=project).order_by('-sprint_number')[0]
		total_sprint = last_sprint.sprint_number
	except Exception as e:
		total_sprint = 0
	
	
	if request.method == "POST":
		newSprint = newSprintForm(request.POST, total_spirnt=total_sprint)
		if newSprint.is_valid():
			P_exist, Sprint_created = False, False
			sprintNumber = newSprint.cleaned_data['sprintNumber']
			capacity = newSprint.cleaned_data['capacity']
			
			try:
				currentProject = Project.objects.get(id=project)
			except Exception as e:
				messages.error(request, str(e))
			else:
				P_exist = True

			try:
				Sprint_Backlog.objects.get(sprint_number=sprintNumber, project = currentProject)
			except Sprint_Backlog.DoesNotExist as Sprinterror:
				Sprint_created = True
			except Exception as e:
				messages.error(request, str(e))
			else:
				messages.error(request , "sprint already exist")
			
			if P_exist and Sprint_created:
				newSprint = Sprint_Backlog.objects.create(sprint_number=sprintNumber, project=currentProject, capacity=capacity)
				messages.success(request, 'Sprint created.' )
				try:
					checkProductBacklogs(request, project)
					checkSprintBacklogs(request, project)
				except Exception as e:
					messages.error(request,str(e))
				return redirect('../../' + str(project) + '/developer')
			else:
				return redirect('./')
	else:
		newSprint=newSprintForm(total_spirnt=total_sprint)

	return render(request,"newSprint.html",locals())

def edittask(request,id=None,mode=None):
	if mode == "edit":
		try:
			task = Task.objects.get(id=id)
			task.description = request.GET['Tdescription']
			task.estimated_effort = request.GET['Testimated_effort']
			task.task_status = request.GET['Ttask_status']
			task.save()
		except Exception as e:
			messages.error(request, str(e))
		else:
			messages.success(request, "Task updated successfully.")
		project = task.project
		try:
			checkProductBacklogs(request, project.pk)
			checkSprintBacklogs(request, project.pk)
		except Exception as e:
			messages.error(request,str(e))
		return redirect('http://127.0.0.1:8000/COMP3297/' + str(project.pk) + '/developer')
	else:
		try:
			task = Task.objects.get(id=id)
		except Exception as e:
			messages.error(request, str(e))
		return render(request, "edittask.html",locals())

def editpbi(request,id=None,mode=None):
	if mode == "edit":
		try:
			pbi = PBI.objects.get(id=id)
			pbi.PBI_name = request.GET['Pname']
			pbi.description = request.GET['Pdescription']
			pbi.est_storypoint = request.GET['Pest_storypoint']
			pbi.priority = request.GET['Ppriority']
			pbi.PBI_status = request.GET['PPBI_status']
			pbi.save()
		except Exception as e:
			messages.error(request, str(e))
		else:
			messages.success(request, "PBI updated successfully.")
		project = pbi.project
		try:
			checkProductBacklogs(request, project.pk)
			checkSprintBacklogs(request, project.pk)
		except Exception as e:
			messages.error(request,str(e))
		return redirect('http://127.0.0.1:8000/COMP3297/' + str(project.pk) + '/owner')
	else:
		try:
			pbi = PBI.objects.get(id=id)
		except Exception as e:
			messages.error(request, str(e))
		return render(request, "editpbi.html",locals())

def deleteProject(request,id):
	try:
		project = Project.objects.get(id=id)#project id
		pbis = PBI.objects.filter(project = project)
		for pbi in pbis:
			task = Task.objects.filter(pbi = pbi)
			task.delete()
		sprint = Sprint_Backlog.objects.filter(project = project)
		developers = Developer.objects.filter(project = project).update(post='UD')
		project.delete()
		pbi.delete()
		sprint.delete()
		messages.success(request,"delete %s successfully"%project.name)
	except Exception as e:
		messages.error(request, str(e))
	try:
		checkProductBacklogs(request, id)
		checkSprintBacklogs(request, id)
	except Exception as e:
		messages.error(request,str(e))
	return redirect('home')	
	
def deletepbi(request,id=None,mode=None):
	try:
		pbi=PBI.objects.get(id=id)
		task = Task.objects.filter(pbi = pbi)
		project = pbi.project
		target = project.pk
		pbi.delete()
		task.delete()

	except Exception as e:
		messages.error(request,str(e))
	try:
		checkProductBacklogs(request, target)
		checkSprintBacklogs(request, target)
	except Exception as e:
		messages.error(request,str(e))

	return redirect('http://127.0.0.1:8000/COMP3297/' + str(target) + '/owner')

def deletetask(request,id=None,mode=None):
	try:
		task=Task.objects.get(id=id)
		project = task.project
		target = project.pk
		task.delete()
		messages.success(request, "Last Task deleted successfully")
		try:
			checkProductBacklogs(request, target)
			checkSprintBacklogs(request, target)
		except Exception as e:
			messages.error(request,str(e))
		return redirect('http://127.0.0.1:8000/COMP3297/' + str(target) + '/developer')
	except Exception as e:
		messages.error(request,str(e))
		return redirect('home')

def deleteSprint(request,project_id):
	last_sprint = Sprint_Backlog.objects.filter(project__id=project_id).order_by('-sprint_number')[0]
	project = Project.objects.get(id=project_id)
	if last_sprint.sprint_number==project.current_sprint:
		project.current_sprint -= 1
		project.save()
	for task in Task.objects.filter(sprint = last_sprint):
		try:
			task.delete()
		except Exception as e:
			messages.error(request,str(e))
	try:
		last_sprint.delete()
		messages.success(request, "Last sprint deleted successfully")
	except Exception as e:
		messages.error(request,str(e))
	try:
		checkProductBacklogs(request, project_id)
		checkSprintBacklogs(request, project_id)
	except Exception as e:
		messages.error(request,str(e))

	return redirect('http://127.0.0.1:8000/COMP3297/' + str(project_id) + '/developer')

def nextSprint(request,project_id):
	current_sprint = Project.objects.get(id=project_id).current_sprint
	last_sprint = Sprint_Backlog.objects.filter(project__id=project_id).order_by('-sprint_number')[0]

	if (current_sprint < last_sprint.sprint_number):
		current_sprint += 1
		Project.objects.filter(id=project_id).update(current_sprint=current_sprint)
	else:
		messages.error(request, 'This is the last sprint already!')
	
	try:
		checkProductBacklogs(request, project_id)
		checkSprintBacklogs(request, project_id)
	except Exception as e:
		messages.error(request,str(e))

	
	return redirect('http://127.0.0.1:8000/COMP3297/' + str(project_id) + '/developer')

def SignUpView(request):
	if request.method == 'POST':
		form = ManagerOrDeveloperCreationForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password1')
			name = form.cleaned_data.get('name')
			post = form.cleaned_data.get('post')
			email = form.cleaned_data.get('email')
			#user = authenticate(request=request, username=username, password=password)
			#user.delete()
			if post == 'M':
				user = Manager.objects.create_user(username=username, password=password, name=name, post=post, email=email)
				messages.success(request, 'Manager %s created'%name)
			elif post == 'UD':
				user = Developer.objects.create_user(username=username, password=password, name=name, post=post, email=email)
				messages.success(request, 'Developer %s created'%name)
			login(request, user, backend='COMP3297.auth.ManagerOrDeveloperBackTrack')
			return redirect('home')
	else:
		form = ManagerOrDeveloperCreationForm()
	return render(request, 'signup.html', {'form': form})

class OwnerView(TemplateView):
	template_name = "Owner.html"

	def get_context_data(self, **kwargs):
		project = self.kwargs['project']
		context = super().get_context_data(**kwargs)
		context['project'] = Project.objects.get(pk = project)
		context['owner'] = Developer.objects.get(project__id = project, post='O')
		context['pbi_list'] = PBI.objects.filter(project__id = project).order_by('priority')
		context['manager_list'] = Manager.objects.filter(project__id = project)
		context['developer_list'] = Developer.objects.filter(project__id = project, post='AD')
		cum_sp = []
		current_sp = 0
		task_of_pbi = {}
		for pbi in PBI.objects.filter(project__id = project).order_by('priority'):
			current_sp += pbi.est_storypoint
			cum_sp.append(current_sp)
			task_of_pbi[pbi.priority] = Task.objects.filter(pbi=pbi).order_by('sprint__sprint_number')
		context['task_of_pbi'] = task_of_pbi
		context['cum_sp'] = cum_sp
		return context

class ManagerView(TemplateView):
	template_name = "Manager.html"

	def get_context_data(self, **kwargs):
		project = self.kwargs['project']
		context = super().get_context_data(**kwargs)
		project_object = Project.objects.get(pk = project)
		context['project'] = project_object
		context['owner'] = Developer.objects.get(project__id = project, post='O')
		context['pbi_list'] = PBI.objects.filter(project__id = project)
		context['manager_list'] = project_object.manager_set.all()
		context['developer_list'] = Developer.objects.filter(project__id = project, post='AD')

		task_list = []
		sprint_list = {}
		for sprint in Sprint_Backlog.objects.filter(project__id = project).order_by('sprint_number'):
			task_list.append(Task.objects.filter(project__id = project, sprint__sprint_number = sprint.sprint_number).order_by('pbi__priority'))
			sprint_list[sprint.sprint_number] = sprint.capacity
		context['task_list'] = task_list
		context['sprint_list'] = sprint_list
		cum_sp = []
		current_sp = 0
		task_of_pbi = {}
		for pbi in PBI.objects.filter(project__id = project).order_by('priority'):
			current_sp += pbi.est_storypoint
			cum_sp.append(current_sp)
			task_of_pbi[pbi.priority] = Task.objects.filter(pbi=pbi).order_by('sprint__sprint_number')
		context['task_of_pbi'] = task_of_pbi
		context['cum_sp'] = cum_sp
		return context

class DeveloperView(TemplateView):
	template_name = "Developer.html"

	def get_context_data(self, **kwargs):
		project = self.kwargs['project']
		context = super().get_context_data(**kwargs)
		context['project'] = Project.objects.get(pk = project)
		context['owner'] = Developer.objects.get(project__id = project, post='O')
		context['pbi_list'] = PBI.objects.filter(project__id = project)
		context['manager_list'] = Manager.objects.filter(project__id = project)
		context['developer_list'] = Developer.objects.filter(project__id = project, post='AD')
		task_list = []
		sprint_list = {}
		for sprint in Sprint_Backlog.objects.filter(project__id = project).order_by('sprint_number'):
			task_list.append(Task.objects.filter(project__id = project, sprint__sprint_number = sprint.sprint_number).order_by('pbi__priority'))
			sprint_list[sprint.sprint_number] = sprint.capacity
		context['task_list'] = task_list
		context['sprint_list'] = sprint_list
		cum_sp = []
		current_sp = 0
		task_of_pbi = {}
		for pbi in PBI.objects.filter(project__id = project).order_by('priority'):
			current_sp += pbi.est_storypoint
			cum_sp.append(current_sp)
			task_of_pbi[pbi.priority] = Task.objects.filter(pbi=pbi).order_by('sprint__sprint_number')
		context['task_of_pbi'] = task_of_pbi
		context['cum_sp'] = cum_sp
		return context

class UnassignedDeveloperView(TemplateView):
	template_name = "UnassignedDeveloper.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['project_list'] = Project.objects.all().order_by('name')
		return context

class HomeView(TemplateView):
	template_name = "home.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['project_list'] = Project.objects.all().order_by('name')
		return context

class ManagerHomeView(TemplateView):
	template_name = "ManagerHome.html"

	def get_context_data(self, **kwargs):
		username = self.kwargs['username']
		context = super().get_context_data(**kwargs)
		context['project_list'] = Manager.objects.get_by_natural_key(username).project.all()
		return context

def GoToWork(request):
	#messages.success(request, 'GoToWork is work')
	name = request.user.name
	error = []
	is_Dev, is_Man = False, False
	try:
		developer = Developer.objects.get(name=name)
	except Exception as e:
		error.append(e)
	else:
		is_Dev = True
		if developer.post=='O':
			return redirect('../%d/owner'%developer.project.id)
		elif developer.post=='AD':
			return redirect('../%d/developer'%developer.project.id)
		else:
			return redirect('unassigneddeveloper')

	try:
		is_Man = True
		manager = Manager.objects.get(name=name)
	except Exception as e:
		error.append(e)
	else:
		return redirect('../managerhome/%s'%request.user.username)

	if not (is_Dev or is_Man):
		for e in error:
			messages.error(request, str(e))

	return redirect('home')

def checkSprintBacklogs(request, project_id):
	currentSprint = Project.objects.get(id=project_id).current_sprint
	for sprint in Sprint_Backlog.objects.filter(project__id=project_id):
		totalEffort = 0
		for task in Task.objects.filter(sprint=sprint):
			if sprint.sprint_number<currentSprint and task.task_status!='F':
				task.task_status = 'U'
				task.save()
			totalEffort += task.estimated_effort
		if totalEffort > sprint.capacity:
			messages.warning(request, 'The total effort of tasks in Sprint %d has exceed its capacity.'%sprint.sprint_number)

def checkProductBacklogs(request, project_id):
	for pbi in PBI.objects.filter(project__id=project_id):
		tasks_F = 0
		tasks_IP = 0
		latest_sprint = None
		task_list = Task.objects.filter(pbi=pbi).order_by('sprint')
		tasks_total = len(task_list)
	
		if tasks_total==0:
			pbi.PBI_status = 'TD'
			pbi.sprint = None
			pbi.save()
			return
	
		for task in task_list:
			latest_sprint = task.sprint	
			if task.task_status=='F':
				tasks_F += 1
			if task.task_status=='IP':
				tasks_IP += 1

		if pbi.project.current_sprint <= latest_sprint.sprint_number: 
			if tasks_F==tasks_total:
				pbi.PBI_status = 'F'
				pbi.sprint = latest_sprint
				pbi.save()
			elif tasks_F==0 and tasks_IP==0:
				pbi.PBI_status = 'TD'
				pbi.sprint = None
				pbi.save()
			else:
				pbi.PBI_status = 'IP'
				pbi.sprint = latest_sprint
				pbi.save()
		else: 
			if tasks_F==tasks_total:
				pbi.PBI_status = 'F'
				pbi.sprint = latest_sprint
				pbi.save()
			else:
				pbi.PBI_status = 'U'
				pbi.sprint = None
				pbi.save()

def sendEmail(request, project_id, user, post):
	from django.core.mail import send_mail
	from django.conf import settings
	project = Project.objects.get(id=project_id)
	subject = 'You have been included in a project in BackTrack!'
	message = 'Project name: %s\n'%project.name + 'Project link: http://127.0.0.1:8000/COMP3297/%s/%s'%(project_id, post)
	email_from = settings.EMAIL_HOST_USER
	recipient_list = [user.email,]
	send_mail( subject, message, email_from, recipient_list )
	messages.success(request, 'Successfully sent email to %s'%user.name)