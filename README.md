pdfmanip
========
A python script to modify your PDF documents with PDFtk toolkit.
You can manipulate the pages of your document and save it as a new one.

The interactive mode lets you interact with the PDF document, add and remove pages, then create the new document.
The direct mode takes a list of pages, for example: 1,5,9-15 and creates the new document without entering the interactive mode.

Usage
=====
Interactive mode:
> pdfmanip.py &lt;input PDF file> &lt;output PDF file> --interactive

Direct mode:
> pdfmanip.py &lt;input PDF file> &lt;output PDF file> --pages="&lt;range>"

Interactive mode commands
=========================
See help for more

* rm - remove pages (ex: rm 1,5,9-15)
* add - add pages (ex: add 1,5,9-15)
* keep - keep pages (ex: keep 9-15)
