# Airbnb Clone

Cloning Airbnb with Python, Django, Tailwind and more...

# Project

- A project consists of several applications.
 Airbnb = Room Management + Review + Users + etc.


1. Create several applications first.
- Describe an application in one sentence, not using 'and'. (Divide and Conquer)
- An application name should be plural, not singular. (rooms, users, reviews, conversations, lists, reservations)

2. User application substitues the default admin
- Customising the admin panel using user app model. (+bio)

# Git
- git add .
- git commit -m "New"
- git push origin master

# 3. User App
- Installed Pillow
- No need to make migrations and migrate when models are changed. forms are just changed.
- Instead, need to migrate when fields are added

- when making model, good to migrate only once. 

- python manage.py makemigrations
- python manage.py migrate
- python manage.py createsuperuser

# 4. Room App
1. to set the Room model, in settings.py in config, Add "rooms.apps.RoomsConfig" in PROJECT_APPS.
2. set models.py in rooms
3. set admin.py in rooms
4. (before migration) make a 'core' app to manage common model fields. 
(So that to prevent all common model from 'copy and paste' to all models that need common field('created', 'updated') in otehr apps)
    - All the other models, except user model, will be extended from 'core' model.
    - in order not to register 'core' into the DB, add Meta(abstract model, which is the model not go to DB, like AbstractUser in 'users' app).
5. Set models.py 
    - Installed django-countries.
    - Connected user_models, using foreign key, from users app to add a field called host in rooms app.
    - Connected RoomType to a room model using many to many field.
    - (when one needs to be connected, use foreign key. or many things need to be connected, use Many to many field)

# 5. All Other Apps
1. Set reviews' Model, and review's admin panel
2. Set reservations' model, and admin panel
3. Set lists' model, and admin panel
4. Set conversations' model, and admin panel

# 6. Room admin
1. Set RoomAdmin to add (better) filter search (list_display, list_filter, search_fields, filter_horizontal, fieldsets, ordering).
2. Make count_amenities function
    - A function inside of admin class gets self(RoomAdmin), and obj(current row) as a parameter

# If you interact with your project using Django configuration and model?
    1. (in your terminal) pipenv shell
    2. python manage.py shell
    3. (from users.models import User)

    - Use these
    - 'vars' returns dict. vars(User)
    - 'dir' returns list

    - Use User manager. this gives us the DB-abstraction API(Query set API). NO need to make SQL queries.
    e.g. 'User.objects.all()' gives the list(Query set) that shows all users
    
    >>> all_user = User.objects.all()
    >>> all_user.filter(superhost=True)
    >>> david = User.objects.get(username="david")
    >>> vars(david)
    >>> dir(david)

    - Set is the way that the target of the foreign key gets the element.
    - How do we change the (name of) set? - by setting 'related_name' in model.
    - 'related_name' is the way the target finds you.
    - Important to understand how in the code a object is able to access to foreign keys.

    - 'related_name' is for Django ORM model. ORM model is for communicating with DB without query.
    - 따라서 몇 가지 related_name을 생성해 줄 때 알아야 할 것이 있다.
    - 폴인키로 연결시켜 놓은 클래스에 related_name = comment라고 해놓으면 user.comment라는 것이 comment모델에 생기는 것이 아나리 comment가 참조하고 있는 user모델에 생긴다.
    
    =>>> 따라서 참조해준 객체 입장에서 related_name을 설정해줘야 한다. 
    =>>> 따라서 related_name을 쓸 때는 참조해준 객체 입장에서 생각한다. e.g. count_messages in conversations app.

    https://fabl1106.github.io/django/2019/05/27/Django-26.-%EC%9E%A5%EA%B3%A0-related_name-%EC%84%A4%EC%A0%95%EB%B0%A9%EB%B2%95.html

    - many to many fields are not like sets.
    >>> from rooms.models import Room
    >>> room = Room.objects.get(pk=1)   # pk = id.
    >>> room.amenities
    >>> room.amenities.all(). gives query set. You can all(), count(), filter(), etc.
    
    - Find all rooms that have shower amenity?
    >>> from rooms.models import Amenity
    >>> Amenity.objects.all()
    >>> a = amenity.objects.get(id=1)
    >>> a.room_set.all()

