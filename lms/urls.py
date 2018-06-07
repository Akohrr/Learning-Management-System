from django.conf.urls import url, include
from django.contrib import admin
from .views import landing_page, home_page
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', landing_page, name='landing_page'),
    url(r'^home/$', home_page, name='home'),
    url(r'^accounts/', include(('accounts.urls'), namespace='accounts')),
    url(r'^classroom/', include(('classroom.urls'), namespace='classroom')),
    url(r'^admin/', admin.site.urls),

]

# if settings.DEBUG:
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
