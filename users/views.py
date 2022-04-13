from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, FormView, CreateView
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

import json
User = get_user_model()
# from .models import User

from .forms import (
	PhoneNumberForm,
	ConfirmationForm,
	SignUpForm,

	LoginForm,

	PasswordResetPhonenumberForm,
	PasswordResetVerificationForm,
	PasswordResetNewpasswordForm,

	ChangePasswordForm,

)
from .send_sms import send_sms
from .confirmation_code_generator import code_generator
from .models import CustomToken
from .session_key import current_user_session_id
from .client_ip import get_client_ip
from product.models import Product


def check_valid_token():
	print('check_valid_token is working')
	obj_list = CustomToken.objects.all()
	for obj in obj_list:
		obj.check_valid_token
	return None

class PhoneNumberView(View):
	template_name='registration/phonenumber-view.html'
	
	def get(self, request, *args, **kwargs):
		'''
		check all objects with check_valid_token property in CustomToken, 
		if object created time longer than 5 minut it will be deleted.
		'''
		check_valid_token() 
		'-----------------'
		form = PhoneNumberForm()
		context={'form':form}
		return render(request, self.template_name, context)

	def post(self, request, *args, **kwargs):
		'''
		check all objects with check_valid_token property in CustomToken, 
		if object created time longer than 5 minut it will be deleted.
		'''
		check_valid_token() 
		'-----------------'
		client_ip = get_client_ip(request) # return current user ip address
		session_key = current_user_session_id(request) # return current user session id

		success_msg = "Confirmation code sent to your mobile number. The confirmation code is valid for 5 minutes."
		
		if request.method=='POST':
			form = PhoneNumberForm(request.POST)
			if form.is_valid():
				phone_number = form.cleaned_data['phone_number']

				confirmation_code = code_generator()
				status = send_sms(phone_number, confirmation_code)

				custom_token, created = CustomToken.objects.get_or_create( phone_number=phone_number, client_ip=client_ip)

				if created:
					custom_token.confirmation_code = confirmation_code
					custom_token.save()
				else:
					custom_token.delete()
					custom_token = CustomToken.objects.create(
						phone_number=phone_number, 
						confirmation_code=confirmation_code,
						client_ip=client_ip
					)
					
				if status['status'] == 'waiting':
					messages.success(request, _(success_msg))
					return redirect('users:phone-verification', custom_token.key)
				else:
					messages.error(request, _("Something went wrong, try again"))
					context={'form':form}
					return render(request, self.template_name, context)
		context={'form':form}
		return render(request, self.template_name, context)


class PhoneNumberVerificationView(View):
	template_name = 'registration/phonenumber-confirmation-view.html'
	
	def get(self, request, key, *args, **kwargs):
		'''
		check all objects with check_valid_token property in CustomToken, 
		if object created time longer than 5 minut it will be deleted.
		'''
		check_valid_token() 
		'-----------------'

		client_ip = get_client_ip(request) # return current user ip address
		session_key = current_user_session_id(request) # return current user session id
		try:
			custom_token = CustomToken.objects.get(
				key         = key, 
				client_ip   = client_ip,
				# session_key = session_key,
			)
		except:
			messages.error(request, _("Something went wrong or confirmation code valid time is expired"))
			return redirect('users:phone-number-view')
		form = ConfirmationForm()
		context={'form': form, 'phone_number': custom_token.phone_number}
		return render(request, self.template_name, context)

	def post(self, request, key, *args, **kwargs):
		'''
		check all objects with check_valid_token property in CustomToken, 
		if object created time longer than 5 minut it will be deleted.
		'''
		check_valid_token() 
		'-----------------'

		client_ip = get_client_ip(request) # return current user ip address
		session_key = current_user_session_id(request) # return current user session id
		try:
			custom_token = CustomToken.objects.get(
				key         = key, 
				client_ip   = client_ip,
				# session_key = session_key,
			)
		except:
			messages.warning(request, _("Confirmation code valid time is expired."))
			return redirect('users:phone-number-view')
			
		if request.method == 'POST':
			form = ConfirmationForm(request.POST)
			if form.is_valid():
				confirmation_code = form.cleaned_data['confirmation_code']
				print(int(confirmation_code), custom_token.confirmation_code)
				if int(confirmation_code) == custom_token.confirmation_code and custom_token.check_valid_token:
					phone_number = custom_token.phone_number
					custom_token.delete()
					custom_token = CustomToken.objects.create(
						phone_number = phone_number, 
						client_ip    = client_ip,
						# session_key  = session_key,
					)
					messages.success(request, _('Phone number successfully confirmed, now you can create an account.'))
					return redirect('users:signup-view', custom_token.key)
				else:
					messages.error(request, _('Password didn\'t match :(, \nOr confiramtion code expired' ))
					
		context={'phone_number': custom_token.phone_number, 'form':form}
		return render(request, self.template_name, context)


