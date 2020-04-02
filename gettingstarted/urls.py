from django.conf import settings
from django.urls import path, include
from django.contrib import admin

admin.autodiscover()

urlpatterns = [
    path('',          include('core.urls', namespace='core')),
    path("admin/",    admin.site.urls),
    path('accounts/', include('allauth.urls'))
]

# if settings.DEBUG:
#     import debug_toolbar 
#     urlpatterns += [path('__debug__',include(debug_toolbar.urls))]
