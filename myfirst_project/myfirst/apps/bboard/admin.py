from django.contrib import admin
from django.contrib.admin import AdminSite

from .models import AdvUser

import datetime
from .utilites import send_activation_notification

class BlogAdminSite(AdminSite):
    site_header='Администрирование доски управления' 
    
bboard_admin=BlogAdminSite(name='bboard_admin')

def send_activation_notifications(modeladmin, request, queryset):
    for rec in queryset:
        if not rec.is_activated:
            send_activation_notification(rec)
    modeladmin.message_user(request, 'Письма с оповещениями отправлены')
send_activation_notifications.short_description = 'Отправка писем с ' + \
'оповещениями об активации'


class NonactivatedFilter(admin.SimpleListFilter):
    title = 'Прошли активацию?'
    parameter_name = 'actstate'

    def lookups(self, request, model_admin):
        return (
            ('activated', 'Прошли'),
            ('threedays', 'Не прошли более 3 дней'),
            ( 'week' , 'Не прошли более недели' ) ,
        )
        
    def queryset(self, request, queryset):
        val = self.value()
        if val == 'activated':
            return queryset.filter(is_active=True, is_activated=True)
        elif val == 'threedays':
            d = datetime.date.today() - datetime.timedelta(days=3)
            return queryset.filter(is_active=False, is_activated=False,
                  date_joined__date__lt=d)
        elif val == 'week':
            d = datetime.date.today() - datetime.timedelta(weeks=l)
            return queryset.filter(is_active=False, is_activated=False,
                date_joined__date__lt=d)

class AdvUserAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'is_activated', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    list_filter = (NonactivatedFilter,)
    fields = (('username', 'email'), ('first_name', 'last_name'),
               ('send_messages', 'is_active', 'is_activated'),
               ('is_staff', 'is_superuser'),
                'groups', 'user_permissions',
               ('last_login', 'date_joined'))
    readonly_fields = ('last_login', 'date_joined')
    actions = (send_activation_notifications,)

bboard_admin.register(AdvUser,AdvUserAdmin)

from .models import SuperRubric, SubRubric

class SubRubricInline(admin.TabularInline):
    model=SubRubric
    
class SuperRubricAdmin(admin.ModelAdmin):
    exclude=('super_rubic',)
    inlines =(SubRubricInline,)
    
bboard_admin.register(SuperRubric,SuperRubricAdmin)

from .forms import SubRubricForm

class SubRubricAdmin(admin.ModelAdmin):
    form =SubRubricForm
    
bboard_admin.register(SubRubric,SubRubricAdmin)

from .models import Bb, AdditionalImage,Comment_bb

bboard_admin.register(Comment_bb)
    

    
class AdditionalImageInline(admin.TabularInline):
    model=AdditionalImage
    
class BbAdmin(admin.ModelAdmin):
    list_display=('rubric','title','content','author','created_at')
    fields=(('rubric','author'),'title','content','price','contacts','image','is_active')
    inlines=(AdditionalImageInline,)
    
bboard_admin.register(Bb, BbAdmin)

# Register your models here.
