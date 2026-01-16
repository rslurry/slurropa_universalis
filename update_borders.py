#! /usr/bin/env python

import sys, os
import re
from dotenv import load_dotenv

load_dotenv()

FCOUNTRIES = os.path.join("main_menu", "setup", "start", "10_countries.txt")
FINPUT  = os.path.join(os.getenv("EU5_GAME_FOLDER"), FCOUNTRIES)
FOUTPUT = os.path.join(os.getenv("SLURROPA_FOLDER"), FCOUNTRIES)

with open(FINPUT, "r") as foo:
    country_data = foo.read()

# Move Pisaq and Pikillaqta to start under Qusqu

# Remove the Pinagua block - they will cease to exist after losing Pikillaqta
def remove_tag_block(text: str, tag: str, replacement: str) -> str:
    # 1. Find the "TAG = {" start
    start_match = re.search(rf"^\s*{tag}\s*=\s*\{{", text, flags=re.MULTILINE)
    if not start_match:
        return text  # tag not found; nothing to do

    start_idx = start_match.start()        # beginning of "PIG = {"
    brace_start = start_match.end() - 1    # position of the '{'

    # 2. Walk forward and count braces to find the matching closing '}'
    depth = 0
    end_idx = brace_start

    for i in range(brace_start, len(text)):
        ch = text[i]
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                end_idx = i + 1  # include the closing brace
                break

    # 3. Remove the block [start_idx:end_idx]
    return text[:start_idx] + replacement + text[end_idx:]

country_data = remove_tag_block(country_data, "PIG", "\t# Slurropa: absorbed into Qusqu for playability")

# Remove Pisaq from Ayarmaca, move capital to Urupampa
# Capture the AYA (Ayarmaca) block
aya_pattern = r"(AYA\s*=\s*\{)(.*?)(\n\})"
aya_match = re.search(aya_pattern, country_data, flags=re.DOTALL)

if aya_match:
    aya_start = aya_match.group(1)
    aya_body = aya_match.group(2)
    aya_end = aya_match.group(3)

    occ_pattern = r"(own_control_core\s*=\s*\{)([^}]*)\}"

    item_to_remove = "pisaq"
    new_capital = "urupampa"

    def occ_replacer(match):
        start = match.group(1)
        inner = match.group(2)

        # Detect indentation of inner items
        inner_indent_match = re.search(r"\n(\s*)\S", inner)
        inner_indent = inner_indent_match.group(1) if inner_indent_match else "        "

        # Normalize items
        items = inner.split()

        # Remove the target item
        items = [i for i in items if i != item_to_remove]

        # Rebuild block
        new_inner = (
            "\n" + inner_indent + " ".join(items) +
            "\n" + inner_indent[:-4]  # closing brace indentation
        )

        return f"{start}{new_inner}}}"

    aya_body = re.sub(occ_pattern, occ_replacer, aya_body, flags=re.DOTALL)

    # Move their capital
    capital_pattern = r"(capital\s*=\s*)(\S+)"

    aya_body = re.sub(capital_pattern, r"\1" + new_capital, aya_body)

    # Rebuild the full AYA block
    new_aya_block = f"{aya_start}{aya_body}{aya_end}"

    # Replace only the AYA block in the file
    country_data = country_data.replace(aya_match.group(0), new_aya_block)
else:
    raise ValueError("AYA tag block not found.")

# Add it into Qusqu
#Capture the CSU (Qusqu) block
csu_pattern = r"(CSU\s*=\s*\{)(.*?)(\n\})"
csu_match = re.search(csu_pattern, country_data, flags=re.DOTALL)

if csu_match:
    csu_start = csu_match.group(1)
    csu_body = csu_match.group(2)
    csu_end = csu_match.group(3)

    # Modify only the own_control_core inside CSU
    occ_pattern = r"(own_control_core\s*=\s*\{)([^}]*)\}"

    new_items = ["pisaq", "pikillaqta"]

    def occ_replacer(match):
        start = match.group(1)          # 'own_control_core = {'
        inner = match.group(2)          # everything inside the braces, including whitespace

        # Detect indentation of the block header
        # (look backward from the match start)
        header_indent_match = re.search(r"^(\s*)own_control_core", match.group(0), flags=re.MULTILINE)
        header_indent = header_indent_match.group(1) if header_indent_match else ""

        # Detect indentation of inner items
        inner_indent_match = re.search(r"\n(\s*)\S", inner)
        inner_indent = inner_indent_match.group(1) if inner_indent_match else header_indent + "    "

        # Normalize existing items
        items = inner.split()
        
        # Add new items
        for item in ["pisaq", "pikillaqta"]:
            if item not in items:
                items.append(item)

        # Rebuild using detected indentation
        new_inner = (
            "\n" + inner_indent + " ".join(items) +
            "\n" + header_indent
        )

        return f"{start}{new_inner}}}"

    new_csu_body = re.sub(occ_pattern, occ_replacer, csu_body, flags=re.DOTALL)

    # Rebuild the CSU block
    new_csu_block = f"{csu_start}{new_csu_body}{csu_end}"

    # Replace only the CSU block in the file
    country_data = country_data.replace(csu_match.group(0), new_csu_block)
else:
    raise ValueError("CSU tag block not found.")

with open(FOUTPUT, "w") as foo:
    foo.write(country_data)

