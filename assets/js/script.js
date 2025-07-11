let words = [];
let currentWord = {};
let currentCharIndex = 0;
let typedSegments = [];
let skippedSegments = [];
let incorrectAttempts = 0;

// Load dictionary from JSON file
async function loadDictionary() {
    try {
        const response = await fetch("data/dictionary.json");
        words = await response.json();
        loadNewWord();
    } catch (error) {
        console.error("Error loading dictionary:", error);
    }
}

function getRandomWord() {
    return words[Math.floor(Math.random() * words.length)];
}

function loadNewWord() {
    if (words.length === 0) return;
    currentWord = getRandomWord();
    currentCharIndex = 0;
    typedSegments = [];
    skippedSegments = [];
    incorrectAttempts = 0;
    document.getElementById("input-box").value = "";
    hideMeaning();
    hideHint();
    updateKannadaDisplay();
}

function showMeaning() {
    const meaningElement = document.getElementById("meaning-display");
    meaningElement.textContent = currentWord.en;
    meaningElement.classList.add("show", "completed");
}

function hideMeaning() {
    const meaningElement = document.getElementById("meaning-display");
    meaningElement.classList.remove("show", "completed");
    meaningElement.textContent = "";
}

function showHint() {
    const hintElement = document.getElementById("hint-display");
    const expectedSegment = currentWord.segments[currentCharIndex].tr;
    hintElement.textContent = `Answer: ${expectedSegment}`;
    hintElement.classList.add("show");
}

function hideHint() {
    const hintElement = document.getElementById("hint-display");
    hintElement.classList.remove("show");
    hintElement.textContent = "";
}

function moveToNextChar() {
    incorrectAttempts = 0;
    currentCharIndex++;
    document.getElementById("input-box").value = "";
    hideHint();
    updateKannadaDisplay();

    // Show meaning and auto-advance to next word if completed
    if (currentCharIndex >= currentWord.segments.length) {
        showMeaning();
        setTimeout(() => {
            loadNewWord();
        }, 1500);
    }
}

function handleKey(event) {
    if (event.key === " ") {
        event.preventDefault();
        // Space only validates and moves to next character
        validateCurrentInput();
    } else if (event.key === "Enter") {
        event.preventDefault();
        validateCurrentInput();
    } else if (event.key === "Escape") {
        event.preventDefault();
        loadNewWord();
    }
}

function validateCurrentInput() {
    const inputBox = document.getElementById("input-box");
    const currentSegment = inputBox.value.trim();

    if (currentSegment && currentCharIndex < currentWord.segments.length) {
        const expectedSegment = currentWord.segments[currentCharIndex].tr;

        if (currentSegment === expectedSegment) {
            // Correct input - flash character green
            flashCurrentCharacter("correct");
            typedSegments[currentCharIndex] = currentSegment;
            setTimeout(() => {
                moveToNextChar();
            }, 200);
        } else {
            // Incorrect input
            incorrectAttempts++;

            if (incorrectAttempts >= 4) {
                // Show correct answer and move on
                showHint();
                skippedSegments[currentCharIndex] = true;
                setTimeout(() => {
                    moveToNextChar();
                }, 1200);
            } else {
                // Flash character and input red, then clear
                flashCurrentCharacter("incorrect");
                inputBox.classList.add("error");
                setTimeout(() => {
                    inputBox.classList.remove("error");
                    inputBox.value = "";
                }, 300);
            }
        }
    }
}

