from django import forms
from .models import LessonDetail,Post2, Video,ReferenceBook,Listening,QuizModel, QuestionDetail, AnswerDetail, ImageCard
from django.contrib.auth.models import User
import re  # For regex validation


class AddLessonForm(forms.ModelForm):
    class Meta:
        model=LessonDetail
        fields=['lesson','title','order']

class DeleteLessonForm(forms.ModelForm):
    class Meta:
        model=LessonDetail
        fields=['lesson','title']

class PostForm2(forms.ModelForm):
    class Meta:
        model = Post2
        fields = ['title', 'text', 'image']  # Add title field


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'autocomplete': 'off'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}))

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username does not exist")
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')
        return password

import re
from django import forms
from django.contrib.auth.models import User

class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput,
        help_text="Password must be at least 6 characters long and contain @ or ! and a dot (.)"
    )
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email address is already registered.")
        return email

    def clean_password(self):
        password = self.cleaned_data.get("password")
        if len(password) < 6:
            raise forms.ValidationError("Password must be at least 6 characters long.")
        if not re.search(r"[!@]", password):
            raise forms.ValidationError("Password must contain at least one '@' or '!'.")
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

class VideoUploadForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = [ 'video_type','video']


class ReferenceBookForm(forms.ModelForm):
    class Meta:
        model = ReferenceBook
        fields = ['title', 'level', 'file']

class ListeningExerciseForm(forms.ModelForm):
    class Meta:
        model = Listening
        fields = ['title', 'audio_file']


class QuizForm(forms.ModelForm):
    class Meta:
        model = QuizModel
        fields = ['quiz_level', 'quiz_type', 'title']

class QuestionDetailForm(forms.ModelForm):
    class Meta:
        model = QuestionDetail
        fields = ['qzText']

class AnswerDetailForm(forms.ModelForm):
    class Meta:
        model = AnswerDetail
        fields = ['ansText', 'is_correct']


class EditQuestionForm(forms.ModelForm):
    class Meta:
        model = QuestionDetail
        fields = ['qzText']  # Add other fields if necessary



class FlashcardForm(forms.ModelForm):
    class Meta:
        model = ImageCard
        fields = ['title', 'front_image', 'back_image']