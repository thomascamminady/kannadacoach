#!/usr/bin/env python3
"""
Script to extract the most common Kannada words from Wiktionary and create a comprehensive dictionary
for the Kannada learning app.
"""

import json
import re
import time
from urllib.parse import quote, unquote

import requests
from bs4 import BeautifulSoup


# Configure transliteration (using the Kannada transliteration library)
def transliterate_kannada(text):
    """Convert Kannada text to romanized transliteration"""
    try:
        # Use a basic transliteration mapping for common Kannada characters
        mapping = {
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
            "ೱ": "fa",
            "ಃ": "h",
            "ಂ": "m",
            "ಁ": "n",
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
            "್": "",
            "಼": "",
            "।": ".",
            "॥": "..",
        }

        result = ""
        i = 0
        while i < len(text):
            # Check for compound characters first
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
    except Exception:
        return text


def get_kannada_segments(word):
    """Break down a Kannada word into individual segments for typing practice"""
    segments = []
    i = 0
    while i < len(word):
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
            "್",
            "಼",
        ]:
            # Include the vowel sign or virama with the consonant
            segments.append(word[i : i + 2])
            i += 2
        else:
            segments.append(word[i])
            i += 1
    return segments


def fetch_wiktionary_page(url):
    """Fetch a Wiktionary page with error handling"""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None


def extract_kannada_words_from_category(category_url, max_words=500):
    """Extract Kannada words from a Wiktionary category page"""
    words = []

    html = fetch_wiktionary_page(category_url)
    if not html:
        return words

    soup = BeautifulSoup(html, "html.parser")

    # Find all links to Kannada words
    mw_pages = soup.find("div", {"class": "mw-category-generated"})
    if mw_pages:
        links = mw_pages.find_all("a")
        for link in links:
            href = link.get("href", "")
            if href.startswith("/wiki/"):
                word_title = unquote(href.split("/")[-1])
                if is_kannada_word(word_title):
                    words.append(word_title)
                    if len(words) >= max_words:
                        break

    return words


def is_kannada_word(text):
    """Check if text contains Kannada characters"""
    kannada_range = range(0x0C80, 0x0CFF)  # Kannada Unicode range
    return any(ord(char) in kannada_range for char in text)


def get_word_definition(word):
    """Get the definition of a Kannada word from Wiktionary"""
    try:
        url = f"https://en.wiktionary.org/wiki/{quote(word)}"
        html = fetch_wiktionary_page(url)
        if not html:
            return None

        soup = BeautifulSoup(html, "html.parser")

        # Look for Kannada section
        kannada_section = None
        for h2 in soup.find_all("h2"):
            if "Kannada" in h2.get_text():
                kannada_section = h2
                break

        if not kannada_section:
            return None

        # Extract definition
        definition = ""
        current = kannada_section.find_next_sibling()
        while current and current.name != "h2":
            if current.name == "ol":
                # Extract first definition
                li = current.find("li")
                if li:
                    definition = li.get_text().strip()
                    break
            current = current.find_next_sibling()

        return definition if definition else None
    except Exception as e:
        print(f"Error getting definition for {word}: {e}")
        return None


def create_word_entry(word, definition=None):
    """Create a standardized word entry for the dictionary"""
    transliteration = transliterate_kannada(word)
    segments = get_kannada_segments(word)

    return {
        "kannada": word,
        "transliteration": transliteration,
        "english": definition or "Common word",
        "segments": segments,
    }


def extract_common_kannada_words():
    """Extract common Kannada words from multiple Wiktionary categories"""

    # Categories to extract from (ordered by importance)
    categories = [
        ("https://en.wiktionary.org/wiki/Category:Kannada_nouns", 400),
        ("https://en.wiktionary.org/wiki/Category:Kannada_verbs", 200),
        ("https://en.wiktionary.org/wiki/Category:Kannada_adjectives", 150),
        ("https://en.wiktionary.org/wiki/Category:Kannada_adverbs", 50),
        ("https://en.wiktionary.org/wiki/Category:Kannada_pronouns", 30),
        ("https://en.wiktionary.org/wiki/Category:Kannada_numerals", 30),
        ("https://en.wiktionary.org/wiki/Category:Kannada_conjunctions", 20),
        ("https://en.wiktionary.org/wiki/Category:Kannada_particles", 20),
        ("https://en.wiktionary.org/wiki/Category:Kannada_interjections", 20),
        ("https://en.wiktionary.org/wiki/Category:Kannada_determiners", 20),
        ("https://en.wiktionary.org/wiki/Category:Kannada_prepositions", 10),
        ("https://en.wiktionary.org/wiki/Category:Kannada_postpositions", 10),
    ]

    all_words = []
    word_set = set()  # To avoid duplicates

    print("Extracting Kannada words from Wiktionary...")

    for category_url, max_count in categories:
        print(f"Extracting from {category_url.split('/')[-1]}...")
        words = extract_kannada_words_from_category(category_url, max_count)

        for word in words:
            if word not in word_set and len(word) > 0:
                word_set.add(word)
                all_words.append(word)

        print(f"  Found {len(words)} words")
        time.sleep(1)  # Be respectful to the server

    print(f"\nTotal unique words extracted: {len(all_words)}")

    # Create word entries
    dictionary_entries = []
    print("\nCreating dictionary entries...")

    for i, word in enumerate(all_words):
        if i % 50 == 0:
            print(f"  Processing word {i + 1}/{len(all_words)}: {word}")

        # Get definition for first 100 words to save time
        definition = None
        if i < 100:
            definition = get_word_definition(word)
            if definition:
                # Clean up the definition
                definition = re.sub(
                    r"\[.*?\]", "", definition
                )  # Remove references
                definition = re.sub(r"\s+", " ", definition).strip()
                definition = definition[:100]  # Limit length
            time.sleep(0.5)  # Be respectful to the server

        entry = create_word_entry(word, definition)
        dictionary_entries.append(entry)

    return dictionary_entries


def save_dictionary(dictionary_entries, filename="expanded_dictionary.json"):
    """Save the dictionary to a JSON file"""
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(dictionary_entries, f, ensure_ascii=False, indent=2)
        print(f"\nDictionary saved to {filename}")
        print(f"Total entries: {len(dictionary_entries)}")
    except Exception as e:
        print(f"Error saving dictionary: {e}")


def main():
    """Main function to extract and save Kannada words"""
    print("Starting Kannada word extraction from Wiktionary...")

    # Extract words
    dictionary_entries = extract_common_kannada_words()

    # Save to file
    save_dictionary(dictionary_entries)

    # Display some sample entries
    print("\nSample dictionary entries:")
    for i, entry in enumerate(dictionary_entries[:5]):
        print(
            f"{i + 1}. {entry['kannada']} ({entry['transliteration']}) - {entry['english']}"
        )

    print(f"\nExtraction complete! Found {len(dictionary_entries)} words.")


if __name__ == "__main__":
    main()