function updateKannadaDisplay() {
    let kannadaHTML = "";

    for (let i = 0; i < currentWord.segments.length; i++) {
        const segment = currentWord.segments[i];

        if (i < currentCharIndex) {
            if (skippedSegments[i]) {
                // Character was skipped after 4 wrong attempts
                kannadaHTML += `<div class='kannada-char-container'>
                    <span class='kannada-skipped-char'>${segment.kn}</span>
                    <span class='transliteration'>${segment.tr}</span>
                </div>`;
            } else {
                // Character has been typed correctly
                kannadaHTML += `<div class='kannada-char-container'>
                    <span class='kannada-typed-correct'>${segment.kn}</span>
                    <span class='transliteration'>${
                        typedSegments[i] || segment.tr
                    }</span>
                </div>`;
            }
        } else if (i === currentCharIndex) {
            // Current character position
            kannadaHTML += `<div class='kannada-char-container'>
                <span class='kannada-current-char'>${segment.kn}</span>
            </div>`;
        } else {
            // Not yet typed
            kannadaHTML += `<div class='kannada-char-container'>
                <span class='kannada-pending-char'>${segment.kn}</span>
            </div>`;
        }
    }

    document.getElementById("kannada-word").innerHTML = kannadaHTML;
}

// Help modal functions
function showHelp() {
    const modal = document.getElementById("help-modal");
    modal.style.display = "flex";
    modal.classList.add("show");
    // Prevent body scrolling when modal is open
    document.body.style.overflow = "hidden";
}

function hideHelp() {
    const modal = document.getElementById("help-modal");
    modal.style.display = "none";
    modal.classList.remove("show");
    document.body.style.overflow = "auto";
}

// Alphabet modal functions
function showAlphabet() {
    const modal = document.getElementById("alphabet-modal");
    modal.style.display = "flex";
    modal.classList.add("show");
    // Prevent body scrolling when modal is open
    document.body.style.overflow = "hidden";
}

function hideAlphabet() {
    const modal = document.getElementById("alphabet-modal");
    modal.style.display = "none";
    modal.classList.remove("show");
    document.body.style.overflow = "auto";
}

// Close modal on Escape key
document.addEventListener("keydown", function (event) {
    if (event.key === "Escape") {
        const helpModal = document.getElementById("help-modal");
        const alphabetModal = document.getElementById("alphabet-modal");

        if (helpModal.classList.contains("show")) {
            event.preventDefault();
            hideHelp();
        } else if (alphabetModal.classList.contains("show")) {
            event.preventDefault();
            hideAlphabet();
        }
    }
});

// Theme toggle functionality
function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute("data-theme");
    const newTheme = currentTheme === "dark" ? "light" : "dark";

    document.documentElement.setAttribute("data-theme", newTheme);
    localStorage.setItem("theme", newTheme);

    updateThemeButton(newTheme);
}

function updateThemeButton(theme) {
    const themeIcon = document.getElementById("theme-icon");
    const themeText = document.getElementById("theme-text");

    if (theme === "dark") {
        // In dark mode, show moon icon and "Light" text (what it will switch to)
        themeIcon.innerHTML = `
            <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
        `;
        themeText.textContent = "Light";
    } else {
        // In light mode, show sun icon and "Dark" text (what it will switch to)
        themeIcon.innerHTML = `
            <circle cx="12" cy="12" r="5"></circle>
            <line x1="12" y1="1" x2="12" y2="3"></line>
            <line x1="12" y1="21" x2="12" y2="23"></line>
            <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line>
            <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line>
            <line x1="1" y1="12" x2="3" y2="12"></line>
            <line x1="21" y1="12" x2="23" y2="12"></line>
            <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line>
            <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line>
        `;
        themeText.textContent = "Dark";
    }
}

// Initialize theme on page load
function initializeTheme() {
    const savedTheme = localStorage.getItem("theme");
    const prefersDark = window.matchMedia(
        "(prefers-color-scheme: dark)"
    ).matches;
    const theme = savedTheme || (prefersDark ? "dark" : "light");

    document.documentElement.setAttribute("data-theme", theme);
    updateThemeButton(theme);
}

// Initialize app
initializeTheme();
loadDictionary();
initializeTheme();

function flashCurrentCharacter(type) {
    const currentChar = document.querySelector(".kannada-current-char");
    if (currentChar) {
        const originalClass = currentChar.className;
        if (type === "correct") {
            currentChar.classList.add("flash-correct");
        } else {
            currentChar.classList.add("flash-incorrect");
        }
        setTimeout(() => {
            currentChar.className = originalClass;
        }, 200);
    }
}
