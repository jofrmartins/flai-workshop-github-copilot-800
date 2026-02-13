from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum
from pymongo import MongoClient
from .models import User, Team, Activity, Leaderboard, Workout
from .serializers import (
    UserSerializer, TeamSerializer, ActivitySerializer,
    LeaderboardSerializer, WorkoutSerializer
)


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for User operations
    Provides CRUD operations for user profiles
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def list(self, request):
        """Custom list method to include team_name and date_joined from MongoDB"""
        # Connect to MongoDB to get additional fields
        client = MongoClient('localhost', 27017)
        db = client['octofit_db']
        
        # Get users from MongoDB
        users_data = []
        for user_doc in db.users.find():
            # Get team name
            team_name = None
            if user_doc.get('team_id'):
                team = db.teams.find_one({'_id': user_doc['team_id']})
                if team:
                    team_name = team.get('name')
            
            user_data = {
                'id': user_doc.get('_id'),
                'username': user_doc.get('username'),
                'email': user_doc.get('email'),
                'first_name': user_doc.get('first_name'),
                'last_name': user_doc.get('last_name'),
                'age': user_doc.get('age'),
                'fitness_level': user_doc.get('fitness_level'),
                'total_points': user_doc.get('total_points', 0),
                'created_at': user_doc.get('created_at'),
                'updated_at': user_doc.get('updated_at'),
                'team_name': team_name,
                'date_joined': user_doc.get('joined_at'),
            }
            users_data.append(user_data)
        
        client.close()
        
        # Sort by total_points descending
        users_data.sort(key=lambda x: x.get('total_points', 0), reverse=True)
        
        return Response(users_data)

    @action(detail=True, methods=['get'])
    def activities(self, request, pk=None):
        """Get all activities for a specific user"""
        user = self.get_object()
        activities = Activity.objects.filter(user_id=str(user._id))
        serializer = ActivitySerializer(activities, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def stats(self, request, pk=None):
        """Get user statistics"""
        user = self.get_object()
        activities = Activity.objects.filter(user_id=str(user._id))
        total_activities = activities.count()
        total_duration = activities.aggregate(Sum('duration'))['duration__sum'] or 0
        total_distance = activities.aggregate(Sum('distance'))['distance__sum'] or 0
        
        return Response({
            'user_id': str(user._id),
            'username': user.username,
            'total_points': user.total_points,
            'total_activities': total_activities,
            'total_duration': total_duration,
            'total_distance': total_distance,
        })


class TeamViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Team operations
    Provides CRUD operations for teams
    """
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

    @action(detail=True, methods=['post'])
    def add_member(self, request, pk=None):
        """Add a member to the team"""
        team = self.get_object()
        user_id = request.data.get('user_id')
        
        if not user_id:
            return Response(
                {'error': 'user_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if user_id not in team.member_ids:
            team.member_ids.append(user_id)
            team.save()
            return Response({'message': 'Member added successfully'})
        
        return Response(
            {'error': 'User is already a member'},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=True, methods=['post'])
    def remove_member(self, request, pk=None):
        """Remove a member from the team"""
        team = self.get_object()
        user_id = request.data.get('user_id')
        
        if not user_id:
            return Response(
                {'error': 'user_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if user_id in team.member_ids:
            team.member_ids.remove(user_id)
            team.save()
            return Response({'message': 'Member removed successfully'})
        
        return Response(
            {'error': 'User is not a member'},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(detail=True, methods=['get'])
    def members(self, request, pk=None):
        """Get all members of the team"""
        team = self.get_object()
        members = User.objects.filter(_id__in=team.member_ids)
        serializer = UserSerializer(members, many=True)
        return Response(serializer.data)


class ActivityViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Activity operations
    Provides CRUD operations for activity logging
    """
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer

    def list(self, request):
        """Custom list method to include user_name from MongoDB"""
        # Connect to MongoDB to get user names
        client = MongoClient('localhost', 27017)
        db = client['octofit_db']
        
        # Get activities from MongoDB
        activities_data = []
        for activity_doc in db.activities.find().sort('date', -1):
            # Get user name
            user_name = None
            if activity_doc.get('user_id'):
                user = db.users.find_one({'_id': activity_doc['user_id']})
                if user:
                    user_name = user.get('username')
            
            activity_data = {
                'id': str(activity_doc.get('_id')),
                'user_id': activity_doc.get('user_id'),
                'user_name': user_name,
                'activity_type': activity_doc.get('activity_type'),
                'duration': activity_doc.get('duration'),
                'distance': activity_doc.get('distance'),
                'calories_burned': activity_doc.get('calories_burned'),
                'points_earned': activity_doc.get('points_earned'),
                'notes': activity_doc.get('notes'),
                'date': activity_doc.get('date').isoformat() if activity_doc.get('date') else None,
                'created_at': activity_doc.get('created_at'),
                'updated_at': activity_doc.get('updated_at'),
            }
            activities_data.append(activity_data)
        
        client.close()
        
        return Response(activities_data)

    def perform_create(self, serializer):
        """Update user points when activity is created"""
        activity = serializer.save()
        
        # Update user's total points
        try:
            user = User.objects.get(_id=activity.user_id)
            user.total_points += activity.points_earned
            user.save()
        except User.DoesNotExist:
            pass

    @action(detail=False, methods=['get'])
    def by_user(self, request):
        """Get activities filtered by user_id"""
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response(
                {'error': 'user_id parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        activities = Activity.objects.filter(user_id=user_id)
        serializer = self.get_serializer(activities, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_type(self, request):
        """Get activities filtered by activity_type"""
        activity_type = request.query_params.get('activity_type')
        if not activity_type:
            return Response(
                {'error': 'activity_type parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        activities = Activity.objects.filter(activity_type=activity_type)
        serializer = self.get_serializer(activities, many=True)
        return Response(serializer.data)


class LeaderboardViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Leaderboard operations
    Provides CRUD operations for leaderboard rankings
    """
    queryset = Leaderboard.objects.all()
    serializer_class = LeaderboardSerializer

    @action(detail=False, methods=['get'])
    def current(self, request):
        """Get current leaderboard for a specific period"""
        period = request.query_params.get('period', 'weekly')
        
        try:
            leaderboard = Leaderboard.objects.filter(period=period).latest('period_start')
            serializer = self.get_serializer(leaderboard)
            return Response(serializer.data)
        except Leaderboard.DoesNotExist:
            return Response(
                {'error': f'No leaderboard found for period: {period}'},
                status=status.HTTP_404_NOT_FOUND
            )


class WorkoutViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Workout operations
    Provides CRUD operations for workout suggestions
    """
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer

    @action(detail=False, methods=['get'])
    def by_fitness_level(self, request):
        """Get workouts filtered by fitness level"""
        fitness_level = request.query_params.get('fitness_level', 'all')
        
        workouts = Workout.objects.filter(
            fitness_level__in=[fitness_level, 'all']
        )
        serializer = self.get_serializer(workouts, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_activity_type(self, request):
        """Get workouts filtered by activity type"""
        activity_type = request.query_params.get('activity_type')
        if not activity_type:
            return Response(
                {'error': 'activity_type parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        workouts = Workout.objects.filter(activity_type=activity_type)
        serializer = self.get_serializer(workouts, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def recommendations(self, request):
        """Get personalized workout recommendations for a user"""
        user_id = request.query_params.get('user_id')
        if not user_id:
            return Response(
                {'error': 'user_id parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user = User.objects.get(_id=user_id)
            workouts = Workout.objects.filter(
                fitness_level__in=[user.fitness_level, 'all']
            )[:5]  # Return top 5 recommendations
            serializer = self.get_serializer(workouts, many=True)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response(
                {'error': 'User not found'},
                status=status.HTTP_404_NOT_FOUND
            )
