from django.contrib import admin
from .models import Ad, MedicalAdvice


# Ad Admin Configuration
class AdAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'created_at', 'image')  # What fields to show in the list view
    list_filter = ('created_by', 'created_at')  # Filters to show in the sidebar
    search_fields = ('title', 'content')  # Fields to search by in the admin interface
    ordering = ('-created_at',)  # Order by creation date, descending
    exclude = ('created_by',)  # Exclude the created_by field from the form

    def save_model(self, request, obj, form, change):
        if not change or not obj.created_by:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)






# MedicalAdvice Admin Configuration
class MedicalAdviceAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'created_at', 'advice', 'image')  # What fields to show in the list view
    list_filter = ('created_by', 'created_at')  # Filters to show in the sidebar
    search_fields = ('title', 'advice')  # Fields to search by in the admin interface
    ordering = ('-created_at',)  # Order by creation date, descending

admin.site.register(MedicalAdvice, MedicalAdviceAdmin)
admin.site.register(Ad, AdAdmin)