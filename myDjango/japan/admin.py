from django.contrib import admin
from japan.models import Lesson, LessonDetail, Video, Post2, Progress,Listening,ReferenceBook,QuizModel, QuestionDetail, AnswerDetail, QuizScore, UserProfile, Achievement, ListeningProgress


# Register your models here.
class SoftDeleteAdmin(admin.ModelAdmin):
    list_filter = ('archived',)

    def delete_model(self, request, obj):
        obj.archived = True
        obj.save()

    def delete_queryset(self, request, queryset):
        queryset.update(archived=True)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(archived=False)  # Show only non-archived by default

admin.site.register(Lesson)
@admin.register(LessonDetail)
class LessonDetailAdmin(SoftDeleteAdmin):
    list_display = ('title', 'archived')

@admin.register(Post2)
class Post2Admin(SoftDeleteAdmin):
    list_display = ('title', 'archived')

@admin.register(Video)
class VideoAdmin(SoftDeleteAdmin):
    list_display = ('lesson', 'video_type', 'archived')

@admin.register(ReferenceBook)
class ReferenceBookAdmin(SoftDeleteAdmin):
    list_display = ('title', 'level', 'archived')

@admin.register(Listening)
class ListeningAdmin(SoftDeleteAdmin):
    list_display = ('title', 'archived')

@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'lesson_detail', 'completed')  # Use the actual field names
    list_filter = ('completed', 'user')
    search_fields = ('user__username', 'lesson_detail__title')


admin.site.register(QuizScore)
@admin.register(QuizModel)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'quiz_level', 'quiz_type')  # Display important details
    list_filter = ('quiz_level', 'quiz_type')  # Filter options for better navigation

class AnswerInline(admin.TabularInline):
    model = AnswerDetail
    extra = 0  # Prevent extra empty fields

@admin.register(QuestionDetail)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('qzText', 'quiz_title')
    list_filter = ('qzQuestion__quiz_level', 'qzQuestion__quiz_type')
    inlines = [AnswerInline]  # Show answers inline with the question

    def quiz_title(self, obj):
        return obj.qzQuestion.title
    quiz_title.short_description = "Quiz Title"

@admin.register(AnswerDetail)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('ansText', 'question_text', 'quiz_title', 'is_correct')
    list_filter = ('question__qzQuestion__quiz_level', 'question__qzQuestion__quiz_type', 'is_correct')
    search_fields = ('ansText', 'question__qzText')

    def question_text(self, obj):
        return obj.question.qzText  # Show question text in AnswerDetail admin
    question_text.short_description = "Question"

    def quiz_title(self, obj):
        return obj.question.qzQuestion.title  # Show quiz title
    quiz_title.short_description = "Quiz Title"

from .models import ImageCard

@admin.register(ImageCard)
class ImageCardAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at')  # Added 'id' as first field
    list_display_links = ('id',)  # Specify which field should link to edit page
    list_editable = ('title',)  # Now 'title' can be editable
    ordering = ('-created_at',)  # Optional: order by most recent first

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'level')

@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    list_display = ('action', 'original_model', 'original_pk', 'changed_by', 'changed_at')
    list_filter = ('action', 'original_model', 'changed_by')
    search_fields = ('original_model', 'original_pk', 'title', 'text')

from django.contrib import admin
from .models import ListeningProgress

@admin.register(ListeningProgress)
class ListeningProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'listening', 'completed')
    list_filter = ('completed',)
    search_fields = ('user__username', 'listening__title')