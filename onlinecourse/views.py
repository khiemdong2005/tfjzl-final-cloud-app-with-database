from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Course, Question, Choice, Submission

# --- TASK 4: HIỂN THỊ CHI TIẾT KHÓA HỌC VÀ ĐỀ THI ---
def course_details(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    context = {'course': course}
    return render(request, 'onlinecourse/course_details_bootstrap.html', context)


# --- TASK 5 & 6: XỬ LÝ NỘP BÀI TRẮC NGHIỆM ---
def submit(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    
    if request.method == 'POST':
        # 1. Tạo một đối tượng nộp bài mới cho User hiện tại
        submission = Submission.objects.create(user=request.user, course=course)
        
        # 2. Lấy danh sách tất cả các lựa chọn (choices) được tích từ form HTML gửi lên
        selected_choice_ids = request.POST.getlist('choice')
        
        # 3. Lưu các lựa chọn đã chọn vào bảng liên kết của Submission
        for choice_id in selected_choice_ids:
            choice = get_object_or_404(Choice, pk=int(choice_id))
            submission.choices.add(choice)
        
        submission.save()
        
        # 4. Chuyển hướng sang trang kết quả (Task 7) kèm theo ID của lượt nộp bài này
        return HttpResponseRedirect(reverse('onlinecourse:show_exam_result', args=(course.id, submission.id)))
        
    return redirect('onlinecourse:course_details', course_id=course.id)


# --- TASK 7: TÍNH ĐIỂM VÀ HIỂN THỊ KẾT QUẢ ĐẬU/RỚT ---
def show_exam_result(request, course_id, submission_id):
    # Lấy thông tin khóa học và lượt làm bài
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)
    
    # Lấy tất cả các câu hỏi thuộc các bài học trong khóa học này
    questions = Question.objects.filter(lesson__course=course)
    total_questions = questions.count()
    
    correct_answers_count = 0
    
    # Duyệt qua từng câu hỏi để kiểm tra xem học viên trả lời đúng hay sai
    for question in questions:
        # Lấy tất cả các đáp án ĐÚNG của câu hỏi này trong Database
        correct_choices = set(question.choice_set.filter(is_correct=True))
        
        # Lấy tất cả các đáp án mà học viên ĐÃ CHỌN cho câu hỏi này
        user_choices = set(submission.choices.filter(question=question))
        
        # Nếu đáp án học viên chọn khớp hoàn toàn với đáp án đúng trong DB -> Tính 1 câu đúng
        if correct_choices == user_choices and correct_choices:
            correct_answers_count += 1

    # Tính toán phần trăm kết quả (Đạt từ 80% trở lên là ĐẬU)
    score_percentage = (correct_answers_count / total_questions) * 100 if total_questions > 0 else 0
    is_passed = score_percentage >= 80

    # Gom tất cả dữ liệu gửi sang giao diện HTML hiển thị kết quả
    context = {
        'course': course,
        'submission': submission,
        'correct_count': correct_answers_count,
        'total_questions': total_questions,
        'score_percentage': round(score_percentage, 1),
        'is_passed': is_passed
    }
    
    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)