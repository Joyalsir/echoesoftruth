"""
URL configuration for cybercrime_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from cybercrime_app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('ad',views.admin),
    path('',views.index,name='index'),
    path('view_login/',views.view_login,name='view_login'),
    path('user_logout',views.user_logout,name='user_logout'),
    path('admin_dashboard',views.admin_dashboard, name='admin_dashboard'),
    path('investigator_dashboard',views.investigator_dashboard,name='investigator_dashboard'),
    path('Court_dashboard',views.Court_dashboard,name='Court_dashboard'),

    path('investigator_register/', views.investigator_register, name='investigator_register'),
    path('victim_register/', views.victim_register, name='victim_register'),

    path('display_all_investigators/', views.display_all_investigators, name='display_all_investigators'),
    path('accept_investigator/<int:investigator_id>/', views.accept_investigator, name='accept_investigator'),
    path('reject_investigator/<int:investigator_id>/', views.reject_investigator, name='reject_investigator'),

    path('display_all_victims/', views.display_all_victims, name='display_all_victims'),
    path('accept_victim/<int:victim_id>/', views.accept_victim, name='accept_victim'),
    path('reject_victim/<int:victim_id>/', views.reject_victim, name='reject_victim'),
    path('investigator_profile/', views.investigator_profile, name='investigator_profile'),
    path('edit_investigator_profile/', views.edit_investigator_profile, name='edit_investigator_profile'),

    path('victim_profile/', views.victim_profile, name='victim_profile'),
    path('victim/edit-profile/', views.edit_victim_profile, name='edit_victim_profile'),
    path('apply_case/',views.apply_case,name='apply_case'),
    path('victim_cases/', views.victim_cases, name='victim_cases'),
    path('edit_case/<int:case_id>/', views.edit_case, name='edit_case'),

    path('delete_case/<int:case_id>/', views.delete_case, name='delete_case'),

    path('investigator_cases', views.investigator_cases, name='investigator_cases'),
    path("update_case_status/", views.update_case_status, name="update_case_status"),

    path('evidence_collection/<int:case_id>/', views.evidence_collection, name='evidence_collection'),

    path('display_evidence_collection',views.display_evidence_collection, name='display_evidence_collection'),
    path('add_suspect/', views.add_suspect, name='add_suspect'),

    path('display_suspects/',views.display_suspects,name='display_suspects'),

    path('edit_suspect/<int:suspect_id>/', views.edit_suspect, name='edit_suspect'),
    path('delete_suspect/<int:suspect_id>/', views.delete_suspect, name='delete_suspect'),

    path('view_evidence/<int:case_id>/', views.view_evidence, name='view_evidence'),

    path('request-investigator/', views.request_investigator, name='request_investigator'),

    path('chat/',views.chat,name='chat'),

    path('reply/',views.reply, name='reply'),
    path("requested-investigators/", views.requested_investigators_list, name="requested_investigators_list"),

    path('approve-investigator/<int:case_id>/', views.approve_investigator_change, name='approve_investigator_change'),
    path('reject-investigator/<int:case_id>/', views.reject_investigator_change, name='reject_investigator_change'),

    path('suspect_list',views.suspect_list, name='suspect_list'),
    # path('dell/',views.dell, name='dell'),
    path('submit-final-report/<int:case_id>/', views.submit_final_report, name='submit_final_report'),

    path('victim_case_analysis/', views.victim_case_analysis, name='victim_case_analysis'),
    path('case-analyses/', views.investigator_case_analysis, name='investigator_case_analysis'),
    path('view_case_analysis_admin/', views.view_case_analysis_admin, name='view_case_analysis_admin'),

    path('case_analysis_view',views.case_analysis_view,name='case_analysis_view'),
    path('admin_view_cases',views.admin_view_cases,name='admin_view_cases'),
path('add_court/', views.add_court, name='add_court'),
path('view_courts/', views.admin_view_courts, name='admin_view_courts'),
path('court_cases/', views.court_cases, name='court_cases'),
path('add_case/', views.add_case, name='add_case'),
path('court_display_evidence_collection/', views.court_display_evidence_collection, name='ccourt_display_evidence_collectionourt_cases'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
