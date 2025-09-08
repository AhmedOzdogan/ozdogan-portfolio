from django.shortcuts import render
from django.db.models import Prefetch
import os, requests
from decouple import config

from .models import Certificates, CertificateGroups, WorkExperience, Languages

from django.core.mail import send_mail

def index(request):
    return render(request, 'maincvapp/index.html')

def resume(request):

    certificate_groups = (
    CertificateGroups.objects
    .order_by("-date_issued")      # groups sorted newest → oldest
    .prefetch_related("certificates")  # certs come pre-sorted by sort_value
)
    
    experience = WorkExperience.objects.all().order_by('-start_date')
    categories = Languages.categories  # the choices
    skills_by_category = []

    for key, label in categories:
        skills = Languages.objects.filter(category=key)
        if skills.exists():
            skills_by_category.append({
                "label": label,
                "skills": skills
            })

    return render(request, 'maincvapp/resume.html', {'certificate_groups': certificate_groups, 
                                                     'experience': experience,
                                                     'skills_by_category': skills_by_category})
def projects(request):
    return render(request, 'maincvapp/projects.html')

def contact(request):
    captcha_site = config("RECAPTCHA_SITE_KEY", default="")
    captcha_secret = config("RECAPTCHA_SECRET_KEY", default="")

    if request.method == "POST":
        token = request.POST.get("g-recaptcha-response", "")
        if not token:
            return render(request, "maincvapp/contact.html", {
                "captcha": captcha_site, "error": True,
                "error_message": "reCAPTCHA token missing. Please try again."
            })

        r = requests.post("https://www.google.com/recaptcha/api/siteverify", data={
            "secret": captcha_secret,
            "response": token,
            "remoteip": request.META.get("REMOTE_ADDR"),
        })
        result = r.json()
        score = result.get("score", 0)
        action_ok = result.get("action") in (None, "submit")  
        print("reCAPTCHA result:", result)

        if not result.get("success") or score < 0.5 or not action_ok:
            return render(request, "maincvapp/contact.html", {
                "captcha": captcha_site, "error": True,
                "error_message": "reCAPTCHA verification failed. Please try again."
            })

        subject = f"[Portfolio Contact] {request.POST.get('subject','No Subject')}"
        sender  = request.POST.get("email","")
        name    = request.POST.get("name","Anonymous")
        body    = f"From: {name} <{sender}>\n\n{request.POST.get('message','')}"

        send_mail(subject, body, "ahmeddozdogan@gmail.com", ["ahmeddozdogan@gmail.com"], fail_silently=False)

        if sender:
            ack = (
                f"Hello {name},\n\n"
                "Thank you for reaching out! I’ve received your message and will get back to you as soon as possible.\n\n"
                "Best regards,\nAhmed Özdoğan\n📧 Email: ahmeddozdogan@gmail.com\n📞 Phone: +84 353 572 862"
            )
            send_mail("Message received – thank you!", ack, "ahmeddozdogan@gmail.com", [sender], fail_silently=False)

        return render(request, "maincvapp/contact.html", {"captcha": captcha_site, "success": True})

    return render(request, "maincvapp/contact.html", {"captcha": captcha_site})



def details(request, content):
    templates = {
        "schedeye": "maincvapp/details-schedeye.html",
        "restaurant": "maincvapp/details-restaurant.html",
        "bakery": "maincvapp/details-bakery.html",
        "schedule": "maincvapp/details-schedule.html",
    }
    template = templates.get(content)
    if template:
        return render(request, template)
    return render(request, "maincvapp/404.html", status=404)