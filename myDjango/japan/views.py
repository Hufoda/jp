
from django.shortcuts import render, get_object_or_404,redirect
from django.urls import reverse
from japan.form import AddLessonForm, PostForm2, LoginForm, RegisterForm,VideoUploadForm,ReferenceBookForm,DeleteLessonForm,ListeningExerciseForm,QuestionDetailForm, AnswerDetailForm,EditQuestionForm,FlashcardForm
from japan.models import Lesson,LessonDetail,Video,Post2,Progress, Listening,ReferenceBook,QuizModel,QuestionDetail,AnswerDetail,QuizScore,ImageCard, ListeningProgress, Achievement
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.utils.timezone import now
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.core.files.base import equals_lf
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from django.http import JsonResponse
from django.contrib.auth import logout
from django.views.decorators.http import require_POST
from django.contrib.admin.views.decorators import staff_member_required
from .form import QuizForm
from .utils import check_level_up
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse


def health_check(request):
    return HttpResponse("ok", content_type="text/plain")


# Create your views here.
def start(request):
    return render(request, "FirstPage/base.html")

def about(request):
    return render(request, 'FirstPage/about.html')

def services(request):
    return render(request, 'FirstPage/services.html')

def contact(request):
    return render(request, 'FirstPage/contact.html')


def home(request):
    user_name = request.user.username if request.user.is_authenticated else "Guest"
    return render(request, 'Home.html', {'user_name': user_name})


def Reference(request):
    return render(request,'Reference.html')

def n5_details(request):
    return render(request, 'Detail/n5_details.html')

def n4_details(request):
    return render(request, 'Detail/n4_details.html')

def n3_details(request):
    return render(request, 'Detail/n3_details.html')

def n2_details(request):
    return render(request, 'Detail/n2_details.html')

def n1_details(request):
    return render(request, 'Detail/n1_details.html')

def n5_quiz(request):
    return render(request, 'Quiz/n5_quiz.html')

def n4_quiz(request):
    return render(request, 'Quiz/n4_quiz.html')

def n3_quiz(request):
    return render(request, 'Quiz/n3_quiz.html')

def n2_quiz(request):
    return render(request, 'Quiz/n2_quiz.html')

def n1_quiz(request):
    return render(request, 'Quiz/n1_quiz.html')

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from .models import Lesson, Progress

@login_required
def lesson_list(request, level):
    is_admin = check_is_admin(request.user)
    lesson = get_object_or_404(Lesson, level=level)
    lesson_details = lesson.lesson_details.all()

    # Get all completed video IDs for this user
    completed_videos = Progress.objects.filter(
        user=request.user,
        completed=True
    ).values_list('video_id', flat=True)

    completed_lessons = []
    for lesson_detail in lesson_details:
        # Get all videos in this lesson detail
        videos = lesson_detail.videos.all()
        # Check if all videos are completed
        if videos and all(video.id in completed_videos for video in videos):
            completed_lessons.append(lesson_detail.id)

    context = {
        'lesson': lesson,
        'lesson_details': lesson_details,
        'is_admin': is_admin,
        'completed_lessons': completed_lessons,
    }

    return render(request, 'lesson_details.html', context)






def check_is_admin(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser or user.groups.filter(name="Admins").exists())


@login_required
@user_passes_test(check_is_admin, login_url='forbidden_page')
def addLesson(request):
    is_admin = check_is_admin(request.user)
    if request.method=='POST':
        a_form=AddLessonForm(request.POST)
        if a_form.is_valid():
            a_form.save()
            return redirect('level_selection')
    else:
        a_form=AddLessonForm()
    return render(request,"AddLesson_form.html",{'form':a_form, 'is_admin': is_admin})


from django.shortcuts import get_object_or_404
from django.http import Http404


@login_required
@user_passes_test(check_is_admin, login_url='forbidden_page')
def LessonDelete(request, lesson_id):  # Pass lesson_id to the view
    lesson = get_object_or_404(LessonDetail, id=lesson_id)  # Retrieve the lesson

    if request.method == 'POST':
        lesson.delete()  # Delete the lesson object
        return redirect('level_selection')  # Redirect to another page after deletion

    return render(request, "DeleteLesson.html", {'lesson': lesson})


