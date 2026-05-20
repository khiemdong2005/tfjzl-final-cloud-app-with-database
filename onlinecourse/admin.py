from django.contrib import admin
# 1. Import đủ các class cần thiết từ models.py
from .models import Course, Lesson, Question, Choice, Enrollment, Submission

# 2. Cấu hình Inline cho Choice (để tạo câu trả lời ngay trong câu hỏi)
class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 4  # Mặc định hiện sẵn 4 ô để nhập 4 đáp án A, B, C, D

# 3. Cấu hình Inline cho Question (để tạo câu hỏi ngay trong bài học nếu cần)
class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1

# 4. Cấu hình hiển thị trang Admin cho Lesson và Question
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'course']
    inlines = [QuestionInline] # Hiện danh sách câu hỏi trong bài học

class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text', 'lesson', 'grade']
    inlines = [ChoiceInline] # Hiện các đáp án ngay dưới câu hỏi

# 5. Đăng ký tất cả các class này với admin site (Đủ 7 classes)
admin.site.register(Course)
# Đăng ký kèm theo class Admin tùy biến
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Enrollment)
admin.site.register(Submission)