from django import forms

class newSprintForm(forms.Form):
    def __init__(self, *args,**kwargs):
        #username = kwargs.pop('username')
        # project_id = kwargs.pop('project_id')
        # project_names = kwargs.pop('project_names')
        #PBI_names = kwargs.pop('PBI_names')
        super(newSprintForm,self).__init__(*args,**kwargs)
        # self.fields['Developer_Name'] = forms.CharField(max_length = 40, initial = username)
        # self.fields['Project_name'] = forms.ChoiceField(choices = project_names)
        #self.fields['PBI_name'] = forms.ChoiceField(choices=PBI_names)
        # self.initial['Project_name'] = str(project_id)

    # Project_Name = forms.ChoiceField()
    sprintNumber = forms.IntegerField()
    capacity     = forms.IntegerField()