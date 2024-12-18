from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm


class LoginUser(LoginView):
	redirect_authenticated_user = True

	form_class = AuthenticationForm
	template_name = 'user/login.html'
	
	def get_success_url(self):
		return reverse_lazy('point-control') 


def sign_out(request):
	if request.user.is_authenticated:
		logout(request)
	return redirect('show-status-page')
