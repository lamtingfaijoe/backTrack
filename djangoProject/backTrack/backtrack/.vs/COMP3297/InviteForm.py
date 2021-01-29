from django import forms

class InviteForm(forms.Form):
    def __init__(self, *args,**kwargs):
        project_id = kwargs.pop('project_id')
        developer_id = kwargs.pop('developer_id')
        super(InviteForm,self).__init__(*args,**kwargs)
        self.fields['ID'] = forms.ChoiceField(choices=developer_id)
        
    ID = forms.ChoiceField(initial="None")
