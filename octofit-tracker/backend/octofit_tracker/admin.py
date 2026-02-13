from django.contrib import admin
from .models import User, Team, Activity, Leaderboard, Workout


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Admin interface for User model"""
    list_display = ['username', 'email', 'fitness_level', 'total_points', 'created_at']
    list_filter = ['fitness_level', 'created_at']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    readonly_fields = ['_id', 'total_points', 'created_at', 'updated_at']
    ordering = ['-total_points']


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    """Admin interface for Team model"""
    list_display = ['name', 'captain_id', 'total_points', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['_id', 'total_points', 'created_at', 'updated_at']
    ordering = ['-total_points']


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    """Admin interface for Activity model"""
    list_display = ['user_id', 'activity_type', 'duration', 'distance', 'points_earned', 'date', 'created_at']
    list_filter = ['activity_type', 'date', 'created_at']
    search_fields = ['user_id', 'activity_type', 'notes']
    readonly_fields = ['_id', 'points_earned', 'created_at', 'updated_at']
    ordering = ['-date', '-created_at']
    date_hierarchy = 'date'


@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    """Admin interface for Leaderboard model"""
    list_display = ['period', 'period_start', 'period_end', 'created_at']
    list_filter = ['period', 'period_start']
    readonly_fields = ['_id', 'created_at', 'updated_at']
    ordering = ['-period_start']
    date_hierarchy = 'period_start'


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    """Admin interface for Workout model"""
    list_display = ['title', 'fitness_level', 'activity_type', 'duration', 'estimated_calories', 'created_at']
    list_filter = ['fitness_level', 'activity_type', 'created_at']
    search_fields = ['title', 'description']
    readonly_fields = ['_id', 'created_at', 'updated_at']
    ordering = ['fitness_level', 'title']
