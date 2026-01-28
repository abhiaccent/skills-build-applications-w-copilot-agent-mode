from django.test import TestCase
from .models.models import User, Team, Activity, Workout, Leaderboard

class UserModelTest(TestCase):
    def test_create_user(self):
        team = Team.objects.create(name='Test Team', description='A test team')
        user = User.objects.create(name='Test User', email='test@example.com', team=team)
        self.assertEqual(user.name, 'Test User')
        self.assertEqual(user.team.name, 'Test Team')

class TeamModelTest(TestCase):
    def test_create_team(self):
        team = Team.objects.create(name='Another Team', description='Another test')
        self.assertEqual(team.name, 'Another Team')

class ActivityModelTest(TestCase):
    def test_create_activity(self):
        team = Team.objects.create(name='Activity Team', description='Activity test')
        user = User.objects.create(name='Activity User', email='activity@example.com', team=team)
        activity = Activity.objects.create(user=user, activity_type='Test', duration_minutes=10, date='2026-01-01')
        self.assertEqual(activity.user.name, 'Activity User')

class WorkoutModelTest(TestCase):
    def test_create_workout(self):
        workout = Workout.objects.create(name='Workout Test', description='Workout desc')
        self.assertEqual(workout.name, 'Workout Test')

class LeaderboardModelTest(TestCase):
    def test_create_leaderboard(self):
        team = Team.objects.create(name='Leaderboard Team', description='Leaderboard desc')
        leaderboard = Leaderboard.objects.create(team=team, total_points=50)
        self.assertEqual(leaderboard.team.name, 'Leaderboard Team')
