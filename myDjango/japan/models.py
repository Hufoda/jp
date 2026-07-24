from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Lesson(models.Model):
    JLPT_LEVELS = [
        ('N5', 'N5 - Beginner'),
        ('N4', 'N4 - Upper Beginner'),
        ('N3', 'N3 - Intermediate'),
        ('N2', 'N2 - Upper Intermediate'),
        ('N1', 'N1 - Advanced'),
    ]
    level = models.CharField(max_length=2, choices=JLPT_LEVELS, default='N5')

    def __str__(self):
        return self.level

class LessonDetail(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='lesson_details')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    order = models.PositiveIntegerField(default=1)
    archived = models.BooleanField(default=False)
    class Meta:
        ordering = ['order']  # Sort lessons by order

    def __str__(self):
        return f"{self.lesson.level} - {self.title}"

class Video(models.Model):
    VIDEO_TYPES = [
        ('kanji', 'Kanji'),
        ('grammar', 'Grammar'),
        ('vocabulary', 'Vocabulary'),
        ('reading', 'Reading'),
        ('other','Other'),
    ]

    lesson = models.ForeignKey(LessonDetail, on_delete=models.CASCADE, related_name="videos")
    video_type = models.CharField(max_length=20, choices=VIDEO_TYPES)
    video = models.FileField(upload_to='videos/', blank=True, null=True)
    archived = models.BooleanField(default=False)  # NEW FIELD

    def __str__(self):
        return f"{self.lesson.title} ({self.get_video_type_display()}) [{self.id}]"


from django.utils.timezone import now  # Import timezone


class Progress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson_detail = models.ForeignKey(LessonDetail, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE, null=True, blank=True)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        if self.video:
            return f"{self.user.username} - {self.video.lesson.title} ({self.video.get_video_type_display()}) ✅ {self.completed}"
        else:
            return f"{self.user.username} - {self.lesson_detail.title} ✅ {self.completed}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'video'],
                name='unique_user_video',
                condition=models.Q(video__isnull=False)  # Only enforce uniqueness when video is not null
            )
        ]

class Listening(models.Model):
    title = models.CharField(max_length=255)
    audio_file = models.FileField(upload_to='listening/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    transcript = models.TextField(blank=True, null=True)
    archived = models.BooleanField(default=False)  # NEW FIELD

    def __str__(self):
        return self.title

class ListeningProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listening_progress')
    listening = models.ForeignKey(Listening, on_delete=models.CASCADE, related_name='user_progress')
    completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'listening')
        verbose_name_plural = 'Listening Progress'

    def __str__(self):
        return f"{self.user.username} - {self.listening.title} - {'Completed' if self.completed else 'Incomplete'}"

class ReferenceBook(models.Model):
    LEVEL_CHOICES = [
        ('N5', 'N5'),
        ('N4', 'N4'),
        ('N3', 'N3'),
        ('N2', 'N2'),
        ('N1', 'N1'),
    ]

    title = models.CharField(max_length=255)
    level = models.CharField(max_length=2, choices=LEVEL_CHOICES)
    file = models.FileField(upload_to='books/')
    archived = models.BooleanField(default=False)  # NEW FIELD
    def __str__(self):
        return self.title


class Post2(models.Model):
    title = models.CharField(max_length=200)  # Add title field
    text = models.TextField()
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    archived = models.BooleanField(default=False)  # NEW FIELD
    def __str__(self):
        return self.title


class QuizModel(models.Model):
    Quiz_Level = [
        ('N5', 'N5'),
        ('N4', 'N4'),
        ('N3', 'N3'),
        ('N2', 'N2'),
        ('N1', 'N1'),
    ]
    QUIZ_TYPES = [
        ('Vocabulary', 'Vocabulary'),
        ('Grammar', 'Grammar'),
        ('Kanji', 'Kanji'),
        ('All','All')
    ]

    quiz_level = models.CharField(max_length=50, choices=Quiz_Level)
    quiz_type = models.CharField(max_length=20, choices=QUIZ_TYPES)
    title = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.quiz_level} - {self.quiz_type} - {self.title}"

class QuestionDetail(models.Model):
    qzQuestion = models.ForeignKey(QuizModel, on_delete=models.CASCADE)
    qzText = models.CharField(max_length=2000)
    def __str__(self):
        return f"{self.qzQuestion.quiz_level} - {self.qzQuestion.quiz_type} - {self.qzQuestion.title} - {self.qzText}"

class AnswerDetail(models.Model):
    question = models.ForeignKey(QuestionDetail, on_delete=models.CASCADE, related_name='answers')
    ansText = models.CharField(max_length = 2000)
    is_correct = models.BooleanField(default = False)

    def __str__(self):
        return f"{self.question.qzText} - \t{self.ansText} - {self.is_correct}"



class QuizScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(QuizModel, on_delete=models.CASCADE)
    score = models.IntegerField()
    date_taken = models.DateTimeField(auto_now_add=True)
    def get_quizby_questions_count(self):
        return self.quiz
    def __str__(self):
        return f"{self.user.username} - {self.quiz.title} - {self.score}"


class ImageCard(models.Model):
    LEVEL_CHOICES = [
        ("N5", "JLPT N5"),
        ("N4", "JLPT N4"),
        ("N3", "JLPT N3"),
        ("N2", "JLPT N2"),
        ("N1", "JLPT N1"),
    ]

    title = models.CharField(max_length=100)
    front_image = models.ImageField(upload_to="flashcards/front/")
    back_image = models.ImageField(upload_to="flashcards/back/")
    created_at = models.DateTimeField(auto_now_add=True)
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES, default="N5")


from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    level = models.IntegerField(default=5)

    def __str__(self):
        return f"{self.user.username} - Level {self.level}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance, defaults={'level': 5})


from django.utils import timezone
from django.conf import settings
class Achievement(models.Model):
    ACTION_CHOICES = [
        ('edited', 'Edited'),
        ('deleted', 'Deleted'),
    ]

    original_model = models.CharField(max_length=100)  # e.g., 'Post2'
    original_pk = models.IntegerField()
    title = models.CharField(max_length=200, blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    image_path = models.CharField(max_length=500, blank=True, null=True)
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    changed_at = models.DateTimeField(default=timezone.now)
    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True
    )

    def __str__(self):
        return f"{self.original_model} #{self.original_pk} - {self.action} on {self.changed_at}"

class VideoProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)