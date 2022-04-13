from django.shortcuts import render, get_object_or_404, HttpResponse
from django.contrib import messages 
from django.http import  JsonResponse, HttpResponseRedirect
from django.db.models import F, Q, When, Value, Case
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import ugettext as _
from django.views.generic import (
	ListView,
	DetailView,
	UpdateView,
	CreateView,
	DeleteView,
)
from django.urls import reverse
from django.contrib.auth import get_user_model
import json
User=get_user_model()
# from users.models import User

from product.models import (
	UserViews,
	Category,
	Product,
	MockUp,
	Image,
	Tag,
)

from .models import (
	UseFull,
	UseFullCategory,
)
from users.forms import (
	UpdateProfileForm,
)
# Create your views here.

class HomeView(ListView):
	model = Product
	template_name = "index.html"
	paginate_by = 18

	slug_field = 'slug'
	slug_url_kwargs = 'slug'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		downloaded_viewed = Product.objects.order_by("-downloaded",)[:4]
		context['recommended_list'] = downloaded_viewed

		context['category_list'] = Category.objects.all()

		return context
	
	def get_queryset(self):
		qs = super().get_queryset()
		try: # if some q exits then all products are found that matches q
			query = self.request.GET.get('q')
			qs = qs.filter( Q(name__icontains=query) | Q(slug__icontains=query) | Q(description__icontains=query))
			if len(qs) == 0:
				print("nothing")
				messages.warning(self.request, f"Qidiruv natijasi topilmadi :(")
			return qs
		except:
			if 'slug' in self.kwargs: # if exact category sellected, exception catch the slug then return all products of this category
				slug = self.kwargs.get('slug')
				category = get_object_or_404(Category, slug=slug)
				return qs.filter(category=category)[:9]
			else: # if none of wxacptions above are exacuted then returns qs itself
				return qs 


class MockUpListView(ListView):
	model = Product
	template_name = 'products.html'
	paginate_by = 9

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		if 'slug' in self.kwargs:
			slug = self.kwargs['slug']
			context['category'] = Category.objects.get(slug=slug)
		else:
			context['category'] = {'name':None}

		context['category_list'] = Category.objects.all()
		downloaded_viewed = Product.objects.order_by("-downloaded",)[:4]
		context['recommended_list'] = downloaded_viewed

		return context

	def get_queryset(self):
		qs = super().get_queryset()
		
		try: # if some q exits then all products are found that matches q
			query = self.request.GET.get('q')
			# print(query)
			qs = qs.filter( Q(name__icontains=query) | Q(slug__icontains=query) | Q(description__icontains=query))
			if len(qs) == 0:
				print("nothing")
				messages.warning(self.request, f"Qidiruv natijasi topilmadi :(")
			return qs
		except:
			if 'slug' in self.kwargs: # if exact category sellected, exception catch the slug then return all products of this category
				slug = self.kwargs.get('slug')
				category = get_object_or_404(Category, slug=slug)
				return qs.filter(category=category)
			else: # if none of wxacptions above are exacuted then returns qs itself
				return qs 


class MockUpDetailView(DetailView):
	model = Product
	template_name = "detail.html"

	slug_field      = 'slug'
	slug_url_kwargs = 'slug'
	
	def get_client_ip(self, request, *args, **kwargs):
		x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
		if x_forwarded_for:
			ip = x_forwarded_for.split(',')[0]
		else:
			ip = request.META.get('REMOTE_ADDR')
		print(ip)
		return ip

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		mockup = Product.objects.get(slug=self.kwargs['slug'])

		# Product.objects.filter(slug=self.kwargs['slug']).update(viewed=F('viewed')+1) # increase viewed field by 1 every request, count viewed 
		# <--------- view counter by ip ---------!>
		visitor_ip = self.get_client_ip(self.request)
		print(visitor_ip)
		UserViews.objects.get_or_create(visitor_ip=visitor_ip, mockup=mockup)
		# <--------- view counter by ip ---------!>

		category = Category.objects.get(slug=mockup.category.slug)
		category_product = category.product_category.all().order_by('-downloaded',)[:4]
		context['recommended_list'] = category_product
		return context



def download_counter(request):
	data = json.loads(request.body)
	slug = data['slug']
	Product.objects.filter(slug = slug).update(downloaded = F('downloaded')+1)
	return JsonResponse({"success":"Increased"}, safe=False, status=200)


def aboutus(request, *args, **kwargs):
	template_name = "aboutus.html"
	return render(request, template_name, {})


class UseFullListView(ListView):
	template_name = 'usefull.html'
	model = UseFullCategory


@login_required
def mockup_like(request):
	data = json.loads(request.body)
	slug = data['slug']
	print('slug', slug)
	try:
		obj = Product.objects.get(slug=slug)
	except Exception as e:
		obj=None
	if obj and obj.liked.filter(id=request.user.id).exists():
		obj.liked.remove(request.user)
		return JsonResponse({"success":"Unliked"}, safe=False, status=200)
	elif obj and not obj.liked.filter(id=request.user.id).exists():
		obj.liked.add(request.user)
		return JsonResponse({"success":"Liked"}, safe=False, status=200)
	return JsonResponse({"success":"Something went wrong :("}, safe=False, status=200)


class UserProfile(LoginRequiredMixin, ListView):
	model=Product
	template_name='myprofile.html'

	def get_queryset(self):
		qs =  super().get_queryset()
		return qs.filter(liked__pk=self.request.user.pk)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['user_info'] = User.objects.get(pk=self.request.user.pk)
		return context


class UpdateUserProfileView(LoginRequiredMixin, UpdateView):
	template_name='update-myprofile.html'
	model=User
	form_class=UpdateProfileForm

	def get_success_url(self):
		messages.success(self.request, _("User info updated successfully"))
		return reverse('core:user-profile')

	
