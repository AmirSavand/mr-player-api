from django.contrib import admin
from django.urls import path, include
from rest_auth.views import PasswordResetView, PasswordResetConfirmView, PasswordChangeView
from rest_framework import routers
from rest_framework.documentation import include_docs_urls
from rest_framework_jwt.views import obtain_jwt_token

from account.views import UserViewSet, AccountViewSet
from like.views import LikeViewSet
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
router.register('like', LikeViewSet, basename='Like')

urlpatterns = router.urls
urlpatterns += (
    path(ADMIN_URL, admin.site.urls),
    path('docs/', include_docs_urls(title='PlayzEM API')),
    path('auth/', include('rest_framework.urls')),
    path('auth/', obtain_jwt_token),
    path('auth/password/change/', PasswordChangeView.as_view(), name='rest_password_change'),
    path('auth/password/reset/', PasswordResetView.as_view(), name='rest_password_reset'),
    path('auth/password/reset/confirm/', PasswordResetConfirmView.as_view(), name='rest_password_reset_confirm'),
)
