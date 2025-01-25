from .models import Job
from rest_framework.views import APIView
from rest_framework.response import Response
from geopy.distance import geodesic
from django.db.models import Count, Sum

# Create your views here.
class RoleAnalyticsView(APIView):
    def get(self, request):
        roles = {}
        jobs = Job.objects.all()

        for job in jobs:
            role = self.get_role_from_title(job.title)
            key = (role, job.city, job.state)
            if key not in roles:
                roles[key] = {'count': 0, 'population': 0}

            roles[key]['count'] += 1
            roles[key]['population'] += job.population

        result = [
            {
                'role': key[0],
                'city': key[1],
                'state': key[2],
                'count': data['count'],   
                'population': data['population']
            }
            for key, data in roles.items()
        ]

        return Response(result)

    def get_role_from_title(self, title):
        if 'RN' in title:
            return 'RN'
        elif 'LPN' in title:
            return 'LPN'
        else:
            return 'Other'


class JobRoleClusterView(APIView):
    def get(self, request):

        jobs = Job.objects.all()
        clusters = []

        for job in jobs:
            job_location = (job.latitude, job.longitude)
            job_role = self.get_role_from_title(job.title) 
            cluster_found = False

       
            for cluster in clusters:
                cluster_location = cluster['center']
                if geodesic(job_location, cluster_location).miles <= 50 and cluster['role'] == job_role:
                    # Add to existing cluster
                    cluster['jobs'].append(job)
                    cluster['population'] += job.population
                    cluster['job_count'] += 1
                    cluster['cities'].add(job.city)
                    cluster['states'].add(job.state)
                    cluster_found = True
                    break

           
            if not cluster_found:
                clusters.append({
                    'center': job_location,
                    'role': job_role,  
                    'jobs': [job],
                    'population': job.population,
                    'job_count': 1,
                    'cities': {job.city},  
                    'states': {job.state},  
                })

        
        result = []
        for cluster in clusters:
            city_list = list(cluster['cities'])
            state_list = list(cluster['states'])
            if len(city_list) > 3:
                location = f"{', '.join(city_list[:3])}, and {len(city_list) - 3} more cities, {', '.join(state_list)}"
            else:
                location = f"{', '.join(city_list)}, {', '.join(state_list)}"

            result.append({
                'role': cluster['role'],
                'location': location,
                'job_count': cluster['job_count'],
                'population': cluster['population']
            })

        return Response(result)

    def get_role_from_title(self, title):
        if 'LPN' in title.upper():
            return 'LPN'
        elif 'RN' in title.upper():
            return 'RN'
        else:
            return 'Other'

    

class RoleDistributionView(APIView):
    def get(self, request):
        data = (
            Job.objects.values("title", "city", "state")
            .annotate(job_count=Count("id"), total_population=Sum("population"))
            .order_by("state", "city", "title")
        )
        result = [
            {
                "role": item["title"],
                "city": item["city"],
                "state": item["state"],
                "job_count": item["job_count"],
                "population": item["total_population"],
            }
            for item in data
        ]

        return Response(result)


class RoleDistributionPerStateView(APIView):
    def get(self, request):
        data = (
            Job.objects.values("title", "state")
            .annotate(
                job_count=Count("id"),
                job_cities=Count("city", distinct=True) 
            )
            .order_by("state", "title")
        )
        result = [
            {
                "role": item["title"],
                "state": item["state"],
                "job_count": item["job_count"],
                "job_cities": item["job_cities"],
            }
            for item in data
        ]

        return Response(result)        