"""
Security parity tests for product (row scope + API rights) against the openimis-dev-tools
reference (release/26.10: `Product.row_scope = LocationScope("location")` + ScopedQuerysetMixin
on ProductGQLType). Each test asserts the REFERENCE behaviour: a failure is a gap in Cameroon.

Tags: [REF <reference file>::<test>] ported, [NEW] no reference equivalent.

Fixture: core.test_helpers.create_security_tree -> R1>D1>W1>V1 / R2>D2>W2>V2.
Products: national (no location), on R1, on R2. `user_a` holds the product rights in the
GLOBAL bag, district D1 only, and is a member of the products' program (Cameroon filters
`products` on the user's programs too).
"""
import json

from django.core.cache import cache
from django.core.exceptions import PermissionDenied
from django.test import TestCase, override_settings
from django.utils.translation import gettext as _

from core.models.openimis_graphql_test_case import openIMISGraphQLTestCase
from core.test_helpers import create_security_tree, create_right_only_user, get_test_token, perm_ids
from product.apps import ProductConfig
from product.models import Product

QUERY = perm_ids(ProductConfig.gql_query_products_perms)
WRITE = list(dict.fromkeys(
    perm_ids(ProductConfig.gql_mutation_products_add_perms)
    + perm_ids(ProductConfig.gql_mutation_products_edit_perms)
    + perm_ids(ProductConfig.gql_mutation_products_delete_perms)))


def _unauthorized(call):
    try:
        result = call()
    except PermissionDenied:
        return True
    text = json.dumps(result or [], default=str).lower()
    return "unauthorized" in text or _("unauthorized").lower() in text


def _build(prefix):
    from program.models import Program
    tree = create_security_tree(prefix)
    program = Program.objects.create(code=f"{prefix}PG", nameProgram=f"Program {prefix}")

    def product(code, location):
        return Product.objects.create(
            code=code, name=f"Test product {code}", lump_sum=1, max_members=5,
            grace_period_enrolment=1, insurance_period=12, date_from="2019-01-01",
            date_to="2049-01-01", validity_from="2019-01-01", audit_user_id=-1,
            program=program, location=location)

    prods = {"nat": product(f"{prefix}NAT", None), "r1": product(f"{prefix}PR1", tree.r1),
             "r2": product(f"{prefix}PR2", tree.r2)}
    return tree, program, prods


@override_settings(ROW_SECURITY=True)
class ProductReadScopeTest(openIMISGraphQLTestCase):

    @classmethod
    def setUpTestData(cls):
        cls.t, cls.program, cls.p = _build("SPR")
        cls.user_a = create_right_only_user("sprread", QUERY, [cls.t.d1.id])
        cls.program.user.add(cls.user_a.i_user)
        cls.token = get_test_token(cls.user_a)
        cls.no_right = create_right_only_user("sprnone", [], [cls.t.d1.id])
        cls.no_right_token = get_test_token(cls.no_right)

    def setUp(self):
        cache.clear()

    def _q(self, query, token=None):
        headers = {"HTTP_AUTHORIZATION": f"Bearer {token}"} if token else {}
        return json.loads(self.query(query, headers=headers).content)

    def test_gql_products_scoped(self):
        """[REF product LocationScope("location")] national + own-region products visible,
        the district-2 region's product hidden."""
        content = self._q('{ products(search: "SPR") { edges { node { code } } } }', self.token)
        self.assertNotIn("errors", content, content.get("errors"))
        codes = {e["node"]["code"] for e in content["data"]["products"]["edges"]}
        self.assertIn("SPRNAT", codes)
        self.assertIn("SPRPR1", codes)
        self.assertNotIn("SPRPR2", codes)

    def test_gql_product_by_uuid_foreign_region_denied(self):
        """[REF ProductGQLType(ScopedQuerysetMixin)] `product(uuid)` of a product on R2 is
        refused / null (Cameroon: `_products_scope` returns None for a global-bag user,
        schema.py:292, so `.get(uuid)` is unscoped)."""
        content = self._q(f'{{ product(uuid: "{self.p["r2"].uuid}") {{ code }} }}', self.token)
        product = (content.get("data") or {}).get("product")
        self.assertIsNone(product, "R2 product readable by uuid")

    def test_gql_product_by_uuid_own_region_allowed(self):
        """[control] `product(uuid)` of the R1 product works."""
        content = self._q(f'{{ product(uuid: "{self.p["r1"].uuid}") {{ code }} }}', self.token)
        self.assertEqual("SPRPR1", ((content.get("data") or {}).get("product") or {}).get("code"), content)

    def test_gql_products_without_right_denied(self):
        """[REF product/tests/test_rights_roles.py] no right -> error."""
        content = self._q('{ products { edges { node { code } } } }', self.no_right_token)
        self.assertIn("errors", content)

    def test_gql_products_anonymous_denied(self):
        """[REF core OrderedDjangoFilterConnectionField requires authentication] anonymous -> error."""
        content = self._q('{ products { edges { node { code } } } }')
        self.assertIn("errors", content)


@override_settings(ROW_SECURITY=True)
class ProductWriteScopeTest(TestCase):
    """[NEW] writes on a product attached to another region (the reference still looks
    the target up with an unscoped `Product.objects.get`, product/gql_mutations.py:129)."""

    @classmethod
    def setUpTestData(cls):
        cls.t, cls.program, cls.p = _build("SPS")
        cls.user_a = create_right_only_user("spswrite", list(dict.fromkeys(QUERY + WRITE)), [cls.t.d1.id])
        cls.program.user.add(cls.user_a.i_user)

    def setUp(self):
        cache.clear()

    def _valid(self, key):
        return Product.objects.filter(id=self.p[key].id, validity_to__isnull=True).exists()

    def test_delete_foreign_region_product_refused(self):
        """[NEW] DeleteProduct on the R2 product leaves it valid."""
        from product.gql_mutations import DeleteProductMutation
        try:
            DeleteProductMutation.async_mutate(self.user_a, uuids=[str(self.p["r2"].uuid)])
        except PermissionDenied:
            pass
        self.assertTrue(self._valid("r2"), "R2 product deleted by a district-1 user")

    def test_delete_own_region_product_allowed(self):
        """[control] DeleteProduct on the R1 product works."""
        from product.gql_mutations import DeleteProductMutation
        DeleteProductMutation.async_mutate(self.user_a, uuids=[str(self.p["r1"].uuid)])
        self.assertFalse(self._valid("r1"))

    def test_update_foreign_region_product_refused(self):
        """[NEW] UpdateProduct on the R2 product is refused for rights."""
        from product.gql_mutations import UpdateProductMutation
        self.assertTrue(_unauthorized(lambda: UpdateProductMutation.async_mutate(
            self.user_a, uuid=str(self.p["r2"].uuid), code="SPSPR2", name="SPS hacked")))

    def test_delete_without_right_refused(self):
        """[REF product/tests/test_rights_roles.py] no delete right -> PermissionDenied."""
        from product.gql_mutations import DeleteProductMutation
        reader = create_right_only_user("spsreader", QUERY, [self.t.d1.id])
        self.assertTrue(_unauthorized(lambda: DeleteProductMutation.async_mutate(
            reader, uuids=[str(self.p["r1"].uuid)])))
        self.assertTrue(self._valid("r1"))
