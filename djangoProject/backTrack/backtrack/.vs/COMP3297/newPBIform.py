from django import forms

class PBIForm(forms.Form):
    def __init__(self, *args,**kwargs):
        project_id = kwargs.pop('project_id')
        project_names = kwargs.pop('project_names')
        super(PBIForm,self).__init__(*args,**kwargs)
        self.fields['Project_name'] = forms.ChoiceField(choices=project_names)
        self.initial['Project_name'] = str(project_id)


    Project_name = forms.ChoiceField() 
    PBI_name = forms.CharField(max_length = 200, initial='')
    description = forms.CharField(max_length = 200, initial='')
    est_storypoint = forms.IntegerField()
    priority = forms.IntegerField()
    status = forms.ChoiceField(choices=(
		('TD', 'To Do'),
		('IP', 'In Progress'),
		('F', 'Finished'),
		('U', 'Unfinished'),
		), initial='TD')