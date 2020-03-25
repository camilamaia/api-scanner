import pytest

from scanapi.refactor.tree import EndpointNode, RequestNode


class TestRequestNode:
    @pytest.fixture
    def mock_evaluate(self, mocker):
        mock_func = mocker.patch(
            "scanapi.refactor.tree.request_node.SpecEvaluator.evaluate"
        )
        mock_func.return_value = ""

        return mock_func

    class TestHTTPMethod:
        def test_when_request_has_method(self):
            request = RequestNode({"method": "put"}, endpoint=EndpointNode({}))
            assert request.http_method == "put"

        def test_when_request_has_no_method(self):
            request = RequestNode({}, endpoint=EndpointNode({}))
            assert request.http_method == "get"

    class TestName:
        def test_when_request_has_name(self):
            request = RequestNode({"name": "list-users"}, endpoint=EndpointNode({}))
            assert request.name == "list-users"

        @pytest.mark.skip("it should validate mandatory `name` key before")
        def test_when_request_has_no_name(self):
            request = RequestNode({}, endpoint=EndpointNode({}))

    class TestFullPathUrl:
        def test_request_with_no_path(self):
            base_path = "http://foo.com/"
            request = RequestNode({}, endpoint=EndpointNode({"path": base_path}))
            assert request.full_url_path == base_path

        def test_when_endpoint_has_no_url(self):
            path = "http://foo.com"
            request = RequestNode({"path": path}, endpoint=EndpointNode({}))
            assert request.full_url_path == path

        def test_when_endpoint_has_url(self):
            endpoint_path = "http://foo.com/api"
            endpoint = EndpointNode({"path": endpoint_path})
            request = RequestNode({"path": "/foo"}, endpoint=endpoint)
            assert request.full_url_path == f"http://foo.com/api/foo"

        def test_with_trailing_slashes(self):
            endpoint = EndpointNode({"path": "http://foo.com/"})
            request = RequestNode({"path": "/foo/"}, endpoint=endpoint)
            assert request.full_url_path == "http://foo.com/foo/"

        def test_calls_evaluate(self, mocker, mock_evaluate):
            endpoint = EndpointNode({"path": "http://foo.com/"})
            request = RequestNode({"path": "/foo/"}, endpoint=endpoint)
            request.full_url_path
            calls = [mocker.call("http://foo.com/"), mocker.call("/foo/")]

            mock_evaluate.assert_has_calls(calls)

    class TestHeaders:
        def test_when_endpoint_has_no_headers(self):
            headers = {"abc": "def"}
            request = RequestNode({"headers": headers}, endpoint=EndpointNode({}))
            assert request.headers == headers

        def test_when_endpoint_has_headers(self):
            headers = {"abc": "def"}
            endpoint_headers = {"xxx": "www"}
            request = RequestNode(
                {"headers": headers},
                endpoint=EndpointNode({"headers": endpoint_headers}),
            )
            assert request.headers == {"abc": "def", "xxx": "www"}

        def test_with_repeated_keys(self):
            headers = {"abc": "def"}
            endpoint_headers = {"xxx": "www", "abc": "zxc"}
            request = RequestNode(
                {"headers": headers},
                endpoint=EndpointNode({"headers": endpoint_headers}),
            )
            assert request.headers == {"abc": "def", "xxx": "www"}

        def test_calls_evaluate(self, mocker, mock_evaluate):
            endpoint = EndpointNode({"headers": {"abc": "def"}})

            request = RequestNode({"headers": {"ghi": "jkl"}}, endpoint=endpoint)
            request.headers
            calls = [mocker.call({"abc": "def", "ghi": "jkl"})]

            mock_evaluate.assert_has_calls(calls)

    class TestParams:
        def test_when_endpoint_has_no_params(self):
            params = {"abc": "def"}
            request = RequestNode({"params": params}, endpoint=EndpointNode({}))
            assert request.params == params

        def test_when_endpoint_has_params(self):
            params = {"abc": "def"}
            endpoint_params = {"xxx": "www"}
            request = RequestNode(
                {"params": params}, endpoint=EndpointNode({"params": endpoint_params})
            )
            assert request.params == {"abc": "def", "xxx": "www"}

        def test_with_repeated_keys(self):
            params = {"abc": "def"}
            endpoint_params = {"xxx": "www", "abc": "zxc"}
            request = RequestNode(
                {"params": params}, endpoint=EndpointNode({"params": endpoint_params})
            )
            assert request.params == {"abc": "def", "xxx": "www"}

        def test_calls_evaluate(self, mocker, mock_evaluate):
            endpoint = EndpointNode({"params": {"abc": "def"}})

            request = RequestNode({"params": {"ghi": "jkl"}}, endpoint=endpoint)
            request.params
            calls = [mocker.call({"abc": "def", "ghi": "jkl"})]

            mock_evaluate.assert_has_calls(calls)

    class TestBody:
        def test_when_request_has_no_body(self):
            request = RequestNode({}, endpoint=EndpointNode({}))
            assert request.body == {}

        def test_when_request_has_no_body(self):
            request = RequestNode({"body": {"abc": "def"}}, endpoint=EndpointNode({}))
            assert request.body == {"abc": "def"}

        def test_calls_evaluate(self, mocker, mock_evaluate):
            request = RequestNode({"body": {"ghi": "jkl"}}, endpoint=EndpointNode({}))
            request.body
            calls = [mocker.call({"ghi": "jkl"})]

            mock_evaluate.assert_has_calls(calls)

    class TestRun:
        @pytest.fixture
        def mock_request(self, mocker):
            return mocker.patch("scanapi.refactor.tree.request_node.requests.request")

        def test_calls_request(self, mock_request):
            request = RequestNode({}, endpoint=EndpointNode({}))
            request.run()

            mock_request.assert_called_once_with(
                request.http_method,
                request.full_url_path,
                headers=request.headers,
                params=request.params,
                json=request.body,
                allow_redirects=False,
            )
