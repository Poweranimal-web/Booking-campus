from django.db import models
class Role(models.Model):
    role = models.CharField(max_length=150)
    def __str__(self):
        return self.role
class Faculty(models.Model):
    faculty = models.CharField(max_length=300)
    def __str__(self):
        return self.faculty
class User(models.Model):
    profile_photo = models.ImageField(upload_to="photo/")
    last_name = models.CharField(max_length=200)
    first_name = models.CharField(max_length=200)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    role = models.ForeignKey(Role,on_delete=models.CASCADE)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    contact_number = models.CharField(max_length=200)
    def __str__(self):
        return self.email
class Campus(models.Model):
    name = models.CharField(max_length=200)
    number = models.IntegerField()
    detail_text = models.TextField()
    address = models.CharField(max_length=200)
    contact_number = models.CharField(max_length=200)
    head = models.CharField(max_length=200)
    price = models.CharField(max_length=200)
    floors = models.IntegerField()
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    def __str__(self):
        return "{name} {num}".format(name=self.name,num=self.number)
class Floor(models.Model):
    number = models.IntegerField()
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE)
    def __str__(self):
        return "Поверх №{num} Гур №{cump}".format(num=self.number,cump=self.campus.number)
class Room(models.Model):
    number = models.IntegerField()
    taken_beds = models.IntegerField()
    num_beds = models.IntegerField()
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE)
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE)
    def __str__(self):
        return "Кімната №{num}".format(num=self.number)
class Application(models.Model):
    number_application = models.CharField(max_length=50)
    status = models.CharField(max_length=100)
    date_create_application = models.DateField(auto_now_add=True, auto_now=False)
    date_handle_application = models.DateField(auto_now_add=False, auto_now=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, blank=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True)






