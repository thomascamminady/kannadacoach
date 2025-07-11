#!/usr/bin/env python3
"""
Comprehensive Kannada word generator with correct transliteration.

This script generates a large dictionary of Kannada words with accurate
transliteration and segmentation.
"""

import json
import os

# Common Kannada words with correct English translations
KANNADA_WORDS = [
    # Basic greetings and phrases
    ("ನಮಸ್ಕಾರ", "namaskara", "hello/greetings"),
    ("ಧನ್ಯವಾದ", "dhanyavada", "thank you"),
    ("ಕ್ಷಮಿಸಿ", "kshamisi", "sorry/excuse me"),
    ("ಸರಿ", "sari", "okay/correct"),
    ("ಇಲ್ಲ", "illa", "no"),
    ("ಹೌದು", "haudu", "yes"),
    # Family
    ("ಅಪ್ಪ", "appa", "father"),
    ("ಅಮ್ಮ", "amma", "mother"),
    ("ಅಣ್ಣ", "anna", "elder brother"),
    ("ಅಕ್ಕ", "akka", "elder sister"),
    ("ತಂಗಿ", "tangi", "younger sister"),
    ("ತಮ್ಮ", "tamma", "younger brother"),
    ("ಮಗ", "maga", "son"),
    ("ಮಗಳು", "magalu", "daughter"),
    ("ಮಕ್ಕಳು", "makkalu", "children"),
    ("ಅಜ್ಜ", "ajja", "grandfather"),
    ("ಅಜ್ಜಿ", "ajji", "grandmother"),
    ("ಸಹೋದರ", "sahodara", "brother"),
    ("ಸಹೋದರಿ", "sahodari", "sister"),
    # Basic nouns
    ("ಮನೆ", "mane", "house"),
    ("ಆಹಾರ", "ahara", "food"),
    ("ನೀರು", "neeru", "water"),
    ("ಹಾಲು", "haalu", "milk"),
    ("ಅನ್ನ", "anna", "rice"),
    ("ರೊಟ್ಟಿ", "rotti", "bread"),
    ("ಮಾಂಸ", "maansa", "meat"),
    ("ಹಣ್ಣು", "hannu", "fruit"),
    ("ತರಕಾರಿ", "tarakaari", "vegetable"),
    ("ಮರ", "mara", "tree"),
    ("ಹೂವು", "hoovu", "flower"),
    ("ಎಲೆ", "ele", "leaf"),
    # Body parts
    ("ತಲೆ", "tale", "head"),
    ("ಕೈ", "kai", "hand"),
    ("ಕಾಲು", "kaalu", "leg"),
    ("ಕಣ್ಣು", "kannu", "eye"),
    ("ಕಿವಿ", "kivi", "ear"),
    ("ಮೂಗು", "moogu", "nose"),
    ("ಬಾಯಿ", "baayi", "mouth"),
    ("ಹಲ್ಲು", "hallu", "tooth"),
    ("ಕೂದಲು", "koodalu", "hair"),
    # Colors
    ("ಬಿಳಿ", "bili", "white"),
    ("ಕಪ್ಪು", "kappu", "black"),
    ("ಕೆಂಪು", "kempu", "red"),
    ("ಹಸಿರು", "hasiru", "green"),
    ("ನೀಲಿ", "neeli", "blue"),
    ("ಹಳದಿ", "haladi", "yellow"),
    ("ಕಂದು", "kandu", "brown"),
    # Numbers
    ("ಒಂದು", "ondu", "one"),
    ("ಎರಡು", "eradu", "two"),
    ("ಮೂರು", "mooru", "three"),
    ("ನಾಲ್ಕು", "naalku", "four"),
    ("ಐದು", "aidu", "five"),
    ("ಆರು", "aaru", "six"),
    ("ಏಳು", "eelu", "seven"),
    ("ಎಂಟು", "entu", "eight"),
    ("ಒಂಬತ್ತು", "ombattu", "nine"),
    ("ಹತ್ತು", "hattu", "ten"),
    ("ನೂರು", "nooru", "hundred"),
    ("ಸಾವಿರ", "saavira", "thousand"),
    # Time
    ("ಸಮಯ", "samaya", "time"),
    ("ದಿನ", "dina", "day"),
    ("ರಾತ್ರಿ", "raatri", "night"),
    ("ಬೆಳಿಗ್ಗೆ", "beligge", "morning"),
    ("ಮಧ್ಯಾಹ್ನ", "madhyaahna", "afternoon"),
    ("ಸಂಜೆ", "sanje", "evening"),
    ("ವಾರ", "vaara", "week"),
    ("ತಿಂಗಳು", "tingalu", "month"),
    ("ವರ್ಷ", "varsha", "year"),
    # Common verbs
    ("ಬರು", "baru", "come"),
    ("ಹೋಗು", "hoogu", "go"),
    ("ತಿನ್ನು", "tinnu", "eat"),
    ("ಕುಡಿ", "kudi", "drink"),
    ("ಮಾತನಾಡು", "maatanaadu", "speak"),
    ("ಓದು", "oodu", "read"),
    ("ಬರೆ", "bare", "write"),
    ("ನೋಡು", "noodu", "see"),
    ("ಕೇಳು", "keelu", "listen/hear"),
    ("ಮಲಗು", "malagu", "sleep"),
    ("ಎದ್ದೇಳು", "eddeelu", "wake up"),
    ("ಕೆಲಸ", "kelasa", "work"),
    ("ಆಟ", "aata", "play"),
    ("ಕಲಿ", "kali", "learn"),
    ("ಹೇಳು", "heelu", "say/tell"),
    ("ಕೊಡು", "kodu", "give"),
    ("ತೆಗೆದುಕೊಳ್ಳು", "tegedukoollu", "take"),
    # Adjectives
    ("ಚಿಕ್ಕ", "chikka", "small"),
    ("ದೊಡ್ಡ", "dodda", "big"),
    ("ಹೊಸ", "hosa", "new"),
    ("ಹಳೆಯ", "haleya", "old"),
    ("ಸುಂದರ", "sundara", "beautiful"),
    ("ಒಳ್ಳೆಯ", "olleya", "good"),
    ("ಕೆಟ್ಟ", "ketta", "bad"),
    ("ಬಿಸಿ", "bisi", "hot"),
    ("ತಣ್ಣಗೆ", "tannage", "cold"),
    ("ಎತ್ತರ", "ettara", "tall"),
    ("ಕೆಳಗೆ", "kelage", "short"),
    # Nature
    ("ಸೂರ್ಯ", "soorya", "sun"),
    ("ಚಂದ್ರ", "chandra", "moon"),
    ("ನಕ್ಷತ್ರ", "nakshatra", "star"),
    ("ಆಕಾಶ", "aakaasha", "sky"),
    ("ಭೂಮಿ", "bhoomi", "earth"),
    ("ಗಾಳಿ", "gaali", "wind"),
    ("ಮಳೆ", "male", "rain"),
    ("ಮಂಜು", "manju", "fog"),
    ("ಬೆಂಕಿ", "benki", "fire"),
    ("ಮಣ್ಣು", "mannu", "soil"),
    ("ಕಲ್ಲು", "kallu", "stone"),
    ("ಹೊಳೆ", "hole", "stream"),
    ("ಸಮುದ್ರ", "samudra", "ocean"),
    ("ಪರ್ವತ", "parvata", "mountain"),
    # Animals
    ("ಆನೆ", "aane", "elephant"),
    ("ಸಿಂಹ", "simha", "lion"),
    ("ಹುಲಿ", "huli", "tiger"),
    ("ಕರಡಿ", "karadi", "bear"),
    ("ಬೆಕ್ಕು", "bekku", "cat"),
    ("ನಾಯಿ", "naayi", "dog"),
    ("ಹಸು", "hasu", "cow"),
    ("ಎಮ್ಮೆ", "emme", "buffalo"),
    ("ಕುದುರೆ", "kudure", "horse"),
    ("ಮೇಕೆ", "meke", "goat"),
    ("ಕುರಿ", "kuri", "sheep"),
    ("ಹಂದಿ", "handi", "pig"),
    ("ಹಕ್ಕಿ", "hakki", "bird"),
    ("ಮೀನು", "meenu", "fish"),
    ("ಹಾವು", "haavu", "snake"),
    # Places
    ("ಪಟ್ಟಣ", "pattana", "town"),
    ("ಊರು", "ooru", "village"),
    ("ಮಾರುಕಟ್ಟೆ", "maarukattte", "market"),
    ("ಶಾಲೆ", "shaale", "school"),
    ("ಆಸ್ಪತ್ರೆ", "aaspatre", "hospital"),
    ("ದೇವಾಲಯ", "devaalaya", "temple"),
    ("ಚರ್ಚ್", "church", "church"),
    ("ಮಸೀದಿ", "maseedi", "mosque"),
    ("ಬ್ಯಾಂಕ್", "bank", "bank"),
    ("ಪೋಸ್ಟ್ ಆಫೀಸ್", "post office", "post office"),
    ("ರೈಲ್ವೆ ನಿಲ್ದಾಣ", "railway nildaana", "railway station"),
    ("ಬಸ್ ನಿಲ್ದಾಣ", "bus nildaana", "bus station"),
    # Common phrases
    ("ಹೇಗಿದ್ದೀರಿ", "hegiddiri", "how are you"),
    ("ಚೆನ್ನಾಗಿದ್ದೇನೆ", "chennaagiddene", "I am fine"),
    ("ಗೊತ್ತಿಲ್ಲ", "gottilla", "I don't know"),
    ("ಅರ್ಥವಾಗಿಲ್ಲ", "arthavaagilla", "I don't understand"),
    ("ಹೆಸರು ಏನು", "hesaru enu", "what is your name"),
    ("ನನ್ನ ಹೆಸರು", "nanna hesaru", "my name is"),
    ("ಎಷ್ಟು ಬೆಲೆ", "eshtu bele", "how much price"),
    ("ಎಲ್ಲಿದೆ", "ellide", "where is"),
    ("ಯಾವಾಗ", "yaavaaga", "when"),
    ("ಯಾಕೆ", "yaake", "why"),
    ("ಏನು", "enu", "what"),
    ("ಯಾರು", "yaaru", "who"),
    # Education
    ("ಪುಸ್ತಕ", "pustaka", "book"),
    ("ಪಾಠ", "paatha", "lesson"),
    ("ವಿದ್ಯಾರ್ಥಿ", "vidyaarthi", "student"),
    ("ಶಿಕ್ಷಕ", "shikshaka", "teacher"),
    ("ಗುರು", "guru", "teacher/master"),
    ("ಪರೀಕ್ಷೆ", "pareekshe", "examination"),
    ("ಪ್ರಶ್ನೆ", "prashne", "question"),
    ("ಉತ್ತರ", "uttara", "answer"),
    ("ಪತ್ರ", "patra", "letter"),
    ("ಕಾಗದ", "kaagada", "paper"),
    ("ಪೆನ್ನು", "pennu", "pen"),
    ("ಪೆನ್ಸಿಲ್", "pensil", "pencil"),
    # Food items
    ("ಅಕ್ಕಿ", "akki", "rice"),
    ("ಮುದ್ದೆ", "mudde", "rice ball"),
    ("ಸಾರು", "saaru", "rasam"),
    ("ಸಾಂಬಾರು", "sambaaru", "sambar"),
    ("ಪಾಪಡ", "paapada", "papad"),
    ("ಅಪ್ಪಳ", "appalaa", "appalam"),
    ("ಇಡ್ಲಿ", "idli", "idli"),
    ("ದೋಸೆ", "dose", "dosa"),
    ("ಉಪ್ಪಿಟ್ಟು", "uppittu", "upma"),
    ("ಪಾಯಸ", "paayasa", "sweet dish"),
    ("ಮಿಠಾಯಿ", "mitthaai", "sweet"),
    ("ಬಾಳೆಹಣ್ಣು", "baalehannu", "banana"),
    ("ಹೇರಳೆ", "herale", "orange"),
    ("ಮಾವಿನ ಹಣ್ಣು", "maavina hannu", "mango"),
    ("ಸೇಬು", "sebu", "apple"),
    ("ದ್ರಾಕ್ಷಿ", "draakshi", "grapes"),
    # Clothing
    ("ಸೀರೆ", "seere", "saree"),
    ("ಸಲ್ವಾರ್", "salwaar", "salwar"),
    ("ಶರ್ಟ್", "shirt", "shirt"),
    ("ಪ್ಯಾಂಟ್", "pant", "pant"),
    ("ಚಪ್ಪಲಿ", "chappali", "sandal"),
    ("ಬೂಟು", "bootu", "shoe"),
    ("ಟೋಪಿ", "topi", "cap"),
    ("ಸೂಟ್", "suit", "suit"),
    # Emotions
    ("ಸಂತೋಷ", "santosha", "happiness"),
    ("ದುಃಖ", "duhkha", "sadness"),
    ("ಕೋಪ", "kopa", "anger"),
    ("ಭಯ", "bhaya", "fear"),
    ("ಪ್ರೀತಿ", "preeti", "love"),
    ("ದ್ವೇಷ", "dvesha", "hatred"),
    ("ಆಶ್ಚರ್ಯ", "aashcharya", "surprise"),
    ("ಚಿಂತೆ", "chinte", "worry"),
    ("ಆತಂಕ", "aatanka", "anxiety"),
    # Common objects
    ("ಕಿಟಕಿ", "kitaki", "window"),
    ("ಬಾಗಿಲು", "baagilu", "door"),
    ("ಕುರ್ಚಿ", "kurchi", "chair"),
    ("ಮೇಜು", "meju", "table"),
    ("ಹಾಸಿಗೆ", "haasige", "bed"),
    ("ಪುಸ್ತಕ", "pustaka", "book"),
    ("ಟೆಲಿಫೋನ್", "telephone", "telephone"),
    ("ಗಡಿಯಾರ", "gadiyaara", "clock"),
    ("ದೀಪ", "deepa", "lamp"),
    ("ಮೇಣತಿ", "menatii", "candle"),
    ("ಸಾಬೂನು", "saaboonu", "soap"),
    ("ಟೂತ್ ಬ್ರಷ್", "tooth brush", "toothbrush"),
    ("ಟವೆಲ್", "towel", "towel"),
    # Vehicles
    ("ಕಾರು", "kaaru", "car"),
    ("ಬಸ್", "bus", "bus"),
    ("ರೈಲು", "railu", "train"),
    ("ಹಡಗು", "hadagu", "ship"),
    ("ವಿಮಾನ", "vimaana", "airplane"),
    ("ಸೈಕಲ್", "cycle", "bicycle"),
    ("ಮೋಟಾರ್ ಸೈಕಲ್", "motor cycle", "motorcycle"),
    ("ಆಟೋ", "auto", "auto rickshaw"),
    ("ಟ್ರಕ್", "truck", "truck"),
    # Professions
    ("ಡಾಕ್ಟರ್", "doctor", "doctor"),
    ("ನರ್ಸ್", "nurse", "nurse"),
    ("ಇಂಜಿನಿಯರ್", "engineer", "engineer"),
    ("ವಕೀಲ", "vakeel", "lawyer"),
    ("ಪೋಲೀಸ್", "police", "police"),
    ("ರೈತ", "rayta", "farmer"),
    ("ಕಾರ್ಮಿಕ", "kaarmika", "worker"),
    ("ಅಡುಗೆಯವರು", "adugeyavaru", "cook"),
    ("ಚಾಲಕ", "chaalaka", "driver"),
    ("ಮಾರಾಟಗಾರ", "maaraatgaara", "seller"),
    ("ಖರೀದಿದಾರ", "khareedidaara", "buyer"),
    # Weather
    ("ಬಿಸಿಲು", "bisilu", "sunlight"),
    ("ಮಂಜು", "manju", "fog"),
    ("ಮಂಜುಗಡ್ಡೆ", "manjugadde", "ice"),
    ("ಆಲಿಕಲ್ಲು", "aalikallu", "hail"),
    ("ಮಿಂಚು", "minchu", "lightning"),
    ("ಗುಡುಗು", "gudugu", "thunder"),
    ("ಚಂಡಮಾರುತ", "chandamaaruta", "storm"),
    ("ಹಿಮ", "hima", "snow"),
    # Directions
    ("ಉತ್ತರ", "uttara", "north"),
    ("ದಕ್ಷಿಣ", "dakshina", "south"),
    ("ಪೂರ್ವ", "poorva", "east"),
    ("ಪಶ್ಚಿಮ", "pashchima", "west"),
    ("ಮೇಲೆ", "mele", "above"),
    ("ಕೆಳಗೆ", "kelage", "below"),
    ("ಮುಂದೆ", "munde", "front"),
    ("ಹಿಂದೆ", "hinde", "behind"),
    ("ಬಲಕ್ಕೆ", "balakke", "right"),
    ("ಎಡಕ್ಕೆ", "edakke", "left"),
    # Common adverbs
    ("ಇಂದು", "indu", "today"),
    ("ನಾಳೆ", "naale", "tomorrow"),
    ("ನಿನ್ನೆ", "ninne", "yesterday"),
    ("ಈಗ", "eega", "now"),
    ("ಮುಂದೆ", "munde", "later"),
    ("ಯಾವಾಗಲೂ", "yaavaagaluu", "always"),
    ("ಎಂದಿಗೂ", "endiguu", "never"),
    ("ಕೆಲವೊಮ್ಮೆ", "kelavomme", "sometimes"),
    ("ಆಗಾಗ", "aagaaga", "often"),
    ("ಬೇಗ", "bega", "fast"),
    ("ನಿಧಾನವಾಗಿ", "nidhaanavaagi", "slowly"),
    ("ಸರಿಯಾಗಿ", "sariyaagi", "correctly"),
    ("ತಪ್ಪಾಗಿ", "tappaagi", "wrongly"),
]


