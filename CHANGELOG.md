# Change Log

## [Unreleased]

### Changed
## [1.3] - 2017-01-07
- Update version of Django.

### Added
## [1.2] - 2016-09-07
- Implement work-around for Constant Contact known issue.  When
  triggered, it causes the Advanced Editor to display nothing.

### Changed
## [1.1.3] - 2016-08-18
- Upgrade version of premailer used.

### Changed
## [1.1.2] - 2016-08-09
- Upgrade pip and setuptools in .travis.yml. django-bulletin
  depends on django-minify, which depends on other
  packages which need the upgraded setuptools.

### Added
## [1.1] - 2016-08-09
- Email content is now html-minified before sending to Constant Contact.

### Changed
## [1.0.5] - 2016-03-18
- Don't allow Django 1.9rcx to be installed.

### Changed
## [1.0.4] - 2016-03-18
- Set zip_safe = False in setup.py.

### Changed
## [1.0.2] - 2016-03-18
- Replaced README.md with README.rst.

### Changed
## [1.0.1] - 2016-03-18
- Removed Mailchimp dependency.
