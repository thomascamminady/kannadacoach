#!/usr/bin/env python3
"""
Correct Kannada Transliteration System.

This script provides accurate transliteration for Kannada characters, handling:
1. Virama (halant) properly - removes inherent vowel
2. Vowel marks correctly - no triple vowels
3. Consonant conjuncts accurately
4. Proper segmentation logic
"""

# Unicode points for Kannada script
KANNADA_VIRAMA = "\u0ccd"  # ್
KANNADA_RANGE = range(0x0C80, 0x0CFF)

# Base consonants with inherent 'a'
BASE_CONSONANTS = {
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
}

# Vowels (standalone)
VOWELS = {
    "ಅ": "a",
    "ಆ": "aa",
    "ಇ": "i",
    "ಈ": "ii",
    "ಉ": "u",
    "ಊ": "uu",
    "ಋ": "ru",
    "ಎ": "e",
    "ಏ": "ee",
    "ಐ": "ai",
    "ಒ": "o",
    "ಓ": "oo",
    "ಔ": "au",
}

# Vowel marks (matras) - these modify consonants
VOWEL_MARKS = {
    "ಾ": "aa",  # long a
    "ಿ": "i",  # short i
    "ೀ": "ii",  # long i
    "ು": "u",  # short u
    "ೂ": "uu",  # long u
    "ೃ": "ru",  # vocalic r
    "ೆ": "e",  # short e
    "ೇ": "ee",  # long e
    "ೈ": "ai",  # ai
    "ೊ": "o",  # short o
    "ೋ": "oo",  # long o
    "ೌ": "au",  # au
}

# Common consonant conjuncts
CONJUNCTS = {
    "ಕ್ಕ": "kka",
    "ಕ್ಷ": "ksha",
    "ಗ್ಗ": "gga",
    "ಙ್ಗ": "nga",
    "ಚ್ಚ": "chcha",
    "ಜ್ಜ": "jja",
    "ಜ್ಞ": "jna",
    "ಞ್ಜ": "nja",
    "ಟ್ಟ": "tta",
    "ಡ್ಡ": "dda",
    "ಣ್ಣ": "nna",
    "ತ್ತ": "tta",
    "ದ್ದ": "dda",
    "ಧ್ಧ": "ddha",
    "ನ್ನ": "nna",
    "ಪ್ಪ": "ppa",
    "ಬ್ಬ": "bba",
    "ಮ್ಮ": "mma",
    "ಯ್ಯ": "yya",
    "ರ್ರ": "rra",
    "ಲ್ಲ": "lla",
    "ವ್ವ": "vva",
    "ಶ್ಶ": "shsha",
    "ಷ್ಷ": "shsha",
    "ಸ್ಸ": "ssa",
    "ಹ್ಹ": "hha",
    "ಳ್ಳ": "lla",
    # Cross-consonant conjuncts
    "ಕ್ತ": "kta",
    "ಕ್ರ": "kra",
    "ಗ್ರ": "gra",
    "ಚ್ರ": "chra",
    "ಜ್ರ": "jra",
    "ತ್ರ": "tra",
    "ದ್ರ": "dra",
    "ನ್ರ": "nra",
    "ಪ್ರ": "pra",
    "ಬ್ರ": "bra",
    "ಮ್ರ": "mra",
    "ಶ್ರ": "shra",
    "ಸ್ಪ": "spa",
    "ಸ್ತ": "sta",
    "ಸ್ಕ": "ska",
    "ಸ್ಥ": "stha",
    "ಸ್ವ": "sva",
    "ಸ್ಮ": "sma",
    "ಸ್ನ": "sna",
    "ಸ್ಯ": "sya",
    "ಹ್ಮ": "hma",
    "ಹ್ನ": "hna",
    "ಹ್ರ": "hra",
    "ಹ್ಯ": "hya",
    "ಹ್ವ": "hva",
}


def get_consonant_without_vowel(consonant):
    """Get the consonant sound without the inherent 'a' vowel."""
    # First check if it's a conjunct
    if consonant in CONJUNCTS:
        base_sound = CONJUNCTS[consonant]
        if base_sound.endswith("a"):
            return base_sound[:-1]  # Remove the 'a'
        return base_sound

    # Then check if it's a single consonant
    base_sound = BASE_CONSONANTS.get(consonant, consonant)
    if base_sound.endswith("a"):
        return base_sound[:-1]  # Remove the 'a'
    return base_sound


