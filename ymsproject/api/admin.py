from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Yard)
admin.site.register(Slot)
admin.site.register(Truck)
admin.site.register(Trailer)
admin.site.register(Container)
admin.site.register(Driver)
admin.site.register(Division)
admin.site.register(Chassis)
# 