@login_required
@user_passes_test(check_is_admin, login_url='forbidden_page')
def upload_post(request):
    is_admin = check_is_admin(request.user)
    if request.method == 'POST':
        form = PostForm2(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('view_posts')
    else:
        form = PostForm2()
    return render(request, 'Post/upload.html', {'form': form, 'is_admin': is_admin})

from django.core.paginator import Paginator
@login_required
def view_posts(request):
    if check_is_admin(request.user):
        # Teachers/Admins see all posts including archived
        post_list = Post2.objects.all().order_by('-created_at')
    else:
        post_list = Post2.objects.filter(archived=False).order_by('-created_at')
    paginator = Paginator(post_list, 2)  # 5 posts per page
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    is_admin = check_is_admin(request.user)

    return render(request, 'Home.html', {'posts': posts, 'is_admin': is_admin})


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post2, id=post_id)
    if request.method == 'POST':
        form = PostForm2(request.POST, request.FILES, instance=post)
        if form.is_valid():
            updated_post = form.save()

            log_achievement(
                user=request.user,
                action='edited',
                model_name='Post2',
                pk=updated_post.id,
                title=updated_post.title,
                text=updated_post.text,
                image_path=updated_post.image.url if updated_post.image else None
            )

            return redirect('view_posts')
    else:
        form = PostForm2(instance=post)
    return render(request, 'Post/edit.html', {'form': form})


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post2, id=post_id)
    if request.method == 'POST':
        # Log activity before archiving
        log_achievement(
            user=request.user,
            action='disabled',   # 👈 better wording than "deleted"
            model_name='Post2',
            pk=post.id,
            title=post.title,
            text=post.text,
            image_path=post.image.url if post.image else None
        )

        # Soft delete: mark as archived
        post.archived = True
        post.save()

        return redirect('view_posts')
    return render(request, 'Post/delete.html', {'post': post})

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Post2, Achievement
from django.utils import timezone

@login_required
def restore_post(request, post_id):
    if request.user.is_staff:  # Only admin can restore
        post = get_object_or_404(Post2, id=post_id)
        post.archived = False
        post.save()

        # Log restore action
        log_achievement(
            user=request.user,
            action='restored',
            model_name='Post2',
            pk=post.id,
            title=post.title,
            text=post.text,
            image_path=post.image.url if post.image else None
        )

    return redirect('view_posts')


def first(request):
    return render(request, 'First.html')

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            raw_username = form.cleaned_data["username"].strip()
            password = form.cleaned_data["password"]

            user = User.objects.filter(username__iexact=raw_username).first()
            if user:
                authenticated_user = authenticate(request, username=user.username, password=password)
                if authenticated_user:
                    login(request, authenticated_user)
                    return redirect("home")

            messages.error(request, "Username or password is invalid")
            return render(request, "login.html", {"form": form})
    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form})


def home1_view(request):
    return render(request, 'Home.html')

def home2_view(request):
    return render(request, 'Home.html')


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])

            # Hash the password
            user.save()
            learner_group, _ = Group.objects.get_or_create(name="Learners")
            user.groups.add(learner_group)

            return redirect('login')
    else:
        form = RegisterForm()

    return render(request, 'test2.html', {'form': form})  # Return form with errors if invalid

def forbidden_page(request):
    return render(request, 'forbidden.html')



@login_required
def progress_view(request):
    is_admin = check_is_admin(request.user)
    if request.user.is_staff:  # Check if user is an admin
        registered_members = User.objects.all()  # Get all registered users
        return render(request, 'progress_dashboard.html', {'is_admin': True, 'registered_members': registered_members})
    else:
        user_progress = request.user.progress_set.all()
        return render(request, 'progress_dashboard.html', {'is_admin': False, 'user_progress': user_progress, 'is_admin': is_admin})



