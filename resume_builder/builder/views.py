from django.template import loader
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import (ResumeForm, ExperienceForm, EducationForm, CertificateForm, SkillForm,
                    ExperienceFormSet, EducationFormSet, CertificateFormSet, SkillFormSet)
from .forms import CreateUserForm
from django.http import HttpResponse
from weasyprint import HTML, CSS
from .models import Resume
import os
from resume_builder.settings import BASE_DIR
import random
from email import message
import razorpay
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

def home(request):
    template = loader.get_template('home.html')
    return HttpResponse(template.render(request=request))

def login_user(request):
    if request.user.is_authenticated:
        return redirect("/profile")
    
    if request.method == "GET":
        return render(request, "login.html")
    else:
        username = request.POST["uname"]
        passw = request.POST["upass"]
        #print(username,password)
        user = authenticate(request, username=username, password=passw)
        if user is not None:
            login(request, user)
            request.session['uname'] = username
            print("Logged in successfully")
            messages.success(request, "Logged in successfully")
            return redirect("/profile")
        else:
            messages.error(request,"there was an error.Try again")
            return redirect("/login_user")
        
def logout_user(req):
    try:
        logout(req)
        del req.sessiom['uname']
        messages.success(req, "you have logged out successfully")
        return redirect("/login_user")
    except:
        logout(req)
        messages.success(req,"You have Logged out successfully")
        return redirect("/login_user")

def register(request):
    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            print("User created successfully")
            return redirect("/login_user")
        else:
            messages.error(request, "Your username or password format is invalid")
    context = {'form' : form}
    return render(request, "register.html", context)


def profile(request):
    template = loader.get_template('profile.html')
    return HttpResponse(template.render(request=request))

@login_required
def editor(request):
    template_choice = request.session.get('template_choice')
    if not template_choice:
        return redirect('choose_template')
    
    if template_choice == 'template1':
        htmltemplate = 'editor1.html'
    else:
        htmltemplate = 'editor2.html'
        
    if request.method == 'POST':
        resume_form = ResumeForm(request.POST)
        experience_formset = ExperienceFormSet(request.POST, prefix='exp')
        education_formset = EducationFormSet(request.POST, prefix='edu')
        certificate_formset = CertificateFormSet(request.POST, prefix='cert')
        skill_formset = SkillFormSet(request.POST, prefix='skill')

        if resume_form.is_valid():
            resume = resume_form.save()  # Save the main resume form and get the instance

            # Now handle the formsets
            if all([experience_formset.is_valid(), education_formset.is_valid(),
                    certificate_formset.is_valid(), skill_formset.is_valid()]):
                # Save Experience data
                for form in experience_formset:
                    if form.is_valid() and form.has_changed():
                        experience = form.save(commit=False)
                        experience.resume = resume
                        experience.save()

                # Repeat the process for other formsets
                for form in education_formset:
                    if form.is_valid() and form.has_changed():
                        education = form.save(commit=False)
                        education.resume = resume
                        education.save()

                for form in certificate_formset:
                    if form.is_valid() and form.has_changed():
                        certificate = form.save(commit=False)
                        certificate.resume = resume
                        certificate.save()

                for form in skill_formset:
                    if form.is_valid() and form.has_changed():
                        skill = form.save(commit=False)
                        skill.resume = resume
                        skill.save()

                # After saving everything, redirect
                return generate_resume(request, resume_form, experience_formset,
                                        education_formset, certificate_formset, skill_formset, htmltemplate)
        
        # If some formsets are not valid, re-render the page with all forms and formsets
        return render(request, htmltemplate, {
            'resume_form': resume_form,
            'experience_formset': experience_formset,
            'education_formset': education_formset,
            'certificate_formset': certificate_formset,
            'skill_formset': skill_formset
        })

    else:
        # GET request, so create empty forms and formsets
        resume_form = ResumeForm()
        experience_formset = ExperienceFormSet(prefix='exp')
        education_formset = EducationFormSet(prefix='edu')
        certificate_formset = CertificateFormSet(prefix='cert')
        skill_formset = SkillFormSet(prefix='skill')
        return render(request, htmltemplate, {
            'resume_form': resume_form,
            'experience_formset': experience_formset,
            'education_formset': education_formset,
            'certificate_formset': certificate_formset,
            'skill_formset': skill_formset
        })

def generate_resume(request, resume_form, experience_formset, education_formset, certificate_formset, skill_formset, htmltemplate):
    # Extract cleaned data from forms
    personal_info = resume_form.cleaned_data
    experiences = experience_formset.cleaned_data
    educations = education_formset.cleaned_data
    certificates = certificate_formset.cleaned_data
    skills = skill_formset.cleaned_data

    parts = personal_info.get('full_name', '').split()
    initials = ''.join(part[0].upper() for part in parts)

    context = {
        'personal_info': personal_info,
        'experiences': experiences,
        'educations': educations,
        'certificates': certificates,
        'skills': skills,
        'initials': initials
    }

    template_choice = request.session.get('template_choice')
    if template_choice == 'template1':
        template = 'resume_template1.html'
        css = 'builder/static/css/resume-template1.css'
    else:
        template = 'resume_template2.html'
        css = 'builder/static/css/resume-template2.css'

    try:
        html_string = loader.render_to_string(template, context)
        css_file = os.path.join(BASE_DIR, css)
        with open(css_file, 'r') as f:
            css = CSS(string=f.read())
    
        rendered_html = HTML(string=html_string, base_url=request.build_absolute_uri())
        rendered_html.write_pdf(os.path.join(BASE_DIR, 'resume.pdf'), stylesheets=[css])

        oid =random.randrange(1000,9999)
        oid=str(oid)
        amount=29900
        client = razorpay.Client(auth=("####","####"))

        data = { "amount": amount, "currency": "INR", "receipt": oid }
        payment = client.order.create(data=data)
        context = {}
        context['data'] = payment
        return render(request, "payment.html", context)
    except:
        message.error(request, "Resume creation failed. Please try again")
        return render(request, htmltemplate, {
            'resume_form': resume_form,
            'experience_formset': experience_formset,
            'education_formset': education_formset,
            'certificate_formset': certificate_formset,
            'skill_formset': skill_formset
        })
    
def payment_success(request):
    resume_file = os.path.join(BASE_DIR, 'resume.pdf')
    subject = "Your resume from Quick Resume"
    body = "Please find attached your resume."
    from_email = settings.EMAIL_HOST_USER
    to_email = ["##@gmail.com"]
    # Assuming 'resume_file' is the path to a file on your system.

    # Create an email message object
    email = EmailMessage(
        subject,
        body,
        from_email,
        to_email
    )
    
    # Attach a file
    email.attach_file(resume_file)

    # Send the email
    email.send()

    return render(request, "payment_success.html")

@login_required
def choose_template(request):
    if request.method == 'POST':
        template_choice = request.POST.get('template')
        request.session['template_choice'] = template_choice
        return redirect('editor')

    return render(request, 'choose_template.html')