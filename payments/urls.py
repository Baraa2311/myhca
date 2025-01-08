from django.urls import path
from .views import ChangePlanView, SwitchPlanView, ProcessPaymentView

urlpatterns = [
    # Path to view available plans (without switching)
    path('change-plan/', ChangePlanView.as_view(), name='change_plan'),

    # Path to switch to a specific plan
    path('switch-plan/<int:plan_id>/', SwitchPlanView.as_view(), name='switch_plan'),

    # Path to process the payment for a specific plan
    path('process-payment/<int:plan_id>/', ProcessPaymentView.as_view(), name='process_payment'),
]