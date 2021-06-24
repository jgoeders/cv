import jinja2
import os
from jinja2 import Template
import argparse
import pathlib
import yaml
from nbconvert.filters import markdown2latex, escape_latex


def bold_my_name(s):
    if s:
        return s.replace("Jeffrey Goeders", r"\textbf{Jeffrey Goeders}")
    else:
        return s


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
        # line_comment_prefix="%",
        trim_blocks=True,
        autoescape=False,
        loader=jinja2.FileSystemLoader(os.path.abspath(".")),
    )
    env.filters["escape_latex"] = escape_latex
    env.filters["md2latex"] = markdown2latex
    env.globals["bold_my_name"] = bold_my_name

    template = env.get_template(str(args.template_path))
    with open(args.data_yml_path) as fp:
        data = yaml.safe_load(fp)
    print(template.render(data))


if __name__ == "__main__":
    main()