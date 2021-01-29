from django import forms

class InviteDeveloperForm(forms.Form):
    def __init__(self, *args,**kwargs):
        project_id = kwargs.pop('project_id')
        developer_id = kwargs.pop('developer_id')
        super(InviteDeveloperForm,self).__init__(*args,**kwargs)
        self.fields['ID'] = forms.ChoiceField(choices=developer_id)
        
    ID = forms.ChoiceField(initial="None")

class InviteManagerForm(forms.Form):
    def __init__(self, *args,**kwargs):
        project_id = kwargs.pop('project_id')
        manager_id = kwargs.pop('manager_id')
        super(InviteManagerForm,self).__init__(*args,**kwargs)
        self.fields['ID'] = forms.ChoiceField(choices=manager_id)
        
    ID = forms.ChoiceField(initial="None")