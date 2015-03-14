from django import forms

from projects.models import Project


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = (
            'title',
            'outline',
            'members',
            'content',
            'cover_photo',
        )
        widgets = {
            'members': forms.CheckboxSelectMultiple(),
        }


class OperatorProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
        widgets = {
            'members': forms.CheckboxSelectMultiple(),
        }
