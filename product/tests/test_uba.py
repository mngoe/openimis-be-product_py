"""
UBA coverage for the product module: the products an enrolment officer may enrol into.

The query right (121001) held globally opens every product, as before. Held in the UBA
bag by a user with an ENROLMENT link, it opens the national products (no location) and
the ones attached to a linked village or to any location above it.
"""
from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from django.test import TestCase

from core.apps import ENROLMENT_UBA_LINK_TYPE
from core.test_helpers import (
    create_test_interactive_user,
    create_test_role,
    create_test_user_business_access,
)
from location.models import Location
from location.test_helpers import create_test_village
from product.apps import ProductConfig
from product.models import Product
from product.schema import _products_scope
from product.test_helpers import create_test_product


class EnrolmentUbaProductScopeTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.village = create_test_village({"name": "UbaProdLinked"})
        cls.ward = cls.village.parent
        cls.district = cls.ward.parent
        cls.region = cls.district.parent
        cls.other_district = Location.objects.create(
            name="UbaProdOtherD", code="UBAPD2", type="D", parent=cls.region,
            audit_user_id=-1, validity_from="2019-01-01")

        right = int(ProductConfig.gql_query_products_perms[0])
        uba_role = create_test_role(name="UBA products", uba_rights=[right])
        global_role = create_test_role(name="Global products", rights=[right])
        cls.officer = create_test_interactive_user(username="ubaprodofficer", roles=[uba_role.id])
        cls.unlinked = create_test_interactive_user(username="ubaprodunlinked", roles=[uba_role.id])
        cls.global_user = create_test_interactive_user(username="ubaprodglobal", roles=[global_role.id])
        create_test_user_business_access(
            user=cls.officer, business_object=cls.village, link_type=ENROLMENT_UBA_LINK_TYPE)

        cls.national = create_test_product("UBAPN")
        cls.on_district = create_test_product("UBAPD", custom_props={"location": cls.district})
        cls.on_region = create_test_product("UBAPR", custom_props={"location": cls.region})
        cls.elsewhere = create_test_product("UBAPE", custom_props={"location": cls.other_district})
        cls.products = Product.objects.filter(code__startswith="UBAP")

    def setUp(self):
        cache.clear()

    def tearDown(self):
        cache.clear()

    def test_the_global_right_opens_every_product(self):
        self.assertIsNone(_products_scope(self.global_user))

    def test_an_officer_sees_the_national_products_and_the_ones_above_the_village(self):
        visible = set(self.products.filter(_products_scope(self.officer)).values_list("code", flat=True))
        self.assertEqual({"UBAPN", "UBAPD", "UBAPR"}, visible)

    def test_the_uba_right_without_a_link_is_refused(self):
        with self.assertRaises(PermissionDenied):
            _products_scope(self.unlinked)
