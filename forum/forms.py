from django import forms

class PostForm(forms.Form):
    title = forms.CharField(max_length=30)
    content = forms.CharField(max_length=20000, widget=forms.Textarea)
