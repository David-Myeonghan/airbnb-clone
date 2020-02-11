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
   (So that to prevent all common model from 'copy and paste' to all models that need common field('created', 'updated') in otehr apps) - All the other models, except user model, will be extended from 'core' model. - in order not to register 'core' into the DB, add Meta(abstract model, which is the model not go to DB, like AbstractUser in 'users' app).
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
        - when users click a github login, it will redirect to github. if users login and accept application, github will redirect to here back again.

    # Create OAuth app in Github
        - 'Authorization callback URL' is where github sends our user back when accepted.
        - save client id and client secret in .env
        - in 'github_login view', redirect users to github with setting clientID, clientURI, and scope
        - in Mode, Add LOGIN_CHOICES, and field 'login_method'

    # When users redirect back to my site,
        - Githib gives 'code' which can exchange with access_token that is able to access to github api.
        - Post the code to the designated url, with the help of 'pipenv install requests'.
        - The 'code' is valid for 10 minutes and can be used once.
        - When the code is used twice, then there gonna be an error.

    # Make a request to Github
        - if you get the access token from the response, request to Github API.
        - (Make suer your name, email, bio are typed correctly and public in your Github account)

        - If a user already exists with email, make the user login.
        - If a user has no account with the email, create a new account.
        - in Models, add a new field login_method whith login choices.

# 18. Kakao Login

    # Almost same with the github login. Refer to "https://developers.kakao.com/docs/restapi/user-management#%EB%A1%9C%EA%B7%B8%EC%9D%B8"

    # Get profile image from Kakao.
        - in modeal Avatar, save profile_image_url using 'save' method, with 'ContentFile' which makes the contect a raw file.


    # Instead of using 'forms.ModelForm' in SignUpForm, you can extend this from Django 'UserCreationForm'
        - don't need to devise all that clean and save method.
        - you can override Django's default form.
        - but you need to use 'username' to create an account. Get username typed from users, and label it email as if it's email=username.

        - if you don't want to use UserCreationFrom but want to use password validator, import and use passwordvalidator only.

# 19. Tailwind CSS

    # utility framework
        - has many CSS property as classes
        - need less knoweledge about CSS
        - use Gulp to use tailwind CSS

    # Install tailwindcss
        - install "autoprefixer", "gulp", "gulp-csso", "gulp-postcss", "gulp-sass", "node-sass", "tailwindcss"
        - npx tailwind init
        - set gulpfile.js
        - make styles.scss in scss in assets folder.

        - in styles.scss, can write sass code and there is a @tailwind directive
        - everytime you run 'npm run css', it will call gulp i created.

        - the one that we gives to the browser is gonna be static/css/styles.css
        - 'assets' folder is for programmer.
        - if you need to edit something, edit it in styles.scss file, not styles.css
        - and run 'npm run css' to apply what you modified in styles.scss, but not need to when you modify in html tag.

        - make static folder to be exposed to browser.
        - set 'STATICFILES_DIRS'
        - add link in base.html

# 20. Tailwind CSS

    # Size of Tailwind CSS
        - 'em'  = em 1em. 1 * font size. 2em = 2 * font size.
        - 'rem' = root em. connected to root font size. By default, root font size is 16. if width= 0.5rem, then (by default) font size is 8px.

    # container
        - width: 100%, by default.

    # @apply
        - Instead of long class names, make these into one class including all things using @apply
        - or, customise and extend by editing tailwind.config.js, if you think there are few lists of word to use in Tailwind class name.

    # responsive design
        - mobile-first. all property will work on mobiles. and adapt the screen to bigger size. (small screen first -> large screen later)
        - very easy to make responsive design. when it's large, 'lg: (width)', if's medium, 'md: ...'. No need to small screen as this is mobile-first.

    # Making Errors!
        - If you're going to make non-field errors, make non_field_errors in html.
        - Know that how you can create errors when there's errors in manual, and do it in a automatical way using all fields united.

# 21. Django messages framework

     - Kind of one-time notification to users
     - another HTML template on screens.
     - use animation to beautify

