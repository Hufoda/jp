from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from japan import views

urlpatterns = [
    path("health/", views.health_check, name="health_check"),
   # path('',views.first),
   # path('home2/', views.home, name='home2'),  # Learner's home page, name='home'),
    path('home/', views.view_posts, name='home'),
    path('level/', views.level_selection, name='level_selection'),
    path('quiz/', views.quiz_home, name='quiz_home'),
    path('achievements/', views.achievement_list, name='achievement_list'),

    #path('quiz/<str:quiz_id>/submit_answers/', views.submit_answers, name='submit_answers'),

    path('quiz/<str:quiz_id>/add/', views.add_quiz, name='add_quiz'),
    # <a href="{% url 'edit_quiz_question' quiz_id=quiz.id question_id=item.question.id %}" class="edit-btn">Edit</a>
    # path('quiz/<int:quiz_id>/edit/<int:question_id>/', views.edit_quiz_question, name='edit_quiz_question'),  # Edit a question
    path('quiz/<int:quiz_id>/delete/<int:question_id>/', views.delete_quiz_question, name='delete_quiz_question'),
    path('quiz/n5/', views.n5_quiz, name='n5_quiz'),
    path('quiz/n4/', views.n4_quiz, name='n4_quiz'),
    path('quiz/n3/', views.n3_quiz, name='n3_quiz'),
    path('quiz/n2/', views.n2_quiz, name='n2_quiz'),
    path('quiz/n1/', views.n1_quiz, name='n1_quiz'),
    path('level/n5/', views.n5_details, name='n5_details'),
    path('level/n4/', views.n4_details, name='n4_details'),
    path('level/n3/', views.n3_details, name='n3_details'),
    path('level/n2/', views.n2_details, name='n2_details'),
    path('level/n1/', views.n1_details, name='n1_details'),
    path('lessons/<str:level>/', views.lesson_list, name='lesson_list'),
    #path('lesson/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
    path('add/',views.addLesson, name='lesson_add'),

    path('lesson/delete/<int:lesson_id>/', views.delete_lesson, name='lesson_delete'),
    path('upload/', views.upload_post, name='upload_post'),
    path('view/', views.view_posts, name='view_posts'),
    path('edit/<int:post_id>/', views.edit_post, name='edit_post'),
    path('delete/<int:post_id>/', views.delete_post, name='delete_post'),

    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
   # path('complete_video/<int:video_id>/', views.complete_video, name='complete_video'),
    path('lesson/<int:lesson_detail_id>/', views.lesson_detail, name='lesson_detail'),
    #path('lesson/<int:lesson_detail_id>/mark_complete/', views.mark_video_complete, name='mark_video_complete'),
   # path("lesson/<int:lesson_detail_id>/mark_complete/", views.mark_video_complete, name="mark_video_complete"),
    path('book/', views.book_list, name='book_list'),
    path('progress/', views.progress_view, name='progress_dashboard'),

  # ✅ Use int:lesson_detail_id
    path('listening/', views.listening_section, name='listening_section'),
    path('listening/delete/<int:listening_id>/', views.delete_listening, name='delete_listening'),
    path('bookdelete/<int:book_id>/', views.delete_book, name='dbook'),
    path('adding/', views.add_book, name='addbook'),
    path('upload-video/<int:lesson_id>/', views.upload_video, name='upload_video'),
    path('logout/', views.logout_page, name='logout_page'),  # Show logout page
    path('logout/confirm/', views.logout_view, name='logout'),  # Log out and redirect
    path('Lessondelete/',views.LessonDelete, name='lesson_delete'),
    path('user/<int:user_id>/', views.user_detail, name='user_detail'),
    path('new/', views.upload_listening_exercise, name='upload_listening_exercise'),
    path("lesson/<int:lesson_detail_id>/complete_lesson/", views.complete_lesson, name="lesson_complete"),
    path("lesson/<int:lesson_detail_id>/mark_video/", views.mark_video_complete, name="mark_video_complete"),


   # path('watch_video/<int:video_id>/', views.watch_video, name='watch_video'),

path('quizzes/<str:level>/add/', views.add_quiz_level, name='add_quiz_level'),
    path('quiz-level/delete/<int:quiz_id>/', views.delete_quiz_level, name='delete_quiz_level'),
    path('quizzes/<str:level>/', views.qz_list, name='qz_list'),
    path('quiz/<int:quiz_id>/', views.quiz_view, name='quiz_view'),
    path('quiz/<int:quiz_id>/submit/', views.quiz_view, name='submit_quiz'),
    path('quiz/results/<int:quiz_score_id>/', views.quiz_results, name='quiz_results'),
    path('user/scores/<str:quiz_id>/', views.user_scores, name='user_scores'),
    path('quiz/<str:quiz_id>/', views.qz_detail, name='qz_detail'),
    path('quiz/<int:quiz_id>/edit/<int:question_id>/', views.edit_quiz_question, name='edit_quiz_question'),
    path('delete_video/<int:video_id>/', views.delete_video, name='delete_video'),
    path("flash/<str:level>/", views.card_list, name="card_list"),
    path('add/<str:level>/', views.flashcard_add, name='flashcard_add'),
    # Listening
    path('listening/<int:id>/completed/', views.mark_listening_completed, name='mark_listening_completed'),
    path('mark-listening-completed/<int:listening_id>/', views.mark_listening_completed,name='mark_listening_completed'),
    #path('restore_video/<int:video_id>/', views.restore_video, name='restore_video'),
    path('restore_video/<int:video_id>/', views.restore_video, name='restore_video'),
        #start
    path("", views.start, name="start"),
    path('signup/', views.register_view, name='signup'),
    path('register/', views.register_view, name='register'),
    path('contact/',views.contact,name='contact'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
path('restore/<int:post_id>/', views.restore_post, name='restore_post'),



]

if settings.DEBUG and not settings.USE_S3:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

