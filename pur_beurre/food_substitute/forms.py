from django import forms

class CategoryForm(forms.Form):
    category = forms.CharField(label='categorie', max_length=100)
