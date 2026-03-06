from django.contrib import admin
from django.urls import include, path

from todos.views import BrandedLoginView, LandingView, SignUpView, logout_view

urlpatterns = [
    path('', LandingView.as_view(), name='landing'),
    path('accounts/login/', BrandedLoginView.as_view(), name='login'),
    path('accounts/register/', SignUpView.as_view(), name='signup'),
    path('accounts/logout/', logout_view, name='logout'),
    path('todos/', include('todos.urls')),
    path('admin/', admin.site.urls),
]
