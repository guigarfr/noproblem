from problems.models import Problem,User,NoTest,Test,TestOptions,Area,SubArea,CustomUser
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


class NotestInline(admin.StackedInline):
    model = NoTest
    

class OptionsInline(admin.StackedInline):
    model = TestOptions

class NotestAdmin(admin.ModelAdmin):
    #fields = ['titulo', 'categoria', 'crea_date']
    list_display = ('title', 'category', 'created_at')
    list_filter = ('created_at',)
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)


class TestAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at')
    list_filter = ('created_at',)
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    inlines = [OptionsInline]


class FlatProbAdmin(admin.ModelAdmin):
    fieldsets = (
                 (None, {
                  'fields': ('title','wording')
                  }),
                 ('Classification', {
                  'classes': ('collapse',),
                  'fields': (('subarea', 'points'))
                  }),
                 )



admin.site.register(Problem,NotestAdmin)
admin.site.register(Area)
admin.site.register(SubArea)


admin.site.register(NoTest,NotestAdmin)
admin.site.register(Test,TestAdmin)

# Define an inline admin descriptor for User model
# which acts a bit like a singleton
class UserInline(admin.StackedInline):
    model = CustomUser
    can_delete = False
    verbose_name_plural = 'users'


# Define a new User admin
class UserAdmin(UserAdmin):
    inlines = (UserInline, )

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
