from rest_framework import serializers
from .models import User, Team, Activity, Leaderboard, Workout


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    id = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'age', 'fitness_level', 'total_points', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'total_points', 'created_at', 'updated_at']

    def get_id(self, obj):
        """Convert ObjectId to string"""
        return str(obj._id) if obj._id else None


class TeamSerializer(serializers.ModelSerializer):
    """Serializer for Team model"""
    id = serializers.SerializerMethodField()

    class Meta:
        model = Team
        fields = [
            'id', 'name', 'description', 'captain_id', 'member_ids',
            'total_points', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'total_points', 'created_at', 'updated_at']

    def get_id(self, obj):
        """Convert ObjectId to string"""
        return str(obj._id) if obj._id else None


class ActivitySerializer(serializers.ModelSerializer):
    """Serializer for Activity model"""
    id = serializers.SerializerMethodField()

    class Meta:
        model = Activity
        fields = [
            'id', 'user_id', 'activity_type', 'duration', 'distance',
            'calories_burned', 'points_earned', 'notes', 'date',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'points_earned', 'created_at', 'updated_at']

    def get_id(self, obj):
        """Convert ObjectId to string"""
        return str(obj._id) if obj._id else None

    def create(self, validated_data):
        """Calculate points when creating activity"""
        activity = super().create(validated_data)
        # Simple point calculation: 1 point per minute
        activity.points_earned = validated_data.get('duration', 0)
        activity.save()
        return activity


class LeaderboardSerializer(serializers.ModelSerializer):
    """Serializer for Leaderboard model"""
    id = serializers.SerializerMethodField()

    class Meta:
        model = Leaderboard
        fields = [
            'id', 'period', 'period_start', 'period_end',
            'user_rankings', 'team_rankings', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_id(self, obj):
        """Convert ObjectId to string"""
        return str(obj._id) if obj._id else None


class WorkoutSerializer(serializers.ModelSerializer):
    """Serializer for Workout model"""
    id = serializers.SerializerMethodField()

    class Meta:
        model = Workout
        fields = [
            'id', 'title', 'description', 'fitness_level', 'activity_type',
            'duration', 'estimated_calories', 'instructions', 'equipment_needed',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_id(self, obj):
        """Convert ObjectId to string"""
        return str(obj._id) if obj._id else None
