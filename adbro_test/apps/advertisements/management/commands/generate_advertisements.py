import random

from django.core.management import BaseCommand
from django.db import transaction

from adbro_test.apps.advertisements.model import (
    Advertiser, Campaign, AdvertisementGroup, Advertisement,
    AdvertisementGroupTargetingRule)
from adbro_test.apps.advertisement_views.model import DenormalizedAdvertisement
from adbro_test.apps.publishers.model import Slot

from faker import Faker


class Command(BaseCommand):
    '''
    This command is to creates 10 advertisers with 1-5 campaign for each advertisers,
    and every campaign create 1-4 advertisement group 
    and every advertisement_group create 2 targeting rules and 1-10 advertisement.

    after data advertisement is created, next step is create DenormalizedAdvertisement
    with every data advertisement.
    '''
    def handle(self, *args, **options):
        faker = Faker()

        with transaction.atomic():
            # Create 10 advertisers
            bulk_create_advertisers_list = []
            for i in range(10):
                advertiser = Advertiser(name=faker.name())
                bulk_create_advertisers_list.append(advertiser)
            
            # Validate if bulk_create_advertisers_list is exist
            if bulk_create_advertisers_list:
                advertisers = Advertiser.objects.bulk_create(bulk_create_advertisers_list)

                # Create 1-5 campaigns for each advertiser 
                bulk_create_campaigns_list = []
                for advertiser in advertisers:
                    for i in range(random.randint(1, 5)):
                        campaign = Campaign(advertiser=advertiser, name=faker.sentence())
                        bulk_create_campaigns_list.append(campaign)

            # Validate if bulk_create_campaigns_list is exist
            if bulk_create_campaigns_list:
                campaigns= Campaign.objects.bulk_create(bulk_create_campaigns_list)

                # Create 1-4 advertisement groups for each campaign
                bulk_create_advertisement_group_list = []
                for campaign in campaigns:
                    for i in range(random.randint(1, 4)):
                        advertisement_group = AdvertisementGroup(campaign=campaign, name=faker.word())
                        bulk_create_advertisement_group_list.append(advertisement_group)

            # Validate if bulk_create_advertisement_list is exist
            bulk_create_advertisement_list = []
            if bulk_create_advertisement_group_list:
                advertisement_groups = AdvertisementGroup.objects.bulk_create(bulk_create_advertisement_group_list)

                for advertisement_group in advertisement_groups:
                    # Create 2 targeting rules for each advertisement group
                    for i in range(2):
                        targeting_rule = AdvertisementGroupTargetingRule.objects.create(
                            advertisement_group=advertisement_group,
                            tags=faker.word(),
                            description=faker.sentence())

                        # Select random 1-10 slot for pairing with targeting_rule
                        num_slots = faker.random_int(1, 10)
                        slots = random.sample(list(Slot.objects.all()), num_slots)
                        targeting_rule.slot.add(*slots)

                    # Create 1-10 advertisements for each advertisement group
                    for i in range(random.randint(1, 10)):
                        advertisement = Advertisement(advertisement_group=advertisement_group,
                                                      data=faker.paragraph(nb_sentences=5))
                        bulk_create_advertisement_list.append(advertisement)
            
            # Validate if bulk_create_advertisement_list is exist
            if bulk_create_advertisement_list:
                Advertisement.objects.bulk_create(bulk_create_advertisement_list)