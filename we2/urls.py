from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from user.views import LanguageSelectionView
from .views import set_language

# These patterns are NOT translated and are accessible from the root
urlpatterns = [
    path('admin/', admin.site.urls),
    path('set_language/', set_language, name='set_language'),
    path('', LanguageSelectionView.as_view(), name='language-selection-root'),
]

# These patterns ARE translated and will be prefixed with the language code (e.g., /en/, /fa/)
urlpatterns += i18n_patterns(
    path('', include('user.urls')),
    path('insight/', include('insight.urls')),
)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