@login_required
def complete_lesson(request, lesson_detail_id):
    lesson_detail = get_object_or_404(LessonDetail, id=lesson_detail_id)

    # Mark all Progress objects for this user and lesson_detail as completed
    Progress.objects.filter(user=request.user, lesson_detail=lesson_detail).update(
        completed=True,
        completed_at=timezone.now()
    )

    # Optional: auto-create Progress for videos if missing
    for video in lesson_detail.videos.all():
        Progress.objects.get_or_create(
            user=request.user,
            lesson_detail=lesson_detail,
            video=video,
            defaults={'completed': True, 'completed_at': timezone.now()}
        )

    # Check if all videos in this lesson_detail are completed
    total_videos = lesson_detail.videos.count()
    completed_videos = Progress.objects.filter(
        user=request.user,
        lesson_detail=lesson_detail,
        completed=True
    ).count()

    lesson_completed = total_videos == completed_videos

    # Check AJAX request using header instead of is_ajax
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'lesson_completed': lesson_completed})
    else:
        return redirect('lesson_detail', lesson_detail.id)

@login_required
def book_list(request):
    is_admin = check_is_admin(request.user)
    books = ReferenceBook.objects.all()
    form = ReferenceBookForm()

    if request.method == 'POST':
        form = ReferenceBookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('book_list')  # Refresh the page after upload

    return render(request, 'Reference.html', {'books': books, 'form': form, 'is_admin': is_admin})

@login_required
@user_passes_test(check_is_admin, login_url='forbidden_page')
def add_book(request):
    # If the form is submitted, process the upload
    if request.method == 'POST':
        form = ReferenceBookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('book_list')  # Redirect to book list after uploading

    # If it's a GET request, show the empty form
    else:
        form = ReferenceBookForm()

    return render(request, 'upload_book.html', {'form': form})


@login_required
@user_passes_test(check_is_admin, login_url='forbidden_page')
def delete_book(request, book_id):
    book = get_object_or_404(ReferenceBook, id=book_id)

    if request.method == "POST":  # Confirm delete with a POST request
        book.archived = True
        book.save()
        return redirect('book_list')  # Redirect after deletion

    return render(request, 'delete_confirm.html', {'book': book})


def logout_page(request):
    return render(request, 'logout_confirm.html')

def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to login after logout

@login_required
def upload_video(request, lesson_id):
    lesson = LessonDetail.objects.get(id=lesson_id)

    if not check_is_admin(request.user):
        return redirect('home')  # Prevent non-admin users


    if request.method == "POST":
        form = VideoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.lesson = lesson
            video.save()
            return redirect('upload_video', lesson_id=lesson.id)
    else:
        form = VideoUploadForm()

    return render(request, 'upload_video.html', {'form': form, 'lesson': lesson})


@login_required
def user_detail(request, user_id):
    is_admin = check_is_admin(request.user)
    user = get_object_or_404(User, id=user_id)
    return render(request, 'user_detail.html', {'user': user, 'is_admin': is_admin})

@login_required
def upload_listening_exercise(request):
    is_admin = check_is_admin(request.user)
    if request.method == 'POST':
        form = ListeningExerciseForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('listening_section')  # Redirect to the page showing all exercises
    else:
        form = ListeningExerciseForm()

    return render(request, 'upload_listening_exercise.html', {'form': form, 'is_admin': is_admin})


@login_required

def qz_list(request, level):
    is_admin = check_is_admin(request.user)

    # Get the selected quiz type from the request (default to all if not provided)
    selected_quiz_type = request.GET.get('quiz_type', '')

    # Fetch quizzes based on level
    qz_level = QuizModel.objects.filter(quiz_level=level)

    # Apply quiz type filter if selected
    if selected_quiz_type:
        qz_level = qz_level.filter(quiz_type=selected_quiz_type)

    quiz_types = QuizModel.QUIZ_TYPES  # Get available quiz types

    return render(request, 'Quiz/quiz_level.html', {
        'qz_level': qz_level,
        'is_admin': is_admin,
        'level': level,
        'quiz_types': quiz_types,
        'selected_quiz_type': selected_quiz_type,'is_admin': is_admin
    })


