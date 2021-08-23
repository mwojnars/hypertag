# Change Log

## *upcoming*

- Non-standard operator `<>` can be used as an alternative for `!=` 
  to avoid ambiguity with a verbatim block mark (`!`) inside `if` blocks.
- Shortcut attribute values `.CLS` and `#ID` no longer need to be surrounded 
  by spaces, so `div#main.left.top` is now correct.
- The *if-else* operator returns "" (empty string) rather than None
  when the *else* branch is missing.
- New built-in functions: `$crop()`, alias `$truncate()`.
- New built-in tag for HyperHTML runtime, `doctype_html`.
- Built-in tag/function `dedent` accepts an optional argument `full`.

## [1.1.4] - 2021-07-20

- Bug fix: exception raised in a "try" block caused "dedent" operations to be skipped,
  leading to incorrect calculation of indentations of subsequent blocks.
  Changed to always revert to an initial indentation when translating a body node.
- Bug fix: post-translation state of an imported module included only output symbols.
  Changed to include all symbols (slots), since they can also be needed 
  for hypertag expansion.

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
