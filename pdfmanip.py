#!/usr/bin/env python
# encoding: utf-8

"""
pdfmanip.py

A python script to modify your PDF documents
You can manipulate the pages of your document and save it as a new one

The interactive mode lets you interact with the PDF document, add and remove pages, then create the new document
The direct mode takes a list of pages, for example: 1,5,9-15 and creates the new document without entering the interactive mode
"""


import os
import sys
import subprocess


PDFTK = "pdftk"


def num_pages(pdf_file):
    """
    get number of pages of the PDF file
    """
    p1 = subprocess.Popen([PDFTK, pdf_file, "dump_data"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if p1.wait():
        print "Invalid input PDF file"
        exit(1)

    p2 = subprocess.Popen(["grep", "NumberOfPages"], stdin=p1.stdout, stdout=subprocess.PIPE)
    out, err = p2.communicate()

    return int(out.split()[-1])


def pdftk(input_pdf, output_pdf, pagenumbers):
    """
    create a new PDF file from the original containing @pagenumbers with the pdftk tool
    """
    args = [PDFTK, input_pdf, "cat"]
    args += [str(i) for i in pagenumbers]
    args += ["output", output_pdf]

    p = subprocess.Popen(args, stderr=subprocess.PIPE)

    if p.wait():
        print output_pdf, "failed"
        print p.communicate()[1]
    else:
        print output_pdf, "was written, size:", num_pages(output_pdf)


def modify(pagenumbers, command, maxpage):
    """
    add, remove pages from the @pagenumbers list
    """
    command = command.split(" ")
    if command[0] == "add":
        inc = 1
    elif command[0] == "rm":
        inc = 0
    elif command[0] == "keep":
        inc = 1
        pagenumbers[:] = []
    else:
        print "error:", command[0]
        return 1

    if len(command) > 2:
        print "warning, unexpected input after", command[1]

    for s in command[1].split(","):
        try:
            if s.find("-") > 0:
                a, b = [int(x) for x in s.split("-")]
            else:
                a = b = int(s)
        except ValueError:
            print "error:", s
            continue

        if a >= 1 and b <= maxpage:
            for index in xrange(a, b+1):
                if inc:
                    pagenumbers.append(index)
                else:
                    try:
                        pagenumbers.remove(index)
                    except ValueError:
                        print "Ignoring:", index
        else:
            print "Out of bounds:", s

    status(pagenumbers)
    return 0


def status(pagenumbers):
    """
    print the current status of @pagenumbers
    """
    pagenumbers.append(-1)

    pages = []
    first = pagenumbers[0]
    i = 0
    while i < len(pagenumbers)-1:
        if pagenumbers[i]+1 != pagenumbers[i+1]:
            if first == pagenumbers[i]:
                pages.append(str(first))
            else:
                pages.append(str(first) + "-" + str(pagenumbers[i]))
            first = pagenumbers[i+1]
        i += 1

    pagenumbers.remove(-1)

    print "status:", ','.join(pages)


def usage():
    print """
Usage:
    Interactive mode:
        {s} <input PDF file> <output PDF file> --interactive
    Direct mode:
        {s} <input PDF file> <output PDF file> --pages="<range>"
""".format(s=sys.argv[0]).strip()


def help():
    print """
Help:
    help      print this message
    rm        remove pages (ex: rm 1,5,9-15)
    add       add pages (ex: add 1,5,9-15)
    keep      keep pages (ex: keep 9-15)
    sort      sort pages
    uniq      remove duplicate pages
    status    print status
    open in   open input PDF
    open out  open output PDF
    w         write output PDF
    q         exit
    qq        quickly quit
""".strip()


def main():
    """
    contins the main loop for the interactive mode
    """
    if os.path.exists("/usr/bin/pdftk") == False:
        print "Please install pdftk"
        exit(1)

    if len(sys.argv) != 4:
        usage()
        exit(1)

    input_pdf = ""
    output_pdf = ""
    pagenumbers = ""
    unsaved = False

    is_interactive = -1
    for s in sys.argv[1:]:
        if s == "--interactive":
            is_interactive = 1
        elif s.startswith("--pages="):
            is_interactive = 0
            pagenumbers = s.strip("--pages=")
        elif not input_pdf:
            input_pdf = s
        else:
            output_pdf = s

    if is_interactive == -1:
        usage()
        exit(1)

    if is_interactive:
        n = num_pages(input_pdf)
        pagenumbers = range(1, n+1)

        print input_pdf + ":", n, "pages"

        while True:
            s = raw_input("> ")
            if s == "help":
                help()
            elif s == "status":
                status(pagenumbers)
            elif s == "open in":
                os.system("xdg-open " + input_pdf)
            elif s == "open out":
                os.system("touch " + output_pdf)
                os.system("xdg-open " + output_pdf)
            elif s == "sort":
                unsaved = True
                pagenumbers.sort()
                status(pagenumbers)
            elif s == "uniq":
                unsaved = True
                pagenumbers = list(set(pagenumbers))
                status(pagenumbers)
            elif s == "w":
                pdftk(input_pdf, output_pdf, pagenumbers)
                unsaved = False
            elif s == "qq":
                exit(0)
            elif s == "q":
                if unsaved:
                    print """
Warning: {out} was not saved.
Tip: save it with "w" or exit without saving with "qq".
""".strip().format(out = output_pdf)
                else:
                    exit(0)
            else:
                ret = modify(pagenumbers, s, n)
                if ret == 0:
                    unsaved = True
    else:
        pdftk(input_pdf, output_pdf, pagenumbers.split(","))


if __name__ == "__main__":
    main()
