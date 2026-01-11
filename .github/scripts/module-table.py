import subprocess

level_files = [
    "tlo.ttl",
    "mlo.ttl",
    "full.ttl",
    # "mereocausality/mereocausality.ttl",
    "perspectives/perspectives.ttl",
    "reference/reference.ttl",
    "disciplines/disciplines.ttl",
]

sorting_order = [
    "mereocausality",
    "perspectives",
    "reference",
    "disciplines",
]

def sorter(key):
    """Function defining module sorting order."""
    for i, k in enumerate(sorting_order):
        if key.startswith(k):
            return f"{i}{key}"
    return key

files = subprocess.check_output(
    ["git", "ls-files", "*.ttl"]
).decode().strip().split("\n")

module_files = sorted(set(files).difference(level_files), key=sorter)

# TODO: Consider to add a third column containing the abstract (or dcterms:description) or all the ontology modules.

widths = [0, 0]  # initial column widths
table = [
    ("Module", "Ontology IRI"),
    ("---", "---"),
]
for filename in module_files:
    name = filename[:-4]
    table.append((name.split("/")[-1], f"https://w3id.org/emmo/{name}"))

for row in table:
    for i, cell in enumerate(row):
        if len(cell) > widths[i]:
            widths[i] = len(cell)

lines = []
for row in table:
    lines.append(
        "| "
        + "| ".join(f"{cell: <{widths[i]}}" for i, cell in enumerate(row))
        + " |"
    )

print("\n".join(lines))
