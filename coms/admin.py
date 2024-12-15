from django.contrib import admin
from .models import Ad,MedicalAdvice



# General Custom Admin
class AdAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'image', 'created_at')
    search_fields = ('title', 'content', 'created_by', 'created_at')

    # For viewing/editing details
    fieldsets = (
        (None, {'fields': ('title', 'content', 'image')}),
    )

    # For creating new
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('title', 'content', 'image')}
        ),
    )

# Register Models in Admin Site
admin.site.register(Ad, AdAdmin)    