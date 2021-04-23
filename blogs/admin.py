from django.contrib import admin
from authentication.models import *
from blogs.models import *
# Register your models here.
myModels = [Tags, Blogs, Comments, Likes, Activity]

admin.site.register(myModels)
