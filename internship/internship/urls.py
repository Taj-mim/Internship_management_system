from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

path("admin/", admin.site.urls),
path("index/", views.index, name="index"),
path("", include("accounts.urls")),
path("", include("opportunity_portal.urls")),


# =====================================================
# ADMIN CRUD PAGES
# =====================================================
path("CRUD_post/", views.CRUD_post, name="CRUD_post"),
path("CRUD_org/", views.CRUD_org, name="CRUD_org"),
path("CRUD_application/", views.CRUD_application, name="CRUD_application"),


# =====================================================
# STUDENT CRUD
# =====================================================

path("admin-students/", views.student_list, name="student_list"),
path("admin-students/add/", views.student_add, name="student_add"),
path("admin-students/edit/<int:pk>/", views.student_edit, name="student_edit"),
path("admin-students/delete/<int:pk>/", views.student_delete, name="student_delete"),


# =====================================================
# ORGANIZATION CRUD
# =====================================================

path("admin-organizations/", views.CRUD_org, name="CRUD_org"),
path("admin-organizations/add/", views.organization_add, name="organization_add"),
path("admin-organizations/edit/<int:pk>/", views.organization_edit, name="organization_edit"),
path("admin-organizations/delete/<int:pk>/", views.organization_delete, name="organization_delete"), 



# =====================================================
# POST CRUD
# =====================================================

path("admin-posts/add/", views.post_add, name="post_add"),
path("admin-posts/edit/<int:pk>/", views.post_edit, name="post_edit"),
path("admin-posts/delete/<int:pk>/", views.post_delete, name="post_delete"), 


path(
    'organization/application/<int:application_id>/<str:status>/',
    views.update_application_status,
    name='update_application_status'
),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

