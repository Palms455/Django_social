from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse


class Image(models.Model):
     user = models.ForeignKey(settings.AUTH_USER_MODEL,
     related_name='images_created', on_delete=models.CASCADE, verbose_name='Пользователь')
     title = models.CharField(max_length=200, verbose_name='Заголовок')
     slug = models.SlugField(max_length=200, blank=True)
     url = models.URLField()
     image = models.ImageField(upload_to='images/%Y/%m/%d/')
     description = models.TextField(blank=True, verbose_name='Описание')
     created = models.DateField(auto_now_add=True, db_index=True, verbose_name='Дата создания')
     users_like = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                         related_name='images_liked',
                                         blank=True)

     class Meta:
         verbose_name = 'Фотография'
         verbose_name_plural = 'Фотографии'

     def __str__(self):
        return self.title

     def save(self, *args, **kwargs):
         if not self.slug:
             self.slug = slugify(self.title)
         super(Image, self).save(*args, **kwargs)

     def get_absolute_url(self):
         return reverse('images:detail', args=[self.id, self.slug])


