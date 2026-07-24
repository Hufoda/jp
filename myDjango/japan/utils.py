# utils.py
from .models import QuizScore, UserProfile, QuizModel

def check_level_up(user, quiz):
    if quiz.title != "Level Up Quiz":
        print("Not a level up quiz:", quiz.title)
        return

    print(f"Checking level up for: {user.username}, Profile level: {user.userprofile.level}, Quiz level: {quiz.quiz_level}")

    user_scores = QuizScore.objects.filter(user=user, quiz=quiz)
    if not user_scores.exists():
        print("No scores found")
        return

    latest_score = user_scores.last()
    print("Latest score:", latest_score.score)

    if latest_score.score >= 23:
        profile = user.userprofile

        # mapping for quiz level string to integer
        level_dict = {"N5": 5, "N4": 4, "N3": 3, "N2": 2, "N1": 1}

        required_level = level_dict.get(quiz.quiz_level)

        if required_level is None:
            print("⚠️ Invalid quiz level:", quiz.quiz_level)
            return

        # only allow if user's current level matches quiz level
        if profile.level == required_level and profile.level > 1:
            profile.level -= 1  # move up (e.g., 5 -> 4, 4 -> 3)
            profile.save()
            print("✅ Level up! New level:", profile.level)
        else:
            print(f"❌ Level mismatch: quiz requires {required_level} but user is {profile.level}")
