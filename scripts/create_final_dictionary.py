#!/usr/bin/env python3
"""
Create a comprehensive fixed dictionary with proper segmentation and translations.
"""

import json


def improved_transliterate_kannada(text):
    """Convert Kannada text to proper romanized transliteration."""
    # Map for 3-character combinations (geminated + vowel)
    three_char_map = {
        "ತ್ತು": "ttau",
        "ಕ್ಕು": "kkau",
        "ಗ್ಗು": "ggau",
        "ಚ್ಚು": "cchau",
        "ಜ್ಜು": "jjau",
        "ಣ್ಣು": "nnau",
        "ನ್ನು": "nnau",
        "ಪ್ಪು": "ppau",
        "ಬ್ಬು": "bbau",
        "ಮ್ಮು": "mmau",
        "ಲ್ಲು": "llau",
        "ತ್ತೆ": "ttae",
        "ಕ್ಕೆ": "kkae",
        "ತ್ತಿ": "ttai",
        "ಕ್ಕಿ": "kkai",
    }

    # Map for 2-character combinations
    two_char_map = {
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
        "ಸ್ಕಾ": "skaa",
        "ಸ್ತ": "sta",
        "ಸ್ಪ": "spa",
        "ಸ್ಟ": "sta",
        "ಗು": "gu",
        "ಡು": "du",
        "ಮ": "ma",
        "ಗ": "ga",
        "ನ": "na",
        "ಶಾ": "shaa",
        "ಲೆ": "le",
        "ಅ": "a",
        "ಜ್ಜ": "jja",
        "ಮಾ": "maa",
        "ತು": "tu",
        "ಸ": "sa",
        "ಯ": "ya",
        "ಜೀ": "jii",
        "ವ": "va",
        "ಪ್": "p",
        "ರ": "ra",
        "ಪ": "pa",
        "ಂ": "m",
        "ಚ": "cha",
        "ರೀ": "rii",
        "ಕ್": "k",
        "ಷೆ": "she",
        "ಪ್": "p",
        "ನೆ": "ne",
        "ಉ": "u",
        "ತ್": "t",
        "ತ": "ta",
        "ಭಾ": "bhaa",
        "ಷೆ": "she",
        "ಸಾ": "saa",
        "ಹಿ": "hi",
        "ವಿ": "vi",
        "ಜ್": "j",
        "ಞಾ": "njaa",
        "ಕ": "ka",
        "ಲೆ": "le",
        "ಔ": "au",
        "ಷ": "sha",
        "ಧ": "dha",
        "ಆ": "aa",
        "ಸ್": "s",
        "ಪ": "pa",
        "ರೆ": "re",
        "ಥಿ": "thi",
        "ದ್": "d",
        "ಯಾ": "yaa",
        "ರ್": "r",
        "ಧ್": "dh",
        "ಗ್": "g",
        "ಆ": "aa",
        "ರೋ": "roo",
        "ವೈ": "vai",
        "ದ್": "d",
        "ಯ": "ya",
        "ಸೇ": "see",
        "ವೆ": "ve",
        "ಕೆ": "ke",
        "ಲ": "la",
        "ವ್": "v",
        "ಯಾ": "yaa",
        "ಪಾ": "paa",
        "ಕಾ": "kaa",
        "ರ್": "r",
        "ಖಾ": "khaa",
        "ನೆ": "ne",
        "ಣ": "na",
        "ಇ": "i",
        "ಟ": "ta",
        "ರ್": "r",
        "ನೆ": "ne",
        "ಟ್": "t",
        "ಮೊ": "mo",
        "ಬೈ": "bai",
        "ಲ್": "l",
        "ಕಾ": "kaa",
        "ರು": "ru",
        "ಬ": "ba",
        "ಸ್": "s",
        "ರೈ": "rai",
        "ಲು": "lu",
        "ದೇ": "dee",
        "ಶ": "sha",
        "ಜ": "ja",
        "ತೆ": "te",
        "ಚು": "chu",
        "ನಾ": "naa",
        "ಣೆ": "ne",
        "ನ್": "n",
        "ಲ": "la",
        "ಕಾ": "kaa",
        "ನೂ": "nuu",
        "ನು": "nu",
        "ಪೊ": "po",
        "ಲೀ": "lii",
        "ಸ್": "s",
        "ಅ": "a",
        "ಧಿ": "dhi",
        "ರಿ": "ri",
        "ಅ": "a",
        "ಧ್": "dh",
        "ಕ್": "k",
        "ಷ": "sha",
        "ಬ್": "b",
        "ಯಾ": "yaa",
        "ಂ": "m",
        "ಕ್": "k",
        "ಹ": "ha",
        "ಣ": "na",
        "ಥಿ": "thi",
        "ಬ": "ba",
        "ಜೆ": "je",
        "ಟ್": "t",
        "ದಾ": "daa",
        "ವೆ": "ve",
        "ಚ್": "ch",
        "ಚ": "cha",
        "ಕೃ": "kru",
        "ಷಿ": "shi",
        "ರೈ": "rai",
        "ಬೆ": "be",
        "ಳೆ": "le",
        "ಮೀ": "mii",
        "ಪ್": "p",
        "ರಾ": "raa",
        "ಣಿ": "ni",
        "ಪಾ": "paa",
        "ಶು": "shu",
        "ಭ": "bha",
        "ಸ": "sa",
        "ಭ್": "bh",
        "ಮ": "ma",
        "ನ": "na",
        "ಂ": "m",
        "ದ": "da",
    }

    # Single character mapping
    single_char_map = {
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
        "ಂ": "m",
        "ಃ": "h",
        "್": "",
        "಼": "",
    }

    result = ""
    i = 0
    while i < len(text):
        # Check for 3-char combinations first
        if i < len(text) - 2:
            three_char = text[i : i + 3]
            if three_char in three_char_map:
                result += three_char_map[three_char]
                i += 3
                continue

        # Check for 2-char combinations
        if i < len(text) - 1:
            two_char = text[i : i + 2]
            if two_char in two_char_map:
                result += two_char_map[two_char]
                i += 2
                continue

        # Single character mapping
        if text[i] in single_char_map:
            result += single_char_map[text[i]]
        else:
            result += text[i]
        i += 1

    return result


