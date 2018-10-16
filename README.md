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

Files
=====

Root
----

| **File Name** | **Description** |
|---|---|
| main.py | Main python script |
| charity\_env.yml | Environment description file which allows for easy installation of a python environment with the required packages on another machine.|
  

Inputs
------

  ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  **File Name**                  **Description**
  ------------------------------ ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  charitybase.jsonl              Charity input data. To update download from [*here*](https://charitybase.uk/about). This will be a .jsonl.gz file, which should be extracted into a .jsonl file and saved with the same name in this folder.

  grantnav.csv                   360 Giving grant data. To update download from [*here*](http://grantnav.threesixtygiving.org/). This will be a csv file which should be re-named and saved in this folder.

  dkuk\_cause\_key.csv           Key which describes which charity causes to remove or prioritise. This can be updated if required. Causes with a priority of -1 will be removed, 0 treated no different, and 1 flagged as DKUK priority.

  tech\_keywords\_activity.csv   List of keywords to search for in the activity field. Any term with a 1 in the ‘remove’ column will be ignored. This has been kept in so that DKUK can avoid adding more words which have already been found to produce poor matches.

                                 Negative terms can be added for each search term. This is so that, for example, the term ‘computer’ can be searched for but only returned as a positive match when it is found without any of the terms ‘education, history, club’ also present as these have been found to be poor matches. Any further negative terms should be added separated by commas in the ‘negative’ column. (Note - comma separation is not necessary in the ‘positive’ column as multi-word terms are searched for in that order).

  tech\_keywords\_360.csv        File in the same format as file above for grant keyword matching.
  ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Outputs
-------

  **File Name**                                  **Description**
  ---------------------------------------------- --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  all\_charities\_matched\_YYYY-MM-DD.csv        Main output file - this is a list of charities which match the main conditions, with further descriptive fields as well as charity activity and grant keyword match flags.
  ch\_activity\_match\_results\_YYYY-MM-DD.csv   Charity activity keyword matching results. This can be used to examine the match results for each keyword. Note - charities are duplicated for each term they have matched. This is because if imported into excel and filtered you can then examine the charities and activity which have matched against each keyword.
  gr\_desc\_match\_results\_YYYY-MM-DD.csv       Grant description keyword matching results in the same format as the file above.

Pymatch
-------

  **File Name**            **Description**
  ------------------------ -------------------------------------------------------------------------------------------------------------------------------
  keyword\_matching.py     Main matching script. Reads and formats the CharityBase and 360 Giving data, runs the matching functions and outputs results.
  matching\_functions.py   Data retrieval, formatting and matching fuctions.

Pydash
------

  **File Name**          **Description**
  ---------------------- ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
  charity\_input.csv     This is just a duplicate of the all\_charities\_matched\_YYYY-MM-DD.csv file which is used for displaying the results. It will be updated automatically once the matching is run, no need to update manually.
  dashboard.py           Main dashboard script, reads data and uses [*Bokeh*](https://bokeh.pydata.org/en/latest/) package to display results. This initiates a local server instance so that data is displayed live as filter fields are used.
  download.js            Javascript for file download button.
  templates/index.html   Dashboard page formatting and titles.

Installation
============

This tool requires Python to be run. The easiest way to do this is to
install
[*Miniconda*](https://conda.io/docs/user-guide/install/index.html)
(Anaconda is a popular python distribution, miniconda is a lite version
of it).

Once that’s installed we can use conda (the Anaconda environment and
package manager) to create an environment with the required python
packages to run the scripts.

Note - the screenshots below show installation steps on a linux
computer, but the process will be almost identical for a mac.

1.  Open Terminal and navigate to the **charity\_search** folder. If
    > this is in your root directory you would type &gt; cd
    > charity\_search/

> ![](media/image1.png){width="5.900600393700787in"
> height="3.4114588801399823in"}

1.  Type &gt; conda env create -f charity\_env.yml and hit enter. This
    > will use the environment description file to create a conda
    > environment called ‘charity’.

> ![](media/image4.png){width="3.625in" height="1.0416666666666667in"}
>
> ![](media/image6.png){width="3.625in" height="2.4257524059492566in"}

1.  The environment and packages should now be installed, the
    > environment can be activated using &gt; source activate charity.
    > You’ll see (charity) appear before the directory in Terminal.

> ![](media/image2.png){width="3.776042213473316in"
> height="0.5958103674540682in"}

1.  The environment is now active and python scripts can be run. To run
    > the script type &gt; python main.py. You’ll see the first control
    > option appear, which is an option to run the matching scripts. If
    > yes, they’ll run and you’ll have the option to launch the
    > dashboard. If no it will skip straight to the dashboard option.

> ![](media/image3.png){width="5.088542213473316in"
> height="0.9758847331583552in"}

1.  The keyword matching will show steps and results as it works through
    > (it should run in under 5 minutes), and then give the dashboard
    > launch option.

> ![](media/image5.png){width="5.265625546806649in"
> height="3.3937915573053368in"}

1.  If launched a new browser tab should be automatically opened
    > displaying the dashboard. Use the filter controls to explore the
    > table.

![](media/image7.png){width="6.270833333333333in" height="3.8375in"}

At any point the process can be stopped by pressing Ctrl C. To
de-activate the charity environment use &gt; source deactivate. Once the
dashboard window is closed the local server can be stopped with Ctrl C
and the Terminal window closed.
