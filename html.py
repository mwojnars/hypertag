#
# Hypertag built-ins for HTML.
#
# HTML tags can be imported manually into a Hypertag script with a statement of the form:
#
#    from hypertag.html import %div
#

from hypertag.std.html import register

__tags__ = register.tags                # make all tags available for import
globals().update(register.vars)         # make all variables available for import

del globals()['register']
