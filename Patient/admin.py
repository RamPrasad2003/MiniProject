from django.contrib import admin
from .models import *


admin.site.register(Patient)
admin.site.register(Person)
admin.site.register(Medicine)
admin.site.register(Location)