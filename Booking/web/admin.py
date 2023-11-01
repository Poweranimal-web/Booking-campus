from django.contrib import admin
from web.models import User,Role,Faculty,Campus,Floor,Room,Application


class UserAdmin(admin.ModelAdmin):
    list_display = ("email","role","faculty","contact_number")
    list_filter = ("role","faculty")
class RoomAdmin(admin.ModelAdmin):
    list_display = ("number","floor","campus")
    list_filter = ("floor","campus","num_beds")
class FloorAdmin(admin.ModelAdmin):
    list_display = ("number", "campus")
    list_filter = ("campus",)
class CampusAdmin(admin.ModelAdmin):
    list_display = ("name", "number","address", "head","floors","faculty")
    list_filter = ("faculty",)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("number_application","status","date_create_application",
                    "date_handle_application","room","user")
    list_filter = ("status",)
admin.site.register(User, UserAdmin)
admin.site.register(Role)
admin.site.register(Faculty)
admin.site.register(Campus,CampusAdmin)
admin.site.register(Floor, FloorAdmin)
admin.site.register(Room, RoomAdmin)
admin.site.register(Application,ApplicationAdmin)

