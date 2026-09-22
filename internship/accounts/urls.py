from django.urls import path

from . import views


urlpatterns = [

    path("", views.home, name="home"),
    
    # =====================================================
    # AUTHENTICATION
    # =====================================================

    path(
        "register/",
        views.register,
        name="register"
    ),

    path(
        "register/student/",
        views.student_register,
        name="student_register"
    ),

    path(
        "register/company/",
        views.company_register,
        name="company_register"
    ),

    path(
        "login/",
        views.login_view,
        name="login"
    ),

    path(
        "logout/",
        views.logout_view,
        name="logout"
    ),


    # =====================================================
    # MAIN DASHBOARD
    # =====================================================

    path(
        "dashboard/",
        views.dashboard,
        name="dashboard"
    ),





    # =====================================================
    # COMPANY DASHBOARD
    # =====================================================

    path(
        "company/dashboard/",
        views.company_dashboard,
        name="company_dashboard"
    ),


    # =====================================================
    # ADMIN DASHBOARD
    # =====================================================

    path(
        "admin-dashboard/",
        views.admin_dashboard,
        name="admin_dashboard"
    ),


    # =====================================================
    # NOTIFICATIONS
    # =====================================================

    path(
        "notifications/",
        views.notifications_view,
        name="notifications"
    ),

    path(
        "notifications/<int:pk>/read/",
        views.mark_notification_read,
        name="mark_notification_read"
    ),

    path(
        "notifications/mark-all-read/",
        views.mark_all_notifications_read,
        name="mark_all_notifications_read"
    ),
]