# 22. User profile view

    # Using DetailView and absolute url

    # get_absolute_url
        - use this if you want to go to user profile page in Admin panel.
        - But do not let users changed by typing other users' pk numbers. or something. Don't let the Context changed.
        - get_context_data. this allows you to get more context data.


    # UpdateView
        - It allows users to change their contents of fields in Model.

        # when uploading files, in form HTML, enctype="multipart/form-data' is needed to upload files.

    # PasswordChangeView
        - This takes users to admin panel, which is not good.
        - Make new template.

    # Recommendation
        - When labelling input fields, use django label, not placeholders
        - the best thing to control on forms for more controllable is using your own class(model form).

    # To prevent users from accessing to specific urls whom they don't have authority by just typing urls at the address bar on browser,
    (to stop unauthorised access...)
        - Use Django SuccessMessageMixin.
        - Create your own mixins, mixins.py created.

# 23. Room Detail

    # Pluralise

    # Use users.Mixins to prevent unauthorised access.
    # @login_required cheks whether the user is logged in

    # When uploading a photo, it should have a room id.
        - If you're using CreateView, and need to chage the form, then use FormView.

    # Host/Guest mode (Refer doc. How to use sessions)
        - Use session. When users logged in, save info in session, and log out, delete them.
        - to go into the host mode,
        - to leave the host mode.

    # many-to-many is not saved.
        - m2m cannot be saved when you didn't save the object(when commit=False)
        - so save obejct first '.save()' and then call '.save_m2m()'

# 24. Reservation and Reviews

    # Django is not interactive as JS(React)
        - Make a calendar for two months from this month.
        - Use Calendar class (cal.py)

    # To check whether the room on specific date is booked or not, Use 'custom template tags and filters'
        - Make folder 'templatetags'. Do not change folder name.
        - the filter input goes into the argument of the filter's value, and the filter return(replace) something after filtering.
        - Load the tag you wanna use in .html template

    # To know which date is booked, check-in/out date is not enough.
        - need to check each date between check-in/out dates as well . Make it in model.

    # When user clicks a date on calendar,
        - Check whether the room exist, if exist, raise an Error.
        - Check whether the BookedDate does not exist, if not exist, make an reservation.
        - and then, create an reservation object.
        - as we don't use JS, cannot make more than one day(very hard..)

    # Reviews from score 1 to 5.
        - Using MinValueValidator, and MaxValueValidator saves DB from any other score.
        - Protect form as well using min_value, and max_value.

# 25. Translations

    # makemessages, compilemessages

        - insettings, LOCALE_PATHS = (os.path.join(BASE_DIR, "locale"),)
        - 'brew install gettext'
        - 'brew link gettext --force'
        - 'django-admin makemessages --locale=ko
        - and then translate, after install 'gettext' extension.

        - 'django-admin compilemessages'
        - change language in users' session. language is stored in session.

        - a bit of JS in base.html to select language choice and reload

        - Use 'LocaleMiddleware'

        - When you want to translate block of words, use 'blocktrans'
        - When you want to translate block of words in MODEL, use 'gettext_lazy as _'
        - When you want to translate block of words in Messages, use 'gettext_lazy as _'

    # Lists
        - Add a room into user's favourite list.
        - using templatetages, check whether a room is in users' list(on_favs.py)

        - in template, using action, using one url, add and remove a room.

    # Conversations
        - get two participants. user_one: host, user_two: guest
        - using Q objects, which is user to hard query(filtering)

# 26. Deploy on AWS

    # Read AWS Doc - Deploying Django.

    # Using AWS Elastic Beanstalk - which makes a pre-configured server for you
        - Install EBCLI 'pipenv install awsebcli --dev'
        - eb init
        - Select region, aws-access-id and secret-key
        - name, python version
        - code commit -no
        - SSH no - yes if you want to modify server directly.

        - make .ebextensions, and add option_settings.

        (- EB will call 'wsgi.py' to run server, not 'python manage.py runserver'.)

        - eb create 'app name'

        -ERROR   Your WSGIPath refers to a file that does not exist.: Bebause EB takes what is in the git commit. config is not committed.

        - recommendation: create one for test, and create another for production.

        - eb deploy

        ---
        - eb logs shows all logs

        - ModuleNotFoundError: No module named 'django' BEcasue there is no moduele. which is not in pipenv. so, tell EB to install what is in pipenv.
        - 'pip freeze > requirements.txt', or install pipenv-to-requirements. 'install pipenv-to-requirements --dev'
        - 'pipenv_to_requirements -f'
        - AWS EB will find by default 'requirements.txt'
        - and then eb deploy.
