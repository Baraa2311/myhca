from django.contrib import admin
from .models import Plan, UserSubscription
from accounts.models import Patient  # Import Patient model for UserSubscription

class PlanAdmin(admin.ModelAdmin):
    # Display fields for Plan in the admin list view
    list_display = ('name', 'price', 'data_limit', 'duration')
    
    # Enable searching by name and price
    search_fields = ('name', 'price')
    
    # Add filter options by plan duration
    list_filter = ('duration',)

# Register the Plan model with PlanAdmin settings
admin.site.register(Plan, PlanAdmin)

class UserSubscriptionAdmin(admin.ModelAdmin):
    # Display fields for UserSubscription in the admin list view
    list_display = ('user', 'plan', 'data_used', 'plan_start_date', 'plan_end_date', 'active')
    
    # Enable searching by patient username and plan name
    search_fields = ('user__username', 'plan__name')
    
    # Add filter options by active status and plan
    list_filter = ('active', 'plan')

    # Display the full name of the patient (user)
    def user(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"

    # Allow sorting by patient name in the admin list
    user.admin_order_field = 'user'
    
    # Rename the user field to 'Patient' for better clarity
    user.short_description = 'Patient'

# Register the UserSubscription model with UserSubscriptionAdmin settings
admin.site.register(UserSubscription, UserSubscriptionAdmin)