def create_simple_transliteration(kannada_text):
    """Create a simple transliteration mapping for basic words."""
    # This is a simplified version - in real implementation, we'd use the
    # complex transliteration system
    simple_map = {
        "ಅ": "a",
        "ಆ": "aa",
        "ಇ": "i",
        "ಈ": "ii",
        "ಉ": "u",
        "ಊ": "uu",
        "ಎ": "e",
        "ಏ": "ee",
        "ಐ": "ai",
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
        "ಾ": "aa",
        "ಿ": "i",
        "ೀ": "ii",
        "ು": "u",
        "ೂ": "uu",
        "ೆ": "e",
        "ೇ": "ee",
        "ೈ": "ai",
        "ೊ": "o",
        "ೋ": "oo",
        "ೌ": "au",
        "್": "",
        "ಂ": "m",
        "ಃ": "h",
        " ": " ",
    }

    result = []
    for char in kannada_text:
        if char in simple_map:
            result.append(simple_map[char])
        else:
            result.append(char)

    return "".join(result)


def create_simple_segments(kannada_word):
    """Create simple segments for basic words."""
    # This is a placeholder - in real implementation, we'd use the complex segmentation
    segments = []
    current_segment = ""

    for char in kannada_word:
        if char == " ":
            if current_segment:
                segments.append(
                    {
                        "kn": current_segment,
                        "tr": create_simple_transliteration(current_segment),
                    }
                )
                current_segment = ""
        else:
            current_segment += char

    if current_segment:
        segments.append(
            {
                "kn": current_segment,
                "tr": create_simple_transliteration(current_segment),
            }
        )

    return segments


