from django import forms

from projects.models import Project


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = (
            'title',
            'outline',
            'participants',
            'content',
            'cover_photo',
        )


class OperatorProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'
