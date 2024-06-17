from django import forms
from .models import Resume, Experience, Education, Certificate, Skill
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['full_name', 'job_title', 'email', 'phone_number', 'address', 'github', 'linkedin', 'professional_summary']

class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ['title', 'company', 'start_date', 'end_date', 'description']

ExperienceFormSet = forms.inlineformset_factory(Resume, Experience, form=ExperienceForm, extra=1)

class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['degree', 'major', 'school', 'start_date', 'end_date']

EducationFormSet = forms.inlineformset_factory(Resume, Education, form=EducationForm, extra=1)

class CertificateForm(forms.ModelForm):
    class Meta:
        model = Certificate
        fields = ['certificate_name', 'issuing_organization', 'issue_date']

CertificateFormSet = forms.inlineformset_factory(Resume, Certificate, form=CertificateForm, extra=1)

class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ['skill_name']

SkillFormSet = forms.inlineformset_factory(Resume, Skill, form=SkillForm, extra=1)

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["first_name","last_name","username", "email", "password1", "password2"]