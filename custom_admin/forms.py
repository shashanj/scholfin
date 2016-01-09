from django import forms
from scholarships.models import *

class ScholarshipForm(forms.ModelForm):
    class Meta:
        model = scholarship
        fields = '__all__'
        widgets = {'education_field': forms.CheckboxSelectMultiple,
            'education_interest': forms.CheckboxSelectMultiple,
            'education_caste': forms.CheckboxSelectMultiple,
            'education_religion': forms.CheckboxSelectMultiple,
            'education_level': forms.CheckboxSelectMultiple,
            'education_state': forms.CheckboxSelectMultiple,
            'education_abroad': forms.CheckboxSelectMultiple,
            'document_required': forms.CheckboxSelectMultiple,
            'deadline' : forms.SplitDateTimeWidget,
        }