@login_required
@user_passes_test(check_is_admin, login_url='forbidden_page')
def add_quiz_level(request, level):
    is_admin = check_is_admin(request.user)
    if not check_is_admin(request.user):
        return redirect('Quiz_home')  # Redirect if not admin

    if request.method == "POST":
        quiz_type = request.POST.get("quiz_type").strip()
        title = request.POST.get("title").strip()

        if quiz_type and title:
            QuizModel.objects.create(quiz_level=level, quiz_type=quiz_type, title=title)

        return redirect(request.META.get('HTTP_REFERER', 'Quiz_home'))  # Redirect back

    return render(request, 'Quiz/quizAdd.html', {'level': level,'is_admin': is_admin})


@login_required
def delete_quiz_level(request, quiz_id):
    if not check_is_admin(request.user):
        return redirect('Quiz_home')  # Redirect if not admin

    quiz = get_object_or_404(QuizModel, id=quiz_id)  # Get a specific quiz by ID
    quiz.delete()

    return redirect(request.META.get('HTTP_REFERER', 'Quiz_home'))  # Redirect back


@login_required()
def qz_detail(request, quiz_id):
    quiz_detail = get_object_or_404(QuizModel, id=quiz_id)
    questions = quiz_detail.questions.all()
    questions_with_answers = []
    for question in questions:
        answers = question.answers.all()
        print(f"Question: {question.qzText}, Answers: {list(answers)}")# Fetch answers related to each question
        questions_with_answers.append({
            'question': question,
            'answers': answers,
        })
    return render(request, 'QzQuestions.html', {
        'questions_with_answers': questions_with_answers,
        'quiz_id': quiz_id,
        "quiz": quiz_detail,
        "is_admin": check_is_admin(request.user)
    })

@login_required
@user_passes_test(check_is_admin, login_url='forbidden_page')
def add_quiz(request, quiz_id):
    is_admin = check_is_admin(request.user)
    quiz = get_object_or_404(QuizModel, id=quiz_id)

    if request.method == "POST":
        question_form = QuestionDetailForm(request.POST)

        new_ans_texts = request.POST.getlist("new_ansText[]")
        new_is_corrects = request.POST.getlist("new_is_correct[]")  # Will contain 'true' or 'false'

        if question_form.is_valid():
            question = question_form.save(commit=False)
            question.qzQuestion = quiz
            question.save()

            # Loop through answers and correctly assign "is_correct" values
            for i in range(len(new_ans_texts)):
                ans_text = new_ans_texts[i]
                is_correct = new_is_corrects[i] == "true"  # Convert string to Boolean

                AnswerDetail.objects.create(
                    ansText=ans_text,
                    is_correct=is_correct,
                    question=question
                )

            return redirect('qz_detail', quiz_id=quiz.id)

    else:
        question_form = QuestionDetailForm()

    return render(request, "Quiz/quizAdd.html", {
        "question_form": question_form,
        "quiz": quiz, "is_admin": is_admin
    })



@login_required
def delete_quiz_question(request, quiz_id, question_id):
    question = get_object_or_404(QuestionDetail, id=question_id)
    question.delete()  # This will also delete related answers if set with CASCADE

    return redirect('qz_detail', quiz_id=quiz_id)


@login_required
def quiz_view(request, quiz_id):
    is_admin = check_is_admin(request.user)
    quiz = QuizModel.objects.get(id=quiz_id)
    questions = QuestionDetail.objects.filter(qzQuestion=quiz)
    questions_with_answers = []

    # Collect questions with their answers
    for question in questions:
        answers = question.answers.all()
        questions_with_answers.append({'question': question, 'answers': answers})

    if request.method == "POST":
        score = 0
        feedback = []  # Collect feedback for each question
        total_questions = len(questions_with_answers)

        for item in questions_with_answers:
            question = item['question']
            selected_answer_id = request.POST.get(f"question_{question.id}")

            if selected_answer_id:
                selected_answer = AnswerDetail.objects.get(id=selected_answer_id)
                correct_answer = question.answers.filter(is_correct=True).first()  # Get the correct answer
                correct_answer_text = correct_answer.ansText if correct_answer else "N/A"

                # Check if the answer is correct and add feedback
                if selected_answer.is_correct:
                    score += 1
                    feedback.append({
                        'question': question.qzText,
                        'selected_answer': selected_answer.ansText,
                        'correct_answer': correct_answer_text,
                        'correct': True
                    })
                else:
                    feedback.append({
                        'question': question.qzText,
                        'selected_answer': selected_answer.ansText,
                        'correct_answer': correct_answer_text,
                        'correct': False
                    })

        # Save the quiz score
        quiz_score = QuizScore.objects.create(
            user=request.user,
            quiz=quiz,
            score=score,
            date_taken=timezone.now()
        )
        # 🔹 Call level-up check here
        check_level_up(request.user, quiz)


        # Redirect to show results
        return render(request, 'Quiz/quiz_result.html', {
            'score': score,
            'total_questions': total_questions,
            'feedback': feedback,  # Send feedback with correct answers to the results page
            'quiz_score': quiz_score
        })

    return render(request, 'Quiz/QzQuestions.html', {'quiz': quiz, 'questions_with_answers': questions_with_answers, 'is_admin': is_admin})




