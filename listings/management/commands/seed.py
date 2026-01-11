from django.core.management.base import BaseCommand
from listings.models import Listing
import random

class Command(BaseCommand):
    help = 'Seed the database with sample listings data'

    def handle(self, *args, **kwargs):
        sample_titles = [
            'Modern Apartment in City Center',
            'Cozy Cottage by the Lake',
            'Spacious Family Home',
            'Beachfront Villa',
            'Luxury Mountain Cabin'
        ]
        locations = [
            'London', 'Paris', 'Lagos', 'Nairobi', 'Cape Town'
        ]
        descriptions = [
            'A beautiful place to stay.', 'Close to main attractions.', 'Quiet and relaxing.', 'Great amenities.', 'Perfect for families.'
        ]

        Listing.objects.all().delete()
        for i in range(10):
            listing = Listing.objects.create(
                title=random.choice(sample_titles),
                description=random.choice(descriptions),
                location=random.choice(locations),
                price=random.uniform(50, 500)
            )
            print(f'Created listing: {listing.title}')
