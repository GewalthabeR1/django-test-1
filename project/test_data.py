import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from app.models import Post
from django.utils import timezone

posts_data = [
    {
        'title': 'Мой первый пост в блоге',
        'content': '''Добро пожаловать в мой блог! Это мой первый пост, где я расскажу о своих планах.

Я буду писать о:
* Django разработке
* Веб-технологиях
* Программировании в целом

Следите за обновлениями!''',
    },
    {
        'title': 'Изучение Django: шаблоны и теги',
        'content': '''В этом посте я расскажу о шаблонах Django.

**Шаблоны Django** позволяют разделить логику и представление.

Основные теги:
1. {% raw %}{% block %}{% endraw %} - для наследования
2. {% raw %}{% for %}{% endraw %} - для циклов
3. {% raw %}{% if %}{% endraw %} - для условий
4. {% raw %}{% url %}{% endraw %} - для генерации URL''',
    },
    {
        'title': 'Редиректы в Django',
        'content': '''Редиректы важны для:
- Перенаправления пользователей
- Изменения структуры URL
- Временных перемещений страниц

Используйте функции redirect() или HttpResponseRedirect.''',
    },
]

for post_data in posts_data:
    Post.objects.create(**post_data)

print("Тестовые данные созданы!")