def improved_get_kannada_segments(word):
    """Break down a Kannada word into proper segments."""
    segments = []
    i = 0

    while i < len(word):
        # Check for ತ್ತು pattern specifically
        if i < len(word) - 2 and word[i : i + 3] == "ತ್ತು":
            segments.append({"kn": "ತ್ತು", "tr": "ttau"})
            i += 3
            continue

        # Check for other 3-char patterns
        if i < len(word) - 2:
            three_char = word[i : i + 3]
            three_char_patterns = [
                "ಕ್ಕು",
                "ಗ್ಗು",
                "ಚ್ಚು",
                "ಜ್ಜು",
                "ಣ್ಣು",
                "ನ್ನು",
                "ಪ್ಪು",
                "ಬ್ಬು",
                "ಮ್ಮು",
                "ಲ್ಲು",
            ]
            if three_char in three_char_patterns:
                segments.append(
                    {
                        "kn": three_char,
                        "tr": improved_transliterate_kannada(three_char),
                    }
                )
                i += 3
                continue

        # Check for consonant clusters
        if i < len(word) - 2 and word[i + 1] == "್":
            cluster = word[i : i + 3]
            segments.append(
                {"kn": cluster, "tr": improved_transliterate_kannada(cluster)}
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

        # Single character
        segment = word[i]
        segments.append(
            {"kn": segment, "tr": improved_transliterate_kannada(segment)}
        )
        i += 1

    return segments


def create_comprehensive_dictionary():
    """Create a comprehensive dictionary with proper words and translations."""

    words_data = [
        # Original curated words
        {"kn": "ಕನ್ನಡ", "en": "Kannada (language)"},
        {"kn": "ನಮಸ್ಕಾರ", "en": "Hello / Greetings"},
        {"kn": "ಗುಡುಗು", "en": "Thunder"},
        {"kn": "ಮಗು", "en": "Child"},
        {"kn": "ಶಾಲೆ", "en": "School"},
        {"kn": "ಅಜ್ಜ", "en": "Grandfather"},
        # Fixed words with proper translations
        {"kn": "ಜಗತ್ತು", "en": "world"},
        {"kn": "ಮಾತು", "en": "word"},
        {"kn": "ಸಮಯ", "en": "time"},
        {"kn": "ಜೀವನ", "en": "life"},
        {"kn": "ಪ್ರಪಂಚ", "en": "world"},
        {"kn": "ಮಾನವ", "en": "human"},
        {"kn": "ಸಮಾಜ", "en": "society"},
        {"kn": "ಸಂಸ್ಕೃತಿ", "en": "culture"},
        {"kn": "ಭಾಷೆ", "en": "language"},
        {"kn": "ಸಾಹಿತ್ಯ", "en": "literature"},
        {"kn": "ಕಲೆ", "en": "art"},
        {"kn": "ವಿಜ್ಞಾನ", "en": "science"},
        {"kn": "ತಂತ್ರಜ್ಞಾನ", "en": "technology"},
        {"kn": "ಪ್ರಕೃತಿ", "en": "nature"},
        {"kn": "ಪರಿಸರ", "en": "environment"},
        {"kn": "ಆರೋಗ್ಯ", "en": "health"},
        {"kn": "ವೈದ್ಯ", "en": "doctor"},
        {"kn": "ಔಷಧ", "en": "medicine"},
        {"kn": "ಆಸ್ಪತ್ರೆ", "en": "hospital"},
        {"kn": "ವಿದ್ಯಾರ್ಥಿ", "en": "student"},
        {"kn": "ಪ್ರಾಧ್ಯಾಪಕ", "en": "professor"},
        {"kn": "ಪರೀಕ್ಷೆ", "en": "exam"},
        {"kn": "ಪ್ರಶ್ನೆ", "en": "question"},
        {"kn": "ಉತ್ತರ", "en": "answer"},
        {"kn": "ಸಮಸ್ಯೆ", "en": "problem"},
        {"kn": "ಪರಿಹಾರ", "en": "solution"},
        {"kn": "ಸಹಾಯ", "en": "help"},
        {"kn": "ಸೇವೆ", "en": "service"},
        {"kn": "ಕೆಲಸ", "en": "work"},
        {"kn": "ವ್ಯಾಪಾರ", "en": "business"},
        {"kn": "ಕಾರ್ಖಾನೆ", "en": "factory"},
        {"kn": "ಯಂತ್ರ", "en": "machine"},
        {"kn": "ಗಣಕ", "en": "computer"},
        {"kn": "ಇಂಟರ್ನೆಟ್", "en": "internet"},
        {"kn": "ಮೊಬೈಲ್", "en": "mobile"},
        {"kn": "ಕಾರು", "en": "car"},
        {"kn": "ಬಸ್", "en": "bus"},
        {"kn": "ರೈಲು", "en": "train"},
        {"kn": "ವಿಮಾನ", "en": "airplane"},
        {"kn": "ರಸ್ತೆ", "en": "road"},
        {"kn": "ಸೇತುವೆ", "en": "bridge"},
        {"kn": "ಮಾರುಕಟ್ಟೆ", "en": "market"},
        {"kn": "ಅಂಗಡಿ", "en": "shop"},
        {"kn": "ಬೆಲೆ", "en": "price"},
        {"kn": "ಖರೀದಿ", "en": "purchase"},
        {"kn": "ಮಾರಾಟ", "en": "sale"},
        {"kn": "ಸರ್ಕಾರ", "en": "government"},
        {"kn": "ರಾಜ್ಯ", "en": "state"},
        {"kn": "ದೇಶ", "en": "country"},
        {"kn": "ಜನತೆ", "en": "people"},
        {"kn": "ಮತದಾನ", "en": "voting"},
        {"kn": "ಚುನಾವಣೆ", "en": "election"},
        {"kn": "ನ್ಯಾಯಾಲಯ", "en": "court"},
        {"kn": "ಕಾನೂನು", "en": "law"},
        {"kn": "ಪೊಲೀಸ್", "en": "police"},
        {"kn": "ಅಧಿಕಾರಿ", "en": "officer"},
        {"kn": "ಅಧ್ಯಕ್ಷ", "en": "president"},
        {"kn": "ಬ್ಯಾಂಕ್", "en": "bank"},
        {"kn": "ಹಣ", "en": "money"},
        {"kn": "ಆರ್ಥಿಕ", "en": "financial"},
        {"kn": "ಬಜೆಟ್", "en": "budget"},
        {"kn": "ಆದಾಯ", "en": "income"},
        {"kn": "ವೆಚ್ಚ", "en": "expense"},
        {"kn": "ಕೃಷಿ", "en": "agriculture"},
        {"kn": "ರೈತ", "en": "farmer"},
        {"kn": "ಬೆಳೆ", "en": "crop"},
        {"kn": "ಜಮೀನು", "en": "land"},
        {"kn": "ಪ್ರಾಣಿಪಾಲನೆ", "en": "animal husbandry"},
        {"kn": "ಹಬ್ಬ", "en": "festival"},
        {"kn": "ಉತ್ಸವ", "en": "celebration"},
        {"kn": "ಮಂಗಳ", "en": "auspicious"},
        {"kn": "ಶುಭ", "en": "auspicious"},
        {"kn": "ಸಂಭ್ರಮ", "en": "celebration"},
        {"kn": "ಆನಂದ", "en": "happiness"},
    ]

    dictionary = []

    for word_data in words_data:
        word = word_data["kn"]
        translation = word_data["en"]

        transliteration = improved_transliterate_kannada(word)
        segments = improved_get_kannada_segments(word)

        entry = {
            "kn": word,
            "tr": transliteration,
            "en": translation,
            "segments": segments,
        }

        dictionary.append(entry)
        print(f"Processed: {word} -> {transliteration} ({translation})")
        if segments:
            segments_str = " + ".join(
                [f"{seg['kn']}({seg['tr']})" for seg in segments]
            )
            print(f"   Segments: {segments_str}")

    return dictionary


def main():
    """Create the final comprehensive dictionary."""
    print("Creating comprehensive Kannada dictionary...")

    dictionary = create_comprehensive_dictionary()

    # Save the dictionary
    with open("data/final_dictionary.json", "w", encoding="utf-8") as f:
        json.dump(dictionary, f, ensure_ascii=False, indent=2)

    print(f"\nFinal dictionary saved with {len(dictionary)} entries")

    # Test the ಜಗತ್ತು word specifically
    test_word = next(
        (entry for entry in dictionary if entry["kn"] == "ಜಗತ್ತು"), None
    )
    if test_word:
        print(f"\nTest word ಜಗತ್ತು:")
        print(f"Transliteration: {test_word['tr']}")
        print(f"Translation: {test_word['en']}")
        print("Segments:")
        for segment in test_word["segments"]:
            print(f"  {segment['kn']} -> {segment['tr']}")


if __name__ == "__main__":
    main()
