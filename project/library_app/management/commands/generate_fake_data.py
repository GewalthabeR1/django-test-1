from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import random
from datetime import datetime, timedelta
from django.utils import timezone

class Command(BaseCommand):
    help = 'Генерирует тестовые данные для библиотеки'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--books',
            type=int,
            default=10,
            help='Количество книг для создания'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Очистить существующие данные перед генерацией'
        )
    
    def handle(self, *args, **options):
        books_count = options['books']
        
        self.stdout.write(self.style.SUCCESS('=' * 50))
        self.stdout.write(self.style.SUCCESS('НАЧАЛО ГЕНЕРАЦИИ ТЕСТОВЫХ ДАННЫХ'))
        self.stdout.write(self.style.SUCCESS('=' * 50))
        
        if options['clear']:
            self.clear_existing_data()
        
        try:
            from library_app.models import Author, Genre, Book

            self.create_superuser()
            
            test_user = self.create_test_user()
            
            genres = self.create_genres()
            
            authors = self.create_authors()
            
            books = self.create_books(books_count, authors, genres)
            
            self.create_additional_models(test_user, books)
            
            self.print_statistics()
            
        except ImportError as e:
            self.stdout.write(self.style.ERROR(f'❌ Ошибка импорта: {e}'))
            self.stdout.write('Проверьте наличие моделей в library_app/models.py')
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Ошибка: {e}'))
            import traceback
            traceback.print_exc()
    
    def clear_existing_data(self):
        """Очистка существующих данных"""
        self.stdout.write(self.style.WARNING('Очистка существующих данных...'))
        
        try:
            from library_app.models import BookInstance, Book, Author, Genre
            
            BookInstance.objects.all().delete()
            Book.objects.all().delete()
            Author.objects.all().delete()
            Genre.objects.all().delete()
            
            User.objects.filter(is_superuser=False).delete()
            
            self.stdout.write(self.style.SUCCESS('✅ Данные очищены'))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'Не удалось очистить данные: {e}'))
    
    def create_superuser(self):
        """Создание суперпользователя"""
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@library.ru',
                password='admin123'
            )
            self.stdout.write(self.style.SUCCESS('✅ Создан суперпользователь: admin/admin123'))
        else:
            self.stdout.write('ℹ️ Суперпользователь уже существует')
    
    def create_test_user(self):
        """Создание тестового пользователя"""
        user, created = User.objects.get_or_create(
            username='reader',
            defaults={
                'email': 'reader@library.ru',
                'first_name': 'Иван',
                'last_name': 'Читатель'
            }
        )
        if created:
            user.set_password('password123')
            user.save()
            self.stdout.write(self.style.SUCCESS('✅ Создан тестовый пользователь: reader/password123'))
        
        return user
    
    def create_genres(self):
        """Создание жанров"""
        from library_app.models import Genre
        
        genres_list = [
            'Фантастика', 'Детектив', 'Роман', 'Поэзия', 
            'Драма', 'Комедия', 'Приключения', 'Исторический'
        ]
        
        genres = []
        for genre_name in genres_list:
            genre, created = Genre.objects.get_or_create(name=genre_name)
            genres.append(genre)
            if created:
                self.stdout.write(f'✅ Создан жанр: {genre_name}')
        
        return genres
    
    def create_authors(self):
        """Создание авторов"""
        from library_app.models import Author
        
        authors_data = [
            {'first_name': 'Лев', 'last_name': 'Толстой', 'birth_date': '1828-09-09'},
            {'first_name': 'Фёдор', 'last_name': 'Достоевский', 'birth_date': '1821-11-11'},
            {'first_name': 'Антон', 'last_name': 'Чехов', 'birth_date': '1860-01-29'},
            {'first_name': 'Александр', 'last_name': 'Пушкин', 'birth_date': '1799-06-06'},
            {'first_name': 'Николай', 'last_name': 'Гоголь', 'birth_date': '1809-04-01'},
            {'first_name': 'Михаил', 'last_name': 'Булгаков', 'birth_date': '1891-05-15'},
            {'first_name': 'Иван', 'last_name': 'Тургенев', 'birth_date': '1818-11-09'},
            {'first_name': 'Александр', 'last_name': 'Солженицын', 'birth_date': '1918-12-11'},
        ]
        
        authors = []
        for author_data in authors_data:
            author, created = Author.objects.get_or_create(
                first_name=author_data['first_name'],
                last_name=author_data['last_name'],
                defaults={'birth_date': author_data['birth_date']}
            )
            authors.append(author)
            if created:
                self.stdout.write(f'✅ Создан автор: {author_data["first_name"]} {author_data["last_name"]}')
        
        return authors
    
    def create_books(self, count, authors, genres):
        """Создание книг"""
        from library_app.models import Book
        
        books_titles = [
            'Война и мир', 'Анна Каренина', 'Преступление и наказание',
            'Идиот', 'Вишневый сад', 'Дама с собачкой', 'Евгений Онегин',
            'Капитанская дочка', 'Мертвые души', 'Ревизор', 'Мастер и Маргарита',
            'Отцы и дети', 'Один день Ивана Денисовича', 'Герой нашего времени',
            'Обломов', 'Тихий Дон', 'Доктор Живаго', 'Собачье сердце'
        ]
        
        books = []
        for i in range(min(count, len(books_titles))):
            isbn_prefix = '9785'
            middle_part = str(random.randint(10000, 99999))
            end_part = str(random.randint(100, 999))
            check_digit = str(random.randint(0, 9))
            isbn = f'{isbn_prefix}{middle_part}{end_part}{check_digit}'
            
            isbn = isbn[:13]
            
            book_data = {
                'title': books_titles[i],
                'author': random.choice(authors),
                'summary': f'Классическое произведение русской литературы "{books_titles[i]}"',
                'isbn': isbn,
                'publication_year': random.randint(1950, 2023),
                'publisher': random.choice(['Эксмо', 'АСТ', 'Дрофа', 'Просвещение', 'Азбука']),
                'pages': random.randint(100, 800),
            }
            
            book, created = Book.objects.get_or_create(
                title=book_data['title'],
                defaults=book_data
            )

            if genres:
                book.genre.set(random.sample(genres, random.randint(1, 3)))
            
            books.append(book)
            if created:
                self.stdout.write(f'✅ Создана книга: "{book_data["title"]}"')
        
        return books
    
    def create_additional_models(self, user, books):
        """Создание дополнительных моделей если они существуют"""
        try:
            from library_app.models import Reader
            reader, created = Reader.objects.get_or_create(
                user=user,
                defaults={
                    'phone_number': '+7 (999) 123-45-67',
                    'address': 'г. Москва, ул. Примерная, д. 1',
                    'birth_date': '1990-01-01',
                    'card_number': f'RD-{random.randint(1000, 9999)}'
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS('✅ Создан профиль читателя'))
            else:
                self.stdout.write('ℹ️ Профиль читателя уже существует')
        except ImportError:
            self.stdout.write('ℹ️ Модель Reader не найдена, пропускаем...')
        
        try:
            from library_app.models import BookInstance
            bookinstance_count = 0
            
            for book in books:
                existing_instances = BookInstance.objects.filter(book=book).count()
                max_instances = random.randint(1, 3)

                for i in range(existing_instances, max_instances):
                    try:
                        timestamp = int(timezone.now().timestamp() * 1000)
                        inventory_number = f'BK-{book.id:04d}-{timestamp % 10000:04d}'
                        
                        book_instance = BookInstance.objects.create(
                            book=book,
                            inventory_number=inventory_number,
                            status=random.choice(['a', 'm', 'o']),
                            due_back=timezone.now() + timedelta(days=random.randint(1, 30)) if random.random() > 0.7 else None
                        )
                        bookinstance_count += 1
                    except Exception as e:
                        self.stdout.write(f'⚠️ Ошибка при создании экземпляра книги: {e}')
                        continue
            
            if bookinstance_count > 0:
                self.stdout.write(f'✅ Создано {bookinstance_count} новых экземпляров книг')
            else:
                self.stdout.write('ℹ️ Все экземпляры книг уже существуют')
                
        except ImportError:
            self.stdout.write('ℹ️ Модель BookInstance не найдена, пропускаем...')
    
    def print_statistics(self):
        """Вывод статистики"""
        from django.apps import apps
        
        self.stdout.write(self.style.SUCCESS('=' * 50))
        self.stdout.write(self.style.SUCCESS('ИТОГИ ГЕНЕРАЦИИ:'))
        self.stdout.write(self.style.SUCCESS('=' * 50))
        
        self.stdout.write(f'• Пользователей: {User.objects.count()}')
        
        try:
            from library_app.models import Author, Genre, Book
            self.stdout.write(f'• Авторов: {Author.objects.count()}')
            self.stdout.write(f'• Жанров: {Genre.objects.count()}')
            self.stdout.write(f'• Книг: {Book.objects.count()}')
            
            for model_name in ['Reader', 'BookInstance', 'Loan', 'Reservation', 'Review']:
                try:
                    model_class = apps.get_model('library_app', model_name)
                    count = model_class.objects.count()
                    self.stdout.write(f'• {model_name}: {count}')
                except LookupError:
                    pass  
        
        except ImportError:
            self.stdout.write('⚠️ Не все модели библиотеки доступны')
        
        self.stdout.write(self.style.SUCCESS('=' * 50))
        self.stdout.write(self.style.SUCCESS('✅ ГЕНЕРАЦИЯ УСПЕШНО ЗАВЕРШЕНА!'))
        self.stdout.write(self.style.SUCCESS('=' * 50))