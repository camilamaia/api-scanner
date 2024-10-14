#!/usr/bin/env python3
import datetime
import pathlib
import webbrowser
from importlib.metadata import version

from scanapi.console import write_report_path
from scanapi.session import session
from scanapi.settings import settings
from scanapi.template_render import render


class Reporter:
    """Class that writes the scan report

    Attributes:
        output_path[str, optional]: Report output path
        template[str, optional]: Custom report template path

    """

    def __init__(self, output_path=None, template=None):
        """Creates a Reporter instance object."""
        self.output_path = pathlib.Path(output_path or "scanapi-report.html")
        self.template = template

    def write(self, results, open_in_browser):
        """Part of the Reporter instance that is responsible for writing
        scanapi-report.html.

        Args:
            results [generator]: generator of dicts resulting of Request run().

        Returns:
            None

        """
        template_path = self.template if self.template else "report.html"
        has_external_template = bool(self.template)
        context = self._build_context(results)

        content = render(template_path, context, has_external_template)

        with open(self.output_path, "w", newline="\n") as doc:
            doc.write(content)

        write_report_path(self.output_path.resolve().as_uri())

        if open_in_browser:
            self._open_in_browser()

    def _open_in_browser(self):
        """Open the results file on a browser"""
        webbrowser.open(self.output_path.resolve().as_uri())

    @staticmethod
    def _build_context(results):
        """Build context dict of values required to render template.

        Args:
            results [generator]: generator of dicts resulting of Request run().

        Returns:
            [dict]: values required to render template.

        """
        return {
            "now": datetime.datetime.now().replace(microsecond=0),
            "project_name": settings.get("project_name", ""),
            "results": results,
            "session": session,
            "scanapi_version": version("scanapi"),
        }