class SignUpView(View):
	template_name = "registration/create-account-view.html"

	def get(self, request, key, *args, **kwargs):
		'''
		check all objects with check_valid_token property in CustomToken, 
		if object created time longer than 5 minut it will be deleted.
		'''
		check_valid_token() 
		'-----------------'

		form=SignUpForm()
		context = {}
		
		client_ip = get_client_ip(request) # return current user ip address
		session_key = current_user_session_id(request) # return current user session id
		try:
			custom_token = CustomToken.objects.get(
				key         = key, 
				client_ip   = client_ip,
			)
			context['phone_number'] = custom_token.phone_number	
		except:
			return redirect('users:phone-number-view')
		context['form'] = form
		return render(request, self.template_name, context)
	
	def post(self, request, key, *args, **kwargs):
		client_ip = get_client_ip(request) # return current user ip address
		session_key = current_user_session_id(request) # return current user session id
		if CustomToken.objects.filter(key=key, client_ip=client_ip).exists():
			custom_token = CustomToken.objects.get(key=key, client_ip=client_ip)
		else:
			messages.error(request, _('Confirmation code is expired, try again'))

		if request.method == 'POST':
			form = SignUpForm(request.POST)
			if form.is_valid():
				full_name    = form.cleaned_data['full_name']
				phone_number = form.cleaned_data['phone_number']
				password1    = form.cleaned_data['password1']
				try:
					user = User.objects.create(full_name=full_name, phone_number=phone_number, phone_number_verified=True)
					user.set_password(password1)
					user.save()
					user = authenticate(phone_number=phone_number, password=password1)
					login(request, user)
					return redirect('/')
				except Exception as e:
					messages.error(request, _(f"Something went wrong, {e}"))

		context = {'form': form, 'phone_number': custom_token.phone_number}	
		return render(request, self.template_name, context)



class LoginView(View):
	template_name='registration/login.html'
	def get(self, request, *args, **kwargs):
		form = LoginForm()
		context={'form': form}
		return render(request, self.template_name, context)

	def post(self, request, *args, **kwargs):
		context={}
		if request.method =='POST':
			form = LoginForm(request.POST)
			if form.is_valid():
				phone_number = form.cleaned_data['phone_number']
				password     = form.cleaned_data['password']
				try:
					user = User.objects.get(phone_number=phone_number)
				except:
					messages.error(request, _("This phone number haven't been registred yet"))
					form=LoginForm()
					context={'form': form}
					return render(request, template_name, context)
				user = authenticate(phone_number=phone_number, password=password)
				if user:
					login(request, user)
					messages.success(request, _('Successfully loged in' ))
					return redirect('/')
				else:
					messages.warning(request, _('Phone number or password didn\'t match, please try again' ))
			else:
				messages.error(request, _('Phone number or password didn\'t match, please try again' ))
				# form=LoginForm()
		context['form']=form
		return render(request, self.template_name, context)


class LogOutView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        logout(request)
        messages.info(request, _("You are no longer logged in. Bye bye!"))
        return redirect("users:login")



