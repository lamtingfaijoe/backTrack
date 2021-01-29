from django import forms

class PBIForm(forms.Form):
    def __init__(self, *args,**kwargs):
        project_name = kwargs.pop('project_name')
        super(PBIForm,self).__init__(*args,**kwargs)
        self.fields['Project_name'] = forms.CharField(max_length = 40, initial=project_name)

    Project_name = forms.CharField(max_length = 40)
    PBI_name = forms.CharField(max_length = 200, initial='')
    description = forms.CharField(max_length = 200, initial='')
    est_storypoint = forms.IntegerField()
    priority = forms.IntegerField()
    status = forms.ChoiceField(choices=(
		('TD', 'To Do'),
		('IP', 'In Progress'),
		('F', 'Finished'),
		('U', 'Unfinished'),
		), initial='TD', disabled=True)