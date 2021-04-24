from django import forms

class CommentForm(forms.Form):
    name = forms.CharField(label='Ваше имя', max_length=100)
    text = forms.CharField(label='Текст комментария', max_length=500)