import json
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from web.models import User, Faculty, Role,Application
from django.shortcuts import redirect
from django.urls import reverse
class MainPage(View):
    def get(self,request):
        faculties = Faculty.objects.all()
        return render(request,"main.html", locals())
    def post(self, request):
        data = json.loads(request.body)
        if data["status"] == "create_user":
                exist_email = User.objects.filter(email=data["email"]).exists()
                if exist_email:
                    return JsonResponse({"status":"exist_account","error":"Аккаунт с таким email вже існує"})
                else:
                    faculty = Faculty.objects.get(faculty=data["faculty"])
                    role = Role.objects.get(role="student")
                    User.objects.create(faculty=faculty, role=role, last_name=data["last_name"],
                                        first_name=data["first_name"], email=data["email"],
                                        password=data["password"])
                    request.session["auth"] = True
                    request.session["email"] = data["email"]
                    return JsonResponse({"status": "created account"})
        elif data["status"] == "check_user":
            exist_user = User.objects.filter(email=data["email"], password=data["password"]).exists()
            if exist_user:
                request.session["auth"] = True
                request.session["email"] = data["email"]
                return JsonResponse({"status": "exist_account"})
            else:
                return JsonResponse({"status": "not_exist_account", "error": "Такого аккаунту не уснує, будь ласка перевірте ще раз"})
        return JsonResponse(data)
class ApplicationsPage(View):
    def get(self, request):
        applications = Application.objects.filter(user__email=request.session["email"])
        return render(request, "adminApplied.html", locals())
    def post(self, request):
        data = json.loads(request.body)
        if data["status"] == "delete application":
            Application.objects.filter(id=data["id"]).delete()
            return JsonResponse({"status":"deleted"})
class ProfilePage(View):
    def get(self, request):
        try:
            if request.session["auth"]:
                return render(request,"adminProfile.html", locals())
            else:
                return redirect(reverse("main"))
        except KeyError:
            return redirect(reverse("main"))
    def post(self, request):
        content_type = request.META.get('HTTP_ACCEPT')
        if content_type == "application/json":
            data = json.loads(request.body)
            if data["status"] == "get_data_user":
                user = User.objects.filter(email=request.session["email"]).values()[0]
                return JsonResponse(user)
        else:
            image = request.FILES.get("photo")
            account = json.loads(request.POST.get("text_data"))
            if image == None:
                User.objects.filter(email=request.session["email"]).update(last_name=account["last_name"],
                                                                           first_name= account["first_name"],
                                                                           email=account["email"],
                                                                           password=account["password"],
                                                                           contact_number=account["contact-phone"]
                                                                           )
                request.session["email"] = account["email"]
                return JsonResponse({"status":"updated"})
            else:
                user = User.objects.filter(email=request.session["email"])[0]
                user.profile_photo = image
                user.last_name = account["last_name"]
                user.first_name = account["first_name"]
                user.email = account["email"]
                user.password = account["password"]
                user.contact_number = account["contact-phone"]
                user.save()
                request.session["email"] = account["email"]
                return JsonResponse({"status": "updated"})
class Logout(View):
    def get(self, request):
        del request.session["auth"]
        del request.session["email"]
        return redirect(reverse('main'))


