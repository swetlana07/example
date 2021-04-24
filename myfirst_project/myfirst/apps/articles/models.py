import datetime
from django.db import models
from django.utils import timezone

class Article(models.Model):
   article_title=models.CharField('название ствтьи', max_length=200)
   article_text=models.TextField('текст ствтьи')
   pup_date=models.DateTimeField('дата публикации')
   
   def __str__(self):
       return self.article_title
       
   def was_published_recently(self):
       return self.pup_date>=(timezone.now()-datetime.timedelta(days=7))
       
   class Meta:
        verbose_name='Статья'
        verbose_name_plural='Статьи'
        
class Comment(models.Model):
    article=models.ForeignKey(Article, on_delete=models.CASCADE)
    author_name=models.CharField('имя авторв', max_length=100)
    comment_text=models.CharField('текст комментария', max_length=500)
    comment_dt=models.DateTimeField('дата комментария')
     
    def __str__(self):
       return self.author_name
       
    class Meta:
        verbose_name='Комментарий'
        verbose_name_plural='Комментарии'
