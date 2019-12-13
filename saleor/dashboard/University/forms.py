from django import forms
from ...University.models import University,CollegeRepr

class CreateUniversity(forms.ModelForm):
    class Meta():
        model = University
        fields = '__all__'