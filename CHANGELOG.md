# Changelog

## [2025-11-24] - Python 3.13 Compatibility Update

### Changed

#### Dependencies (requirements.txt)
- **Django**: Upgraded from `3.0` to `4.2.16` (LTS)
  - **Reason**: Django 3.0 is incompatible with Python 3.13.7 due to removed modules (`distutils`, `cgi`)
  - Django 4.2 LTS provides full Python 3.13 support and extended security updates until April 2026

- **pytest-django**: Upgraded from `3.9.0` to `4.9.0`
  - **Reason**: Required to maintain compatibility with Django 4.2

- **flake8**: Kept at `3.7.0` (no changes required)

### Technical Details

#### Issues Resolved
1. `ModuleNotFoundError: No module named 'distutils'`
   - The `distutils` module was removed from Python 3.12+ standard library
   - Django 3.0 depends on this deprecated module

2. `ModuleNotFoundError: No module named 'cgi'`
   - The `cgi` module was removed from Python 3.13 standard library
   - Django 3.2 and earlier versions depend on this module

#### Environment
- **Python Version**: 3.13.7
- **Platform**: Windows (win32)
- **Django Version**: 4.2.16 LTS

### Notes

#### Pending Actions
1. **Database Migrations**: Run `python manage.py migrate` to apply unapplied migrations
2. **Model Configuration**: Consider adding `DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'` to settings to resolve model warnings

#### Breaking Changes
Django 4.2 may introduce some breaking changes from Django 3.0. Review the following:
- Check for deprecated APIs in your codebase
- Review Django 3.x to 4.x migration guides if issues arise
- Test all application features thoroughly

### Files Modified
- `requirements.txt`: Updated dependency versions
- `CHANGELOG.md`: Created to document changes

---

## [2025-11-24] - Django 4.2 Settings Update

### Changed

#### Settings Configuration (oc_lettings_site/settings.py)
- **Removed**: `USE_L10N = True` (line 103)
  - **Reason**: This setting is deprecated in Django 4.2 and will be removed in Django 5.0
  - **What it was**: `USE_L10N` (Localization) controlled whether Django should format dates, numbers, and other data using locale-specific formatting
  - **Why removed**: Starting with Django 4.0, localized formatting is **always enabled by default**. The setting became redundant and was deprecated.
  - **Impact**: No functional change - localization continues to work automatically
  - **Benefit**: Eliminates deprecation warning: `RemovedInDjango50Warning: The USE_L10N setting is deprecated`

#### What USE_L10N Did
When `USE_L10N = True` was set, Django would:
- Format dates according to the current locale (e.g., "11/24/2025" in US, "24/11/2025" in Europe)
- Format numbers with appropriate thousand separators (e.g., "1,000.00" vs "1.000,00")
- Use locale-specific currency symbols and decimal points
- Apply regional formatting to time zones

**In Django 4.0+**, this behavior is the standard and cannot be disabled, making the setting obsolete.

### Files Modified
- `oc_lettings_site/settings.py`: Removed deprecated `USE_L10N` setting
