from django.db import models

# Create your models here.

class Action(models.Model):
    '''Модель действия пользователя'''
    user = models.ForeignKey('auth.User', related_name='actions', verbose_name='Пользователь', on_delete=models.CASCADE)
    verb = models.CharField(max_length=255, verbose_name='Действие')
    created = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-created']
