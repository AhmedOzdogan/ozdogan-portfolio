from django.shortcuts import render
from django.db.models import Prefetch
import os, requests
from dotenv import load_dotenv

from .models import Certificates, CertificateGroups, WorkExperience, Languages

load_dotenv()

def index(request):
    return render(request, 'maincvapp/index.html')

def resume(request):

    certificate_groups = (
    CertificateGroups.objects
    .order_by("-date_issued")      # groups sorted newest → oldest
    .prefetch_related("certificates")  # certs come pre-sorted by sort_value
)



    experience = WorkExperience.objects.all().order_by('-start_date')
    languages = Languages.objects.all()

    return render(request, 'maincvapp/resume.html', {'certificate_groups': certificate_groups, 
                                                     'experience': experience,
                                                     'languages': languages})
def projects(request):
    url = "https://api.github.com/repos/AhmedOzdogan/ozdogan-portfolio/contents"
    token = os.getenv("GITHUB_TOKEN")

    headers = {"Authorization": f"Bearer {token}"}
    r = requests.get(url, headers=headers)
    contents = r.json()
    
    projects = []
    intro_text = ""

    for item in contents:
        # Main README.md → portfolio intro
        if item["name"].lower() == "readme.md":
            readme = requests.get(item["download_url"]).text
            intro_text = readme[:600] + "..."
            intro_url = item["html_url"]

        # project folders
        elif item["type"] == "dir":
            sub = requests.get(item["url"], headers=headers).json()
            readme_file = next((f for f in sub if f["name"].lower() == "readme.md"), None)
            if readme_file:
                readme_text = requests.get(readme_file["download_url"]).text
                projects.append({
                    "name": item["name"],
                    "readme": readme_text[:600] + "...",
                    "url": readme_file["html_url"]
                })

        # Handle submodules
        elif item["type"] == "file" and item["download_url"] is None:
            repo_name = item["name"]
            readme_res = requests.get(
                f"https://api.github.com/repos/AhmedOzdogan/{repo_name}/readme",
                headers=headers
            ).json()

            if "download_url" in readme_res and readme_res["download_url"]:
                text = requests.get(readme_res["download_url"]).text
                projects.append({
                    "name": repo_name,
                    "readme": text[:600] + "...",
                    "url": readme_res["html_url"]
                })

    return render(request, "maincvapp/projects.html", {
        "intro_text": intro_text,
        "intro_url": intro_url,
        "projects": projects
    })