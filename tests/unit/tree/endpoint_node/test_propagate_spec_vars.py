from pytest import mark

from scanapi.tree import EndpointNode


@mark.describe("endpoint node")
@mark.describe("propagate_spec_vars")
class TestPropagateSpecVars:
    test_data = [
        ({"spec_var": "value"}, None, {"spec_var": "value"}),
        (
            {"spec_var": "${{ response }}"},
            {"response": "value"},
            {"spec_var": "value"},
        ),
    ]

    @mark.it("should update spec_vars of node and all parent nodes")
    @mark.parametrize("new_spec_vars, extra, expected_result", test_data)
    def test_propagate_spec_vars(self, new_spec_vars, extra, expected_result):
        grandparent = EndpointNode({"name": "grandparent"})
        parent = EndpointNode({"name": "parent"}, grandparent)
        node = EndpointNode({"name": "node"}, parent)

        node.propagate_spec_vars(new_spec_vars, extra)

        assert node.spec_vars.registry == expected_result
        assert parent.spec_vars.registry == expected_result
        assert grandparent.spec_vars.registry == expected_result

    @mark.context("when a var has the same name as an existing var in the node")
    @mark.it("should not change the value of the existing var in the node")
    def test_var_with_existing_name(self):
        parent_vars = {"parent_var": "parent_value"}
        parent = EndpointNode({"name": "parent"})
        parent.spec_vars.update(parent_vars)

        node_vars = {"node_var": "node_value"}
        node = EndpointNode({"name": "node"}, parent)
        node.spec_vars.update(node_vars)

        existing_parent_var = {"parent_var": "new_value"}
        existing_node_var = {"node_var": "new_value"}
        new_vars = {**existing_parent_var, **existing_node_var}
        node.propagate_spec_vars(new_vars)

        assert parent.spec_vars.registry == {**parent_vars, **existing_node_var}
        assert node.spec_vars.registry == {**node_vars, **existing_parent_var}
