from django.contrib import admin
from .models import Location,Review,FeedBack,Visited
# Register your models here.
admin.site.register(Location)
admin.site.register(Review)
admin.site.register(FeedBack)
admin.site.register(Visited)
