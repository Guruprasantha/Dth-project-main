from django.urls import path,include
from ddh import views

urlpatterns=[
    path('',views.home,name='home'),
    path('login/',views.login,name='login'),
    path('index',views.index,name='index'),
    path('usignin',views.register,name='register'),
    path('logout',views.logout,name='logout'),
    path('newuser',views.newuser,name='newuser'),
    path('combolist',views.combolist,name='combolist'),
    path('channellist',views.channellist,name="channellist"),
    path('add_combo/',views.add_combo,name="add_combo"),
    path('add_combo',views.add_combo,name="add_combo"),
    path('add_channels/<str:id>/',views.add_channels,name="add_channels"),
    path('channel_del/<int:id>',views.channel_del,name="channel_del"),
    path('user_packs',views.user_packs,name="user_packs"),
    path('user_index',views.user_index,name="user_index"),
    path('user_logout',views.user_logout,name="user_logout"),
    path('user_view_pack/<int:id>',views.user_view_pack,name="user_view_pack"),
    path('pack_booking/<int:id>',views.pack_booking,name="pack_booking"),
    path('payment_done/<str:id>',views.payment_done,name="payment_done"),
    path('user_view',views.user_view,name="user_view"),
    path('activate_user/<str:id>',views.activate_user,name="activate_user"),
    path('pack_channel/<int:id>',views.pack_channel,name="pack_channel"),
    path('ex_ch',views.ex_ch,name='ex_ch'),
    path('channel_view_user/<str:id>',views.channel_view_user,name="channel_view_user"),
    ] 