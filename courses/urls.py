from django.urls import path
from .views import (
    CourseListView,
    CourseCreateView,
    CourseUpdateView,
    CourseDeleteView,
)

urlpatterns = [
    # The main dashboard page that lists all courses
    path('', CourseListView.as_view(), name='dashboard'),
    
    # URL for adding a new course
    path('add/', CourseCreateView.as_view(), name='course_add'),
    
    # URL for editing an existing course (e.g., /1/edit/)
    path('<int:pk>/edit/', CourseUpdateView.as_view(), name='course_edit'),
    
    # URL for deleting a course (e.g., /1/delete/)
    path('<int:pk>/delete/', CourseDeleteView.as_view(), name='course_delete'),
]

