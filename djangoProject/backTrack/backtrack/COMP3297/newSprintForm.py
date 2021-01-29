from django import forms

class newSprintForm(forms.Form):
    def __init__(self, *args,**kwargs):
        total_sprint = kwargs.pop('total_spirnt')
        # project_id = kwargs.pop('project_id')
        # project_names = kwargs.pop('project_names')
        # PBI_names = kwargs.pop('PBI_names')
        super(newSprintForm,self).__init__(*args,**kwargs)
        self.fields['sprintNumber'] = forms.IntegerField(initial=total_sprint+1, disabled = True)
        # self.fields['Project_name'] = forms.ChoiceField(choices = project_names)
        # self.fields['PBI_name'] = forms.ChoiceField(choices=PBI_names)
        # self.initial['Project_name'] = str(project_id)

    # Project_Name = forms.ChoiceField()
    sprintNumber = forms.IntegerField(disabled=True)
    capacity     = forms.IntegerField()