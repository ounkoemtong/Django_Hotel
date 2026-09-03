from app.accounts.models import Profile  # import Profile មកប្រើ
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from faker import Faker

User = get_user_model()


class Command(BaseCommand):
    help = "Seed the database with fake users for accounts app"

    def add_arguments(self, parser):
        parser.add_argument(
            "--count",
            type=int,
            default=10,
            help="Number of fake users to generate",
        )

    def handle(self, *args, **options):
        fake = Faker()
        count = options["count"]
        created_count = 0

        self.stdout.write(f"Seeding {count} users...")

        for _ in range(count):
            first_name = fake.first_name()
            last_name = fake.last_name()
            username = f"{first_name.lower()}.{last_name.lower()}{fake.random_int(10, 99)}"
            email = fake.unique.email()

            if User.objects.filter(username=username).exists():
                continue

            # ១. បង្កើត User
            user = User.objects.create_user(
                username=username,
                email=email,
                password="Password123!",
                first_name=first_name,
                last_name=last_name,
            )

            # ២. បង្កើត ឬ Update Profile ជាមួយ Fake Data តែម្តង
            profile, _ = Profile.objects.get_or_create(user=user)
            profile.phone = fake.phone_number()[:15]
            profile.address = fake.address()
            profile.save()

            created_count += 1

        self.stdout.write(
            self.style.SUCCESS(f"Successfully created {created_count} users!")
        )