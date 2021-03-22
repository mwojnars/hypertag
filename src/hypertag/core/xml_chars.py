########################################################################################################################################################
###
###  Regex patterns for character sets allowed in XML identifiers, to be put inside [...] in a regex.
###  XML identifiers differ substantially from typical name patterns in other computer languages. Main differences:
###   1) national Unicode characters are allowed, specified by ranges of unicode point values
###   2) special characters are allowed:  ':' (colon) '.' (dot) '-' (minus)
###      Colon is allowed as the 1st character according to XML syntax spec., although such a name may be treated as malformed during semantic analysis.
###      Others (dot, minus), are allowed on further positions in the string, after the 1st character.
###  Specification: http://www.w3.org/TR/REC-xml/#NT-NameStartChar
###

# human-readable:  [:_A-Za-z] | [\u00C0-\u00D6] | [\u00D8-\u00F6] | [\u00F8-\u02FF] | [\u0370-\u037D] | [\u037F-\u1FFF] | [\u200C-\u200D] | [\u2070-\u218F] | [\u2C00-\u2FEF] | [\u3001-\uD7FF] | [\uF900-\uFDCF] | [\uFDF0-\uFFFD] | [\U00010000-\U000EFFFF]
XML_StartChar  =  r"_A-Za-z\u00C0-\u00D6\u00D8-\u00F6\u00F8-\u02FF\u0370-\u037D\u037F-\u1FFF\u200C-\u200D\u2070-\u218F\u2C00-\u2FEF\u3001-\uD7FF\uF900-\uFDCF\uFDF0-\uFFFD\U00010000-\U000EFFFF"

# human-readable:  XML_StartChar | [0-9.\u00B7-] | [\u0300-\u036F] | [\u203F-\u2040]
XML_Char       =  XML_StartChar + r"0-9\.\-" + r"\u00B7\u0300-\u036F\u203F-\u2040" + ":"

# XML_EndChar is like XML_Char, but ":" is NOT allowed, to avoid collision with a trailing ":" used in Hypertag blocks
XML_EndChar    =  XML_Char[:-1]

