import subprocess

levels = [
    "foundation",
    "perspectives",
    "reference",
    "disciplines",
]
level_files = [f"{level}/{level}.ttl" for level in levels]


def sorter(key):
    """Function defining module sorting order."""
    for i, k in enumerate(levels):
        if key.startswith(k):
            return f"{i}{key}"
    return key


files = subprocess.check_output(
    ["git", "ls-files", "*.ttl"]
).decode().strip().split("\n")

module_files = sorted(set(files).difference(level_files), key=sorter)

# TODO: Consider to add a forth column containing the abstract (or
# dcterms:description) or all the ontology modules.

widths = [0, 0, 0, 0]  # initial column widths
table = []
for filename in module_files:
    basename = filename[:-4]
    module = basename.split("/")[-1]
    level = basename.split("/")[0]
    if level not in levels:
        level = ""
    iri = f"https://w3id.org/emmo/{basename}"
    humeiri = f"https://w3id.org/emmo/hume/{basename}"
    ontology_iri = f"[{iri}]({iri})"
    hume_ontology_iri = f"[{humeiri}]({humeiri})" if level else ""

    table.append([module, level, ontology_iri, hume_ontology_iri])

for row in table:
    for i, cell in enumerate(row):
        if len(cell) > widths[i]:
            widths[i] = len(cell)

# Insert table header
table.insert(0, ["Module", "Level", "Ontology IRI", "HUME ontology IRI"])
table.insert(1, ["-" * w for w in widths])

lines = []
for row in table:
    lines.append(
        "| "
        + " | ".join(f"{cell: <{widths[i]}}" for i, cell in enumerate(row))
        + " |"
    )


print("# EMMO modules")
print("All EMMO modules, including their IRI and the level they belong to.")
print()
print("\n".join(lines))
print()
