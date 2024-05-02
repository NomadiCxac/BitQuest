from django.test import TestCase
from django.urls import reverse
from .models import Shop, ItemTemplate, Player, StatSheet
from django.core.exceptions import ValidationError


# Create your tests here.
class ShopTestCase(TestCase):
    def setUp(self):
        Shop.objects.create(name="Test Shop", currency=100)

    def test_shop_creation(self):
        shop = Shop.objects.get(name="Test Shop")
        self.assertEqual(shop.currency, 100)

class ItemTemplateTests(TestCase):

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/rpg/items/')
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('rpg:item-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'rpg/items.html')

    def test_post_new_item(self):
        url = reverse('rpg:item-list')
        data = {
            'name': 'New Sword',
            'itemType': 'weapon',
            'stats[physical_damage]': '100',
            # Add other stats as necessary
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)  # Redirect expected after POST
        self.assertEqual(ItemTemplate.objects.last().name, 'New Sword')

    def setUp(self):
        # Setting up a reusable StatSheet for testing
        self.stat_sheet = StatSheet.objects.create(
            physical_damage=100,
            magic_damage=50,
            critical_damage=250,
            critical_chance=5,
            strength=10,
            intelligence=10,
            dexterity=10,
            focus=10,
            strength_modifier=110,
            intelligence_modifier=110,
            dexterity_modifier=110,
            focus_modifier=110
        )

    def test_item_template_creation_with_valid_stats(self):
        item = ItemTemplate.objects.create(
            name="Enchanted Sword",
            itemType="weapon",
            stats=self.stat_sheet
        )
        self.assertEqual(item.name, "Enchanted Sword")
        self.assertEqual(item.stats.physical_damage, 100)

    def test_item_template_prevents_negative_stats(self):
        # Negative values should raise a ValidationError during StatSheet creation
        with self.assertRaises(ValidationError):
            StatSheet.objects.create(
                physical_damage=-100,  # Invalid negative value
            ).full_clean()  # This will trigger validation

    def test_item_template_requirements(self):
        # Ensure item template requires physical or magic damage greater than 1
        new_stats = StatSheet.objects.create(
            physical_damage=0,
            magic_damage=0
        )
        with self.assertRaises(ValidationError):
            ItemTemplate.objects.create(
                name="Mystic Wand",
                itemType="weapon",
                stats=new_stats
            ).full_clean()
    
    def test_missing_name_and_itemType(self):
        # Create a StatSheet for use in testing
        stat_sheet = StatSheet.objects.create(physical_damage=10, magic_damage=20)

        # Test missing name
        with self.assertRaises(ValidationError):
            ItemTemplate.objects.create(
                name="",
                itemType="weapon",
                stats=stat_sheet
            ).full_clean()

        # Test missing itemType
        with self.assertRaises(ValidationError):
            ItemTemplate.objects.create(
                name="Magic Wand",
                itemType="",
                stats=stat_sheet
            ).full_clean()

        # Test missing both
        with self.assertRaises(ValidationError):
            ItemTemplate.objects.create(
                name="",
                itemType="",
                stats=stat_sheet
            ).full_clean()