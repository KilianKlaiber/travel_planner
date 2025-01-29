from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(
    CustomUser,
)

admin.site.register(
    Destination,
)

admin.site.register(
    Activity,
)

admin.site.register(
    TravelPlan,
)

admin.site.register(
    Comment,
)