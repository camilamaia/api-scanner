name = "scanapi"

import click
import logging
import yaml

from scanapi.errors import (
    EmptyConfigFileError,
    FileFormatNotSupportedError,
    InvalidKeyError,
    MissingMandatoryKeyError,
)
from scanapi.config_loader import load_config_file
from scanapi.reporter import Reporter
from scanapi.settings import settings
from scanapi.tree import EndpointNode
from scanapi.tree.tree_keys import API_KEY, ROOT_SCOPE


@click.command()
@click.option("-s", "--spec-path", "spec_path", type=click.Path(exists=True))
@click.option("-o", "--output-path", "output_path", type=click.Path())
@click.option("-c", "--config-path", "config_path", type=click.Path(exists=True))
@click.option(
    "-r", "--reporter", "reporter", type=click.Choice(["console", "markdown", "html"])
)
@click.option("-t", "--template", "template", type=click.Path(exists=True))
@click.option(
    "--log-level",
    "log_level",
    type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]),
    default="INFO",
)
def scan(spec_path, output_path, config_path, reporter, template, log_level):
    """Automated Testing and Documentation for your REST API."""
    logging.basicConfig(level=log_level, format="%(message)s")
    logger = logging.getLogger(__name__)

    settings.save_preferences(
        **{
            "spec_path": spec_path,
            "output_path": output_path,
            "config_path": config_path,
            "reporter": reporter,
            "template": template,
        }
    )

    spec_path = settings["spec_path"]

    try:
        api_spec = load_config_file(spec_path)
    except FileNotFoundError as e:
        error_message = f"Could not find API spec file: {spec_path}. {str(e)}"
        logger.error(error_message)
        return
    except EmptyConfigFileError as e:
        error_message = f"API spec file is empty. {str(e)}"
        logger.error(error_message)
        return
    except (yaml.YAMLError, FileFormatNotSupportedError) as e:
        logger.error(e)
        return

    try:
        if API_KEY not in api_spec:
            raise MissingMandatoryKeyError({API_KEY}, ROOT_SCOPE)

        root_node = EndpointNode(api_spec[API_KEY])
        Reporter(
            settings["output_path"], settings["reporter"], settings["template"]
        ).write(root_node.run())
    except (InvalidKeyError, MissingMandatoryKeyError, KeyError) as e:
        error_message = "Error loading API spec."
        error_message = "{} {}".format(error_message, str(e))
        logger.error(error_message)
        return
