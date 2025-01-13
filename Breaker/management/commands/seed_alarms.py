from django.core.management.base import BaseCommand
from Breaker.models import Alarm
from datetime import datetime, timedelta
import random

class Command(BaseCommand):
    help = 'Seed the Alarm table with 100 dummy rows'

    def handle(self, *args, **kwargs):
        # Clear existing data if needed (optional)
        # Alarm.objects.all().delete()

        # Define some dummy data for randomization
        areas = ['GT1', 'GT2', 'GT3', 'GT4', 'GT5']
        categories = ['52G-1', '52G-2', '52G-3', '52G-4', '52G-5']
        statuses = ['WAS CLOSED IS OPEN', 'WAS OPEN IS CLOSED']
        users = [95419, 97600, 75031, 100935]

        start_date = datetime(2024, 1, 1, 0, 0, 0)

        for i in range(100):
            random_date = start_date + timedelta(days=random.randint(0, 365), hours=random.randint(0, 23), minutes=random.randint(0, 59))
            area = random.choice(areas)
            category = random.choice(categories)
            user = random.choice(users)
            status = random.choice(statuses)

            # Create the dummy entry
            Alarm.objects.create(
                hist_timestamp=datetime(1980, 1, 1, 0, 0, 0),
                hist_timestamp_dst='s',
                hcapi_subscript=0,
                time=random_date,
                text=f"8780 013CB {category} [ {area} BKR ] BREAKER STATUS MANUAL ENTRY BY {user} {status}",
                area=area,
                category=category,
                excdef=category[:4],
                location=f"{area}_LOC",
                time_soe=random_date + timedelta(seconds=random.randint(0, 3600)),
                compid=f"{area}_COMP",
                seqnum=random.randint(100000, 999999),
                audible=random.randint(0, 1),
                event=random.randint(0, 1),
                abnormal=random.randint(0, 1),
                unackiss=random.randint(0, 1),
                priornum=random.randint(1, 10),
                ms=random.randint(1, 10),
                time_dst='s',
                time_soe_dst='s',
            )

        self.stdout.write(self.style.SUCCESS('Successfully seeded the Alarm table with 100 rows!'))
