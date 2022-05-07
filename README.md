# blog-platform-django


[繁體中文版 README.md | Traditional Chinese README.md]()

This is a writing platform built by Django framework. Beside the posting function, it also contains social media features, such as Like, Follow, Bookmark and Notification.

Frontend template was purchased through [themeforest](https://themeforest.net/), even I added a lot of custom css, part of frontend code still won't include in this repo.

:link: [KnowsList](https://www.knowslist.com/) :point_left: View the live demo


## Screenshots

- Homepage
![](https://github.com/ycy-tw/blog-platform-django/blob/91d9370bc365353d02b71e53dbac52b4c4d0934e/screenshots/home_en.PNG)
- Editor
![](https://github.com/ycy-tw/blog-platform-django/blob/91d9370bc365353d02b71e53dbac52b4c4d0934e/screenshots/editor_en.PNG)
- Article
![](https://github.com/ycy-tw/blog-platform-django/blob/91d9370bc365353d02b71e53dbac52b4c4d0934e/screenshots/article_en.PNG)
- Related Posts & Comment
![](https://github.com/ycy-tw/blog-platform-django/blob/91d9370bc365353d02b71e53dbac52b4c4d0934e/screenshots/rel_comment_en.PNG)
- Search
![](https://github.com/ycy-tw/blog-platform-django/blob/91d9370bc365353d02b71e53dbac52b4c4d0934e/screenshots/search_en.PNG)
- Profile
![](https://github.com/ycy-tw/blog-platform-django/blob/91d9370bc365353d02b71e53dbac52b4c4d0934e/screenshots/profile_en.PNG)
- Following
![](https://github.com/ycy-tw/blog-platform-django/blob/91d9370bc365353d02b71e53dbac52b4c4d0934e/screenshots/following_en.PNG)
- Notification
![](https://github.com/ycy-tw/blog-platform-django/blob/91d9370bc365353d02b71e53dbac52b4c4d0934e/screenshots/notification_en.PNG)
- Loc & Lang
![](https://github.com/ycy-tw/blog-platform-django/blob/91d9370bc365353d02b71e53dbac52b4c4d0934e/screenshots/loc_lang_en.PNG)
- Stats
![](https://github.com/ycy-tw/blog-platform-django/blob/91d9370bc365353d02b71e53dbac52b4c4d0934e/screenshots/stats_en.PNG)
- Login
![](https://github.com/ycy-tw/blog-platform-django/blob/91d9370bc365353d02b71e53dbac52b4c4d0934e/screenshots/login_en.PNG)
- Social Auth(Gmail)
![](https://github.com/ycy-tw/blog-platform-django/blob/91d9370bc365353d02b71e53dbac52b4c4d0934e/screenshots/gmail_auth.PNG)
- Google Analytics embedded
![](https://github.com/ycy-tw/blog-platform-django/blob/91d9370bc365353d02b71e53dbac52b4c4d0934e/screenshots/ga.PNG)
- Routine Task by Celery and Redis
![](https://github.com/ycy-tw/blog-platform-django/blob/91d9370bc365353d02b71e53dbac52b4c4d0934e/screenshots/celery.PNG)

## Features

- Routine task for updating article views (Celery + Redis + GA4 API).
- Sign in via third-party accounts (Gmail).
- Tags for each article (django-taggit).
- Notification (Django signal).
- Responsive web design (RWD).
- Internationalization (i18n).
- Localization (pytz).
- Deployment (Heroku).
- What you see is what you get (CKeditor5).
- Use GA4 to observe user behavior.


## Techniques & tools
### Backend
- [Django(3.2)](https://www.djangoproject.com/)
    - custom user model
    - form
    - signal
    - i18n
    - email
    - fixtures
- [social-auth-app-django](https://github.com/python-social-auth/social-app-django)
    - [Gmail](https://python-social-auth.readthedocs.io/en/latest/configuration/django.html)
- [Celery](https://docs.celeryq.dev/en/stable/getting-started/introduction.html)
- [Redis](https://docs.redis.com/latest/rs/references/client_references/client_python/)
- [GA4 API](https://developers.google.com/analytics/devguides/reporting/data/v1)
- [AWS S3](https://aws.amazon.com/s3/)

### Frontend
- [Bootstrap5](https://getbootstrap.com/)
    - [Bootstrap Tags Input](https://bootstrap-tagsinput.github.io/bootstrap-tagsinput/examples/)
- HTML
- CSS
- JavaScript
- [jQuery](https://jquery.com/)
    - [Ajax](https://api.jquery.com/jquery.ajax/)
    - [Datatable](https://datatables.net/)
    - [Autocomplete](https://jqueryui.com/autocomplete/)
    - [TOC](https://ndabas.github.io/toc/)
- [Themeforest](https://themeforest.net/)

### Database
- PostgreSQL

#### ERD(main models)

![](https://github.com/ycy-tw/blog-platform-django/blob/91d9370bc365353d02b71e53dbac52b4c4d0934e/screenshots/ERD.PNG)


### Deployment

[Heroku](https://www.heroku.com/)


### Structure

![](https://github.com/ycy-tw/blog-platform-django/blob/91d9370bc365353d02b71e53dbac52b4c4d0934e/screenshots/structure.PNG)


## Set up
### Build virtual environment
```
virtaulenv env
env\Scripts\activate
pip install -r requirements.txt
```

### Django initial
```
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
visit http://127.0.0.1:8000/


### Git
```git
git init
git add .
git commit -m "first commit"
git push
```

### Heroku
```
git push heroku master
heroku logs
```

### Translation
```
python manage.py makemessages -l <language> -i env
python manage.py compilemessages
```

### Create & load fixtures
```
python manage.py dumpdata app.Model --indent 4 > fixtures/Model.json
python manage.py loaddata fixtures/Model.json --app app.Model
```

## Reference
- [Login page](https://codepen.io/BetaNow/pen/zYNPPJe)


