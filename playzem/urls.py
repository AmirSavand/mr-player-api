from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework.documentation import include_docs_urls
from rest_framework_jwt.views import obtain_jwt_token

from account.views import UserViewSet, AccountViewSet
from party.views import PartyViewSet, PartyUserViewSet, PartyCategoryViewSet
from playzem.settings import ADMIN_URL
from song.views import SongViewSet, SongCategoryViewSet

router = routers.DefaultRouter()

router.register('user', UserViewSet, basename='User')
router.register('account', AccountViewSet, basename='Account')
router.register('party', PartyViewSet, basename='Party')
router.register('party-user', PartyUserViewSet, basename='Party User')
router.register('party-category', PartyCategoryViewSet, basename='Party Category')
router.register('song', SongViewSet, basename='Song')
router.register('song-category', SongCategoryViewSet, basename='Song Category')

urlpatterns = router.urls
urlpatterns += (
    path(ADMIN_URL, admin.site.urls),
    path('docs/', include_docs_urls(title='PlayzEM API')),
    path('auth/', include('rest_framework.urls')),
    path('auth/', obtain_jwt_token),
)
