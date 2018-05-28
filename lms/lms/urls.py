from django.conf.urls import url, include
from django.contrib import admin
from .views import landing_page
from django.conf import settings
from django.conf.urls.static import static
from ajax_select import urls as ajax_select_urls

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', landing_page, name='landing_page'),
    url(r'^accounts/', include(('accounts.urls'), namespace='accounts')),
    url(r'^classroom/', include(('classroom.urls'), namespace='classroom')),
    url(r'^select2/', include('select2.urls')),
    url(r'^ajax_select/', include(ajax_select_urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
