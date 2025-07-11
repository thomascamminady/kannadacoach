#!/usr/bin/env python3
"""
Generate a corrected dictionary with proper segmentation.
"""

import json
import os
import sys

# Add the correct_transliteration module to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from correct_transliteration import (
    segment_kannada_word,
    transliterate_kannada_advanced,
)


def load_current_dictionary():
    """Load the current dictionary."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dict_path = os.path.join(base_dir, "data", "dictionary.json")

    with open(dict_path, "r", encoding="utf-8") as f:
        return json.load(f)


def fix_dictionary_segmentation():
    """Fix the segmentation in the current dictionary."""
    print("Loading current dictionary...")
    dictionary = load_current_dictionary()

    print(f"Fixing segmentation for {len(dictionary)} entries...")

    fixed_dictionary = []

    for i, entry in enumerate(dictionary):
        if i % 50 == 0:
            print(f"Processing entry {i + 1}/{len(dictionary)}...")

        kannada_word = entry["kn"]

        # Get correct segmentation
        correct_segments = segment_kannada_word(kannada_word)

        # Get correct transliteration
        correct_transliteration = transliterate_kannada_advanced(kannada_word)

        # Create fixed entry
        fixed_entry = {
            "kn": kannada_word,
            "tr": correct_transliteration,
            "en": entry["en"],
            "segments": correct_segments,
        }

        fixed_dictionary.append(fixed_entry)

    return fixed_dictionary


def save_fixed_dictionary(dictionary):
    """Save the fixed dictionary."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dict_path = os.path.join(base_dir, "data", "dictionary.json")

    with open(dict_path, "w", encoding="utf-8") as f:
        json.dump(dictionary, f, ensure_ascii=False, indent=2)

    print(f"Fixed dictionary saved to: {dict_path}")


def main():
    """Main function."""
    print("Fixing dictionary segmentation...")

    try:
        fixed_dictionary = fix_dictionary_segmentation()
        save_fixed_dictionary(fixed_dictionary)

        print("\nSample fixed entries:")
        for i, entry in enumerate(fixed_dictionary[:3]):
            print(f"\n{i + 1}. {entry['kn']} -> {entry['tr']} ({entry['en']})")
            print("   Segments:")
            for seg in entry["segments"]:
                print(f"     {seg['kn']} -> {seg['tr']}")

        print(
            f"\nDictionary fixed successfully! Total entries: {len(fixed_dictionary)}"
        )

    except Exception as e:
        print(f"Error fixing dictionary: {e}")
        raise


if __name__ == "__main__":
    main()
