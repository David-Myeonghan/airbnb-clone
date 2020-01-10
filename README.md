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

#3.2

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