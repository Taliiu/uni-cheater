import PyPDF2
import re
from pprint import PrettyPrinter

pp = PrettyPrinter()


def get_whole_text(pdf_reader):
    result = ""
    for i in range(pdf_reader.numPages):
        page = pdf_reader.getPage(i)
        result += page.extractText() + "\n"
    return result


def parse_section(section_text):
    subtasks = []
    subtask_regex = r"^[a-z]\)"
    matches = re.finditer(subtask_regex, section_text, re.MULTILINE)
    matches = list(matches)

    for i, match in enumerate(matches):
        if i < len(matches)-1:
            to_index = matches[i+1].end() - 2
        else:
            to_index = -1

        from_index = match.start() + 2
        ex_text = section_text[from_index:to_index]
        subtasks.append(ex_text.strip())

    first_big_char = re.search(r"[A-Z]", section_text, re.MULTILINE)

    from_index = first_big_char.start()
    if len(subtasks) == 0:
        to_index = -1
    else:
        to_index = matches[0].start()
    description = section_text[from_index:to_index]

    return {
        "description": description,
        "subtasks": subtasks
    }


def get_exercises(f):
    exs = []
    pdf_reader = PyPDF2.PdfFileReader(f)
    pdf_content = get_whole_text(pdf_reader)

    sections = pdf_content.split(". Aufgabe")
    sections = sections[1:]  # skip first section, since it's the title

    for section in sections:
        exercise = parse_section(section)
        exs.append(exercise)

    return exs


def parse_document(filename):
    with open(filename, 'rb') as f:
        return get_exercises(f)


if __name__ == "__main__":
    doc = parse_document("file.pdf")
    pp.pprint(doc)
