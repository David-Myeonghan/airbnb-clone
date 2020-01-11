"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings  # mirrors(import) settings.
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
]

# This is different from the way we can serve the files in amazon.
# (You won't want to save uploaded files in your server, which consumes more spaces in the server, and DB file as well.
# and you'll have Django server, DB server, and storage server.
if settings.DEBUG:  # if this is being developing, serve the files in uplodas folder.
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # If url is urlpattern/media_url, it shows media_root. (connects url with folder)
