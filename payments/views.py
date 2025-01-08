from django.shortcuts import get_object_or_404, render, redirect
from django.views.generic import TemplateView
from django.views import View
from django.http import JsonResponse
from .models import Plan, UserSubscription
import stripe
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# Set your secret key to authenticate with Stripe
stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

class PatientMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_patient

    def handle_no_permission(self):
        logger.warning(f"Access denied for user {self.request.user}. Not a patient.")
        return redirect('home')

class ChangePlanView(LoginRequiredMixin, PatientMixin, TemplateView):
    template_name = 'account/plans.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            # Get the current user's subscription
            user_subscription = UserSubscription.objects.get(user=self.request.user)
            current_plan = user_subscription.plan
        except UserSubscription.DoesNotExist:
            current_plan = None

        # Get all plans except the current one
        plans = Plan.objects.exclude(id=current_plan.id) if current_plan else Plan.objects.all()

        context['current_plan'] = current_plan
        context['plans'] = plans
        context['STRIPE_PUBLIC_KEY'] = settings.STRIPE_TEST_PUBLIC_KEY  # Pass Stripe public key to template

        return context

class SwitchPlanView(LoginRequiredMixin, PatientMixin, View):
    def get(self, request, plan_id):
        # Get the current plan and the new plan
        try:
            user_subscription = get_object_or_404(UserSubscription, user=request.user)
            current_plan = user_subscription.plan
        except UserSubscription.DoesNotExist:
            current_plan = None  # Or redirect to a page where the user can select a plan

        new_plan = get_object_or_404(Plan, id=plan_id)

        # Pass the public key to the template
        return render(request, 'account/switch_plan.html', {
            'current_plan': current_plan,
            'new_plan': new_plan,
            'STRIPE_PUBLIC_KEY': settings.STRIPE_TEST_PUBLIC_KEY,  # Pass Stripe public key to template
        })

    def post(self, request, plan_id):
        user_subscription = get_object_or_404(UserSubscription, user=request.user)
        new_plan = get_object_or_404(Plan, id=plan_id)

        # Assuming the payment method is sent via POST form
        payment_method_id = request.POST.get('payment_method_id')

        if not payment_method_id:
            return JsonResponse({'error': 'Payment method ID is missing'}, status=400)

        try:
            # Create a PaymentIntent with the new plan price
            intent = stripe.PaymentIntent.create(
                amount=int(new_plan.price * 100),  # Stripe expects amount in cents
                currency='usd',
                payment_method=payment_method_id,
                confirmation_method='manual',
                confirm=True
            )
        except stripe.error.StripeError as e:
            return JsonResponse({'error': str(e)}, status=400)

        return JsonResponse({
            'client_secret': intent.client_secret
        })

from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views import View
import stripe
import json
from .models import Plan

# Initialize Stripe with the secret key from settings
stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

class ProcessPaymentView(View):
    def post(self, request, plan_id):
        new_plan = get_object_or_404(Plan, id=plan_id)
        print(f"New plan: {new_plan.name}, Price: {new_plan.price}")

        # Parse the payment method ID from the request data
        try:
            data = json.loads(request.body)
            payment_method_id = data.get('payment_method_id')
            print(f"Received payment method ID: {payment_method_id}")
        except json.JSONDecodeError:
            print("Error: Invalid JSON data")
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

        if not payment_method_id and new_plan.price > 0:
            print("Error: Payment method ID is missing")
            return JsonResponse({'error': 'Payment method ID is missing'}, status=400)

        try:
            # If the price is 0, directly switch the plan without creating a payment intent
            if new_plan.price <= 0:
                print("Price is 0, directly switching the plan.")

                # Get the currently logged-in user
                user = request.user.patient  
                print(f"Current user: {user.name}")

                # Update user's plan
                user.usersubscription.plan = new_plan
                print(f"Updating user's plan to: {new_plan.name}")
                user.usersubscription.save()
                user.save()

                return JsonResponse({
                    'message': 'Plan switched successfully without payment!'
                })

            # Proceed with Stripe payment if the price is greater than 0
            payment_intent = stripe.PaymentIntent.create(
                amount=int(new_plan.price * 100),  # in cents
                currency='usd',
                description=f'Switch to {new_plan.name} plan',
                payment_method=payment_method_id,
                automatic_payment_methods={
                    'enabled': True,
                    'allow_redirects': 'never'  # Prevent redirects
                }
            )
            print(f"Payment intent created: {payment_intent.id}, Client secret: {payment_intent.client_secret}")

            # If the payment is successful, update the user's plan
            user = request.user.patient  # Get the currently logged-in user
            print(f"Current user: {user.name}")

            # Update user's plan
            user.usersubscription.plan = new_plan
            print(f"Updating user's plan to: {new_plan.name}")
            user.usersubscription.save()
            user.save()

            return JsonResponse({
                'client_secret': payment_intent.client_secret,
                'message': 'Payment successful, plan updated!'
            })

        except stripe.error.StripeError as e:
            print(f"Stripe error: {str(e)}")
            return JsonResponse({'error': str(e)}, status=400)

        except Exception as e:
            print(f"Error in payment process: {str(e)}")
            return JsonResponse({'error': 'An error occurred during payment process'}, status=500)