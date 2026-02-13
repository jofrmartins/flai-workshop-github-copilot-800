from djongo import models
from django.contrib.auth.models import User as DjangoUser


class User(models.Model):
    """User profile model for OctoFit Tracker"""
    _id = models.ObjectIdField(primary_key=True)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    age = models.IntegerField(null=True, blank=True)
    fitness_level = models.CharField(
        max_length=50,
        choices=[
            ('beginner', 'Beginner'),
            ('intermediate', 'Intermediate'),
            ('advanced', 'Advanced'),
        ],
        default='beginner'
    )
    total_points = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'
        ordering = ['-total_points']

    def __str__(self):
        return self.username


class Team(models.Model):
    """Team model for group competitions"""
    _id = models.ObjectIdField(primary_key=True)
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(blank=True)
    captain_id = models.CharField(max_length=50)  # Reference to User._id
    member_ids = models.JSONField(default=list)  # List of User._id references
    total_points = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'teams'
        ordering = ['-total_points']

    def __str__(self):
        return self.name


class Activity(models.Model):
    """Activity logging model for tracking user workouts"""
    _id = models.ObjectIdField(primary_key=True)
    user_id = models.CharField(max_length=50)  # Reference to User._id
    activity_type = models.CharField(
        max_length=100,
        choices=[
            ('running', 'Running'),
            ('walking', 'Walking'),
            ('cycling', 'Cycling'),
            ('swimming', 'Swimming'),
            ('strength_training', 'Strength Training'),
            ('yoga', 'Yoga'),
            ('sports', 'Sports'),
            ('other', 'Other'),
        ]
    )
    duration = models.IntegerField(help_text='Duration in minutes')
    distance = models.FloatField(null=True, blank=True, help_text='Distance in kilometers')
    calories_burned = models.IntegerField(null=True, blank=True)
    points_earned = models.IntegerField(default=0)
    notes = models.TextField(blank=True)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'activities'
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.activity_type} - {self.duration} min"


class Leaderboard(models.Model):
    """Leaderboard model for tracking rankings"""
    _id = models.ObjectIdField(primary_key=True)
    period = models.CharField(
        max_length=50,
        choices=[
            ('daily', 'Daily'),
            ('weekly', 'Weekly'),
            ('monthly', 'Monthly'),
            ('all_time', 'All Time'),
        ]
    )
    period_start = models.DateField()
    period_end = models.DateField()
    user_rankings = models.JSONField(default=list)  # List of {"user_id": str, "points": int, "rank": int}
    team_rankings = models.JSONField(default=list)  # List of {"team_id": str, "points": int, "rank": int}
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'leaderboard'
        ordering = ['-period_start']
        unique_together = ('period', 'period_start')

    def __str__(self):
        return f"{self.period} - {self.period_start}"


class Workout(models.Model):
    """Workout suggestions model for personalized recommendations"""
    _id = models.ObjectIdField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    fitness_level = models.CharField(
        max_length=50,
        choices=[
            ('beginner', 'Beginner'),
            ('intermediate', 'Intermediate'),
            ('advanced', 'Advanced'),
            ('all', 'All Levels'),
        ],
        default='all'
    )
    activity_type = models.CharField(
        max_length=100,
        choices=[
            ('running', 'Running'),
            ('walking', 'Walking'),
            ('cycling', 'Cycling'),
            ('swimming', 'Swimming'),
            ('strength_training', 'Strength Training'),
            ('yoga', 'Yoga'),
            ('sports', 'Sports'),
            ('mixed', 'Mixed'),
        ]
    )
    duration = models.IntegerField(help_text='Estimated duration in minutes')
    estimated_calories = models.IntegerField(null=True, blank=True)
    instructions = models.JSONField(default=list)  # List of step-by-step instructions
    equipment_needed = models.JSONField(default=list)  # List of equipment
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'workouts'
        ordering = ['fitness_level', 'title']

    def __str__(self):
        return f"{self.title} ({self.fitness_level})"
