from django.contrib import admin
from .models import User,Branch,BranchAdmin,Course,Subject,Module,Topic
# Register your models here.
admin.site.register(User)
admin.site.register(BranchAdmin)
admin.site.register(Branch)
admin.site.register(Course)
admin.site.register(Subject)
admin.site.register(Module)
admin.site.register(Topic)