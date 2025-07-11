#!/usr/bin/env python3
"""
Fix transliteration errors in Kannada dictionary.
Main issues:
- ಗು should be "gu" not "gau"
- ರು should be "ru" not "rau"
- ಮು should be "mu" not "mau"
- All consonant+vowel combinations are incorrectly adding extra "a"
"""

import json
import re


def fix_transliteration(text):
    """Fix common transliteration errors."""
    # Map of incorrect -> correct transliterations
    fixes = {
        # Consonant + ು (u vowel)
        "gau": "gu",
        "rau": "ru",
        "mau": "mu",
        "nau": "nu",
        "dau": "du",
        "tau": "tu",
        "pau": "pu",
        "bau": "bu",
        "yau": "yu",
        "lau": "lu",
        "vau": "vu",
        "sau": "su",
        "hau": "hu",
        "kau": "ku",
        "chau": "chu",
        "jau": "ju",
        "thau": "thu",
        "dhau": "dhu",
        "phau": "phu",
        "bhau": "bhu",
        "shau": "shu",
        # Consonant + ೂ (uu vowel)
        "gauu": "guu",
        "rauu": "ruu",
        "mauu": "muu",
        "nauu": "nuu",
        "dauu": "duu",
        "tauu": "tuu",
        "pauu": "puu",
        "bauu": "buu",
        "yauu": "yuu",
        "lauu": "luu",
        "vauu": "vuu",
        "sauu": "suu",
        "hauu": "huu",
        "kauu": "kuu",
        "chauu": "chuu",
        "jauu": "juu",
        "thauu": "thuu",
        "dhauu": "dhuu",
        "phauu": "phuu",
        "bhauu": "bhuu",
        "shauu": "shuu",
        # Other common errors
        "aee": "ee",
        "aoo": "oo",
        "aau": "au",
    }

    # Apply fixes
    result = text
    for incorrect, correct in fixes.items():
        result = result.replace(incorrect, correct)

    return result


def fix_dictionary(input_file, output_file):
    """Fix transliteration in dictionary file."""
    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    fixed_count = 0

    for entry in data:
        # Fix main transliteration
        old_tr = entry["tr"]
        entry["tr"] = fix_transliteration(entry["tr"])

        # Fix segment transliterations
        for segment in entry.get("segments", []):
            old_seg_tr = segment["tr"]
            segment["tr"] = fix_transliteration(segment["tr"])
            if old_seg_tr != segment["tr"]:
                fixed_count += 1

        if old_tr != entry["tr"]:
            fixed_count += 1

    # Write corrected data
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Fixed {fixed_count} transliteration errors")
    print(f"Corrected dictionary saved to {output_file}")


if __name__ == "__main__":
    fix_dictionary(
        "data/comprehensive_dictionary.json", "data/corrected_dictionary.json"
    )
