import notifications

from rn import views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^inbox/notifications/', include(notifications.urls)),
    url(r'', include('user_sessions.urls', 'user_sessions')),

    # url(r'^$', 'rn.views.home', name='home'),
    # url(r'^send_notification/$', 'rn.views.send_notification', name='send_notification'),
    # url(r'^mark_as_read/$', 'rn.views.mark_as_read', name='mark_as_read'),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'admin/login.html'}, name='login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
    url(r'^realtime/$', views.home_realtime, name='home_realtime'),
	url(r'^ajax_send_notification/$', views.ajax_send_notification, name='ajax_send_notification'),
	url(r'^ajax_mark_as_read/$', views.ajax_mark_as_read, name='ajax_mark_as_read'),
    url(r'^update_bid',views.update_bid,name='update_bid'),
    url(r'^raise_bid',views.raise_bid,name='raise_bid'),
    url(r'^send_notification',views.send_notification,name='send_notification'),
    url(r'^timer_update',views.timer_update,name='timer_update'),
    url(r'^treset',views.treset,name='treset'),
    url(r'^$',views.home),
    url(r'^update_player/$',views.update_player,name='update_player'),
    url(r'^bidder_quit/$', views.bidder_quit,name='bidder_quit'),
    (r'^form_search',views.form_search),
    (r'^search_this',views.search_this),
    (r'^submit_data',views.submit_data),
    (r'^login_check',views.login_check),
    (r'^home',views.home),
    (r'^confirm_signup',views.confirm_signup),
    (r'^login_submit',views.login_submit),
    (r'^logout',views.logout),
    (r'^timer/',views.timer),
    (r'^auc_screen',views.auc_screen),
    (r'^setup', views.setup),
    (r'^bidder_signup', views.bidder_signup),
    (r'^select_teams', views.select_team),
    (r'^usr_login', views.usr_login),
    (r'^auction_start', views.auction_start),
    (r'^detail/(?P<player_id>\d+)/$', views.detail),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve',
                 {'document_root': settings.MEDIA_ROOT}),
    )
