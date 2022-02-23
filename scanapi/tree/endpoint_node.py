import copy
import logging
from itertools import chain
from typing import Any, Dict, Optional

from scanapi.evaluators import SpecEvaluator
from scanapi.exit_code import ExitCode
from scanapi.session import session
from scanapi.tree.request_node import RequestNode
from scanapi.tree.tree_keys import (
    DELAY_KEY,
    ENDPOINTS_KEY,
    HEADERS_KEY,
    NAME_KEY,
    PARAMS_KEY,
    PATH_KEY,
    REQUESTS_KEY,
    ROOT_SCOPE,
    VARS_KEY,
)
from scanapi.utils import join_urls, validate_keys

logger = logging.getLogger(__name__)


class EndpointNode:
    """
    Class that represents an endpoint. It follows a tree-like structure
    where each EndpointNode may contain multiple children EndpointNodes.

    Attributes:
        spec[dict]: dictionary containing the endpoint's specifications
        parent[EndpointNode, optional]: the parent node
        child_nodes[list of EndpointNodes]: the children nodes
        spec_vars[SpecEvaluator]: evaluator used to evaluate expressions
                                  and store spec variables
    """

    SCOPE = "endpoint"
    ALLOWED_KEYS = (
        ENDPOINTS_KEY,
        HEADERS_KEY,
        NAME_KEY,
        PARAMS_KEY,
        PATH_KEY,
        REQUESTS_KEY,
        DELAY_KEY,
        VARS_KEY,
    )
    REQUIRED_KEYS = (NAME_KEY,)
    ROOT_REQUIRED_KEYS = ()

    def __init__(self, spec, parent=None):
        self.spec = spec
        self.parent = parent
        self.child_nodes = []
        self.__build()
        self.spec_vars = SpecEvaluator(self, spec.get(VARS_KEY, {}))

    def __build(self):
        """Validate the EndpointNode keys and create children EndpointNodes
        from endpoints in its specifications.
        """
        self._validate()

        self.child_nodes = [
            EndpointNode(spec, parent=self)
            for spec in self.spec.get(ENDPOINTS_KEY, [])
        ]

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.name}>"

    @property
    def name(self):
        """Get the endpoint's name. The name is prepended by the parent's name,
        if it is not a root node.

        Returns:
            [str]: The endpoint's name.
        """
        name = self.spec.get(NAME_KEY, "")

        if self.is_root or not self.parent.name:
            return name

        return f"{self.parent.name}::{name}"

    @property
    def path(self):
        """Get the endpoint's path. The path is prepended by the parent's path,
        if it is not a root node. The returned path already has all variables
        evaluated.

        Returns:
            [str]: The endpoint's url.
        """
        path = str(self.spec.get(PATH_KEY, "")).strip()
        url = join_urls(self.parent.path, path) if self.parent else path

        return self.spec_vars.evaluate(url)

    @property
    def headers(self):
        """Get the headers used in the endpoint call. The headers of the
        call include the parent's headers.

        Returns:
            [dict]: the headers used in the endpoint call.
        """
        return self._get_specs(HEADERS_KEY)

    @property
    def params(self):
        """Get the parameters used in the endpoint call. The parameters of the
        call include the parent's parameters.

        Returns:
            [dict]: the parameters used in the endpoint call.
        """
        return self._get_specs(PARAMS_KEY)

    @property
    def delay(self):
        """Get the time in milliseconds to be waited before making the endpoint
        call.

        Returns:
            [int]: the time to be waited.
        """
        delay = self.spec.get(DELAY_KEY, 0)
        return delay or getattr(self.parent, DELAY_KEY, 0)

    @property
    def is_root(self):
        """Check if the EndpointNode is a root node.

        Returns:
            [bool]: true if the node has no parent, false otherwise.
        """
        return not self.parent

    def propagate_spec_vars(
        self,
        spec_vars: Dict[str, Any],
        extras: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Update the endpoint node spec_vars and propagate those changes
        to the parent nodes. It only includes new variables.

        Args:
            new_spec_vars [dic]: the new spec_vars.
            extras [dict]: extra variables used to update the spec_vars.
        """
        new_spec_vars = {
            key: value
            for key, value in spec_vars.items()
            if key not in self.spec_vars.registry
        }
        self.spec_vars.update(new_spec_vars, extras)
        if not self.is_root:
            self.parent.propagate_spec_vars(spec_vars, extras)

    def get_all_vars(self) -> Dict[str, Any]:
        """Get all variables in spec_vars from the node and its parents.

        Returns:
            [dict]: dict from the variable's name to its value.
        """
        variables = copy.deepcopy(self.spec_vars.registry)
        if not self.is_root:
            variables.update(self.parent.get_all_vars())
        return variables

    def run(self):
        """Run the requests of the node and all children nodes.

        Returns:
            [iterator]: Iterator that yields the test result of each request.
        """
        for request in self._get_requests():
            try:
                yield request.run()
            except Exception as e:
                error_message = f"\nError to make request `{request.full_url_path}`. \n{str(e)}\n"
                logger.error(error_message)
                session.exit_code = ExitCode.REQUEST_ERROR
                continue

    def _validate(self):
        """Private method that checks if the specification has any invalid key
        or if there is any required key missing.
        """
        required_keys = (
            self.ROOT_REQUIRED_KEYS if self.is_root else self.REQUIRED_KEYS
        )
        scope = ROOT_SCOPE if self.is_root else self.SCOPE

        validate_keys(self.spec.keys(), self.ALLOWED_KEYS, required_keys, scope)

    def _get_specs(self, field_name):
        """Get a specification of the endpoint.

        Args:
            field_name [str]: name of the specification field.

        Returns:
            [dict]: a dictionary containing the values of the field.
        """
        values = self.spec.get(field_name, {})
        parent_values = getattr(self.parent, field_name, None)

        if parent_values:
            return {**parent_values, **values}

        return values

    def _get_requests(self):
        """Get all requests from the node and children nodes as RequestNodes.

        Returns:
            [iterator]: Iterator that yields a RequestNode for
            each request.
        """
        return chain(
            (
                RequestNode(spec, self)
                for spec in self.spec.get(REQUESTS_KEY, [])
            ),
            *(child._get_requests() for child in self.child_nodes),
        )