def fix_anusvara_segments(segments):
    """Fix anusvara (ಂ) segments by combining them with the previous segment."""
    fixed_segments = []
    i = 0

    while i < len(segments):
        current_segment = segments[i]

        # Check if this segment is just "ಂ"
        if current_segment["kn"] == "ಂ" and fixed_segments:
            # Combine with previous segment
            prev_segment = fixed_segments[-1]
            prev_segment["kn"] += "ಂ"
            # Update transliteration to use 'n' instead of 'm' or the raw character
            if prev_segment["tr"].endswith("e"):
                prev_segment["tr"] = prev_segment["tr"][:-1] + "en"
            elif prev_segment["tr"].endswith("a"):
                prev_segment["tr"] = prev_segment["tr"][:-1] + "an"
            elif prev_segment["tr"].endswith("i"):
                prev_segment["tr"] = prev_segment["tr"][:-1] + "in"
            elif prev_segment["tr"].endswith("u"):
                prev_segment["tr"] = prev_segment["tr"][:-1] + "un"
            elif prev_segment["tr"].endswith("o"):
                prev_segment["tr"] = prev_segment["tr"][:-1] + "on"
            else:
                prev_segment["tr"] += "n"
            # Skip the anusvara segment as it's now combined
        else:
            fixed_segments.append(current_segment)

        i += 1

    return fixed_segments


