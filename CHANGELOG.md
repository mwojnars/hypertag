# Change Log

## [1.1.4] -

- Bug fix in the import of hypertags from other scripts: local state now includes 
  all local symbols, not just the output ones.

## [1.1.3] - 2021-04-10

- Syntax extended: loops may have an `else` clause.
- Syntax extended: tags can be referenced inside expressions using the _tag embedding_ operator `%`.

## [1.1.2], [1.1.0] - 2021-04-02

- Added Django integration: a Hypertag backend (`hypertag.django.backend.Hypertag`) that can be plugged into a Django application.
- Changed syntax for importing from dynamic context: added "context" blocks in place of "from ~ import ..." syntax.
- Fixed and improved the import mechanism, classes: `Runtime`, `Loader`, `Module`.

## [1.0.3] - 2021-03-23

## [1.0.2] - 2021-03-22

## [1.0.1] - 2021-03-22

Initial release.
