from django import forms

class ProjectForm(forms.Form):
	def __init__(self, *args,**kwargs):
		username = kwargs.pop('username')
		super(ProjectForm,self).__init__(*args,**kwargs)
		self.fields['Name_of_the_owner'] = forms.CharField(max_length = 40, initial=username, disabled=True)

	Project_Name = forms.CharField(max_length=40,initial='')
	Name_of_the_owner = forms.CharField(max_length=40,initial='')