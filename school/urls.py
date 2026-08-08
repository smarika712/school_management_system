from django.urls import path
from . import views

urlpatterns = [
    path('',views.home_view,name='home'),
    path('student/',views.student_list_view,name='student_list'),
    path('student/add/',views.student_detail_view,name='student_detail'),
    path('student/<int:pk>/',views.student_detail_view,name='student_detail'),
    # path('student/<int:pk>/edit/',views.student_edit_view,name='student_edit'),
    path('student/<int:pk>/edit/', views.student_update_view, name='student_edit'),
    path('student/<int:pk>/delete/',views.student_delete_view,name='student_delete'),
    path('student/<int:pk>/upload-document/',views.student_document_upload_view,name='student_document_upload'),
    # path('api/upload-image/',views.api_upload_view,name='upload_image'),
    path('api/upload-image/', views.upload_image, name='upload_image'),
    # path('api/upload-document/',views.api_upload_file_view,name='upload_document'),
    path('api/upload-document/', views.upload_document, name='upload_document'),
    path('teachers/',views.teacher_list_view,name='teacher_list'),
    path('teachers/<int:pk>/',views.teacher_detail_view,name='teacher_detail'),
    path('courses/',views.course_list_view,name='course_list'),
    path('courses/<int:pk>/',views.course_detail_view,name='course_detail'),
]
