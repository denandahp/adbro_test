from django.core.management import BaseCommand
from django.db import transaction

from adbro_test.apps.publishers.model import Site, Slot, Publisher

from faker import Faker

class Command(BaseCommand):
    def handle(self, *args, **options):
        faker = Faker()

        with transaction.atomic():
            # Create publishers
            publishers_list = []
            for i in range(10):
                publisher = Publisher(name=faker.name())
                publishers_list.append(publisher)
            
            if publishers_list:
                publishers = Publisher.objects.bulk_create(publishers_list)

                # Create sites for each publisher
                sites_list = []
                for publisher in publishers:
                    for i in range(faker.random_int(1, 3)):
                        site = Site(publisher=publisher, name=faker.company())
                        sites_list.append(site)
            
            if sites_list:
                sites = Site.objects.bulk_create(sites_list)

                # Create slots for each site
                slots_list = []
                for site in sites:
                    for i in range(faker.random_int(1, 10)):
                        slot = Slot(site=site, name=faker.word())
                        slots_list.append(slot)
                Slot.objects.bulk_create(slots_list)
            
