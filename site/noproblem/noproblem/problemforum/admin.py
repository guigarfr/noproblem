from noproblem.problemforum.models import Thread, Post
from noproblem.problems.models import Problem
from django.contrib import admin


### Admin

# class ForumAdmin(admin.ModelAdmin):
#     pass
# 
class ThreadAdmin(admin.ModelAdmin):
    list_display = ["prob"]
    list_filter = ["prob__title"]

class PostAdmin(admin.ModelAdmin):
    search_fields = ["creator"]
    list_display = ["creator", "created"]

admin.site.register(Post, PostAdmin)
admin.site.register(Thread, ThreadAdmin)