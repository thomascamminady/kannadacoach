#!/usr/bin/env python3
"""
Create a comprehensive Kannada dictionary with proper segmentation and translations.
Focus on fixing compound consonant segmentation issues.
"""

import json
import re
from typing import Any, Dict, List


def fixed_transliterate_kannada(text: str) -> str:
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
        # Vowel signs (matras)
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


def fixed_get_kannada_segments(word: str) -> List[Dict[str, str]]:
    """
    Break down a Kannada word into proper segments for typing practice.
    Fixed to handle compound consonants properly.
    """
    segments = []
    i = 0

    while i < len(word):
        segment_found = False

        # Check for geminated consonants (like ತ್ತು from ಜಗತ್ತು)
        if i < len(word) - 2:
            # Pattern: consonant + virama + same consonant + vowel sign
            if (
                word[i + 1] == "್"
                and i + 2 < len(word)
                and word[i] == word[i + 2]
                and i + 3 < len(word)
                and word[i + 3]
                in ["ಾ", "ಿ", "ೀ", "ು", "ೂ", "ೃ", "ೆ", "ೇ", "ೈ", "ೊ", "ೋ", "ೌ"]
            ):
                # Geminated consonant with vowel sign (e.g., ತ್ತು)
                segment = word[i : i + 4]
                segments.append(
                    {"kn": segment, "tr": fixed_transliterate_kannada(segment)}
                )
                i += 4
                segment_found = True

            # Pattern: consonant + virama + same consonant (no vowel)
            elif (
                word[i + 1] == "್"
                and i + 2 < len(word)
                and word[i] == word[i + 2]
            ):
                # Geminated consonant without vowel sign (e.g., ತ್ತ)
                segment = word[i : i + 3]
                segments.append(
                    {"kn": segment, "tr": fixed_transliterate_kannada(segment)}
                )
                i += 3
                segment_found = True

        if not segment_found:
            # Check for consonant + virama + vowel sign
            if (
                i < len(word) - 2
                and word[i + 1] == "್"
                and word[i + 2]
                in ["ಾ", "ಿ", "ೀ", "ು", "ೂ", "ೃ", "ೆ", "ೇ", "ೈ", "ೊ", "ೋ", "ೌ"]
            ):
                segment = word[i : i + 3]
                segments.append(
                    {"kn": segment, "tr": fixed_transliterate_kannada(segment)}
                )
                i += 3
                segment_found = True

        if not segment_found:
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
                    {"kn": segment, "tr": fixed_transliterate_kannada(segment)}
                )
                i += 2
                segment_found = True

        if not segment_found:
            # Check for consonant + virama (without vowel)
            if i < len(word) - 1 and word[i + 1] == "್":
                segment = word[i : i + 2]
                segments.append(
                    {"kn": segment, "tr": fixed_transliterate_kannada(segment)}
                )
                i += 2
                segment_found = True

        if not segment_found:
            # Single character
            segment = word[i]
            segments.append(
                {"kn": segment, "tr": fixed_transliterate_kannada(segment)}
            )
            i += 1

    return segments