@login_required
def quiz_results(request, quiz_score_id):
    quiz_score = QuizScore.objects.get(id=quiz_score_id)
    return render(request, 'Quiz/quiz_result.html', {'quiz_score': quiz_score})

@login_required
def user_scores(request,quiz_id):
    scores = QuizScore.objects.filter(user=request.user)
    questions_count=QuizScore.objects.filter(quiz=quiz_id).values('quiz')
    results=QuestionDetail.objects.filter(qzQuestion__in=questions_count).count()

    return render(request, 'Quiz/quiz_result.html', {'scores': scores,'results':results})

@login_required
def edit_quiz_question(request, quiz_id, question_id):
    question = get_object_or_404(QuestionDetail, id=question_id, qzQuestion__id=quiz_id)

    if request.method == "POST":
        form = EditQuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            return redirect('qz_detail', quiz_id=quiz_id)
    else:
        form = EditQuestionForm(instance=question)

    return render(request, 'Quiz/edit_question.html', {
        'form': form,
        'quiz_id': quiz_id,
        'is_admin': check_is_admin(request.user)  # ✅ fixed
    })


@login_required
def delete_lesson(request, lesson_id):
    if not request.user.is_superuser:  # Ensure only admins can delete
        messages.error(request, "You don't have permission to delete lessons.")
        return redirect('lesson_list')

    lesson = get_object_or_404(LessonDetail, id=lesson_id)
    lesson.archived = True
    lesson.save()
    return redirect('level_selection')

@user_passes_test(check_is_admin)
def delete_listening(request, listening_id):
    listening = get_object_or_404(Listening, id=listening_id)
    listening.archived = True
    listening.save()

    return redirect('listening_section')

@login_required
@user_passes_test(check_is_admin, login_url='forbidden_page')
@require_POST
def delete_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    video.archived = True
    video.save()
    return JsonResponse({'success': True})


@login_required
def lesson_detail(request, lesson_detail_id):
    lesson_detail = get_object_or_404(LessonDetail, id=lesson_detail_id)
    videos = lesson_detail.videos.all()

    completed_videos = Progress.objects.filter(
        user=request.user,
        video__in=videos,
        completed=True
    ).values_list('video_id', flat=True)

    all_completed = videos.count() == len(completed_videos)

    context = {
        'lesson_detail': lesson_detail,
        'videos': videos,
        'completed_videos': list(completed_videos),
        'all_completed': all_completed,
        'is_admin': check_is_admin(request.user),  # ✅ FIXED
    }
    return render(request, 'ShowVideo.html', context)



@login_required
def mark_video_complete(request, lesson_detail_id):
    if request.method == "POST":
        import json
        data = json.loads(request.body)
        video_id = data.get("video_id")
        video = get_object_or_404(Video, id=video_id)
        lesson_detail = get_object_or_404(LessonDetail, id=lesson_detail_id)

        # Create or update progress for this user and video
        progress, created = Progress.objects.get_or_create(
            user=request.user,
            video=video,
            lesson_detail=lesson_detail
        )
        progress.completed = True
        from django.utils import timezone
        progress.completed_at = timezone.now()
        progress.save()

        # Check if all videos in this lesson_detail are completed
        videos = lesson_detail.videos.all()
        completed_videos = Progress.objects.filter(
            user=request.user,
            video__in=videos,
            completed=True
        ).count()

        lesson_completed = completed_videos == videos.count()

        return JsonResponse({
            "success": True,
            "lesson_completed": lesson_completed
        })

