# blog-platform-django


這是一個透過Django框架所打造的寫作平台，同時也包含了常見的設交平台功能，例如按讚、追蹤、收藏以集通知功能。

前端模板透過[Themeforest](https://themeforest.net/)所購入，即便我加了很多客製化的CSS，部份的前端程式碼將不會包括在這項專案中。


:link: [KnowsList](https://www.knowslist.com/) :point_left: 點入左邊連結進入專案


## 專案截圖

- 首頁
![](https://github.com/ycy-tw/blog-platform-django/blob/a94944b8d0500a786c21e2df289bdcd5ec8bbb22/screenshots/home_zhhant.PNG)
- 編輯器
![](https://github.com/ycy-tw/blog-platform-django/blob/a94944b8d0500a786c21e2df289bdcd5ec8bbb22/screenshots/editor_zhhant.PNG)
- 文章
![](https://github.com/ycy-tw/blog-platform-django/blob/a94944b8d0500a786c21e2df289bdcd5ec8bbb22/screenshots/article_zhhant.PNG)
- 相關文章 & 留言
![](https://github.com/ycy-tw/blog-platform-django/blob/a94944b8d0500a786c21e2df289bdcd5ec8bbb22/screenshots/rel_comment_zhhant.PNG)
- 搜尋
![](https://github.com/ycy-tw/blog-platform-django/blob/a94944b8d0500a786c21e2df289bdcd5ec8bbb22/screenshots/search_zhhant.PNG)
- 作者簡介
![](https://github.com/ycy-tw/blog-platform-django/blob/a94944b8d0500a786c21e2df289bdcd5ec8bbb22/screenshots/profile_zhhant.PNG)
- 追蹤中
![](https://github.com/ycy-tw/blog-platform-django/blob/a94944b8d0500a786c21e2df289bdcd5ec8bbb22/screenshots/following_zhhant.PNG)
- 通知
![](https://github.com/ycy-tw/blog-platform-django/blob/a94944b8d0500a786c21e2df289bdcd5ec8bbb22/screenshots/notification_zhhant.PNG)
- 時區 & 語言
![](https://github.com/ycy-tw/blog-platform-django/blob/a94944b8d0500a786c21e2df289bdcd5ec8bbb22/screenshots/loc_lang_zhhant.PNG)
- 文章統計
![](https://github.com/ycy-tw/blog-platform-django/blob/a94944b8d0500a786c21e2df289bdcd5ec8bbb22/screenshots/stats_zhhant.PNG)
- 登入
![](https://github.com/ycy-tw/blog-platform-django/blob/a94944b8d0500a786c21e2df289bdcd5ec8bbb22/screenshots/login_zhhant.PNG)
- 透過第三方社群平台登入(Gmail)
![](https://github.com/ycy-tw/blog-platform-django/blob/a94944b8d0500a786c21e2df289bdcd5ec8bbb22/screenshots/gmail_auth.PNG)
- 加入Google Analytics
![](https://github.com/ycy-tw/blog-platform-django/blob/a94944b8d0500a786c21e2df289bdcd5ec8bbb22/screenshots/ga.PNG)
- 透過 Celery and Redis 執行排程任務
![](https://github.com/ycy-tw/blog-platform-django/blob/a94944b8d0500a786c21e2df289bdcd5ec8bbb22/screenshots/celery.PNG)

## 特色

- 自動排程更新文章瀏覽數 (Celery + Redis + GA4 API).
- 透過第三方帳號登入 (Gmail).
- 文章標籤系統 (django-taggit).
- 通知功能 (Django signal).
- 響應式網頁設計' (RWD).
- 翻譯功能 (i18n).
- 時區功能 (pytz).
- 佈署 (Heroku).
- 所見即所得 (CKeditor5).
- 使用 GA4 觀察使用者行為


## 技術 & 工具
### 後端
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

### 前端
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

### 資料庫
- [PostgreSQL](https://www.postgresql.org/)

#### ERD(main models)

![](https://github.com/ycy-tw/blog-platform-django/blob/a94944b8d0500a786c21e2df289bdcd5ec8bbb22/screenshots/ERD.png)


### 佈署

[Heroku](https://www.heroku.com/)


### 架構

![](https://github.com/ycy-tw/blog-platform-django/blob/55c8137b00d3cbb822eb11bfd96a6d929e2e8f88/screenshots/structure.png)


## 前置作業
### 建立虛擬環境
```
virtaulenv env
env\Scripts\activate
pip install -r requirements.txt
```

### Django 初始化
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

### 翻譯
```
python manage.py makemessages -l <language> -i env
python manage.py compilemessages
```

### 製作 & 讀取測試資料
```
python manage.py dumpdata app.Model --indent 4 > fixtures/Model.json
python manage.py loaddata fixtures/Model.json --app app.Model
```

## 參考
- [Login page](https://codepen.io/BetaNow/pen/zYNPPJe)