# 8. Admins
    - Make 'related_name' in all models.
    
    - Make more function in users, rooms, reviews admin panel.
    - If you want to use some functions shown to users, not only to admin panel, you can make functions in models
    - The functions for using only in admin panel, make functions in admin panel.
    
    - In reservations app, Make 'total_rating' function that calculates user's average review score.
    - Make 'in_progress' function showing the current date is between check-in and check-out, and 'is_finished'

    - In lists app, make 'count_rooms'

    - In Conversations app, make
    >>> for user in User.objects.all():
    ...     print(user.username)
    ... 
    david
    me

    # To make photos available, set 'MEDIA_ROOT' in settings.
    - 'MEDIA_ROOT' should be absolute filesystem path. (Refer to 'BASE_DIR' in settings)
    - Uploaded photos will be saved in uploads folder.
    - set 'upload_to' to upload media files on wherever you want. (in class)

    # To make photos available in browser, set 'MEDIA_URL' in settings.
    - 'MEDIA_URL' connects media in uploads folder. (handles photos in uploads folder)

    # To make photos available in browser in absolute path, not relative path, set urls.py in config.
    - absolute path showing media file: http://127.0.0.1:8000/media/room_photos/Picture1.png
    - This is different from the way we can serve the files in amazon.
    - (You won't want to save uploaded files in your server, which consumes more spaces in the server, and DB file as well.
    - and you'll have Django server, DB server, and storage server.

    # make thumbnail in photo admin panel
    - Photo is not just a path or file. It is one class that has many filed. You can see it by dir(file), or vars(file).
    - Import and use 'mark_safe'. As Django protects the admin by preventing executing code in input field, we have to mark it safe, saying this is safe code you can execute.

    # Admin more manageable
    - Use 'raw_id_fields' for many users that you cannot just scrollable.
    - Use 'InlineModelAdmin' to make admin in admin. to edit models on the same page as a parent model.

    # Intercept the way of save() method in model. i.e. city: 's'eoul -> make 'S'eoul and save.
    - Use 'super' when overriding save() method. 
    - 'save()' is for the whole model saving, including admin panel.
    - NB. 'save_model()' is just for admin saving. 

# 9. Custom Commands and Seeding (To make fake data)
    # Make custom commands in management folder in any app. 
    - This will give us the command that I made.

    # Make amenities object using code. (not manually in admin panel)
    - 'seed_amenities.py' - this will make amenity objects, using command "python manage.py seed_amenities".
    - 'seed_facilities.py' - this creates facilities.

    # Make fake data - using 'django_seed'
    - install Django-seed 'pipenv install django_seed'
    - when using seed, refer to https://github.com/Brobin/django-seed/issues/65
    - 'seed_users.py' creates 50 users. 'python manage.py seed_users --number 50'
    
    - Make room type yourself. shared rooom, hotel room, entire house, private room.

    - 'seed_rooms.py' creates rooms, but Room model cannnot be created without foreign key 'host' and 'room_types. So, lambda(anonymous function in JS) is used to put random numbers of users to create rooms.
    - To make moderate random number, not like -19285 guests, Use 'random.randint(1,5)' and 'faker' for appropriate address or something.
    - Need to know that when adding many-to-many field, need to 'add()'

    - 'seed_reviews.py' creates reviews
    - 'seed_lists.py' creates lists. Create lists first and add rooms later.
    - No need to make message and conversation
    - 'seed_reservations.py' creates reservations. starts from today to random(3,25) days.

# 10. Views and Urls
    # URLs is the way we direct request

    # Views are the way we answer to the request
    - view is a function

    # Urls starts with '/room' will be managed in rooms app. and etc.
    - urls starts with '/' nothing will be managed in core app.
    - When using a namespace, Set the app_name attribute in the included app.

    # When we go to views through urls, it creates HttpRequest, and you need to answer this with Httpresponse.
    - Instead of using Httpresponse manually all the time, we'll use render using template(just an html).

    1. Make 'templates' folder, and make templates
    - Set templates directory in setting.py

    -When displaying a variable sent from view, use {{something}}
    -When using a logic, use i.e. {% if %} {% endif %} No need to indent or something.

    2. Make base template and inherit from other html file.
    - In template, pretending it is in one folder. i.e. {% extends "base.html" %}
    
    3. Extend a children template using a 'block' to put something from a parent template.
    - You can create blocks as many as you want. 
    - Break a big html file into small pieces(Divide and Conquer)
        - That would be easy to work with CSS.

    4. Only show 10-20 rooms on one page (Pagination)
        1. Manual page without Django
            1) limit the number of rooms. i.e. all_rooms = models.Room.objects.all()[:10]. [offset:limit]
            Django's sequence point is at the end of line..? so, until the next line, current line will not be executed.
            
            When QuerySets are evaluated? - Internally, a QuerySet can be constructed, filtered, sliced, and generally passed around without actually hitting the database. No database activity actually occurs until you do something to evaluate the queryset.
            
            QuerySets are lazy – the act of creating a QuerySet doesn’t involve any database activity. You can stack filters together all day long, and Django won’t actually run the query until the QuerySet is evaluated. Take a look at this example:

            - everything from the url is 'GET request'
            - Show which page we are seeing. Show which page is gonna be the last page.
            - Make arrow 
            - In Django template, all Python code is not working. If custom logic is needed, pass what you need from the context in python view.
            - Or, use Django's template filter
            
            2) To make previous button, need to know whether there is a previous page.


        2. with Django(shortcut)
            - Use Paginator!

        3. without code.

    # Catch an exception using try and catch.

    # Use 'ListView' to represent a list of objects instead of setting many settings.
        - no need to render, return or anything on this view, using 'as_view()'
        - only by configuring model, the 'ListView' know what should be displayd on this view.
        - hard to know configuration of this view. Refer to here. "http://ccbv.co.uk"
        - get 'paginator' for free
        
        - "Function based view" -> code should be explicit!, if you wanna see super controll, and see what's going on. vs "Class vased view" -> too easy to use, very flexible, function can be added

