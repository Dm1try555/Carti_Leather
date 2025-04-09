
# Установка

1. Клонируйте репозиторий
```
clone <<git>>

cd OnlineStore
```


2. Создайте виртуальное окружение и активируйте его
```
py -m venv venv
source venv/bin/activate
```
3. Установите зависимости
```
pip install -r requirements.txt
```
4. Создайте в корне проекта .env 

5. Запустите миграции и загрузите данные в БД
```
python manage.py migrate
python manage.py loaddata data.json
```
6. Создайте администратора магазина
```
python manage.py createsuperuser
```
7. Запустите сервер
```
python manage.py runserver
```
Откройте браузер и перейдите по адресу http://127.0.0.1:8000/admin/. Введите имя пользователя и пароль администратора, чтобы войти в панель управления магазином.

