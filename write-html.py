from structurepdf import parse_document
from jinja2 import Environment, FileSystemLoader

exercises = parse_document("file.pdf")

file_loader = FileSystemLoader("templates")
env = Environment(loader=file_loader)
rendered = env.get_template("test.html").render(exercises=exercises, title="Titel")

file_name = "index.html"

with open(f"{file_name}", "w") as f:
    f.write(rendered)
