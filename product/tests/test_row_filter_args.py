import json
from dataclasses import dataclass

from graphql_jwt.shortcuts import get_token

from core.models import User
from core.models.openimis_graphql_test_case import openIMISGraphQLTestCase
from core.test_helpers import create_test_interactive_user
from product.test_helpers import create_test_product
from program.test_helpers import create_test_program


@dataclass
class DummyContext:
    user: User


class ProductRowFilterArgsTest(openIMISGraphQLTestCase):
    """products: the legacy showHistory keeps its meaning, isDeleted is new.

    Validity is applied by Product.get_queryset (OP-2029) through ProductGQLType,
    not by the resolver: the resolver only states what showHistory means.
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        program = create_test_program(code="PRAPG", name="Row args")
        cls.live = create_test_product("PRAP001", custom_props={"program": program})
        cls.deleted = create_test_product(
            "PRAP002", valid=False, custom_props={"program": program})
        cls.copy = create_test_product(
            "PRAP003", valid=False,
            custom_props={"program": program, "legacy_id": cls.live.id})
        cls.admin = create_test_interactive_user(username="prodRowArgsAdmin")
        program.user.add(cls.admin.i_user)
        cls.token = get_token(cls.admin, DummyContext(user=cls.admin))

    def _codes(self, args=""):
        response = self.query(
            '{ products(search: "PRAP"%s) { edges { node { code } } } }' % args,
            headers={"HTTP_AUTHORIZATION": f"Bearer {self.token}"})
        self.assertResponseNoErrors(response)
        edges = json.loads(response.content)["data"]["products"]["edges"]
        return sorted(e["node"]["code"] for e in edges)

    def test_default_hides_deleted_products(self):
        self.assertEqual(["PRAP001"], self._codes())

    def test_show_history_keeps_its_legacy_meaning(self):
        # legacy: no validity filter at all, deleted products and history copies included
        self.assertEqual(["PRAP001", "PRAP002", "PRAP003"], self._codes(", showHistory: true"))
        self.assertEqual(["PRAP001"], self._codes(", showHistory: false"))

    def test_is_deleted(self):
        self.assertEqual(["PRAP002"], self._codes(", isDeleted: true"))
        self.assertEqual(["PRAP001"], self._codes(", isDeleted: false"))

    def test_is_deleted_overrides_show_history(self):
        self.assertEqual(["PRAP001", "PRAP003"], self._codes(", showHistory: true, isDeleted: false"))
