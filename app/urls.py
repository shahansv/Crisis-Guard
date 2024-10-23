
from django.contrib import admin
from django.urls import path, include

from app import views

urlpatterns = [
    path('',views.login),
    path('login_post',views.login_post,name='login_post'),
    path('admin_home_page',views.admin_home_page,name='admin_home_page'),
    path('emergency_response_team_home_page',views.emergency_response_team_home_page),

    path('admin_add_camp_coordinator',views.admin_add_camp_coordinator),
    path('admin_add_camp_coordinator_post',views.admin_add_camp_coordinator_post),

    path('admin_add_camp',views.admin_add_camp),
    path('admin_add_camp_post', views.admin_add_camp_post),

    path('admin_add_emergency_team',views.admin_add_emergency_team),

    path('admin_add_guideline',views.admin_add_guideline),
    path('admin_add_guideline_post', views.admin_add_guideline_post),


    path('admin_add_notification',views.admin_add_notification),
    path('admin_add_notification_post',views.admin_add_notification_post),

    path('admin_view_notification',views.admin_view_notification),


    path('admin_manage_camp_coordinator',views.admin_manage_camp_coordinator),
    path('admin_delete_camp_coordinator/<id>',views.admin_delete_camp_coordinator),
    path('admin_delete_camp/<id>',views.admin_delete_camp),
    path('coordinator_delete_member/<id>',views.coordinator_delete_member),

    path('admin_delete_notification/<id>',views.admin_delete_notification),

    path('admin_manage_notification',views.admin_manage_notification),
    path('admin_reply_complaint',views.admin_reply_complaint),

    path('admin_edit_camp/<id>',views.admin_edit_camp),
    path('admin_edit_camp_post',views.admin_edit_camp_post),

    path('admin_edit_camp_coordinator/<id>', views.admin_edit_camp_coordinator),
    path('admin_edit_camp_coordinator_post', views.admin_edit_camp_coordinator_post),

    path ('coordinator_home_page',views.coordinator_home_page),
    path('search_camp',views.search_camp),
    path('search_member',views.search_member),
    path('search_coordinator',views.search_coordinator),
    path('search_complaint',views.search_complaint),
    path('search_ERT',views.search_ERT),

    path('admin_accept_ERT/<id>',views.admin_accept_ERT),
    path('admin_reject_ERT/<id>',views.admin_reject_ERT),

    path('coordinator_add_member', views.coordinator_add_member),
    path('coordinator_view_members',views.coordinator_view_members),
    path('coordinator_add_member_post',views.coordinator_add_member_post),


    path('admin_verify_emergency_team',views.admin_verify_emergency_team),

    path('admin_view_camp',views.admin_view_camp),
    path('admin_view_camplaint',views.admin_view_camplaint),

    path('admin_view_guideline',views.admin_view_guideline),
    path('admin_view_guideline_post',views.admin_view_guideline),


    path('camp_coordinator_add_needs',views.camp_coordinator_add_needs),



    path('coordinator_add_volunteer_post',views.coordinator_add_volunteer_post),
    path('coordinator_view_volunteer',views.coordinator_view_volunteer),



    path('camp_coordinator_view_medical_request',views.camp_coordinator_view_medical_request),
    path('camp_coordinator_view_needs',views.camp_coordinator_view_needs),

    path('coordinator_add_stock', views.coordinator_add_stock),
    path('coordinator_add_stock_post',views.coordinator_add_stock_post),
    path('coordinator_view_stock',views.coordinator_view_stock),

    path('coordinator_edit_member/<id>',views.coordinator_edit_member),

    path('coordinator_edit_member_post',views.coordinator_edit_member_post),

    path('emergency_response_tean_add_emergency_request',views.emergency_response_tean_add_emergency_request),
    path('emergency_response_tean_view_emergency_request',views.emergency_response_tean_view_emergency_request),


    path('coordinator_register_missing_asset',views.coordinator_register_missing_asset),
    path('coordinator_register_missing_asset_post',views.coordinator_register_missing_asset_post),
    path('coordinator_view_missing_asset_registration', views.coordinator_view_missing_asset_registration),

    path('coordinator_edit_asset_registration/<id>',views.coordinator_edit_asset_registration),
    path('coordinator_edit_asset_registration_post', views.coordinator_edit_asset_registration_post),
    path('coordinator_delete_asset_registration/<id>',views.coordinator_delete_asset_registration),

    path('coordinator_add_needs',views.coordinator_add_needs),
    path('coordinator_add_needs_post',views.coordinator_add_needs_post),
    path('coordinator_view_needs', views.coordinator_view_needs),

    path('coordinator_edit_needs/<id>',views.coordinator_edit_needs),
    path('coordinator_edit_needs_post', views.coordinator_edit_needs_post),

    path('coordinator_delete_needs/<id>', views.coordinator_delete_needs),


    path('coordinator_add_volunteer',views.coordinator_add_volunteer),
    path('coordinator_add_volunteer_post',views.coordinator_add_volunteer_post),
    

]
