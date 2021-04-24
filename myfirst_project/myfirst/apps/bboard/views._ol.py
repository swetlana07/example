from django.shortcuts import render

def index(request):
    return render(request, 'bboard/index.html')


from django.http import HttpResponse, Http404
from django.template import TemplateDoesNotExist
from django.template.loader import get_template
def other_page(request, page):
    try:
        template=get_template('bboard/'+page+'.html')
    except TemplateDoesNotExist:
        raise Http404
    return HttpResponse(template.render(request=request))
    
from django.contrib.auth.views import LoginView
class BBLoginView(LoginView):
    template_name = 'bboard/login.html'
    redirect_field_name=next

from django.contrib.auth.views import LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
class BBLogoutView(LoginRequiredMixin,LogoutView):
    template_name = 'bboard/logout.html'
    
from django.contrib.auth.decorators import login_required
@login_required
def profile(request):
    return render(request, 'bboard/profile.html')
    

from django.views.generic.edit import UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from .models import AdvUser
from .forms import ChangeUserInfoForm
class ChangeUserInfoView(SuccessMessageMixin, LoginRequiredMixin,UpdateView):
    model = AdvUser
    template_name = 'bboard/change_user_info.html'
    form_class = ChangeUserInfoForm
    success_url = reverse_lazy('bboard:profile')
    success_message ='Личные данные пользователя изменены'
    def dispatch(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().dispatch(request, *args, **kwargs)
    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)
   
from django.contrib.auth.views import PasswordChangeView
class BBPasswordChangeView(SuccessMessageMixin,LoginRequiredMixin,PasswordChangeView):
    template_name = 'bboard/password_change.html'
    success_url = reverse_lazy('bboard:profile')
    success_message ='Пароль пользователя изменен'
    # Create your views here.
    
from django.views.generic import CreateView
from .forms import RegisterUserForm
class RegisterUserView(CreateView):
    model = AdvUser
    template_name = 'bboard/register_user.html'
    form_class=RegisterUserForm
    success_url=reverse_lazy('bboard:register_done')
    
from django.views.generic.base import TemplateView
class RegisterDoneView(TemplateView):
    template_name = 'bboard/register_done.html'

from django.core.signing import BadSignature
from .utilites import signer
def user_activate(request, sign):
    try:
        username = signer.unsign(sign)
    except BadSignature:
        return render(request, 'bboard/bad_signature.html')
    user = get_object_or_404(AdvUser, username=username)
    if user.is_activated:
        template='bboard/user_is_activated.html'
    else:
        template='bboard/activation_done.html'
        user.is_active = True
        user.is_activated = True
        user.save()
    return render(request, template)

from django.views.generic.edit import DeleteView
from django.contrib.auth import logout
from django.contrib import messages

class DeleteUserView(LoginRequiredMixin, DeleteView) :
    model = AdvUser
    template_name ='bboard/delete_user.html'
    success_url=reverse_lazy('bboard:index')
    def dispatch(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().dispatch(request, *args, **kwargs)
        
    def post(self, request, *args, **kwargs):
        logout(request)
        messages.add_message(request, messages.SUCCESS,
           'Пользователь удален')
        return super().post(request, *args, **kwargs)
        
    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


