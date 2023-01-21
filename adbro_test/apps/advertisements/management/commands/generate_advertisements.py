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
    def handle(self, *args, **options):
        faker = Faker()

        with transaction.atomic():
            # Create advertisers
            bulk_create_advertisers_list = []
            for i in range(10):
                advertiser = Advertiser(name=faker.name())
                bulk_create_advertisers_list.append(advertiser)
            
            if bulk_create_advertisers_list:
                advertisers = Advertiser.objects.bulk_create(bulk_create_advertisers_list)

                # Create campaigns for each advertiser
                bulk_create_campaigns_list = []
                for advertiser in advertisers:
                    for i in range(random.randint(1, 5)):
                        campaign = Campaign(advertiser=advertiser, name=faker.sentence())
                        bulk_create_campaigns_list.append(campaign)

            if bulk_create_campaigns_list:
                campaigns= Campaign.objects.bulk_create(bulk_create_campaigns_list)

                # Create advertisement groups for each campaign
                bulk_create_advertisement_group_list = []
                for campaign in campaigns:
                    for i in range(random.randint(1, 4)):
                        advertisement_group = AdvertisementGroup(campaign=campaign, name=faker.word())
                        bulk_create_advertisement_group_list.append(advertisement_group)

            bulk_create_advertisement_list = []
            if bulk_create_advertisement_group_list:
                advertisement_groups = AdvertisementGroup.objects.bulk_create(bulk_create_advertisement_group_list)

                for advertisement_group in advertisement_groups:
                    # Create targeting rules for each advertisement group
                    for i in range(2):
                        targeting_rule = AdvertisementGroupTargetingRule.objects.create(
                            advertisement_group=advertisement_group,
                            tags=faker.word(),
                            description=faker.sentence())

                        # Randomly select a number of slots to associate with the targeting rule
                        num_slots = faker.random_int(1, 10)
                        slots = random.sample(list(Slot.objects.all()), num_slots)
                        targeting_rule.slot.add(*slots)

                    # Create advertisements for each advertisement group
                    for i in range(random.randint(1, 10)):
                        advertisement = Advertisement(advertisement_group=advertisement_group,
                                                    data=faker.paragraph(nb_sentences=5))
                        bulk_create_advertisement_list.append(advertisement)
            
            if bulk_create_advertisement_list:
                advertisements = Advertisement.objects.bulk_create(bulk_create_advertisement_list)

                # Create denormalized advertisement for each advertisement
                bulk_create_denormalized_advertisements = []
                for advertisement in advertisements:
                    advertisement_group = advertisement.advertisement_group
                    campaign = advertisement_group.campaign

                    targeting_rules = advertisement_group.targeting_rules.all()
                    for targeting_rule in targeting_rules:
                        slots = targeting_rule.slot.all()
                        for slot in slots:
                            denormalized_advertisement = DenormalizedAdvertisement(
                                advertisement=advertisement.guid,
                                group=advertisement_group.guid,
                                campaign=campaign.guid,
                                site=slot.site.guid,
                                slot=slot.guid,
                                tags=targeting_rule.tags,
                                data=advertisement.data
                            )
                            bulk_create_denormalized_advertisements.append(denormalized_advertisement)

                if bulk_create_denormalized_advertisements:
                    DenormalizedAdvertisement.objects.bulk_create(bulk_create_denormalized_advertisements)


