from django import forms


class PostForm(forms.Form):
    text_area = forms.CharField(max_length=280, widget=forms.Textarea)
