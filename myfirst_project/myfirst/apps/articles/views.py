from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone
from .models import Article, Comment
from django.core.paginator import Paginator
#from .forms import CommentForm

def index(request):
   # latest_articles_list=Article.objects.order_by('-pup_date')[:5]

    paginator=Paginator(Article.objects.order_by('-pup_date'),5) 
    if 'page' in request.GET:
        page_num=request.GET['page'] 
    else:
        page_num=1
    page=paginator.get_page(page_num)

    return render(request, 'articles/list.html',{'page':page,'latest_articles_list':page.object_list})

#    return render(request, 'articles/list.html',#{'latest_articles_list':latest_articles_list})
    

def detail(request,article_id):
    try:
        a=Article.objects.get(id=article_id)
    except:
        raise Http404("Статья не найдена!")

    paginator=Paginator(a.comment_set.order_by('-comment_dt'),10)   
    if 'page' in request.GET:
        page_num=request.GET['page'] 
    else:
        page_num=1
    page=paginator.get_page(page_num)  
     
    #latest_comments_list=a.comment_set.order_by('-comment_dt')[:10]

    return render(request, 'articles/detail.html',{'article':a, 'page':page,'latest_comments_list':page.object_list})        
   # return render(request, 'articles/detail.html',##{'article':a,'latest_comments_list':latest_comments_list})
    


def leave_comment(request,article_id):
    if request.method =='POST':
    #form=CommentForm()
    #return render(request, 'detail.html',{'form':form}) 
    #else:
        try:
            a=Article.objects.get(id=article_id)
        except:
            raise Http404("Статья не найдена!")
    #if form.is_valid():
    #    author_name=form.cleaned_data['name']
    #    comment_text=form.cleaned_data['text']     
    # form=NameForm(request.POST)
    # if form.is_valid():
        author_name=(str)(request.POST.get('name','anonim'))
        if(not author_name): 
            author_name ='anon'
        comment_text=(str)(request.POST.get('text','-'))
        if(not comment_text): 
            comment_text=''
        a.comment_set.create(author_name= request.POST['name'], comment_text=request.POST['text'], comment_dt=timezone.now())
       # a.comment_set.create(author_name, comment_text, timezone.now())
        return HttpResponseRedirect(reverse('articles:detail',args=(a.id,)))