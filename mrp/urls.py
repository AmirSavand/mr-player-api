"""mrp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path, include
from rest_framework import routers
from rest_framework.documentation import include_docs_urls
from rest_framework_jwt.views import obtain_jwt_token

from account.views import UserViewSet
from mrp.settings import ADMIN_URL
from song.views import SongViewSet, SongPartyViewSet

router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('songs', SongViewSet)
router.register('song-parties', SongPartyViewSet)

urlpatterns = router.urls
urlpatterns += [
    path(ADMIN_URL, admin.site.urls),
    path('docs/', include_docs_urls(title='Nano Gaming API')),
    path('auth/', include('rest_framework.urls')),
    path('auth/', obtain_jwt_token),
]
