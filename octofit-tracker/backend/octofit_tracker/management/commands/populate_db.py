from django.core.management.base import BaseCommand
from pymongo import MongoClient
from datetime import datetime, timedelta
import random


class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Connect to MongoDB
        client = MongoClient('localhost', 27017)
        db = client['octofit_db']

        self.stdout.write(self.style.SUCCESS('Connected to octofit_db'))

        # Clear existing data
        self.stdout.write('Clearing existing data...')
        db.users.delete_many({})
        db.teams.delete_many({})
        db.activities.delete_many({})
        db.leaderboard.delete_many({})
        db.workouts.delete_many({})

        # Create unique index on email field
        db.users.create_index([("email", 1)], unique=True)
        self.stdout.write(self.style.SUCCESS('Created unique index on email field'))

        # Insert Teams
        self.stdout.write('Creating teams...')
        teams = [
            {
                '_id': 'team_marvel',
                'name': 'Team Marvel',
                'description': 'Earth\'s Mightiest Heroes',
                'created_at': datetime.now(),
                'member_count': 0
            },
            {
                '_id': 'team_dc',
                'name': 'Team DC',
                'description': 'Justice League United',
                'created_at': datetime.now(),
                'member_count': 0
            }
        ]
        db.teams.insert_many(teams)
        self.stdout.write(self.style.SUCCESS(f'Created {len(teams)} teams'))

        # Insert Users
        self.stdout.write('Creating superhero users...')
        users = [
            # Team Marvel
            {
                '_id': 'user_ironman',
                'name': 'Tony Stark',
                'email': 'ironman@avengers.com',
                'hero_name': 'Iron Man',
                'team_id': 'team_marvel',
                'joined_at': datetime.now() - timedelta(days=100),
                'total_points': 950
            },
            {
                '_id': 'user_spiderman',
                'name': 'Peter Parker',
                'email': 'spiderman@avengers.com',
                'hero_name': 'Spider-Man',
                'team_id': 'team_marvel',
                'joined_at': datetime.now() - timedelta(days=80),
                'total_points': 890
            },
            {
                '_id': 'user_blackwidow',
                'name': 'Natasha Romanoff',
                'email': 'blackwidow@avengers.com',
                'hero_name': 'Black Widow',
                'team_id': 'team_marvel',
                'joined_at': datetime.now() - timedelta(days=95),
                'total_points': 870
            },
            {
                '_id': 'user_captainamerica',
                'name': 'Steve Rogers',
                'email': 'cap@avengers.com',
                'hero_name': 'Captain America',
                'team_id': 'team_marvel',
                'joined_at': datetime.now() - timedelta(days=110),
                'total_points': 920
            },
            {
                '_id': 'user_thor',
                'name': 'Thor Odinson',
                'email': 'thor@avengers.com',
                'hero_name': 'Thor',
                'team_id': 'team_marvel',
                'joined_at': datetime.now() - timedelta(days=120),
                'total_points': 880
            },
            # Team DC
            {
                '_id': 'user_batman',
                'name': 'Bruce Wayne',
                'email': 'batman@justiceleague.com',
                'hero_name': 'Batman',
                'team_id': 'team_dc',
                'joined_at': datetime.now() - timedelta(days=105),
                'total_points': 940
            },
            {
                '_id': 'user_superman',
                'name': 'Clark Kent',
                'email': 'superman@justiceleague.com',
                'hero_name': 'Superman',
                'team_id': 'team_dc',
                'joined_at': datetime.now() - timedelta(days=115),
                'total_points': 980
            },
            {
                '_id': 'user_wonderwoman',
                'name': 'Diana Prince',
                'email': 'wonderwoman@justiceleague.com',
                'hero_name': 'Wonder Woman',
                'team_id': 'team_dc',
                'joined_at': datetime.now() - timedelta(days=100),
                'total_points': 910
            },
            {
                '_id': 'user_flash',
                'name': 'Barry Allen',
                'email': 'flash@justiceleague.com',
                'hero_name': 'The Flash',
                'team_id': 'team_dc',
                'joined_at': datetime.now() - timedelta(days=85),
                'total_points': 860
            },
            {
                '_id': 'user_aquaman',
                'name': 'Arthur Curry',
                'email': 'aquaman@justiceleague.com',
                'hero_name': 'Aquaman',
                'team_id': 'team_dc',
                'joined_at': datetime.now() - timedelta(days=90),
                'total_points': 850
            }
        ]
        db.users.insert_many(users)
        self.stdout.write(self.style.SUCCESS(f'Created {len(users)} superhero users'))

        # Update team member counts
        db.teams.update_one({'_id': 'team_marvel'}, {'$set': {'member_count': 5}})
        db.teams.update_one({'_id': 'team_dc'}, {'$set': {'member_count': 5}})

        # Insert Activities
        self.stdout.write('Creating activities...')
        activity_types = [
            'Running', 'Cycling', 'Swimming', 'Weight Training', 
            'Hero Training', 'Combat Practice', 'Flying', 'Super Speed Training'
        ]
        
        activities = []
        for user in users:
            for i in range(random.randint(5, 10)):
                days_ago = random.randint(1, 30)
                duration = random.randint(20, 120)
                distance = round(random.uniform(2, 15), 2) if random.choice([True, False]) else None
                activity_type = random.choice(activity_types)
                
                activities.append({
                    'user_id': user['_id'],
                    'activity_type': activity_type,
                    'duration': duration,  # minutes
                    'distance': distance,  # km
                    'calories': random.randint(150, 800),
                    'points': random.randint(10, 100),
                    'date': datetime.now() - timedelta(days=days_ago),
                    'notes': f'{user["hero_name"]} {activity_type.lower()} session'
                })
        
        db.activities.insert_many(activities)
        self.stdout.write(self.style.SUCCESS(f'Created {len(activities)} activities'))

        # Insert Workouts
        self.stdout.write('Creating workout suggestions...')
        workouts = [
            {
                'name': 'Hero Strength Training',
                'description': 'Build superhuman strength',
                'difficulty': 'intermediate',
                'duration': 45,
                'exercises': [
                    {'name': 'Super Squats', 'sets': 4, 'reps': 12},
                    {'name': 'Power Push-ups', 'sets': 3, 'reps': 15},
                    {'name': 'Hero Deadlifts', 'sets': 4, 'reps': 10}
                ],
                'category': 'strength'
            },
            {
                'name': 'Speed Force Cardio',
                'description': 'Lightning-fast cardio workout',
                'difficulty': 'advanced',
                'duration': 30,
                'exercises': [
                    {'name': 'Sprint Intervals', 'sets': 8, 'duration': '30 seconds'},
                    {'name': 'High Knees', 'sets': 4, 'duration': '1 minute'},
                    {'name': 'Burpees', 'sets': 3, 'reps': 20}
                ],
                'category': 'cardio'
            },
            {
                'name': 'Warrior Flexibility',
                'description': 'Improve agility and flexibility',
                'difficulty': 'beginner',
                'duration': 25,
                'exercises': [
                    {'name': 'Dynamic Stretching', 'duration': '5 minutes'},
                    {'name': 'Yoga Flow', 'duration': '15 minutes'},
                    {'name': 'Cool Down Stretches', 'duration': '5 minutes'}
                ],
                'category': 'flexibility'
            },
            {
                'name': 'Combat Core Training',
                'description': 'Build a steel core',
                'difficulty': 'intermediate',
                'duration': 35,
                'exercises': [
                    {'name': 'Plank Holds', 'sets': 3, 'duration': '1 minute'},
                    {'name': 'Russian Twists', 'sets': 4, 'reps': 20},
                    {'name': 'Leg Raises', 'sets': 3, 'reps': 15},
                    {'name': 'Mountain Climbers', 'sets': 4, 'duration': '45 seconds'}
                ],
                'category': 'core'
            },
            {
                'name': 'Endurance Mission',
                'description': 'Build stamina for long missions',
                'difficulty': 'intermediate',
                'duration': 60,
                'exercises': [
                    {'name': 'Long Distance Run', 'duration': '40 minutes'},
                    {'name': 'Jump Rope', 'duration': '10 minutes'},
                    {'name': 'Cool Down Walk', 'duration': '10 minutes'}
                ],
                'category': 'endurance'
            }
        ]
        db.workouts.insert_many(workouts)
        self.stdout.write(self.style.SUCCESS(f'Created {len(workouts)} workout suggestions'))

        # Insert Leaderboard
        self.stdout.write('Creating leaderboard...')
        leaderboard = []
        for user in users:
            leaderboard.append({
                'user_id': user['_id'],
                'name': user['name'],
                'hero_name': user['hero_name'],
                'team_id': user['team_id'],
                'total_points': user['total_points'],
                'activities_completed': random.randint(15, 50),
                'rank': 0,  # Will be calculated
                'last_updated': datetime.now()
            })
        
        # Sort by points and assign ranks
        leaderboard.sort(key=lambda x: x['total_points'], reverse=True)
        for idx, entry in enumerate(leaderboard, start=1):
            entry['rank'] = idx
        
        db.leaderboard.insert_many(leaderboard)
        self.stdout.write(self.style.SUCCESS(f'Created leaderboard with {len(leaderboard)} entries'))

        # Display summary
        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS('Database Population Summary:'))
        self.stdout.write('='*50)
        self.stdout.write(f'Teams: {db.teams.count_documents({})}')
        self.stdout.write(f'Users: {db.users.count_documents({})}')
        self.stdout.write(f'Activities: {db.activities.count_documents({})}')
        self.stdout.write(f'Workouts: {db.workouts.count_documents({})}')
        self.stdout.write(f'Leaderboard Entries: {db.leaderboard.count_documents({})}')
        self.stdout.write('='*50)
        self.stdout.write(self.style.SUCCESS('\nDatabase populated successfully!'))
        
        # Display top 3 heroes
        self.stdout.write('\nTop 3 Heroes:')
        for entry in leaderboard[:3]:
            self.stdout.write(
                f"{entry['rank']}. {entry['hero_name']} ({entry['name']}) - "
                f"{entry['total_points']} points - Team: {entry['team_id'].replace('team_', '').title()}"
            )

        client.close()
