# Bib To HTML Converter

Python program that checks if a given .bib file is in correct format and converts it to a .html file. 

## How It Works

The program takes a .bib file name from the user in the console. Then it checks multiple criteria to confirm given .bib file

is in correct format. Some criteria include but are not limited to:

- Each item should have a non-empty unique key UNIQKEY which may only contain alphanumeric characters.

- Each field should be in a single line.

- The value FIELDCONTENT should be enclosed either in " " or { }.

- Every item has to contain the fields "author", "title", "journal", "year" and "volume".

After checking the format python code proceeds to write the .bib file contents inside the .html file. A general form of the

output is as follows:

```html

<html> 
<br> <center> <b> YEAR </b> </center> 
<br> 
[J1] FIRSTNAME1 LASTNAME1, FIRSTNAME2 LASTNAME2, FIRSTNAME3 LASTNAME3... and FIRSTNAMEn LASTNAMEn, <b>TITLE</b>, <i>JOURNAL</i>, VOLUME[:NUMBER][, pp. PAGES], YEAR. [<a href="https://doi.org/DOI">link</a>] <br>
<br>
</html>

```

### Prerequisites

An IDE or text editor to run the python code.

## Running the tests

Enter the name of the .bib file you want to convert into .html file in the console. The .bib file should be in the same folder

as the source code.

