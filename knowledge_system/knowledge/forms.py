from django import forms
from .models import Knowledge

class KnowledgeForm(forms.ModelForm):

    class Meta:
        model = Knowledge
        fields = ('titile', 'content',)