from django.urls import path
from . import views

app_name = 'onlinecourse'
urlpatterns = [
    # Đường dẫn xem chi tiết khóa học (Task 4 & 6)
    path('course/<int:course_id>/', views.course_details, name='course_details'),
    
    # Đường dẫn xử lý nộp bài thi (Task 5)
    path('course/<int:course_id>/submit/', views.submit, name='submit'),
    
    # Đường dẫn hiển thị kết quả Đậu/Rớt (Task 7)
    path('course/<int:course_id>/submission/<int:submission_id>/result/', views.show_exam_result, name='show_exam_result'),
]