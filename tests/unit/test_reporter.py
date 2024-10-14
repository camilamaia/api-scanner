import pathlib

from freezegun.api import FakeDatetime
from pytest import fixture, mark

from scanapi.reporter import Reporter

fake_results = [
    {"response": "foo", "tests_results": [], "no_failure": True},
    {"response": "bar", "tests_results": [], "no_failure": False},
]


@mark.describe("reporter")
@mark.describe("__init__")
class TestInit:
    @mark.context("when there is no argument")
    @mark.it(
        "should set output_path with the default value `scanapi-report.html`.\n\t\t\b\b"
        "should set template as None"
    )
    def test_init_output_path_and_template(self):
        reporter = Reporter()

        assert str(reporter.output_path) == "scanapi-report.html"
        assert reporter.template is None

    @mark.context("when there is a template argument")
    @mark.it(
        "should set output_path with the default value `scanapi-report.html`.\n\t\t\b\b"
        "should set template accordingly"
    )
    def test_init_output_path_and_template_2(self):
        reporter = Reporter(template="my_template.jinja")

        assert str(reporter.output_path) == "scanapi-report.html"
        assert reporter.template == "my_template.jinja"

    @mark.context("when there is an output path argument")
    @mark.it(
        "should set output_path accordingly.\n\t\t\b\bshould set template as None"
    )
    def test_init_output_path_and_template_3(self):
        reporter = Reporter(output_path="my-report.html")

        assert str(reporter.output_path) == "my-report.html"
        assert reporter.template is None


@mark.describe("reporter")
@mark.describe("write")
@mark.freeze_time("2020-05-12 11:32:34")
class TestWrite:
    @fixture
    def mocked__render(self, mocker):
        return mocker.patch("scanapi.reporter.render")

    @fixture
    def mocked__session(self, mocker):
        return mocker.patch("scanapi.reporter.session")

    @fixture
    def mocked__logger(self, mocker):
        return mocker.patch("scanapi.reporter.logger")

    @fixture
    def mocked__webbrowser(self, mocker):
        return mocker.patch("scanapi.reporter.webbrowser")

    @fixture
    def mock_version(self, mocker):
        mocker.patch("scanapi.reporter.version", return_value="2.0.0")

    @fixture
    def context(self, mocked__session):
        return {
            "now": FakeDatetime(2020, 5, 12, 11, 32, 34),
            "project_name": "",
            "results": fake_results,
            "session": mocked__session,
            "scanapi_version": "2.0.0",
        }

    @fixture
    def mocked__open(self, mocker):
        mock = mocker.mock_open()
        mocker.patch("scanapi.reporter.open", mock)
        return mock

    @mark.it("should write to default output")
    def test_should_write_to_default_output(
        self,
        mocker,
        mocked__render,
        mocked__open,
        mocked__session,
        mock_version,
        context,
    ):
        mocked__render.return_value = "ScanAPI Report"
        reporter = Reporter()
        reporter.write(fake_results, False)

        mocked__render.assert_called_once_with("report.html", context, False)
        mocked__open.assert_called_once_with(
            pathlib.Path("scanapi-report.html"), "w", newline="\n"
        )
        mocked__open().write.assert_called_once_with("ScanAPI Report")

    @mark.it("should write to custom output")
    def test_should_write_to_custom_output(
        self,
        mocker,
        mocked__render,
        mocked__open,
        mocked__session,
        mock_version,
        context,
    ):
        mocked__render.return_value = "ScanAPI Report"
        reporter = Reporter("./custom/report-output.html", "html")
        reporter.write(fake_results, False)

        mocked__render.assert_called_once_with("html", context, True)
        mocked__open.assert_called_once_with(
            pathlib.Path("./custom/report-output.html"), "w", newline="\n"
        )
        mocked__open().write.assert_called_once_with("ScanAPI Report")

    @mark.it("should handle custom templates")
    def test_should_handle_custom_templates(
        self,
        mocker,
        mocked__render,
        mocked__open,
        mocked__session,
        mock_version,
        context,
    ):
        mocked__render.return_value = "ScanAPI Report"
        reporter = Reporter(template="my-template.html")
        reporter.write(fake_results, False)

        mocked__render.assert_called_once_with(
            "my-template.html", context, True
        )
        mocked__open.assert_called_once_with(
            pathlib.Path("scanapi-report.html"), "w", newline="\n"
        )
        mocked__open().write.assert_called_once_with("ScanAPI Report")

    @mark.it("should open report in browser")
    def test_should_open_report_in_browser(
        self,
        mocker,
        mocked__render,
        mocked__open,
        mocked__session,
        mock_version,
        context,
        mocked__webbrowser,
    ):

        reporter = Reporter()
        reporter.write(fake_results, True)
        assert mocked__webbrowser.open.call_count == 1
