from django.db import models
from django.contrib.auth.models import AbstractUser

class AdvUser(AbstractUser):
    is_activated=models.BooleanField(default=True, db_index=True, verbose_name='Прошел активацию?')
    
    send_messages=models.BooleanField(default=True, verbose_name='Слать оповещение о новых комментариях?')
    
    class Meta(AbstractUser.Meta):
        pass

from django.dispatch import Signal
from .utilites import send_activation_notification
user_registrated = Signal(providing_args=['instance'])
def user_registrated_dispatcher(sender, **kwargs):
    send_activation_notification(kwargs['instance'])
user_registrated.connect(user_registrated_dispatcher)

class Rubric(models.Model):
    name=models.CharField(max_length=20,db_index=True,unique=True,
    verbose_name='Название')
    order=models.SmallIntegerField(default=0, db_index=True,
    verbose_name='Порядок')
    super_rubric=models.ForeignKey('SuperRubric', on_delete=models.PROTECT, 
    null=True,blank=True,verbose_name='Надрубрика')
    
class SuperRubricManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(super_rubric__isnull=True)

class SuperRubric(Rubric):
    objects =SuperRubricManager()
    
    def __str__(self):
        return self.name
    class Meta:
        proxy = True
        ordering = ('order', 'name')
        verbose_name ='Надрубрика'
        verbose_name_plural ='Надрубрики'

class SubRubricМanager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(super_rubric__isnull=False)

class SubRubric(Rubric):
    objects =SubRubricМanager()
    
    def __str__(self):
        return '%s-%s' % (self.super_rubric.name,self.name)
    class Meta:
        proxy = True
        ordering = ( 'super_rubric__order', 'super_rubric__name','order','name')
        verbose_name ='Подрубрика'
        verbose_name_plural ='Подрубрики'
        
from .utilites import get_timestamp_path

class Bb(models.Model):
    rubric=models.ForeignKey(SubRubric, on_delete=models.PROTECT,
           verbose_name='Рубрика')
    title=models.CharField(max_length=40, verbose_name='Товар')
    content=models.TextField(verbose_name='Oпиcaниe')
    price = models.FloatField(default=0,verbose_name='Цeнa')
    contacts =models.TextField(verbose_name='Koнтaкты')
    image =models.ImageField(blank=True,upload_to=get_timestamp_path,
            verbose_name='Изображение')
    author = models.ForeignKey(AdvUser, on_delete=models.CASCADE,
            verbose_name='Aвтop объявления')
    is_active = models.BooleanField(default=True, db_index=True,
            verbose_name='Выводить в списке?')
    created_at=models.DateTimeField(auto_now_add=True,db_index=True,
            verbose_name='Опубликовано')
    def delete(self, *args, **kwargs):
        for ai in self.additionalimage_set.all():
            ai.delete()
        super().delete(*args, **kwargs)
        
    class Meta:
        verbose_name_plural ='Объявлния'
        verbose_name ='Объявлние'
        ordering=['-created_at']
        
class AdditionalImage(models.Model):
    bb=models.ForeignKey(Bb,on_delete=models.CASCADE,
          verbose_name='Объявление')
    image = models.ImageField(upload_to=get_timestamp_path,
          verbose_name='Изображение')
    class Meta:
        verbose_name_plural ='Дополнительные иллюстрации'
        verbose_name ='Дополнительная иллюстрация'        
        #Create your models here.
