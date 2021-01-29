from django import template

register = template.Library()

@register.filter
def index(value, i):
	return value[i]

@register.filter
def total_effort(Tasks):
	effort = 0
	for task in Tasks:
		effort += task.estimated_effort
	return effort

@register.filter
def remain_effort(Tasks):
	effort = 0
	for task in Tasks:
		if task.task_status=='F':
			effort += task.estimated_effort
	return effort

@register.filter
def check_PBI_status(pbi, task_of_pbi):
	tasks_finished = 0
	tasks_started = 0
	tasks_total = len(task_of_pbi[pbi.priority])
	latest_sprint = None
	
	if tasks_total==0:
		pbi.pbi_status = 'TD'
		pbi.sprint = None
		pbi.save()
		return pbi.get_PBI_status_display()
	
	for task in task_of_pbi[pbi.priority] :
		latest_sprint = task.sprint	
		if task.task_status=='F':
			tasks_finished += 1
		if task.task_status=='IP':
			tasks_started += 1

	if pbi.project.current_sprint <= latest_sprint.sprint_number: 
		if tasks_finished==tasks_total:
			pbi.pbi_status = 'F'
			pbi.sprint = latest_sprint
			pbi.save()
		elif tasks_finished==0 and tasks_started==0:
			pbi.pbi_status = 'TD'
			pbi.sprint = None
			pbi.save()
		else:
			pbi.pbi_status = 'IP'
			pbi.sprint = latest_sprint
			pbi.save()
	else: 
		if tasks_finished==tasks_total:
			pbi.pbi_status = 'F'
			pbi.sprint = latest_sprint
			pbi.save()
		else:
			pbi.pbi_status = 'U'
			pbi.sprint = None
			pbi.save()

	return pbi.get_PBI_status_display()

