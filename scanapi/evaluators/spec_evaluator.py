import logging
import re
from functools import singledispatch

from scanapi.evaluators.string_evaluator import StringEvaluator

logger = logging.getLogger(__name__)


class SpecEvaluator:
    def __init__(self, endpoint, spec_vars, extras=None, filter_responses=True):
        self.endpoint = endpoint
        self.registry = {}
        self.update(spec_vars, extras=extras, filter_responses=filter_responses)

    def evaluate(self, element):
        return evaluate(element, self)

    def evaluate_assertion(self, element):
        return _evaluate_str(element, self, is_a_test_case=True)

    def update(self, spec_vars, extras=None, filter_responses=False):
        if extras is None:
            extras = {}

        if filter_responses:
            spec_vars = self.filter_response_var(spec_vars)

        values = {
            key: evaluate(value, extras) for key, value in spec_vars.items()
        }
        self.registry.update(values)

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def __repr__(self):
        return self.registry.__repr__()

    def __getitem__(self, key):
        if key in self:
            return self.registry[key]

        all_vars = self.endpoint.get_all_vars()
        if key in all_vars:
            return all_vars[key]

        raise KeyError(key)

    def __delitem__(self, key):
        if key in self:
            del self.registry[key]
        else:
            raise KeyError(key)

    def __contains__(self, key):
        return key in self.registry

    def keys(self):
        """Returns a copy of the dictionary’s list of keys.
        Returns:
            [list]: list of keys.

        """
        return self.registry.keys()

    @classmethod
    def filter_response_var(cls, spec_vars):
        """Returns a copy of ``spec_vars`` without 'response' references.

        Any items with a ``response.*`` reference in their value are left out.

        Returns:
            [dict]: filtered dictionary.

        """
        pattern = re.compile(r"(?:(\s*response\.\w+))")
        return {k: v for k, v in spec_vars.items() if not pattern.search(v)}


@singledispatch
def evaluate(expression, spec_vars):
    return expression


@evaluate.register(str)
def _evaluate_str(element, spec_vars, is_a_test_case=False):
    return StringEvaluator.evaluate(element, spec_vars, is_a_test_case)


@evaluate.register(dict)
def _evaluate_dict(element, spec_vars):
    return {key: evaluate(value, spec_vars) for key, value in element.items()}


@evaluate.register(list)
@evaluate.register(tuple)
def _evaluate_collection(elements, spec_vars):
    return [evaluate(item, spec_vars) for item in elements]
