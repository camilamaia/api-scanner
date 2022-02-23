from pytest import fixture, mark, raises

from scanapi.evaluators.spec_evaluator import SpecEvaluator
from scanapi.tree import EndpointNode


@fixture
def mock_string_evaluate(mocker):
    return mocker.patch(
        "scanapi.evaluators.spec_evaluator.StringEvaluator.evaluate"
    )


@fixture
def mock_get_all_vars(mocker):
    return mocker.patch("scanapi.tree.endpoint_node.EndpointNode.get_all_vars")


@fixture
def spec_evaluator():
    parent = EndpointNode({"name": "bar", "requests": [{}]})
    endpoint = EndpointNode({"name": "foo", "requests": [{}]}, parent)
    return SpecEvaluator(endpoint, {"name": "foo"})


@mark.describe("spec evaluator")
@mark.describe("get")
class TestGet:
    @mark.context("when key does not exist")
    @mark.it("should return none")
    def test_should_return_none(self, spec_evaluator):
        key = "some_key"
        value = spec_evaluator.get(key)
        assert value is None

    @mark.describe("spec evaluator get key")
    @mark.context("when key exists")
    @mark.it("should return foo")
    def test_should_return_foo(self, spec_evaluator):
        key = "name"
        value = spec_evaluator.get(key)
        assert value == "foo"

    @mark.context("when key exists in endpoint node")
    @mark.it("should search endpoint node")
    @mark.it("should return the value in endpoint node")
    def test_should_return_list(self, mock_get_all_vars, spec_evaluator):
        key = "requests"
        expected_value = "value"
        mock_get_all_vars.side_effect = lambda: {key: expected_value}
        value = spec_evaluator.get(key)
        mock_get_all_vars.assert_called_once()
        assert value == expected_value


@mark.describe("spec evaluator")
@mark.describe("del")
class TestDel:
    @mark.describe("spec evaluator del key")
    @mark.context("when key does not exist")
    @mark.it("should raise key error")
    def test_should_raise_key_error(self, spec_evaluator):
        with raises(KeyError) as excinfo:
            key = "this_key_not_exists"
            del spec_evaluator[key]
        assert isinstance(excinfo.value, KeyError)

    @mark.describe("spec evaluator del key")
    @mark.context("when key exists")
    @mark.it("should del key")
    def test_should_del_key(self, spec_evaluator):
        key = "name"
        del spec_evaluator[key]
        assert key not in spec_evaluator


@mark.describe("spec evaluator")
@mark.describe("keys")
class TestKeys:
    @mark.describe("spec evaluator del key")
    @mark.context("when has keys")
    @mark.it("should return keys")
    def test_should_return_keys(self, spec_evaluator):
        assert spec_evaluator.keys() == {"name": "foo"}.keys()


@mark.describe("spec evaluator")
@mark.describe("filter response var")
class TestFilterResponseVar:
    @mark.describe("spec evaluator filter response var")
    @mark.context("when there is response var to evaluate")
    @mark.it("should return dictionary without response var")
    def test_should_return_dictionary_without_response_var(
        self, spec_evaluator
    ):
        spec_vars = {"var_1": "${{response.json()['key']}}", "var_2": "foo"}
        assert spec_evaluator.filter_response_var(spec_vars) == {"var_2": "foo"}


@mark.describe("spec evaluator")
@mark.describe("_evaluate_str")
class TestEvaluateString:
    @mark.describe("evaluate string")
    @mark.it("should call evaluate string")
    def test_should_call_evaluate_string(
        self, spec_evaluator, mock_string_evaluate
    ):
        string = "foo"
        spec_evaluator.evaluate(string)
        assert mock_string_evaluate.called_once_with(string)

    @mark.describe("evaluate string")
    @mark.it("should call evaluate assertion string")
    def test_should_call_evaluate_assertion_string(
        self, spec_evaluator, mock_string_evaluate
    ):
        string = "foo"
        spec_evaluator.evaluate_assertion(string)
        assert mock_string_evaluate.called_once_with(string)


@mark.describe("spec evaluator")
@mark.describe("_evaluate_dict")
class TestEvaluateDict:
    @mark.context("when dict is empty")
    @mark.it("return empty dict")
    def test_return_empty_dict(self, spec_evaluator):
        evaluated_dict = spec_evaluator.evaluate({})
        assert len(evaluated_dict) == 0

    @mark.context("when dict is not empty")
    @mark.it("return evaluated dict")
    def test_return_evaluated_dict(
        self, spec_evaluator, mocker, mock_string_evaluate
    ):
        mock_string_evaluate.side_effect = ["foo", "bar"]
        assert spec_evaluator.evaluate({"app_id": "foo", "token": "bar"}) == {
            "app_id": "foo",
            "token": "bar",
        }

        mock_string_evaluate.assert_has_calls(
            [
                mocker.call("foo", spec_evaluator, False),
                mocker.call("bar", spec_evaluator, False),
            ]
        )


@mark.describe("spec evaluator")
@mark.describe("_evaluate_list")
class TestEvaluateList:
    @mark.context("when list is empty")
    @mark.it("should return empty list")
    def test_return_empty_list(self, spec_evaluator):
        evaluated_list = spec_evaluator.evaluate([])
        assert len(evaluated_list) == 0

    @mark.context("when list is not empty")
    @mark.it("should return evaluated list")
    def test_return_evaluated_list(
        self, spec_evaluator, mocker, mock_string_evaluate
    ):
        values = ["foo", "bar"]
        mock_string_evaluate.side_effect = values
        assert spec_evaluator.evaluate(values) == ["foo", "bar"]

        mock_string_evaluate.assert_has_calls(
            [
                mocker.call("foo", spec_evaluator, False),
                mocker.call("bar", spec_evaluator, False),
            ]
        )


@mark.describe("spec evaluator")
@mark.describe("__repr__")
class TestRepr:
    @mark.context("when registry is empty")
    @mark.it("should return {}")
    def test_when_registry_is_empty(self):
        spec_evaluator = SpecEvaluator({}, {})
        assert repr(spec_evaluator) == "{}"

    @mark.context("when registry is not empty")
    @mark.it("should return {'name': 'foo'}")
    def test_when_registry_is_not_empty(self, spec_evaluator):
        assert repr(spec_evaluator) == "{'name': 'foo'}"