@login_required
def card_list(request, level):
    cards = ImageCard.objects.filter(level=level)
    lesson = get_object_or_404(Lesson, level=level)  # or however you retrieve the lesson
    return render(request, "flashcards/card_list.html", {"cards": cards, "lesson": lesson, 'is_admin': check_is_admin(request.user)})


@login_required
def flashcard_add(request, level):
    if request.method == 'POST':
        form = FlashcardForm(request.POST, request.FILES)
        if form.is_valid():
            flashcard = form.save(commit=False)
            flashcard.level = level  # Assign the level
            flashcard.save()
            return redirect('card_list', level=level)
    else:
        form = FlashcardForm()

    # Pass a boolean to the template
    context = {
        'form': form,
        'level': level,
        'is_admin': request.user.is_staff,  # ✅ This is the correct boolean
    }
    return render(request, 'flashcards/flashcard_add.html', context)

@login_required
def level_selection(request):
    is_admin = check_is_admin(request.user)
    user_profile = getattr(request.user, 'userprofile', None)
    user_level = user_profile.level if user_profile else 5  # Default N5
    return render(request, 'lesson_list.html', {
        'is_admin': is_admin,
        'user_level': user_level
    })

@login_required
def quiz_home(request):
    is_admin = check_is_admin(request.user)
    user_profile = getattr(request.user, 'userprofile', None)
    user_level = user_profile.level if user_profile else 5
    return render(request, 'Quiz_home.html', {
        'is_admin': is_admin,
        'user_level': user_level
    })

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json


@login_required
def listening_section(request):
    is_admin = check_is_admin(request.user)
    listening_exercises = Listening.objects.all()

    # Get completed exercises for this user
    completed_ids = ListeningProgress.objects.filter(
        user=request.user,
        completed=True
    ).values_list('listening_id', flat=True)

    # Add completion status to each exercise
    for exercise in listening_exercises:
        exercise.completed = exercise.id in completed_ids

    # Calculate progress
    total_count = listening_exercises.count()
    completed_count = len(completed_ids)
    percent = (completed_count / total_count * 100) if total_count > 0 else 0

    return render(request, 'Listening.html', {
        'listening_exercises': listening_exercises,
        'is_admin': is_admin,
        'completed_count': completed_count,
        'total_count': total_count,
        'percent': percent
    })


@login_required
@require_POST
def mark_listening_completed(request, listening_id):
    try:
        print(f"Marking listening {listening_id} as completed for user {request.user.username}")

        listening = Listening.objects.get(id=listening_id)
        # Create or update progress record
        progress, created = ListeningProgress.objects.get_or_create(
            user=request.user,
            listening=listening
        )

        # Mark as completed
        progress.completed = True
        progress.save()

        print(f"Progress record: created={created}, completed={progress.completed}")

        return JsonResponse({'status': 'success'})
    except Listening.DoesNotExist:
        print(f"Listening exercise {listening_id} not found")
        return JsonResponse({'status': 'error', 'message': 'Listening exercise not found'})
    except Exception as e:
        print(f"Error: {str(e)}")
        return JsonResponse({'status': 'error', 'message': str(e)})


@login_required
@user_passes_test(check_is_admin, login_url='forbidden_page')
@require_POST
def restore_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    video.archived = False
    video.save()
    return JsonResponse({'success': True})

def log_achievement(user, action, model_name, pk, title=None, text=None, image_path=None):
    Achievement.objects.create(
        original_model=model_name,
        original_pk=pk,
        title=title,
        text=text,
        image_path=image_path,
        action=action,
        changed_at=timezone.now(),
        changed_by=user
    )

@login_required
def achievement_list(request):
    achievements = Achievement.objects.order_by('-changed_at')
    return render(request, 'achievements.html', {'achievements': achievements,  'is_admin': check_is_admin(request.user)})
