# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Fixed
- Replacing pkg_resources with the builtin importlib.metadata [687](https://github.com/scanapi/scanapi/issues/687)

## [2.10.2] - 2024-11-10
### Removed
- Gitlint dev dependency [685](https://github.com/scanapi/scanapi/pull/685)

## [2.10.1] - 2024-11-10
### Changed
- Upgrade Click dependency [681](https://github.com/scanapi/scanapi/pull/681)

## [2.10.0] - 2024-11-10
### Changed
- Change requests to httpx. [#208](https://github.com/scanapi/scanapi/issues/208)
- Upgrade PyYAML dependecy [678](https://github.com/scanapi/scanapi/pull/678)

### Deprecated
- Drops support for Python 3.7 and Python 3.8 since their EOL were reached out already [678](https://github.com/scanapi/scanapi/pull/678)

## [2.9.0] - 2023-03-16
### Feature
- Enable the use of different content types [#521](https://github.com/scanapi/scanapi/issues/521)

### Fixed
- python -m scanapi command [#501](https://github.com/scanapi/scanapi/issues/501)

## [2.8.2] - 2023-03-06
### Fixed
- Content field not rendered properly on Chrome [#551](https://github.com/scanapi/scanapi/issues/551)

## [2.8.1] - 2023-03-02
### Fixed
- Custom variable evaluated when defined on the path [#508](https://github.com/scanapi/scanapi/issues/508)
- Add missing `--insecure` flag to cURL command on report based on request options [#555](https://github.com/scanapi/scanapi/pull/555)

## [2.8.0] - 2022-08-11
### Added
- Implement new key `options` to request and endpoint nodes [#529](https://github.com/scanapi/scanapi/pull/552)

## [2.7.0] - 2022-06-02
### Deprecated
- Drops support for Python 3.6 since its EOL was reached out in December last year [549](https://github.com/scanapi/scanapi/pull/549)

## [2.6.2] - 2022-06-01
### Added
- Print test results summary in console [#497](https://github.com/scanapi/scanapi/issues/497)

### Fixed
- Error when using list (or any other) comprehension in Python Code [#515](https://github.com/scanapi/scanapi/pull/515)

## [2.6.1] - 2022-04-12
### Changed
- Implement new details to help users on visualize related request data. [#506](https://github.com/scanapi/scanapi/pull/506)

### Fixed
- Fix the `--browser` flag not working on macOS [#504](https://github.com/scanapi/scanapi/pull/504)
- Error on running ScanAPI. `ImportError: cannot import name 'soft_unicode' from 'markupsafe'` [#534](https://github.com/scanapi/scanapi/pull/534)

## [2.6.0] - 2021-08-13
### Changed
- Summary tests location to the top of the report [#479](https://github.com/scanapi/scanapi/pull/479)
- Add the flag `--browser` or `-b` for short [#465]

### Fixed
- Header table gets broken. [#432](https://github.com/scanapi/scanapi/pull/432)

## [2.5.0] - 2021-07-23
### Added
- Enable 'vars' key at endpoint node. [#328](https://github.com/scanapi/scanapi/pull/328)
- Add `--no-report` flag. [#325](https://github.com/scanapi/scanapi/pull/325)

## [2.4.0] - 2021-06-11
### Added
- Request name to report. [#390](https://github.com/scanapi/scanapi/pull/390)
- Show on report the scanapi version used to generate it. [#386](https://github.com/scanapi/scanapi/pull/386)
- Link icon to copy anchor URL. [#398](https://github.com/scanapi/scanapi/pull/398)

### Fixed
- Error making request when request has no body and there is a `report::hide_request::body` configuration. [#393](https://github.com/scanapi/scanapi/pull/393)

## [2.3.0] - 2021-05-25
### Added
- `--version` command to return current scanapi version. [#372](https://github.com/scanapi/scanapi/pull/372)

### Fixed
- hide_response body. [#375](https://github.com/scanapi/scanapi/pull/375)

## [2.2.0] - 2021-04-22
### Added
- Hide sensitive information in the URL Query Params [#304](https://github.com/scanapi/scanapi/pull/325)
- Anchor link for each request in the report to make it easily shareable. [#317](https://github.com/scanapi/scanapi/pull/317)
- Support to HTTP methods HEAD and OPTIONS [#350](https://github.com/scanapi/scanapi/pull/350)
- The `retry` key under requests to setup retry for requests. [#298](https://github.com/scanapi/scanapi/issues/298)

### Fixed
- Curl command [#330](https://github.com/scanapi/scanapi/pull/330)
- Render body according to its request content type [#331](https://github.com/scanapi/scanapi/pull/331)

## [2.1.0] - 2020-10-06
### Added
- Add a `delay` key option to perform a delay between each request. [#266](https://github.com/scanapi/scanapi/issues/266)

### Changed
- Changed relative path to show absolute path to the report in CLI. [#277](https://github.com/scanapi/scanapi/pull/277)
- Considering `-` (dash) in variable names. [#281](https://github.com/scanapi/scanapi/pull/281)
- Moved bandit to dev section [#285](https://github.com/scanapi/scanapi/pull/285)
- Increased Test coverage for `/scanapi/evaluators/spec_evaluator.py` [#291](https://github.com/scanapi/scanapi/pull/291)

### Fixed
- When there is no `body` specified, sending it as `None` instead of `{}`. [#280](https://github.com/scanapi/scanapi/pull/280)
- Removed unused imports. [#294](https://github.com/scanapi/scanapi/pull/294)

## [2.0.0] - 2020-08-25
### Added
- JSON response is now properly rendered, instead of plain text. [#213](https://github.com/scanapi/scanapi/pull/213)
- The report page now has a favicon. [#223](https://github.com/scanapi/scanapi/pull/223)
- Bandit security audit tool. [#219](https://github.com/scanapi/scanapi/pull/219)
- Add Sphinx auto-documentation. [#230](https://github.com/scanapi/scanapi/pull/230)
- Add workflow to package/publish to Test PyPi. [#239](https://github.com/scanapi/scanapi/pull/239)
- Add Github Action workflow for First-time contributors. [#290](https://github.com/scanapi/scanapi/pull/290)
- Add button to copy data from the report page. [#295](https://github.com/scanapi/scanapi/pull/295)

### Changed
- Renamed `api.(yaml|json)` to `scanapi.yaml`. [#222](https://github.com/scanapi/scanapi/issues/20://github.com/scanapi/scanapi/pull/222)
- Remove top-level `api` key in `scanapi.yaml`. [#231](https://github.com/scanapi/scanapi/pull/231)
- Renamed `project-name`, `hide-request` and `hide-response` to use underscore. [#228](https://github.com/scanapi/scanapi/issues/228)
- Changed command `scanapi spec-file.yaml` to `scanapi run spec-file.yaml`. [#247](https://github.com/scanapi/scanapi/pull/247)
- Moved Documentation from README.md to the website. [#250](https://github.com/scanapi/scanapi/pull/250)
- Local and global configuration. [#254](https://github.com/scanapi/scanapi/pull/254)
- Moved `bandit` to `dev` in `pyproject.toml`. [#286](https://github.com/scanapi/scanapi/pull/286)

### Fixed
- Updated language use in README.md and CONTRIBUTING.md plus fix broken links. [#220](https://github.com/scanapi/scanapi/pull/220)
- Removed unused sys import in scan.py and cleaned for PEP8 and spelling errors. [#217](https://github.com/scanapi/scanapi/pull/217)
- Hide body sensitive information. [#238](https://github.com/scanapi/scanapi/pull/238)
- Fix css issues with html template. [#256](https://github.com/scanapi/scanapi/pull/256)
- Fix when vars is declared and used in the same request.[#257](https://github.com/scanapi/scanapi/pull/257)
- Fix when evaluated value is not string. [#257](https://github.com/scanapi/scanapi/pull/257)

### Removed
- APIKeyMissingError. [#218](https://github.com/scanapi/scanapi/pull/218)

## [1.0.5] - 2020-07-18
### Fixed
- Status icons on report were not vertically centered. [#195](https://github.com/scanapi/scanapi/pull/195)

## [1.0.4] - 2020-06-25

## [1.0.3] - 2020-06-25
### Added
- MANIFEST.in.

## [1.0.2] - 2020-06-25
### Fixed
- Fix for TemplateNotFound Error. [#197](https://github.com/scanapi/scanapi/pull/197)

## [1.0.1] - 2020-06-25
### Fixed
- Report example images not loading on PyPI. [#193](https://github.com/scanapi/scanapi/pull/193)

## [1.0.0] - 2020-06-25
### Added
- Add new HTML template. [#157](https://github.com/scanapi/scanapi/pull/157)
- Tests key. [#152](https://github.com/scanapi/scanapi/pull/152)
- `-h` alias for `--help` option. [#172](https://github.com/scanapi/scanapi/pull/172)
- Test results to report. [#177](https://github.com/scanapi/scanapi/pull/177)
- Add test errors to the report. [#187](https://github.com/scanapi/scanapi/pull/187)
- Hides sensitive info in URL. [#185](https://github.com/scanapi/scanapi/pull/185)
- CLI options explanation. [#189](https://github.com/scanapi/scanapi/pull/189)

### Changed
- Unified keys validation in a single method. [#151](https://github.com/scanapi/scanapi/pull/151)
- Default template to html. [#173](https://github.com/scanapi/scanapi/pull/173)
- Project name color on html reporter to match ScanAPI brand [#172](https://github.com/scanapi/scanapi/pull/172)
- Hero banner on README. [#180](https://github.com/scanapi/scanapi/pull/180)
- Entry point to `scanapi:main`. [#172](https://github.com/scanapi/scanapi/pull/172)
- `--spec-path` option to argument. [#172](https://github.com/scanapi/scanapi/pull/172)
- Improve test results on report. [#186](https://github.com/scanapi/scanapi/pull/186)
- Improve Error Message for Invalid Python code error. [#187](https://github.com/scanapi/scanapi/pull/187)
- Handle properly exit errors. [#187](https://github.com/scanapi/scanapi/pull/187)
- Update README.md. [#191](https://github.com/scanapi/scanapi/pull/191)

### Fixed
- Duplicated status code row from report. [#183](https://github.com/scanapi/scanapi/pull/183)
- Sensitive information render on report. [#183](https://github.com/scanapi/scanapi/pull/183)

### Removed
- Console Report. [#175](https://github.com/scanapi/scanapi/pull/175)
- Markdown Report. [#179](https://github.com/scanapi/scanapi/pull/179)
- `--reporter` option. [#179](https://github.com/scanapi/scanapi/pull/179)

## [0.1.0] - 2020-05-14
### Added
- Automated pypi deploy. [#144](https://github.com/scanapi/scanapi/pull/144)

## [0.0.19] - 2020-05-11
### Added
- PATCH HTTP method. [#113](https://github.com/scanapi/scanapi/pull/113)
- Ability to have API spec in multiples files. [#125](https://github.com/scanapi/scanapi/pull/125)
- CLI `--config-path` option. [#128](https://github.com/scanapi/scanapi/pull/128)
- CLI `--template-path` option. [#126](https://github.com/scanapi/scanapi/pull/126)
- GitHub Action checking for missing changelog entry. [#134](https://github.com/scanapi/scanapi/pull/134)

### Changed
- Make markdown report a bit better. [#96](https://github.com/scanapi/scanapi/pull/96)
- `base_url` keyword to `path`. [#116](https://github.com/scanapi/scanapi/pull/116)
- `namespace` keyword to `name`. [#116](https://github.com/scanapi/scanapi/pull/116)
- `method` keyword is not mandatory anymore for requests. Default is `get`. [#116](https://github.com/scanapi/scanapi/pull/116)
- Replaced `hide` key on report config by `hide-request` and `hide-response`. [#116](https://github.com/scanapi/scanapi/pull/116)
- Moved black check from CircleCI to github actions. [#136](https://github.com/scanapi/scanapi/pull/136)

### Fixed
- Cases where custom var has upper case letters. [#99](https://github.com/scanapi/scanapi/pull/99)

### Removed
- Request with no endpoints. [#116](https://github.com/scanapi/scanapi/pull/116)

## [0.0.18] - 2020-01-02
### Changed
- Return params/headers None when request doesn't have params/headers. [#87](https://github.com/scanapi/scanapi/pull/87)

### Fixed
- Report-example image not loading on PyPi. [#86](https://github.com/scanapi/scanapi/pull/86)

## [0.0.17] - 2019-12-19
### Added
- Added PyPI Test section to CONTRIBUTING.md.

### Fixed
- Templates on pypi package. [#85](https://github.com/scanapi/scanapi/pull/85)

## [0.0.16] - 2019-12-18
### Fixed
- Fixed No module named 'scanapi.tree'. [#83](https://github.com/scanapi/scanapi/pull/83)

## [0.0.15] - 2019-12-14
### Added
- CodeCov Setup.
- CircleCI Setup.

### Changed
- Updated Documentation.
- Increased coverage.
- Used dot notation to access responses inside api spec.
- Renamed option report_path to output_path.
- Reporter option -r, --reporter [console|markdown|html].

### Fixed
- Fixed join of urls to keep the last slash.

### Removed
- Removed requirements files and put every dependency under setup.py.
- Removed dcvars key.

## [0.0.14] - 2019-10-09
### Added
- Add math, time, uuid and random libs to be used on api spec.

## [0.0.13] - 2019-10-07
### Changed
- Bumped version.

## [0.0.12] - 2019-08-15
### Added
- Used env variables from os.

## [0.0.11] - 2019-08-09
### Added
- Added Docker file.

## [0.0.10] - 2019-08-09
### Added
- Add logging.
- Option to hide headers fields.

### Fixed
- Fix vars interpolation.

[Unreleased]: https://github.com/scanapi/scanapi/compare/v2.10.2...HEAD
[2.10.2]: https://github.com/scanapi/scanapi/compare/v2.10.1...v2.10.2
[2.10.1]: https://github.com/scanapi/scanapi/compare/v2.10.0...v2.10.1
[2.10.0]: https://github.com/scanapi/scanapi/compare/v2.9.0...v2.10.0
[2.9.0]: https://github.com/scanapi/scanapi/compare/v2.8.2...v2.9.0
[2.8.2]: https://github.com/scanapi/scanapi/compare/v2.8.1...v2.8.2
[2.8.1]: https://github.com/scanapi/scanapi/compare/v2.8.0...v2.8.1
[2.8.0]: https://github.com/scanapi/scanapi/compare/v2.7.0...v2.8.0
[2.7.0]: https://github.com/scanapi/scanapi/compare/v2.6.2...v2.7.0
[2.6.2]: https://github.com/scanapi/scanapi/compare/v2.6.1...v2.6.2
[2.6.1]: https://github.com/scanapi/scanapi/compare/v2.6.0...v2.6.1
[2.6.0]: https://github.com/scanapi/scanapi/compare/v2.5.0...v2.6.0
[2.5.0]: https://github.com/scanapi/scanapi/compare/v2.4.0...v2.5.0
[2.4.0]: https://github.com/scanapi/scanapi/compare/v2.3.0...v2.4.0
[2.3.0]: https://github.com/scanapi/scanapi/compare/v2.2.0...v2.3.0
[2.2.0]: https://github.com/scanapi/scanapi/compare/v2.1.0...v2.2.0
[2.1.0]: https://github.com/scanapi/scanapi/compare/v2.0.0...v2.1.0
[2.0.0]: https://github.com/scanapi/scanapi/compare/v1.0.5...v2.0.0
[1.0.5]: https://github.com/scanapi/scanapi/compare/v1.0.4...v1.0.5
[1.0.4]: https://github.com/scanapi/scanapi/compare/v1.0.3...v1.0.4
[1.0.3]: https://github.com/scanapi/scanapi/compare/v1.0.2...v1.0.3
[1.0.2]: https://github.com/scanapi/scanapi/compare/v1.0.1...v1.0.2
[1.0.1]: https://github.com/scanapi/scanapi/compare/v1.0.0...v1.0.1
[1.0.0]: https://github.com/scanapi/scanapi/compare/v0.1.0...v1.0.0
[0.1.0]: https://github.com/scanapi/scanapi/compare/v0.0.19...v0.1.0
[0.0.19]: https://github.com/scanapi/scanapi/compare/v0.0.18...v0.0.19
[0.0.18]: https://github.com/scanapi/scanapi/compare/v0.0.17...v0.0.18
[0.0.17]: https://github.com/scanapi/scanapi/compare/v0.0.16...v0.0.17
[0.0.16]: https://github.com/scanapi/scanapi/compare/v0.0.15...v0.0.16
[0.0.15]: https://github.com/scanapi/scanapi/compare/v0.0.14...v0.0.15
[0.0.14]: https://github.com/scanapi/scanapi/compare/v0.0.13...v0.0.14
[0.0.13]: https://github.com/scanapi/scanapi/compare/v0.0.12...v0.0.13
[0.0.12]: https://github.com/scanapi/scanapi/compare/v0.0.11...v0.0.12
[0.0.11]: https://github.com/scanapi/scanapi/compare/v0.0.10...v0.0.11
[0.0.10]: https://github.com/scanapi/scanapi/releases/tag/v0.0.10
