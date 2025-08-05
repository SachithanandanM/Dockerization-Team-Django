from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from users import views as user_views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # Home and Authentication
    path('', user_views.home, name='home'),
    path('signup/', user_views.signup, name='signup'),
    path('signin/', auth_views.LoginView.as_view(template_name='signin.html'), name='signin'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Products
    path('categories/', include('products.urls')),

    # JWT endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include('users.urls')),
    
    # Media files (development only)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)