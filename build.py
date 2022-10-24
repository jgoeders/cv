import jinja2
import os
from jinja2 import Template
import argparse
import pathlib
import yaml
from nbconvert.filters import markdown2latex, escape_latex
import re


def bold_my_name(s):
    if s:
        return s.replace("Jeffrey Goeders", r"\textbf{Jeffrey Goeders}")
    else:
        return s


byu_students = [
    "Hayden Cook",
    "Jacob Arscott",
    "Brent George",
    "Tanner Gaskin",
    "Eli Cahill",
    "Benjamin James",
    "Matthew Bohman",
    "Robert Lucas",
    "Matthew Ashcraft",
    "Wesley Stirk",
    "Adam Hastings",
    "Sean Jensen",
]
other_students = [
    "Al-Shahna Jamal",
    "Daniel Holanda Noronha",
    "Ruizhe Zhao",
    "Zhiqiang Que",
    "Pavan Kumar Bussa",
]


def is_student(s):
    return (s in byu_students) or (s in other_students)


def is_byu_student(s):
    return s in byu_students


def format_author_name_for_packet(s, pre_byu):
    if pre_byu:
        return bold_my_name(s)

    ret = s
    if is_student(s):
        ret = r"\ul{" + ret + "}"
    if is_byu_student(s):
        ret += "*"
    return bold_my_name(ret)


def venue_info(series):
    m = re.search(r"\((.*)\)", series)
    assert m
    venue = m.group(1)
    if venue == "TRETS":
        s = 'TRETS (Impact factor 1.95).  This ``ACM Transactions" journal is the top journal specific to my research area.'
    elif venue == "TNS":
        s = 'TNS (Impact factor 1.79). This ``IEEE Transactions" journal is highly-regarded in the field of radiation-hardened software/hardware, and was the ideal place to publish this work.'
    elif venue == "TCAD":
        s = 'TCAD (Impact factor 2.92). This ``IEEE Transactions" journal is a highly regarded journal, and related to my research area.'
    elif venue == "JOLPE":
        s = "JOLPE (Impact factor 1.48)."
    elif venue == "DATE":
        s = "Large European conference related to testing of electronic devices.  Well regarded conference."
    elif venue == "FPL":
        s = "FPL Conference (One of the top few conferences in my field). Acceptance rates usually ~30\%."
    elif venue == "FPT":
        s = "FPT Conference (One of the top few conferences in my field). Acceptance rates usually ~30\%."
    elif venue in ("ReConFig", "ARC"):
        s = venue + " (Secondary conference in my field)"
    elif venue == "FPGA":
        s = "FPGA Conference (Regarded as the top conference in my field). Acceptance rates usually 20-25\%"
    elif venue == "FCCM":
        s = "FCCM Conference (One of the top few conferences in my field). Acceptance rates usually 20-30\%"
    elif venue == "IVSW":
        s = "IVSW Workshop (smaller workshop, but one of the few related to hardware security)."
    elif venue == "NSREC":
        s = "NSREC Conference (although not a publication, the NSREC conference requires submission of a four-page summary, is peer reviewed, and is highly-regarded in the field)."
    else:
        print(venue)
        assert False
    return r"\textit{" + "Venue: " + s + "}"


def format_authors(s, pre_byu):
    # Make sure there is always a comma
    s = s.replace(" and ", ",")

    # Split on comma
    authors = [a.strip() for a in s.split(",")]

    # Remove empty items
    authors = list(filter(None, authors))

    # Produce author list
    ret = ""
    for author in authors[:-1]:
        ret += format_author_name_for_packet(author, pre_byu) + ", "

    # Add last author
    if len(authors) == 1:
        ret = format_author_name_for_packet(authors[0], pre_byu)
    elif len(authors) > 2:
        ret += "and " + format_author_name_for_packet(authors[-1], pre_byu)
    else:
        ret = ret[:-2] + " and " + format_author_name_for_packet(authors[-1], pre_byu)

    # print(authors)
    # print(ret)
    return ret


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("template_path", type=pathlib.Path)
    parser.add_argument("data_yml_path", type=pathlib.Path)
    args = parser.parse_args()

    env = jinja2.Environment(
        block_start_string="\BLOCK{",
        block_end_string="}",
        variable_start_string="\VAR{",
        variable_end_string="}",
        comment_start_string="\#{",
        comment_end_string="}",
        # line_statement_prefix="%%",
        line_comment_prefix="%#",
        trim_blocks=True,
        autoescape=False,
        loader=jinja2.FileSystemLoader(os.path.abspath(".")),
    )
    env.filters["escape_latex"] = escape_latex
    env.filters["md2latex"] = markdown2latex
    env.globals["bold_my_name"] = bold_my_name
    env.globals["format_authors"] = format_authors
    env.globals["venue_info"] = venue_info

    template = env.get_template(str(args.template_path))
    with open(args.data_yml_path) as fp:
        data = yaml.safe_load(fp)
    print(template.render(data))


if __name__ == "__main__":
    main()