from django.conf.urls import patterns, include, url
from django.contrib import admin

import users.views 

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'library.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', users.views.ListUserView.as_view(),
        name='users-list',),
    url(r'^new$', users.views.CreateUserView.as_view(),
        name='users-new',),
)
