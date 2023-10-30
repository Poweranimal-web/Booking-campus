import json
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from web.models import User, Faculty, Role,Application,Campus, Floor, Room
from django.shortcuts import redirect
from django.urls import reverse
import uuid
import random
class MainPage(View):
    def get(self,request):
        faculties = Faculty.objects.all()
        campuses = Campus.objects.all()
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
                    request.session["comendant"] = False
                    return JsonResponse({"status": "created account"})
        elif data["status"] == "check_user":
            exist_user = User.objects.filter(email=data["email"], password=data["password"]).exists()
            if exist_user:
                user = User.objects.get(email=data["email"], password=data["password"])
                if str(user.role) == "student":
                    request.session["auth"] = True
                    request.session["email"] = data["email"]
                    request.session["comendant"] = False
                else:
                    request.session["auth"] = True
                    request.session["email"] = data["email"]
                    request.session["comendant"] = True
                return JsonResponse({"status": "exist_account"})
            else:
                return JsonResponse({"status": "not_exist_account", "error": "Такого аккаунту не уснує, будь ласка перевірте ще раз"})
        return JsonResponse(data)
class ApplicationsPage(View):
    def get(self, request):
        try:
            if request.session["auth"]:
                if request.session["comendant"]:
                    applications = Application.objects.filter(status="На розгляді")
                    return render(request, "adminAccept.html", locals())
                else:
                    applications = Application.objects.filter(user__email=request.session["email"])
                    return render(request, "adminApplied.html", locals())
            else:
                return redirect(reverse("main"))
        except KeyError:
            return redirect(reverse("main"))
    def post(self, request):
        data = json.loads(request.body)
        if data["status"] == "delete application":
            app = Application.objects.filter(id=data["id"]).values()[0]
            room = Room.objects.get(id=app["room_id"])
            room.taken_beds = room.taken_beds - 1
            room.save()
            Application.objects.filter(id=data["id"]).delete()
            return JsonResponse({"status":"deleted"})
        elif data["status"] == "accept application":
            Application.objects.filter(id=data["id"]).update(status="Прийнято")
            return JsonResponse({"status": "accepted"})
        elif data["status"] == "decline application":
            app = Application.objects.filter(id=data["id"]).values()[0]
            Application.objects.filter(id=data["id"]).update(status="Відмовлено")
            room = Room.objects.get(id=app["room_id"])
            room.taken_beds = room.taken_beds - 1
            room.save()
            return JsonResponse({"status": "declined"})
class ApplyPage(View):
    def get(self, request):
        try:
            if request.session["auth"]:
                return render(request, "adminApply.html", locals())
            else:
                return redirect(reverse("main"))
        except KeyError:
            return redirect(reverse("main"))
class ApplyFloorPage(View):
    def get(self, request,pk):
        try:
            if request.session["auth"]:
                campus = Campus.objects.get(id=pk)
                floors = Floor.objects.filter(campus=campus)
                return render(request, "adminFloor.html", locals())
            else:
                return redirect(reverse("main"))
        except KeyError:
            return redirect(reverse("main"))
    def post(self, request, pk):
        data = json.loads(request.body)
        if data["status"] == "get_rooms":
            campus = Campus.objects.get(id=pk)
            floor = Floor.objects.get(campus=campus,number=int(data["floor_num"]))
            rooms = list(Room.objects.filter(floor=floor).values())
            return JsonResponse(rooms,safe=False)
        elif data["status"] == "send_request":
            room = Room.objects.get(id=data["id_room"])
            user = User.objects.get(email=request.session["email"])
            applications = Application.objects.filter(user__email=request.session["email"])
            exist_room_app = Application.objects.filter(room=room,user=user).exists()
            if exist_room_app:
                room_app = Application.objects.get(room=room, user=user)
                if room_app.status == "Відмовлено":
                    room_app.status = "На розгляді"
                    room.taken_beds = room.taken_beds + 1
                    room_app.save()
                    room.save()
                    return JsonResponse({"status": "saved request"})
                if room_app.status == "На розгляді" or room_app.status == "Прийнято":
                    return JsonResponse({"status": "not saved request", "error": "Ви вже надсилали запит на цю кімнату"})

            else:
                if len(applications) >= 5:
                    return JsonResponse({"status": "not saved request", "error": "Ліміт запитів перевищує необхідний"})
                else:
                    if user.contact_number:
                        Application.objects.create(user=user, room=room,
                                                   status="На розгляді",number_application=str(uuid.uuid4())[0:5])
                        room.taken_beds = room.taken_beds + 1
                        room.save()
                        return JsonResponse({"status": "saved request"})
                    else:
                        return JsonResponse({"status": "not saved request","error":"Потрібен контактний номер"})
class ListCampusPage(View):
    def get(self, request):
        try:
            if request.session["auth"]:
                user = User.objects.filter(email=request.session["email"]).values()[0]
                faculty = Faculty.objects.get(id=user["faculty_id"])
                campuses = Campus.objects.filter(faculty=faculty)
                return render(request,"adminAccept2.html", locals())
            else:
                return redirect(reverse("main"))
        except KeyError:
            return redirect(reverse("main"))
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
        del request.session["comendant"]
        return redirect(reverse('main'))
class DetailPage(View):
    def get(self,request,pk):
        campus = Campus.objects.get(id=pk)
        return render(request, "campusDetail.html",locals())
class GenData(View):
    def get(self,request):
        campuses = Campus.objects.all().values()
        for campuse in campuses:
            floors = campuse["floors"]
            camp = Campus.objects.get(id=campuse["id"])
            for floor in range(floors):
                fl = Floor(number=floor, campus=camp)
                fl.save()
                for i in range(20):
                    take = random.randint(1, 4)
                    amount = random.randint(5, 8)
                    rm = Room(number=i + 1, taken_beds=take, num_beds=amount, floor=fl, campus=camp)
                    rm.save()
        return redirect(reverse('main'))


