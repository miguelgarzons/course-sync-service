from django.contrib import admin
from django.urls import include, path
from scalar.scalar import urlpatterns_scalar, scalar_viewer

urlpatterns = [
    path('', scalar_viewer, name='root'),  
    
    path('admin/', admin.site.urls),

    path(
        "api/courses/",
        include("course_sync_service.app.courses.infrastructure.urls"),
    ),


    path(
        "api/student/",
        include("course_sync_service.app.student.infrastructure.urls"),
    ),

]

urlpatterns += urlpatterns_scalar
