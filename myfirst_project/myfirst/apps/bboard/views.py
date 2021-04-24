from django.shortcuts import render

def index(request):
    bbs=Bb.objects.filter(is_active=True)[:10]
    context={'bbs':bbs}
    return render(request, 'bboard/index.html',context)


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
    bbs=Bb.objects.filter(author=request.user.pk)
    context={'bbs':bbs}
    return render(request, 'bboard/profile.html', context)
    

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
        user. save ()
    return render(request, template)

from django.views.generic.edit import DeleteView
from django.contrib.auth import logout
from django.contrib import messages

class DeleteUserView(LoginRequiredMixin, DeleteView) :
    model = AdvUser
    template_name = 'bboard/delete_user.html'
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


from django.core.paginator import Paginator
from django.db.models import Q
from .models import SubRubric,Bb
from .forms import SearchForm

def by_rubric(request,pk):
    rubric=get_object_or_404(SubRubric,pk=pk)
    bbs = Bb.objects.filter(is_active=True, rubric=pk)
    
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        q =Q(title__icontains=keyword)|Q(content__icontains=keyword)
        bbs = bbs.filter(q)
    else:
        keyword = ''
        
    form = SearchForm(initial= {'keyword' : keyword})
      
    paginator = Paginator(bbs, 2)
    if 'page' in request.GET:
        page_num = request.GET['page']
    else:
        page_num = 1
    page = paginator.get_page(page_num)
  
    context ={'rubric':rubric,'page': page, 'bbs': page.object_list,
              'form': form}
         
    return render(request,'bboard/by_rubric.html',context)
 
from .models import Comment_bb
from .forms import UserCommentForm,GuestCommentForm
   
def detail(request, rubric_pk, pk):
    bb=get_object_or_404(Bb,pk=pk)
    ais=bb.additionalimage_set.all()
    
    comments=Comment_bb.objects.filter(bb=pk, is_active=True)
    initial={'bb':bb.pk}
    if request.user.is_authenticated:
        initial['author']=request.user.username
        form_class=UserCommentForm
    else:
        form_class=GuestCommentForm
    form=form_class(initial=initial)
    if request.method=='POST':
        c_form=form_class(request.POST)
        if c_form.is_valid():
            c_form.save()
            messages.add_message(request,messages.SUCCESS,'Комментарий добавлен')
    
    context={'bb':bb, 'ais':ais, 'comments':comments, 'form':form}
    
    return render(request,'bboard/detail.html',context)

@login_required    
def profile_bb_detail(request, pk):
    bb=get_object_or_404(Bb,pk=pk)
    ais=bb.additionalimage_set.all()
    comments=Comment_bb.objects.filter(bb=pk, is_active=True)
    context={'bb':bb, 'ais':ais, 'comments':comments}
    
    #context={'bb':bb, 'ais':ais}
    return render(request,'bboard/profile_bb_detail.html',context)
    
from django.shortcuts import redirect
from .forms import BbForm, AIFormSet

@login_required  
def profile_bb_add(request):
    print("gdgdgdgdgd")
    if request.method=='POST':
        form=BbForm(request.POST, request.FILES)
        if form.is_valid():
            bb=form.save()
            formset=AIFormSet(request.POST, request.FILES, instance=bb)
            if formset.is_valid():
                formset.save()
                messages.add_message(request,messages.SUCCESS, 'Объявление добавлено')
                return redirect('bboard:profile')
    else:
        form=BbForm(initial={'author':request.user.pk})
        formset=AIFormSet()
    context={'form':form,'formset':formset}
    return render(request,'bboard/profile_bb_add.html', context)
    
    
@login_required 
def profile_bb_change(reqest, pk):
    bb=get_object_or_404(Bb,pk=pk)
    if reqest.method=='POST':
        form=BbForm(reqest.POST,reqest.FILES, instance=bb)
        if form.is_valid():
            bb=form.save()
            formset=AIFormSet(reqest.POST, reqest.FILES, instance=bb)
            if formset.is_valid():
                formset.save()
                messages.add_message(reqest,messages.SUCCESS, 'Объявление исправлено')
                return redirect('bboard:profile')
    else:
        form=BbForm(instance=bb)
        formset=AIFormSet(instance=bb)
        context={'form':form,'formset':formset}
        return render(reqest,'bboard/profile_bb_change.html', context)
        
@login_required 
def profile_bb_delete(reqest, pk):
    bb=get_object_or_404(Bb,pk=pk)
    if reqest.method=='POST':
        bb.delete()
        messages.add_message(reqest,messages.SUCCESS, 'Объявление удалено')
        return redirect('bboard:profile')
    else:
        context={'bb':bb}
        return render(reqest,'bboard/profile_bb_delete.html', context)