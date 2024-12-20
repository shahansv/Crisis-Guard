from django.contrib import admin
from django.urls import path, include
from app import views

urlpatterns = [

# LOGIN PAGE
    path('',views.login),
    path('login_post',views.login_post,name='login_post'),
   
   
# REGISTER EMERGENCY RESPONSE TEAM AND CHECK STATUS 
    path('register_emergency_response_team',views.register_emergency_response_team),
    path('register_emergency_response_team_post',views.register_emergency_response_team_post),
    path('search_emergency_team_status',views.search_emergency_team_status),
    path('ert_registration_status',views.ert_registration_status),





# ***** ADMIN *****
    path('admin_home_page',views.admin_home_page,name='admin_home_page'),


# ADD & MANAGE CAMP
    path('admin_add_camp',views.admin_add_camp),
    path('admin_add_camp_post', views.admin_add_camp_post),
    path('admin_manage_camp',views.admin_manage_camp),
    path('admin_search_camp',views.admin_search_camp),
    path('admin_edit_camp/<id>',views.admin_edit_camp),
    path('admin_edit_camp_post',views.admin_edit_camp_post),
    path('admin_delete_camp/<id>',views.admin_delete_camp),
    path('logout',views.logout),


# ADD & MANAGE CAMP COORDINATOR
    path('admin_add_camp_coordinator',views.admin_add_camp_coordinator),
    path('admin_add_camp_coordinator_post',views.admin_add_camp_coordinator_post),
    path('admin_manage_camp_coordinator',views.admin_manage_camp_coordinator),
    path('admin_search_camp_coordinator',views.admin_search_camp_coordinator),
    path('admin_edit_camp_coordinator/<id>', views.admin_edit_camp_coordinator),
    path('admin_edit_camp_coordinator_post', views.admin_edit_camp_coordinator_post),
    path('admin_delete_camp_coordinator/<id>',views.admin_delete_camp_coordinator),


# ADD & MANAGE GUIDELINES
    path('admin_add_guideline',views.admin_add_guideline),
    path('admin_add_guideline_post', views.admin_add_guideline_post),
    path('admin_manage_guideline',views.admin_manage_guideline),
    path('admin_search_guideline',views.admin_search_guideline),
    path('admin_delete_guideline/<id>',views.admin_delete_guideline),


# VERIFY EMERGENCY TEAM
    path('admin_verify_emergency_team',views.admin_verify_emergency_team),
    path('admin_manage_emergency_team',views.admin_manage_emergency_team),
    path('admin_search_verify_emergency_team',views.admin_search_verify_emergency_team),
    path('admin_search_accept_emergency_team',views.admin_search_accept_emergency_team),
    path('admin_search_reject_emergency_team',views.admin_search_reject_emergency_team),
    path('admin_accept_ERT/<id>',views.admin_accept_ERT),
    path('admin_reject_ERT/<id>',views.admin_reject_ERT),


# MANAGE COMPLAINT
    path('admin_manage_camplaint',views.admin_manage_camplaint),
    path('admin_reply_complaint/<id>',views.admin_reply_complaint),
    path('admin_reply_complaint_post',views.admin_reply_complaint_post),
    path('search_complaint',views.search_complaint),


# MANAGE NOTIFICATION
    path('admin_add_notification',views.admin_add_notification),
    path('admin_add_notification_post',views.admin_add_notification_post),
    path('admin_manage_notification',views.admin_manage_notification),
    path('admin_delete_notification/<id>',views.admin_delete_notification),
    path('admin_edit_notification/<id>',views.admin_edit_notification),
    path('admin_edit_notification_post',views.admin_edit_notification_post),
    path('admin_search_notification',views.admin_search_notification),





# ***** CAMP COORDINATOR *****
    path ('coordinator_home_page',views.coordinator_home_page),


# ADD AND MANAGE STOCK
    path('coordinator_add_stock', views.coordinator_add_stock),
    path('coordinator_add_stock_post',views.coordinator_add_stock_post),
    path('coordinator_manage_stock',views.coordinator_manage_stock),
    path('coordinator_edit_stock/<id>',views.coordinator_edit_stock),
    path('coordinator_edit_stock_post',views.coordinator_edit_stock_post),
    path('coordinator_delete_stock/<id>',views.coordinator_delete_stock),
    path('coordinator_search_stock',views.coordinator_search_stock),


# ADD AND MANAGE MEMBER
    path('coordinator_add_member', views.coordinator_add_member),
    path('coordinator_add_member_post',views.coordinator_add_member_post),
    path('coordinator_manage_members',views.coordinator_manage_members),
    path('coordinator_edit_member/<id>',views.coordinator_edit_member),
    path('coordinator_edit_member_post',views.coordinator_edit_member_post),
    path('coordinator_delete_member/<id>',views.coordinator_delete_member),
    path('coordinator_search_member',views.coordinator_search_member),


# REGISTER AND MANAGE MISSING ASSET
    path('coordinator_register_missing_asset',views.coordinator_register_missing_asset),
    path('coordinator_register_missing_asset_post',views.coordinator_register_missing_asset_post),
    path('coordinator_view_missing_asset_registration', views.coordinator_view_missing_asset_registration),
    path('coordinator_edit_asset_registration/<id>',views.coordinator_edit_asset_registration),
    path('coordinator_edit_asset_registration_post', views.coordinator_edit_asset_registration_post),
    path('coordinator_delete_asset_registration/<id>',views.coordinator_delete_asset_registration),
    path('coordinator_search_asset_registration',views.coordinator_search_asset_registration),


# ADD AND MANAGE NEEDS    
    path('coordinator_add_needs',views.coordinator_add_needs),
    path('coordinator_add_needs_post',views.coordinator_add_needs_post),
    path('coordinator_view_needs', views.coordinator_view_needs),
    path('coordinator_edit_needs/<id>',views.coordinator_edit_needs),
    path('coordinator_edit_needs_post', views.coordinator_edit_needs_post),
    path('coordinator_delete_needs/<id>', views.coordinator_delete_needs),
    path('coordinator_search_needs', views.coordinator_search_needs),


# REGISTER AND MANAGE VOLUNTEER
    path('coordinator_volunteer_registration',views.coordinator_volunteer_registration),
    path('coordinator_volunteer_registration_post',views.coordinator_volunteer_registration_post),
    path('coordinator_manage_volunteer',views.coordinator_manage_volunteer),
    path('coordinator_search_volunteer',views.coordinator_search_volunteer),
    path('coordinator_edit_volunteer/<id>',views.coordinator_edit_volunteer),
    path('coordinator_edit_volunteer_post', views.coordinator_edit_volunteer_post),
    path('coordinator_delete_volunteer/<id>', views.coordinator_delete_volunteer),


# MANAGE MEDICAL REQUEST   
    path('coordinator_manage_medical_request', views.coordinator_manage_medical_request),
    path('coordinator_search_medical_request', views.coordinator_search_medical_request),
    path('coordinator_edit_medical_request_status/<id>', views.coordinator_edit_medical_request_status),
    path('coordinator_edit_medical_request_status_post', views.coordinator_edit_medical_request_status_post),
   




# ***** EMERGENCY RESPONCE TEAM *****

# MANAGE EMERGENCY RESPONSE
    path('emergency_response_team_home_page',views.emergency_response_team_home_page),
    path('emergency_response_tean_view_emergency_request',views.emergency_response_tean_view_emergency_request),
    path('emergency_response_team_search_emergency_request',views.emergency_response_team_search_emergency_request),
    path('emergency_response_edit_emergency_request_status/<id>', views.emergency_response_edit_emergency_request_status),
    path('emergency_response_edit_emergency_request_status_post', views.emergency_response_edit_emergency_request_status_post),

]
