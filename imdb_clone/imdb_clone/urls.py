
from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('clone_api_app.urls')),
    path('account/', include('user_app.urls')),
    path('api-auth', include('rest_framework.urls'))
]