# 12. Detail View

    # Make 'room_detail'
    # Make 'urls.py' inside of the rooms and Set url in order to see the details of specific rooms 'rooms/1'
    # Refer 'Django path", 'url dispatcher'

    # Get absolute url, using "get_absolute_url" from django provided. 
     - namespace (in config urls.py) >>> name (in each app's urls.py)

    # Show facilities, amenities, and house rules in 'room_detail' view
     - Use try and 'except' to handle exception handling invalid room # in urls.

        # Make your own 'not found'(404) page. Browser won't record 404.
        - Django automatically found andset 404.html and show when 404. 404.html should be at top in templates folder.
        - Needs to be DEBUG = False in settings.
    
    # Change function based view 'room_detail' to class based view.
     - in <int:pk>, pk is default, so url already knows it.

# 13. Search View

    # Search bar should be on the header.
        - set search.html and set header.html.

    # Hide search bar in search page by doulbing block. If you are in search page, search bar from base.html won't be displayed.

    # Make <select> of city, country, and room type to search
        - put them in <form></form>

    # Make price, guest, bed, bedroom, bath search
        - 'value' in HTML put its value from URL back to select on view.

    # Amenities, Facilities, House rules
        - Use 'getlist' to get list of selected items
        - Use 'slugify' filter as 'amenity.pk' is integer and 'selected_amenities' is string.

    # Search or filter like a boss, using Django 'Field lookups' of Queryset API.

    # The Forms API generates all that things for search 'form'.
        - Make 'forms.py' in an app.
        - put '{{form}} in search.html
        - The form field rends widget. Widget is HTML element. Widget can be changed.

    # Country can be selected by importing django_countres.fields import CountryField

    # To make the form remember the select you did, set 'request.GET' in the form in views.py
        
        - when we go to /rooms/search directly, it will give you an error, becasue we are giving this form the data.
        - unbound form: the moment you give the data to form, it will be validated
        - to be bound form: when somethings's put in the form, this will validate the data, which is connected to data.
        - So it needs to be checked if something is in the url.

    # The form make HTML, and validate the data clean
        - Using Python is enough for making web. no much efforts on HTML.
        
# 14. Login/Logout
    # Use email as an username.

    # CSRF!

    # Make login form using Django Form
        - after get, and post method on the LoginView, the typed info should be validated using 'clean_000' method on forms.py
        - cleaned_data is the result of cleaning all the field
        - if clean_ method is made, and return nothing, it deletes the typed info

        - Use 'clean' method to validate email and password together, not seperate validating as email(username) and password is dependent each other.
        - if you use 'clean' method (from forms.py), return(get and use) cleaned_data always (in views.py).

        - Django 'Context processor' can access to cookies, and look for user in cookies and put them in the templates. so, the template can user.is_authenticated.

    # You can use Django LoginView(LoginForm). 
        - Use 'reverse_lazy' from Django urls to execute the urls, not immediately but when it needs to be.
        - No need to initiate

# 15. Sign Up

    # Use FormView for easy-making singup
        1. Get user info from the forms
        2. Validate these
        3. save it as an object.

    # Use Django ModelForm to make an object easy.
        - it already has clean, save method, and also can validate the uniquness of field in a model.
        - make it commit=False, which is to create an Django object, but put it on DB.

# 16. Email Verification
    # Using Django sending_email would go to junk box.
    # Use mailgun, and 'pipenv install django-dotenv' and set EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD on settings and .env
        - (if you cannot send an email, restart your terminal)
        - Process: When an user makes an account, send an email with random letter link. 
        - and, The view which can take the random letter, look for an user from the link, and if there is the email_secret, then, it's verified.
        
        - Using Python uuid, make 20 digits hex.
        - Send string text and html message as well. 'strip_tags()' enables you to send html messaged with html stripped.
            - some computers don't take html.
        - Make it template what you wanna send.
        - Make complete_verification View(function based)


# 17. Github Login
    # Any social media supports OAuth, you can do login with this.
        - Github Login, and Kakao Login.