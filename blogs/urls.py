from django.urls import path
from blogs import views
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)

router = DefaultRouter()
router.register('signup', views.UserViewSetView, basename='signup')
router.register('blogs', views.BlogViewSetView, basename='blogs')
router.register('public-blogs', views.PublicBlogViewSetView, basename='public-blogs')
router.register('public-blogs/(?P<pk1>[^/.]+)/comments', views.CommentViewSetView, basename='comments')


urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
] + router.urls
