"""get_queryset honours the OP-2029 validity contract (epic OP-3317, phase 1).

Ported from the openIMIS reference product/tests/test_row_filters.py
(feature/OP-3317), plus the row scope Cameroon now declares on Product and its
items / services.
"""
from datetime import datetime, timedelta

from django.test import TestCase

from core.models.row_filters import Validity
from core.test_helpers import (
    assert_row_filters, create_right_only_user, create_security_tree, create_test_interactive_user,
    mark_deleted)
from product.models import Product
from product.test_helpers import create_test_product


class ProductRowFiltersTest(TestCase):
    def test_product(self):
        user = create_test_interactive_user(username="prodrwf")
        live = create_test_product("RWF1")
        deleted = mark_deleted(create_test_product("RWF2"))
        assert_row_filters(
            self, Product, Product.objects.filter(id__in=[live.id, deleted.id]), user,
            live.id, deleted.id, default_hides_deleted=False,
        )

    def test_a_validity_date_picks_the_version_valid_then(self):
        user = create_test_interactive_user(username="prodrwf")
        product = create_test_product("RWF3")
        copy_id = product.save_history()
        rows = Product.objects.filter(code="RWF3")
        self.assertFalse(
            Product.get_queryset(rows, user, validity=Validity.at(product.validity_from - timedelta(days=1))).exists()
        )
        self.assertIn(
            product.id,
            Product.get_queryset(rows, user, validity=Validity.at(datetime.now() + timedelta(seconds=1)))
            .values_list("id", flat=True),
        )
        self.assertNotEqual(product.id, copy_id)


class ProductRowScopeTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.tree = create_security_tree("SPPR")
        cls.user = create_right_only_user("sppruser", [121001], [cls.tree.d1.id])
        cls.national = create_test_product("SPPRN")
        cls.own = create_test_product("SPPR1", custom_props={"location": cls.tree.r1})
        cls.foreign = create_test_product("SPPR2", custom_props={"location": cls.tree.r2})

    def test_national_and_own_region_only(self):
        visible = set(Product.get_queryset(Product.objects.filter(code__startswith="SPPR"), self.user)
                      .values_list("code", flat=True))
        self.assertEqual({"SPPRN", "SPPR1"}, visible)

    def test_items_follow_their_product(self):
        from product.models import ProductItem
        self.assertIn("product__location", ProductItem.location_paths())
