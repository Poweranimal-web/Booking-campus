import json
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from web.models import User, Faculty, Role
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
        return JsonResponse(data)
class Logout(View):
    def get(self, request):
        del request.session["auth"]
        del request.session["email"]
        return redirect(reverse('main'))


