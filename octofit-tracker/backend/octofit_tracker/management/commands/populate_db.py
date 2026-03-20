from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from django.conf import settings
from pymongo import MongoClient

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **kwargs):
        # Delete all data
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Leaderboard.objects.all().delete()
        Workout.objects.all().delete()

        # Teams
        marvel = Team.objects.create(name='Marvel', description='Marvel Superheroes')
        dc = Team.objects.create(name='DC', description='DC Superheroes')

        # Users
        users = [
            User.objects.create(name='Spider-Man', email='spiderman@marvel.com', team=marvel.name),
            User.objects.create(name='Iron Man', email='ironman@marvel.com', team=marvel.name),
            User.objects.create(name='Wonder Woman', email='wonderwoman@dc.com', team=dc.name),
            User.objects.create(name='Batman', email='batman@dc.com', team=dc.name),
        ]

        # Activities
        Activity.objects.create(name='Running Club', description='Group running sessions for all fitness levels.', schedule='Mondays at 6pm', max_attendance=20)
        Activity.objects.create(name='Cycling Club', description='Outdoor and indoor cycling for endurance and fun.', schedule='Wednesdays at 6pm', max_attendance=15)
        Activity.objects.create(name='Swimming Club', description='Lap swimming and water fitness in the pool.', schedule='Fridays at 7am', max_attendance=12)
        Activity.objects.create(name='Yoga Club', description='Relaxation and flexibility through guided yoga sessions.', schedule='Thursdays at 5pm', max_attendance=10)
        Activity.objects.create(name='Manga Maniacs', description='Explore the fantastic stories of the most interesting characters from Japanese Manga (graphic novels).', schedule='Tuesdays at 7pm', max_attendance=15)

        # Leaderboard
        Leaderboard.objects.create(user=users[0], score=100)
        Leaderboard.objects.create(user=users[1], score=90)
        Leaderboard.objects.create(user=users[2], score=110)
        Leaderboard.objects.create(user=users[3], score=95)

        # Workouts
        Workout.objects.create(name='Pushups', description='Upper body', difficulty='Easy')
        Workout.objects.create(name='Squats', description='Lower body', difficulty='Medium')
        Workout.objects.create(name='Plank', description='Core', difficulty='Hard')

        # Ensure unique index on email for users
        client = MongoClient(settings.DATABASES['default']['CLIENT']['host'])
        db = client[settings.DATABASES['default']['NAME']]
        db.user.create_index('email', unique=True)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
