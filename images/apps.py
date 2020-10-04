from django.apps import AppConfig


class ImagesConfig(AppConfig):
    name = 'images'

    def ready(self):
        # для отслеживания изменений импортируем файл с функцией-подписчиком на сигнал
        from . import signals