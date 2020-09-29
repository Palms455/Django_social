from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Create your models here.

class Action(models.Model):
    '''Модель действия пользователя'''
    user = models.ForeignKey('auth.User', related_name='actions', verbose_name='Пользователь', on_delete=models.CASCADE)
    verb = models.CharField(max_length=255, verbose_name='Действие')
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    target_ct = models.ForeignKey(ContentType, blank=True, null=True, related_name='target_obj', on_delete=models.CASCADE)
    target_id = models.PositiveIntegerField(null=True, blank=True, db_index=True)
    # для хранения идентификатора на связанный объект
    target = GenericForeignKey('target_ct', 'target_id')
    # поле для обращения к связанному объекту
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-created']
        verbose_name = 'Действие'
        verbose_name_plural = 'Действия'
