from django.db import models
NULLABLE = {'blank': True, 'null': True}


class Blog(models.Model):
    title = models.CharField(max_length=35, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержание')
    image = models.ImageField(upload_to='media/', verbose_name='Изображение', **NULLABLE)
    view_count = models.IntegerField(verbose_name='Количество просмотров', default=0)
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    is_published = models.BooleanField(default=True, verbose_name='Признак публикации')
    slug = models.CharField(max_length=150, verbose_name='slug', **NULLABLE)

    def __str__(self):
        return f'{self.title} - {self.view_count}, {self.create_date}'

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'
