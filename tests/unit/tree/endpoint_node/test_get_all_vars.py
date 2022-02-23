from pytest import mark

from scanapi.tree import EndpointNode


@mark.describe("endpoint node")
@mark.describe("get_all_vars")
class TestGetAllVars:
    @mark.it("should return spec_var values from the node and all parents")
    def test_get_all_vars(self):
        grandparent = EndpointNode({"name": "grandparent"})
        grandparent_key = "grandparent_key"
        grandparent_value = "grandparent_value"
        grandparent.spec_vars.registry[grandparent_key] = grandparent_value
        parent = EndpointNode({"name": "parent"}, grandparent)
        parent_key = "parent_key"
        parent_value = "parent_value"
        parent.spec_vars.registry[parent_key] = parent_value
        node = EndpointNode({"name": "node"}, parent)
        node_key = "node_key"
        node_value = "node_value"
        node.spec_vars.registry[node_key] = node_value

        spec_vars = node.get_all_vars()

        assert spec_vars == {
            grandparent_key: grandparent_value,
            parent_key: parent_value,
            node_key: node_value,
        }

    @mark.it("should not alter the content of spec_vars")
    def test_do_not_alter_spec_var(self):
        parent = EndpointNode({"name": "parent"})
        parent_key = "parent_key"
        parent_value = "parent_value"
        parent.spec_vars.registry[parent_key] = parent_value
        node = EndpointNode({"name": "node"}, parent)
        node_key = "node_key"
        node_value = "node_value"
        node.spec_vars.registry[node_key] = node_value

        node.get_all_vars()

        assert parent.spec_vars.registry == {parent_key: parent_value}
        assert node.spec_vars.registry == {node_key: node_value}
