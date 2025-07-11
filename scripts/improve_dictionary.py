#!/usr/bin/env python3
"""
Fixed transliteration script that properly handles compound consonants and conjuncts.
"""

import json
import re
import time
from urllib.parse import quote

import requests
from bs4 import BeautifulSoup


def load_existing_dictionary():
    """Load the existing curated dictionary as a base."""
    try:
        with open("data/dictionary.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def improved_transliterate_kannada(text):
    """Convert Kannada text to proper romanized transliteration."""
    # Enhanced mapping with proper compound consonant handling
    mapping = {
        # Vowels
        "ಅ": "a",
        "ಆ": "aa",
        "ಇ": "i",
        "ಈ": "ii",
        "ಉ": "u",
        "ಊ": "uu",
        "ಎ": "e",
        "ಏ": "ee",
        "ಒ": "o",
        "ಓ": "oo",
        "ಔ": "au",
        # Consonants
        "ಕ": "ka",
        "ಖ": "kha",
        "ಗ": "ga",
        "ಘ": "gha",
        "ಙ": "nga",
        "ಚ": "cha",
        "ಛ": "chha",
        "ಜ": "ja",
        "ಝ": "jha",
        "ಞ": "nja",
        "ಟ": "ta",
        "ಠ": "tha",
        "ಡ": "da",
        "ಢ": "dha",
        "ಣ": "na",
        "ತ": "ta",
        "ಥ": "tha",
        "ದ": "da",
        "ಧ": "dha",
        "ನ": "na",
        "ಪ": "pa",
        "ಫ": "pha",
        "ಬ": "ba",
        "ಭ": "bha",
        "ಮ": "ma",
        "ಯ": "ya",
        "ರ": "ra",
        "ಲ": "la",
        "ವ": "va",
        "ಶ": "sha",
        "ಷ": "sha",
        "ಸ": "sa",
        "ಹ": "ha",
        "ಳ": "la",
        "ೞ": "zha",
        # Vowel signs
        "ಾ": "aa",
        "ಿ": "i",
        "ೀ": "ii",
        "ು": "u",
        "ೂ": "uu",
        "ೃ": "ri",
        "ೆ": "e",
        "ೇ": "ee",
        "ೈ": "ai",
        "ೊ": "o",
        "ೋ": "oo",
        "ೌ": "au",
        # Special characters
        "ಂ": "m",
        "ಃ": "h",
        "್": "",
        "಼": "",
        # Double consonants (geminated)
        "ಕ್ಕ": "kka",
        "ಗ್ಗ": "gga",
        "ಚ್ಚ": "ccha",
        "ಜ್ಜ": "jja",
        "ಟ್ಟ": "tta",
        "ಡ್ಡ": "dda",
        "ಣ್ಣ": "nna",
        "ತ್ತ": "tta",
        "ದ್ದ": "dda",
        "ನ್ನ": "nna",
        "ಪ್ಪ": "ppa",
        "ಬ್ಬ": "bba",
        "ಮ್ಮ": "mma",
        "ಯ್ಯ": "yya",
        "ರ್ರ": "rra",
        "ಲ್ಲ": "lla",
        "ವ್ವ": "vva",
        "ಶ್ಶ": "shsha",
        "ಸ್ಸ": "ssa",
        "ಹ್ಹ": "hha",
    }

    result = ""
    i = 0
    while i < len(text):
        # Check for 3-char combinations first (like ತ್ತು)
        if i < len(text) - 2:
            three_char = text[i : i + 3]
            if three_char in mapping:
                result += mapping[three_char]
                i += 3
                continue

        # Check for 2-char combinations
        if i < len(text) - 1:
            two_char = text[i : i + 2]
            if two_char in mapping:
                result += mapping[two_char]
                i += 2
                continue

        # Single character mapping
        if text[i] in mapping:
            result += mapping[text[i]]
        else:
            result += text[i]
        i += 1

    return result


def improved_get_kannada_segments(word):
    """Break down a Kannada word into proper segments for typing practice."""
    segments = []
    i = 0

    while i < len(word):
        # Check for geminated consonants (like ತ್ತ)
        if i < len(word) - 2:
            # Check for patterns like ತ್ತು (consonant + virama + same consonant + vowel)
            if (
                word[i + 1] == "್"
                and i + 2 < len(word)
                and word[i] == word[i + 2]
                and i + 3 < len(word)
                and word[i + 3]
                in ["ಾ", "ಿ", "ೀ", "ು", "ೂ", "ೃ", "ೆ", "ೇ", "ೈ", "ೊ", "ೋ", "ೌ"]
            ):
                # Geminated consonant with vowel sign
                segment = word[i : i + 4]
                segments.append(
                    {
                        "kn": segment,
                        "tr": improved_transliterate_kannada(segment),
                    }
                )
                i += 4
                continue
            elif (
                word[i + 1] == "್"
                and i + 2 < len(word)
                and word[i] == word[i + 2]
            ):
                # Geminated consonant without vowel sign
                segment = word[i : i + 3]
                segments.append(
                    {
                        "kn": segment,
                        "tr": improved_transliterate_kannada(segment),
                    }
                )
                i += 3
                continue

        # Check for consonant + virama + vowel sign
        if (
            i < len(word) - 2
            and word[i + 1] == "್"
            and word[i + 2]
            in ["ಾ", "ಿ", "ೀ", "ು", "ೂ", "ೃ", "ೆ", "ೇ", "ೈ", "ೊ", "ೋ", "ೌ"]
        ):
            segment = word[i : i + 3]
            segments.append(
                {"kn": segment, "tr": improved_transliterate_kannada(segment)}
            )
            i += 3
            continue

        # Check for consonant + vowel sign
        if i < len(word) - 1 and word[i + 1] in [
            "ಾ",
            "ಿ",
            "ೀ",
            "ು",
            "ೂ",
            "ೃ",
            "ೆ",
            "ೇ",
            "ೈ",
            "ೊ",
            "ೋ",
            "ೌ",
        ]:
            segment = word[i : i + 2]
            segments.append(
                {"kn": segment, "tr": improved_transliterate_kannada(segment)}
            )
            i += 2
            continue

        # Check for consonant + virama (without vowel)
        if i < len(word) - 1 and word[i + 1] == "್":
            segment = word[i : i + 2]
            segments.append(
                {"kn": segment, "tr": improved_transliterate_kannada(segment)}
            )
            i += 2
            continue

        # Single character
        segment = word[i]
        segments.append(
            {"kn": segment, "tr": improved_transliterate_kannada(segment)}
        )
        i += 1

    return segments


def get_better_translation(word):
    """Get better English translation using multiple sources."""

    # Comprehensive word translations
    translations = {
        "ಜಗತ್ತು": "world",
        "ಪ್ರಪಂಚ": "world",
        "ಸಮಾಜ": "society",
        "ಸಂಸ್ಕೃತಿ": "culture",
        "ಕಲೆ": "art",
        "ತಂತ್ರಜ್ಞಾನ": "technology",
        "ಪ್ರಕೃತಿ": "nature",
        "ಪರಿಸರ": "environment",
        "ಸೇವೆ": "service",
        "ವ್ಯಾಪಾರ": "business",
        "ಕಾರ್ಖಾನೆ": "factory",
        "ಇಂಟರ್ನೆಟ್": "internet",
        "ಮೊಬೈಲ್": "mobile",
        "ಬಸ್": "bus",
        "ರೈಲು": "train",
        "ಮಾರುಕಟ್ಟೆ": "market",
        "ಮಾರಾಟ": "sale",
        "ಜನತೆ": "people",
        "ಮತದಾನ": "voting",
        "ನ್ಯಾಯಾಲಯ": "court",
        "ಕಾನೂನು": "law",
        "ಪೊಲೀಸ್": "police",
        "ಅಧಿಕಾರಿ": "officer",
        "ಅಧ್ಯಕ್ಷ": "president",
        "ಬ್ಯಾಂಕ್": "bank",
        "ಆರ್ಥಿಕ": "financial",
        "ಬಜೆಟ್": "budget",
        "ಆದಾಯ": "income",
        "ವೆಚ್ಚ": "expense",
        "ಕೃಷಿ": "agriculture",
        "ಬೆಳೆ": "crop",
        "ಪ್ರಾಣಿಪಾಲನೆ": "animal husbandry",
        "ಶುಭ": "auspicious",
        "ಸಂಭ್ರಮ": "celebration",
        "ಪ್ರಾಧ್ಯಾಪಕ": "professor",
        "ಉತ್ತರ": "answer",  # Fix: was "northern"
        "ಮಾತು": "word",
        "ಸಮಯ": "time",
        "ಜೀವನ": "life",
        "ಮಾನವ": "human",
        "ಭಾಷೆ": "language",
        "ಸಾಹಿತ್ಯ": "literature",
        "ವಿಜ್ಞಾನ": "science",
        "ಆರೋಗ್ಯ": "health",
        "ವೈದ್ಯ": "doctor",
        "ಔಷಧ": "medicine",
        "ಆಸ್ಪತ್ರೆ": "hospital",
        "ವಿದ್ಯಾರ್ಥಿ": "student",
        "ಪರೀಕ್ಷೆ": "exam",
        "ಪ್ರಶ್ನೆ": "question",
        "ಸಮಸ್ಯೆ": "problem",
        "ಪರಿಹಾರ": "solution",
        "ಸಹಾಯ": "help",
        "ಕೆಲಸ": "work",
        "ಯಂತ್ರ": "machine",
        "ಗಣಕ": "computer",
        "ಕಾರು": "car",
        "ವಿಮಾನ": "airplane",
        "ರಸ್ತೆ": "road",
        "ಸೇತುವೆ": "bridge",
        "ಅಂಗಡಿ": "shop",
        "ಬೆಲೆ": "price",
        "ಖರೀದಿ": "purchase",
        "ಸರ್ಕಾರ": "government",
        "ರಾಜ್ಯ": "state",
        "ದೇಶ": "country",
        "ಚುನಾವಣೆ": "election",
        "ಹಣ": "money",
        "ರೈತ": "farmer",
        "ಜಮೀನು": "land",
        "ಹಬ್ಬ": "festival",
        "ಉತ್ಸವ": "celebration",
        "ಮಂಗಳ": "auspicious",
        "ಆನಂದ": "happiness",
    }

    return translations.get(word, None)


def create_improved_dictionary():
    """Create an improved dictionary with better segmentation and translations."""
    print("Loading existing dictionary...")
    existing_dict = load_existing_dictionary()

    print(f"Processing {len(existing_dict)} existing words...")

    improved_entries = []

    for entry in existing_dict:
        word = entry["kn"]

        # Get better translation
        better_translation = get_better_translation(word)
        if better_translation:
            translation = better_translation
        else:
            translation = entry["en"]

        # Improved transliteration and segmentation
        transliteration = improved_transliterate_kannada(word)
        segments = improved_get_kannada_segments(word)

        improved_entry = {
            "kn": word,
            "tr": transliteration,
            "en": translation,
            "segments": segments,
        }

        improved_entries.append(improved_entry)
        print(f"Processed: {word} -> {transliteration} ({translation})")

    return improved_entries


def main():
    """Main function to create the improved dictionary."""
    print("Creating improved Kannada dictionary...")

    improved_dict = create_improved_dictionary()

    # Save the improved dictionary
    with open("data/improved_dictionary.json", "w", encoding="utf-8") as f:
        json.dump(improved_dict, f, ensure_ascii=False, indent=2)

    print(f"Improved dictionary saved with {len(improved_dict)} entries")

    # Display sample entries
    print("\nSample improved entries:")
    for i, entry in enumerate(improved_dict[:10]):
        print(f"{i + 1}. {entry['kn']} ({entry['tr']}) - {entry['en']}")
        if entry["segments"]:
            segments_str = " + ".join(
                [f"{seg['kn']}({seg['tr']})" for seg in entry["segments"]]
            )
            print(f"   Segments: {segments_str}")


if __name__ == "__main__":
    main()
