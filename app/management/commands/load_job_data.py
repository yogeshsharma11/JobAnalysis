from django.core.management.base import BaseCommand
import pandas as pd
from app.models import Job
class Command(BaseCommand):
    help = 'Load job data from CSV'

    def handle(self, *args, **kwargs):
        file_path = 'C:/Users/LENOVO/Desktop/Intern/csv/myproject/interview_test.csv'
        data = pd.read_csv(file_path)
        for _, row in data.iterrows():
            if pd.isna(row['population']):
                print(f"Skipping row with missing population: {row}")
                continue

            Job.objects.create(
                title=row['title'],
                description=row['description'],
                city=row['city'],
                state=row['state'],
                population=int(row['population'] or 0),  
                latitude=row.get('latitude', 0.0),  
                longitude=row.get('longitude', 0.0)  
            )