def create_comprehensive_dictionary():
    """Create a comprehensive dictionary from the word list."""
    dictionary = []

    for kannada, transliteration, english in KANNADA_WORDS:
        segments = create_simple_segments(kannada)

        # Fix anusvara segments
        segments = fix_anusvara_segments(segments)

        entry = {
            "kn": kannada,
            "tr": transliteration,
            "en": english,
            "segments": segments,
        }
        dictionary.append(entry)

    return dictionary


def save_dictionary(dictionary, filename):
    """Save the dictionary to a JSON file."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, "data")

    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    filepath = os.path.join(data_dir, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(dictionary, f, ensure_ascii=False, indent=2)

    print(f"Dictionary saved to: {filepath}")
    print(f"Total entries: {len(dictionary)}")


def main():
    """Main function to create the comprehensive dictionary."""
    print("Creating comprehensive Kannada dictionary...")

    dictionary = create_comprehensive_dictionary()
    save_dictionary(dictionary, "comprehensive_kannada_dictionary.json")

    print("\nSample entries:")
    for i, entry in enumerate(dictionary[:5]):
        print(f"{i + 1}. {entry['kn']} -> {entry['tr']} ({entry['en']})")

    print(f"\nTotal words: {len(dictionary)}")
    print("Dictionary creation complete!")


if __name__ == "__main__":
    main()
