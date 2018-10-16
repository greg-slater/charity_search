Purpose
=======

This document describes how to use the charity search tool. This tool
uses charity activity description data from the Charity Commission and
grant description data from 360 Giving along with keyword lists for each
to find charities which might make good partners for DataKind UK.

With the correct input files the python scripts will run each of the
keyword matching processes and output the results in an interactive
table which can be explored using additional filter fields (these
filtered results can also be downloaded as a csv file), as well as full
csv outputs which can be explored in more detail if necessary.

From the \~168k input charities and \~100k grants the output results
will be all charities which meet the conditions below, with filter
fields for positive or negative charity activity / grant keyword
matches.

Conditions - final charities must have:

-   An ‘activity’ description in the Charity Commission data

-   Latest income data, with an income between £100,000 and £2,000,000

-   A ‘cause’ which is not in the following:
    > ‘General charitable purposes’, ‘Religious activities’, ‘Amateur sport’,
    > ‘Animals’ or ‘Armed forces/emergency service efficiency’

Limitations
===========

Keyword Match Results
---------------------

While the results from the matching are certainly promising the
intention is that this tool is developed further as it is used. As the
results are interpreted, a user with domain knowledge will be able to
add or remove keywords to search for, as well as adding negative
keywords (which will cause a positive keyword to be ignored if it is
also present in the text).

Error Handling
--------------

This is really a collection of scripts which can be run together, rather
than a full python package or application and as such there is little
error handling built in. Any problems are most likely to be caused by
changes to file formats, so if issues are experienced as a first check
always make sure the format of the input files is as originally supplied