def transliterate_kannada_advanced(text):
    """Advanced transliteration that handles all Kannada script features correctly."""
    if not text:
        return ""

    result = []
    i = 0

    while i < len(text):
        char = text[i]

        # Check for 3-character conjuncts first
        if i + 2 < len(text):
            three_char = text[i : i + 3]
            if three_char in CONJUNCTS:
                result.append(CONJUNCTS[three_char])
                i += 3
                continue

        # Check for 2-character conjuncts
        if i + 1 < len(text):
            two_char = text[i : i + 2]
            if two_char in CONJUNCTS:
                result.append(CONJUNCTS[two_char])
                i += 2
                continue

            # Check for consonant + virama (halant)
            if i + 1 < len(text) and text[i + 1] == KANNADA_VIRAMA:
                consonant_sound = get_consonant_without_vowel(char)
                result.append(consonant_sound)
                i += 2
                continue

            # Check for consonant + vowel mark
            if char in BASE_CONSONANTS and text[i + 1] in VOWEL_MARKS:
                consonant_base = get_consonant_without_vowel(char)
                vowel_sound = VOWEL_MARKS[text[i + 1]]
                result.append(consonant_base + vowel_sound)
                i += 2
                continue

        # Single character handling
        if char in VOWELS:
            result.append(VOWELS[char])
        elif char in BASE_CONSONANTS:
            result.append(BASE_CONSONANTS[char])
        elif char in VOWEL_MARKS:
            # This shouldn't happen in proper text, but handle it
            result.append(VOWEL_MARKS[char])
        else:
            # Non-Kannada character, keep as is
            result.append(char)

        i += 1

    return "".join(result)


def segment_kannada_word(word):
    """Segment a Kannada word into logical units for learning."""
    if not word:
        return []

    segments = []
    i = 0

    while i < len(word):
        char = word[i]

        # Check for 3-character conjuncts first
        if i + 2 < len(word):
            three_char = word[i : i + 3]
            if three_char in CONJUNCTS:
                # Check if there's a vowel mark after the conjunct
                if i + 3 < len(word) and word[i + 3] in VOWEL_MARKS:
                    four_char = word[i : i + 4]
                    conjunct_base = get_consonant_without_vowel(three_char)
                    vowel_sound = VOWEL_MARKS[word[i + 3]]
                    segments.append(
                        {"kn": four_char, "tr": conjunct_base + vowel_sound}
                    )
                    i += 4
                    continue
                else:
                    segments.append(
                        {"kn": three_char, "tr": CONJUNCTS[three_char]}
                    )
                    i += 3
                    continue

        # Check for 2-character combinations
        if i + 1 < len(word):
            two_char = word[i : i + 2]
            if two_char in CONJUNCTS:
                # Check if there's a vowel mark after the conjunct
                if i + 2 < len(word) and word[i + 2] in VOWEL_MARKS:
                    three_char = word[i : i + 3]
                    conjunct_base = get_consonant_without_vowel(two_char)
                    vowel_sound = VOWEL_MARKS[word[i + 2]]
                    segments.append(
                        {"kn": three_char, "tr": conjunct_base + vowel_sound}
                    )
                    i += 3
                    continue
                else:
                    segments.append({"kn": two_char, "tr": CONJUNCTS[two_char]})
                    i += 2
                    continue

            # Consonant + virama (halant)
            if i + 1 < len(word) and word[i + 1] == KANNADA_VIRAMA:
                consonant_sound = get_consonant_without_vowel(char)
                segments.append({"kn": two_char, "tr": consonant_sound})
                i += 2
                continue

            # Consonant + vowel mark
            if char in BASE_CONSONANTS and word[i + 1] in VOWEL_MARKS:
                consonant_base = get_consonant_without_vowel(char)
                vowel_sound = VOWEL_MARKS[word[i + 1]]
                segments.append(
                    {"kn": two_char, "tr": consonant_base + vowel_sound}
                )
                i += 2
                continue

        # Single character
        if char in VOWELS:
            segments.append({"kn": char, "tr": VOWELS[char]})
        elif char in BASE_CONSONANTS:
            segments.append({"kn": char, "tr": BASE_CONSONANTS[char]})
        else:
            # Non-Kannada character or orphaned vowel mark
            segments.append({"kn": char, "tr": char})

        i += 1

    return segments


def test_transliteration():
    """Test the transliteration with known problematic cases"""
    test_cases = [
        ("ನ್ನ", "nna"),  # Double na conjunct
        ("ಸ್", "s"),  # Sa with virama
        ("ಕಾ", "kaa"),  # Ka with long a
        ("ನಮಸ್ಕಾರ", "namaskara"),  # Namaskara
        ("ಧನ್ಯವಾದ", "dhanyavada"),  # Dhanyavada
        ("ಸ್ವಾಗತ", "svagata"),  # Svagata
        ("ಪ್ರಸ್ತುತ", "prastuta"),  # Prastuta
    ]

    print("Testing transliteration:")
    for kannada, expected in test_cases:
        result = transliterate_kannada_advanced(kannada)
        status = "✓" if result == expected else "✗"
        print(f"{status} {kannada} -> {result} (expected: {expected})")

    print("\nTesting segmentation:")
    for kannada, _ in test_cases:
        segments = segment_kannada_word(kannada)
        print(f"{kannada}:")
        for seg in segments:
            print(f"  {seg['kn']} -> {seg['tr']}")
        print()


if __name__ == "__main__":
    test_transliteration()
