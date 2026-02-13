from django.test import TestCase
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from datetime import date, timedelta
from .models import User, Team, Activity, Leaderboard, Workout


class UserModelTest(TestCase):
    """Test cases for User model"""

    def setUp(self):
        self.user = User.objects.create(
            username='testuser',
            email='test@example.com',
            first_name='Test',
            last_name='User',
            age=25,
            fitness_level='beginner',
            total_points=0
        )

    def test_user_creation(self):
        """Test user is created successfully"""
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(self.user.fitness_level, 'beginner')
        self.assertEqual(self.user.total_points, 0)

    def test_user_string_representation(self):
        """Test user string representation"""
        self.assertEqual(str(self.user), 'testuser')


class TeamModelTest(TestCase):
    """Test cases for Team model"""

    def setUp(self):
        self.user = User.objects.create(username='captain', email='captain@example.com')
        self.team = Team.objects.create(
            name='Test Team',
            description='A test team',
            captain_id=str(self.user._id),
            member_ids=[],
            total_points=0
        )

    def test_team_creation(self):
        """Test team is created successfully"""
        self.assertEqual(self.team.name, 'Test Team')
        self.assertEqual(self.team.captain_id, str(self.user._id))
        self.assertEqual(self.team.total_points, 0)

    def test_team_string_representation(self):
        """Test team string representation"""
        self.assertEqual(str(self.team), 'Test Team')


class ActivityModelTest(TestCase):
    """Test cases for Activity model"""

    def setUp(self):
        self.user = User.objects.create(username='athlete', email='athlete@example.com')
        self.activity = Activity.objects.create(
            user_id=str(self.user._id),
            activity_type='running',
            duration=30,
            distance=5.0,
            calories_burned=300,
            points_earned=30,
            date=date.today()
        )

    def test_activity_creation(self):
        """Test activity is created successfully"""
        self.assertEqual(self.activity.activity_type, 'running')
        self.assertEqual(self.activity.duration, 30)
        self.assertEqual(self.activity.distance, 5.0)
        self.assertEqual(self.activity.calories_burned, 300)

    def test_activity_string_representation(self):
        """Test activity string representation"""
        self.assertEqual(str(self.activity), 'running - 30 min')


class WorkoutModelTest(TestCase):
    """Test cases for Workout model"""

    def setUp(self):
        self.workout = Workout.objects.create(
            title='Morning Run',
            description='A refreshing morning run',
            fitness_level='beginner',
            activity_type='running',
            duration=30,
            estimated_calories=250,
            instructions=['Warm up', 'Run', 'Cool down'],
            equipment_needed=['Running shoes']
        )

    def test_workout_creation(self):
        """Test workout is created successfully"""
        self.assertEqual(self.workout.title, 'Morning Run')
        self.assertEqual(self.workout.fitness_level, 'beginner')
        self.assertEqual(self.workout.activity_type, 'running')


class UserAPITest(APITestCase):
    """Test cases for User API endpoints"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(
            username='apiuser',
            email='api@example.com',
            fitness_level='intermediate',
            total_points=100
        )
        self.user_url = reverse('user-list')

    def test_get_users_list(self):
        """Test retrieving list of users"""
        response = self.client.get(self.user_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_create_user(self):
        """Test creating a new user"""
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'fitness_level': 'beginner'
        }
        response = self.client.post(self.user_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], 'newuser')


class TeamAPITest(APITestCase):
    """Test cases for Team API endpoints"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username='teamcaptain', email='captain@example.com')
        self.team = Team.objects.create(
            name='API Team',
            captain_id=str(self.user._id),
            member_ids=[]
        )
        self.team_url = reverse('team-list')

    def test_get_teams_list(self):
        """Test retrieving list of teams"""
        response = self.client.get(self.team_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_team(self):
        """Test creating a new team"""
        data = {
            'name': 'New Team',
            'captain_id': str(self.user._id),
            'description': 'A brand new team'
        }
        response = self.client.post(self.team_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class ActivityAPITest(APITestCase):
    """Test cases for Activity API endpoints"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(username='activeuser', email='active@example.com')
        self.activity = Activity.objects.create(
            user_id=str(self.user._id),
            activity_type='walking',
            duration=20,
            date=date.today()
        )
        self.activity_url = reverse('activity-list')

    def test_get_activities_list(self):
        """Test retrieving list of activities"""
        response = self.client.get(self.activity_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_activity(self):
        """Test creating a new activity"""
        data = {
            'user_id': str(self.user._id),
            'activity_type': 'running',
            'duration': 45,
            'distance': 6.5,
            'date': date.today().isoformat()
        }
        response = self.client.post(self.activity_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class WorkoutAPITest(APITestCase):
    """Test cases for Workout API endpoints"""

    def setUp(self):
        self.client = APIClient()
        self.workout = Workout.objects.create(
            title='Test Workout',
            description='A test workout',
            fitness_level='beginner',
            activity_type='strength_training',
            duration=30
        )
        self.workout_url = reverse('workout-list')

    def test_get_workouts_list(self):
        """Test retrieving list of workouts"""
        response = self.client.get(self.workout_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_filter_workouts_by_fitness_level(self):
        """Test filtering workouts by fitness level"""
        url = reverse('workout-by-fitness-level')
        response = self.client.get(url, {'fitness_level': 'beginner'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class LeaderboardAPITest(APITestCase):
    """Test cases for Leaderboard API endpoints"""

    def setUp(self):
        self.client = APIClient()
        self.leaderboard = Leaderboard.objects.create(
            period='weekly',
            period_start=date.today(),
            period_end=date.today() + timedelta(days=7),
            user_rankings=[],
            team_rankings=[]
        )
        self.leaderboard_url = reverse('leaderboard-list')

    def test_get_leaderboard_list(self):
        """Test retrieving leaderboard list"""
        response = self.client.get(self.leaderboard_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