def get_comprehensive_dictionary() -> List[Dict[str, Any]]:
    """
    Create a comprehensive dictionary with proper segmentation and translations.
    """
    words = [
        # Basic words
        {"kn": "ಕನ್ನಡ", "en": "Kannada language"},
        {"kn": "ನಮಸ್ಕಾರ", "en": "greetings"},
        {"kn": "ಧನ್ಯವಾದ", "en": "thank you"},
        {"kn": "ಕ್ಷಮಿಸಿ", "en": "sorry"},
        {"kn": "ಮನೆ", "en": "house"},
        {"kn": "ಆಹಾರ", "en": "food"},
        # Words with compound consonants
        {"kn": "ಜಗತ್ತು", "en": "world"},
        {"kn": "ಮಕ್ಕಳು", "en": "children"},
        {"kn": "ಮಿತ್ರ", "en": "friend"},
        {"kn": "ಶಿಕ್ಷಕ", "en": "teacher"},
        {"kn": "ಗುರು", "en": "teacher"},
        {"kn": "ಪಾಠ", "en": "lesson"},
        {"kn": "ಪತ್ರ", "en": "letter"},
        {"kn": "ಪ್ರಿಯ", "en": "dear"},
        {"kn": "ಸತ್ಯ", "en": "truth"},
        {"kn": "ಮತ್ತು", "en": "and"},
        {"kn": "ಅಥವಾ", "en": "or"},
        {"kn": "ಈಗ", "en": "now"},
        {"kn": "ಮುಂದೆ", "en": "next"},
        {"kn": "ಹಿಂದೆ", "en": "behind"},
        # Family terms
        {"kn": "ಅಪ್ಪ", "en": "father"},
        {"kn": "ಅಮ್ಮ", "en": "mother"},
        {"kn": "ಸಹೋದರ", "en": "brother"},
        {"kn": "ಸಹೋದರಿ", "en": "sister"},
        {"kn": "ಮಗ", "en": "son"},
        {"kn": "ಮಗಳು", "en": "daughter"},
        {"kn": "ಅಜ್ಜ", "en": "grandfather"},
        {"kn": "ಅಜ್ಜಿ", "en": "grandmother"},
        # Colors
        {"kn": "ಬಿಳಿ", "en": "white"},
        {"kn": "ಕಪ್ಪು", "en": "black"},
        {"kn": "ಕೆಂಪು", "en": "red"},
        {"kn": "ಹಸಿರು", "en": "green"},
        {"kn": "ನೀಲಿ", "en": "blue"},
        {"kn": "ಹಳದಿ", "en": "yellow"},
        # Nature
        {"kn": "ಸೂರ್ಯ", "en": "sun"},
        {"kn": "ಚಂದ್ರ", "en": "moon"},
        {"kn": "ನಕ್ಷತ್ರ", "en": "star"},
        {"kn": "ಆಕಾಶ", "en": "sky"},
        {"kn": "ಭೂಮಿ", "en": "earth"},
        {"kn": "ನೀರು", "en": "water"},
        {"kn": "ಗಾಳಿ", "en": "air"},
        {"kn": "ಮಳೆ", "en": "rain"},
        {"kn": "ಹೂವು", "en": "flower"},
        {"kn": "ಮರ", "en": "tree"},
        {"kn": "ಹಣ್ಣು", "en": "fruit"},
        {"kn": "ಎಲೆ", "en": "leaf"},
        # Body parts
        {"kn": "ತಲೆ", "en": "head"},
        {"kn": "ಕೈ", "en": "hand"},
        {"kn": "ಕಾಲು", "en": "leg"},
        {"kn": "ಕಣ್ಣು", "en": "eye"},
        {"kn": "ಕಿವಿ", "en": "ear"},
        {"kn": "ಮೂಗು", "en": "nose"},
        {"kn": "ಬಾಯಿ", "en": "mouth"},
        # Time
        {"kn": "ಸಮಯ", "en": "time"},
        {"kn": "ದಿನ", "en": "day"},
        {"kn": "ರಾತ್ರಿ", "en": "night"},
        {"kn": "ಬೆಳಿಗ್ಗೆ", "en": "morning"},
        {"kn": "ಮಧ್ಯಾಹ್ನ", "en": "afternoon"},
        {"kn": "ಸಂಜೆ", "en": "evening"},
        {"kn": "ವಾರ", "en": "week"},
        {"kn": "ತಿಂಗಳು", "en": "month"},
        {"kn": "ವರ್ಷ", "en": "year"},
        # Numbers
        {"kn": "ಒಂದು", "en": "one"},
        {"kn": "ಎರಡು", "en": "two"},
        {"kn": "ಮೂರು", "en": "three"},
        {"kn": "ನಾಲ್ಕು", "en": "four"},
        {"kn": "ಐದು", "en": "five"},
        {"kn": "ಆರು", "en": "six"},
        {"kn": "ಏಳು", "en": "seven"},
        {"kn": "ಎಂಟು", "en": "eight"},
        {"kn": "ಒಂಬತ್ತು", "en": "nine"},
        {"kn": "ಹತ್ತು", "en": "ten"},
        # Common adjectives
        {"kn": "ಚಿಕ್ಕ", "en": "small"},
        {"kn": "ದೊಡ್ಡ", "en": "big"},
        {"kn": "ಹೊಸ", "en": "new"},
        {"kn": "ಹಳೆಯ", "en": "old"},
        {"kn": "ಸುಂದರ", "en": "beautiful"},
        {"kn": "ಒಳ್ಳೆಯ", "en": "good"},
        {"kn": "ಕೆಟ್ಟ", "en": "bad"},
        {"kn": "ಬಿಸಿ", "en": "hot"},
        {"kn": "ತಣ್ಣಗಿರು", "en": "cold"},
        # Verbs
        {"kn": "ಬರು", "en": "come"},
        {"kn": "ಹೋಗು", "en": "go"},
        {"kn": "ತಿನ್ನು", "en": "eat"},
        {"kn": "ಕುಡಿ", "en": "drink"},
        {"kn": "ಮಾತನಾಡು", "en": "speak"},
        {"kn": "ಓದು", "en": "read"},
        {"kn": "ಬರೆ", "en": "write"},
        {"kn": "ನೋಡು", "en": "see"},
        {"kn": "ಕೇಳು", "en": "listen"},
        {"kn": "ಮಲಗು", "en": "sleep"},
        {"kn": "ಎದ್ದೇಳು", "en": "wake up"},
        {"kn": "ಕೆಲಸ", "en": "work"},
        {"kn": "ಆಟ", "en": "play"},
        # Common phrases
        {"kn": "ಹೇಗಿದ್ದೀರಿ", "en": "how are you"},
        {"kn": "ಚೆನ್ನಾಗಿದ್ದೇನೆ", "en": "I am fine"},
        {"kn": "ಕ್ಷಮಿಸಿ", "en": "excuse me"},
        {"kn": "ಗೊತ್ತಿಲ್ಲ", "en": "don't know"},
        {"kn": "ಸರಿ", "en": "okay"},
        {"kn": "ಇಲ್ಲ", "en": "no"},
        {"kn": "ಹೌದು", "en": "yes"},
    ]

    # Process each word
    processed_words = []
    for word_info in words:
        word = word_info["kn"]
        meaning = word_info["en"]

        # Get segments
        segments = fixed_get_kannada_segments(word)

        # Get full transliteration
        full_transliteration = fixed_transliterate_kannada(word)

        processed_words.append(
            {
                "kn": word,
                "tr": full_transliteration,
                "en": meaning,
                "segments": segments,
            }
        )

    return processed_words


def test_segmentation():
    """Test the segmentation on problematic words."""
    test_words = ["ಜಗತ್ತು", "ಮಕ್ಕಳು", "ಅಮ್ಮ", "ಪತ್ರ", "ಮತ್ತು"]

    print("Testing segmentation:")
    for word in test_words:
        segments = fixed_get_kannada_segments(word)
        transliteration = fixed_transliterate_kannada(word)
        print(f"Word: {word}")
        print(f"Full transliteration: {transliteration}")
        print(
            f"Segments: {[s['kn'] for s in segments]} -> {[s['tr'] for s in segments]}"
        )
        print()


def main():
    """Create the comprehensive dictionary."""
    print("Testing segmentation first...")
    test_segmentation()

    print("\nCreating comprehensive dictionary...")
    dictionary = get_comprehensive_dictionary()

    # Write to file
    with open("data/comprehensive_dictionary.json", "w", encoding="utf-8") as f:
        json.dump(dictionary, f, ensure_ascii=False, indent=2)

    print(f"Created comprehensive dictionary with {len(dictionary)} words")
    print("Saved to: data/comprehensive_dictionary.json")


if __name__ == "__main__":
    main()
