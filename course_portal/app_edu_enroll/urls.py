from django.urls import path, include
from app_edu_enroll import views

from rest_framework.routers import DefaultRouter


course_list = views.CourseView.as_view({
    'get': 'list',
    # 'post': 'create'
})
# course_detail = SnippetViewSet.as_view({
#     'get': 'retrieve',
#     'put': 'update',
#     'patch': 'partial_update',
#     'delete': 'destroy'
# })

router = DefaultRouter()
router.register(r'courses_modelview', views.CourseModelView, basename='course-model-viewset')

urlpatterns = [
    path('get_students/',views.get_students, name="get-students"),
    path('get_students_detail/<int:pk>/',views.students_details, name="get-students-detail"),

    path('get_teachers/',views.TeacherView.as_view(), name="get-teachers"),
    path('get_teachers_detail/<int:pk>/',views.TeacherViewDeatail.as_view(), name="get-teachers-detail"),

    path('get_courses/', course_list, name='course-list'),

    path('',include(router.urls))

]