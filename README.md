# Airbnb Clone

Cloning Airbnb with Python, Django, Tailwind and more...

# Project

A project consists of several applications.
Airbnb = Room Management + Review + Users + etc.

Describe an application in one sentence, not using 'and'.
Divide and Conquer.

Create several applications first.

- An application name should be plural, not singular. (rooms, users, reviews, conversations, lists, reservations)

User application substitues the default admin

- Customising the admin panel using user app model. (+bio)

# Git

git add .
git commit -m "New"
git push origin master

# 3.2

- Installed Pillow
- No need to make migrations and migrate when models are changed. forms are just changed.
- Instead, need to migrate when fields are added

- when making model, good to migrate only once. 

- python manage.py makemigrations
- python manage.py migrate
- python manage.py createsuperuser

# 4 Room App
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

# 5 All Other Apps
1. Set reviews' Model, and review's admin panel
2. Set reservations' model, and admin panel
3. Set lists' model, and admin panel
4. Set conversations' model, and admin panel

# 6 Room admin
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

# 8 Admins
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

# 9 Custom Commands and Seeding (To make fake data)
    # Make custom commands in management folder in any app. 
    - This will give us the command that I made.

    # Make amenities object using code. (not manually in admin panel)
    - 'seed_amenities.py' - this will make amenity objects, using command 'python manage.py seed_amenities'.
    - 'seed_facilities.py' - this creates facilities.

    # Make fake data - using 'django_seed'
    - install Django-seed 'pipenv install django_seed'
    - when using seed, refer to https://github.com/Brobin/django-seed/issues/65
    - 'seed_users.py' creates 50 users. 'python manage.py seed_users --number 50'
    
    - 'seed_rooms.py' creates rooms, but Room model cannnot be created without foreign key 'host' and 'room_types. So, lambda(anonymous function in JS) is used to put random numbers of users to create rooms.
    - To make moderate random number, not like -19285 guests, Use 'random.randint(1,5)' and 'faker' for appropriate address or something.


