from django import forms

class PostForm(forms.Form):
    title = forms.CharField(max_length=500, widget=forms.TextInput(attrs={'size':150}))
    content = forms.CharField(max_length=20000, widget=forms.Textarea(attrs={'rows':25, 'cols':200}))
