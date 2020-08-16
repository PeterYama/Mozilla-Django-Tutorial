from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from catalog.views import BookViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'books', BookViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('catalog/', include('catalog.urls')),
    # Add Django standard Authentication
    path('accounts/', include('django.contrib.auth.urls')),
    path('', RedirectView.as_view(url='catalog/')),
    # 3rd parties routes
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
