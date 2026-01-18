import subprocess

level_files = [
    "foundation/foundation.ttl",
    "perspectives/perspectives.ttl",
    "reference/reference.ttl",
    "disciplines/disciplines.ttl",
]

sorting_order = [
    "foundation",
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

# TODO: Consider to add a forth column containing the abstract (or
# dcterms:description) or all the ontology modules.

widths = [0, 0, 0]  # initial column widths
table = []
for filename in module_files:
    basename = filename[:-4]
    module = basename.split("/")[-1]
    level = basename.split("/")[0]
    if level not in sorting_order:
        level = ""
    iri = f"https://w3id.org/emmo/{basename}"

    table.append([module, level, f"[{iri}]({iri})"])

for row in table:
    for i, cell in enumerate(row):
        if len(cell) > widths[i]:
            widths[i] = len(cell)

# Insert table header
table.insert(0, ["Module", "Level", "Ontology IRI"])
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
