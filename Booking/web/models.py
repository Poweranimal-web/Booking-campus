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
    last_name = models.CharField(max_length=200)
    first_name = models.CharField(max_length=200)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    role = models.ForeignKey(Role,on_delete=models.CASCADE)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
# class Campus(models.Model):
#     name = models.CharField(max_length=200)
#     number = models.IntegerField()
#     detail_text = models.TextField()
#     floors = models.IntegerField()
# class Floor(models.Model):
#     number = models.IntegerField()
#     campus = models.ForeignKey(Campus, on_delete=models.CASCADE)
# class Gender(models.Model):
#     name = models.CharField(max_length=35)
#     def __str__(self):
#         return self.name
# class Room(models.Model):
#     number = models.IntegerField()
#     taken_beds = models.IntegerField()
#     num_beds = models.IntegerField()
#     gender = models.ForeignKey(Gender, on_delete=models.CASCADE)
#     floor = models.ForeignKey(Floor, on_delete=models.CASCADE)
#     campus = models.ForeignKey(Campus, on_delete=models.CASCADE)