def password_reset_phonenumber(request):
	'''
	check all objects with check_valid_token property in CustomToken, 
	if object created time longer than 5 minut it will be deleted.
	'''
	check_valid_token() 
	'-----------------'

	session_key = current_user_session_id(request)
	client_ip   = get_client_ip(request)

	template_name='registration/password-reset-phonenumber.html'
	
	form = PasswordResetPhonenumberForm()
	if request.method=='POST':
		form = PasswordResetPhonenumberForm(request.POST)
		if form.is_valid():
			phone_number = form.cleaned_data['phone_number']
			if User.objects.filter(phone_number=phone_number).exists():	
				confirmation_code = code_generator()
				status = send_sms(phone_number, confirmation_code)
				custom_token, created = CustomToken.objects.get_or_create(
					phone_number=phone_number,
					client_ip=client_ip
				)
				if created:
					custom_token.confirmation_code=confirmation_code
					custom_token.save() 
				else:
					custom_token.delete()
					custom_token = CustomToken.objects.create(phone_number=phone_number, confirmation_code=confirmation_code, client_ip=client_ip)
				
				# if status['status'] == 'waiting':
				# 	messages.success(request, _(success_msg))
				# 	return redirect('users:phone-verification', custom_token.key)
				# else:
				# 	messages.error(request, _("Something went wrong, try again"))
				# 	context={'form':form}
				# 	return render(request, self.template_name, context)
				messages.success(request, _("Confirmation code sent to your mobile number. The confirmation code is valid for 5 minutes."))
				return redirect('users:reset-password-verification', custom_token.key)
			else:
				messages.warning(request, _("This phone number haven't been registered yet"))
	return render(request, template_name, {'form': form})


def password_reset_verification(request, key):
	'''
	check all objects with check_valid_token property in CustomToken, 
	if object created time longer than 5 minut it will be deleted.
	'''
	check_valid_token() 
	'-----------------'

	session_key = current_user_session_id(request)
	client_ip   = get_client_ip(request)

	template_name='registration/password-reset-verification.html'
	try:
		custom_token = CustomToken.objects.get(key=key, client_ip=client_ip)
	except:
		messages.warning(request, _("Confirmation code is expired, try again."))
		return redirect("users:reset-password-phonenumber")

	form = PasswordResetVerificationForm()
	if request.method == 'POST':
		form = PasswordResetVerificationForm(request.POST)
		if form.is_valid():
			confirmation_code = form.cleaned_data['confirmation_code']
			if int(confirmation_code) == custom_token.confirmation_code and custom_token.check_valid_token:
				phone_number = custom_token.phone_number
				custom_token.delete()
				custom_token = CustomToken.objects.create(phone_number=phone_number, client_ip=client_ip)
				messages.success(request, _('Successfully confirmed, now you can create new password'))
				return redirect('users:reset-password-newpassword', custom_token.key)
			else:
				messages.error(request, _('Password didn\'t match :(, \nOr confiramtion code expired' ))

	context={'phone_number': custom_token.phone_number, 'form':form}
	return render(request, template_name, context)


def password_reset_newpassword(request, key):
	'''
	check all objects with check_valid_token property in CustomToken, 
	if object created time longer than 5 minut it will be deleted.
	'''
	check_valid_token() 
	'-----------------'

	session_key = current_user_session_id(request)
	client_ip   = get_client_ip(request)

	template_name = 'registration/password-reset-newpassword.html'
	try:
		custom_token = CustomToken.objects.get(key=key, client_ip=client_ip)
	except:
		messages.error(request, _('Something went wrong, Try again'))
		return redirect('users:reset-password-phonenumber')

	form = PasswordResetNewpasswordForm()
	if request.method == 'POST':
		form = PasswordResetNewpasswordForm(request.POST)
		if form.is_valid():
			password1    = form.cleaned_data['password1']
			try:
				user = User.objects.get(phone_number=custom_token.phone_number, phone_number_verified=True)
				user.set_password(password1)
				user.change_pw = True
				user.save()
				custom_token.delete()
				return redirect('users:login')
			except Exception as e:
				messages.error(request, _(f"Something went wrong, {e}"))
		# messages.error(request, _(""))
	context = {'form':form, 'phone_number':custom_token.phone_number}
	return render( request, template_name, context )


@login_required
def change_password(request, pk):
	template_name = 'registration/change-password.html'
	user_instance = User.objects.get(pk=pk)
	context={}
	form=ChangePasswordForm()
	if request.method == 'POST':
		form = ChangePasswordForm(request.POST)
		if form.is_valid():
			current_password = form.cleaned_data.get('current_password')
			new_password1 = form.cleaned_data.get('new_password1')

			user = authenticate(phone_number=user_instance.phone_number, password=current_password)
			 
			if user:
				user_instance.set_password(new_password1)
				messages.success(request, _("Password changed successfully"))
				user_instance.save()
				return redirect("users:login")
			else:
				messages.error(request, _("Current password didn't match, please try again"))
		else:
			messages.error(request, _("Something went wrong, please check and try again"))
	context['form'] = form
	return render(request, template_name, context)