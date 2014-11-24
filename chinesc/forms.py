from django import forms

class CodeForm(forms.Form):
    user_code = forms.CharField(
        label='Your Code',
        widget=forms.Textarea(attrs={'rows':24, 'cols':80})
    )
