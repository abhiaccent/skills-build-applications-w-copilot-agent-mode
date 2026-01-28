
from django.core.management.base import BaseCommand
from octofit_tracker.models.models import User, Team, Activity, Workout, Leaderboard
from django.db import transaction
from pymongo import MongoClient

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Drop collections directly using pymongo
        client = MongoClient('mongodb://localhost:27017')
        db = client['octofit_db']
        self.stdout.write(self.style.WARNING('Dropping collections...'))
        for coll in ['activity', 'workout', 'leaderboard', 'user', 'team']:
            db[coll].drop()
        client.close()

        with transaction.atomic():
            self.stdout.write(self.style.SUCCESS('Creating teams...'))
            marvel = Team.objects.create(name='Marvel', description='Marvel superheroes')
            dc = Team.objects.create(name='DC', description='DC superheroes')

            self.stdout.write(self.style.SUCCESS('Creating users...'))
            users = [
                User.objects.create(name='Spider-Man', email='spiderman@marvel.com', team=marvel),
                User.objects.create(name='Iron Man', email='ironman@marvel.com', team=marvel),
                User.objects.create(name='Wonder Woman', email='wonderwoman@dc.com', team=dc),
                User.objects.create(name='Batman', email='batman@dc.com', team=dc),
            ]

            self.stdout.write(self.style.SUCCESS('Creating activities...'))
            Activity.objects.create(user=users[0], activity_type='Running', duration_minutes=30, date='2026-01-01')
            Activity.objects.create(user=users[1], activity_type='Cycling', duration_minutes=45, date='2026-01-02')
            Activity.objects.create(user=users[2], activity_type='Swimming', duration_minutes=60, date='2026-01-03')
            Activity.objects.create(user=users[3], activity_type='Yoga', duration_minutes=40, date='2026-01-04')

            self.stdout.write(self.style.SUCCESS('Creating workouts...'))
            w1 = Workout.objects.create(name='Hero HIIT', description='High intensity interval training for heroes')
            w2 = Workout.objects.create(name='Power Yoga', description='Yoga for strength and flexibility')
            w1.suggested_for.set([users[0], users[1]])
            w2.suggested_for.set([users[2], users[3]])

            self.stdout.write(self.style.SUCCESS('Creating leaderboards...'))
            Leaderboard.objects.create(team=marvel, total_points=100)
            Leaderboard.objects.create(team=dc, total_points=120)

            self.stdout.write(self.style.SUCCESS('Database populated with test data!'))
