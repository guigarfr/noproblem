from noproblem.problems.models import Problem,Area,SubArea,UserProfile
from django.contrib import admin

class NotestAdmin(admin.ModelAdmin):
    #fields = ['titulo', 'categoria', 'crea_date']
    list_display = ('title', 'category', 'created_at')
    list_filter = ('created_at',)
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

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