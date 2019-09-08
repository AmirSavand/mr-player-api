from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework.documentation import include_docs_urls
from rest_framework_jwt.views import obtain_jwt_token

from account.views import UserViewSet, AccountViewSet
from mrp.settings import ADMIN_URL
from party.views import PartyViewSet, PartyUserViewSet, PartyCategoryViewSet
from song.views import SongViewSet, SongCategoryViewSet

router = routers.DefaultRouter()

router.register('users', UserViewSet, basename='User')
router.register('accounts', AccountViewSet, basename='Account')
router.register('parties', PartyViewSet, basename='Party')
router.register('party-users', PartyUserViewSet, basename='Party Users')
router.register('party-categories', PartyCategoryViewSet, basename='Party Categories')
router.register('songs', SongViewSet, basename='Song')
router.register('song-categories', SongCategoryViewSet, basename='Song Categories')

urlpatterns = router.urls
urlpatterns += (
    path(ADMIN_URL, admin.site.urls),
    path('docs/', include_docs_urls(title='PlayzEM API')),
    path('auth/', include('rest_framework.urls')),
    path('auth/', obtain_jwt_token),
)
