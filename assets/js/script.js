// Configuration constants
const CONFIG = {
    MAX_INCORRECT_ATTEMPTS: 4,
    FLASH_DURATION: 200,
    HINT_DISPLAY_DURATION: 1200,
    MEANING_DISPLAY_DURATION: 1500,
    ERROR_FLASH_DURATION: 300,
};

// Global state variables
let words = [];
let currentWord = {};
let currentCharIndex = 0;
let typedSegments = [];
let skippedSegments = [];
let incorrectAttempts = 0;

// Cached DOM elements
const elements = {
    loadingIndicator: null,
    kannadaWord: null,
    meaningDisplay: null,
    hintDisplay: null,
    inputBox: null,
    helpModal: null,
    alphabetModal: null,
    themeIcon: null,
    themeText: null,
};

/**
 * Initialize cached DOM elements and set up event listeners
 * Called once when the app loads to cache frequently accessed DOM elements
 */
function initializeDOMElements() {
    elements.loadingIndicator = document.getElementById("loading-indicator");
    elements.kannadaWord = document.getElementById("kannada-word");
    elements.meaningDisplay = document.getElementById("meaning-display");
    elements.hintDisplay = document.getElementById("hint-display");
    elements.inputBox = document.getElementById("input-box");
    elements.helpModal = document.getElementById("help-modal");
    elements.alphabetModal = document.getElementById("alphabet-modal");
    elements.themeIcon = document.getElementById("theme-icon");
    elements.themeText = document.getElementById("theme-text");

    // Add event listeners after DOM elements are cached
    addEventListeners();
}

/**
 * Add event listeners for global keyboard shortcuts
 * Handles modal closing with Escape key
 */
function addEventListeners() {
    // Close modal on Escape key
    document.addEventListener("keydown", function (event) {
        if (event.key === "Escape") {
            if (elements.helpModal.classList.contains("show")) {
                event.preventDefault();
                hideHelp();
            } else if (elements.alphabetModal.classList.contains("show")) {
                event.preventDefault();
                hideAlphabet();
            }
        }
    });
}

/**
 * Load dictionary from JSON file with error handling and loading states
 * Shows loading indicator while fetching and handles success/error cases
 * @async
 */
async function loadDictionary() {
    try {
        // Show loading indicator
        elements.loadingIndicator.style.display = "flex";
        elements.loadingIndicator.classList.remove("hidden");

        const response = await fetch("data/dictionary.json");
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        words = await response.json();
        if (!words || words.length === 0) {
            throw new Error("Dictionary is empty or invalid");
        }

        // Hide loading indicator with a smooth transition
        elements.loadingIndicator.classList.add("hidden");
        setTimeout(() => {
            elements.loadingIndicator.style.display = "none";
        }, 300);

        loadNewWord();
    } catch (error) {
        console.error("Error loading dictionary:", error);

        // Hide loading indicator on error
        elements.loadingIndicator.classList.add("hidden");
        setTimeout(() => {
            elements.loadingIndicator.style.display = "none";
        }, 300);

        elements.kannadaWord.innerHTML =
            '<div style="color: var(--incorrect-color); text-align: center; padding: 20px;">Failed to load dictionary. Please refresh the page.</div>';
    }
}

/**
 * Get a random word from the dictionary
 * @returns {Object} Random word object with segments and English meaning
 */
function getRandomWord() {
    return words[Math.floor(Math.random() * words.length)];
}

/**
 * Load a new word and reset the game state
 * Resets all tracking variables and updates the display
 */
function loadNewWord() {
    if (words.length === 0) return;
    currentWord = getRandomWord();
    currentCharIndex = 0;
    typedSegments = [];
    skippedSegments = [];
    incorrectAttempts = 0;
    elements.inputBox.value = "";
    hideMeaning();
    hideHint();
    updateKannadaDisplay();
}

/**
 * Show the English meaning of the current word
 * Displays the meaning with visual feedback
 */
function showMeaning() {
    elements.meaningDisplay.textContent = currentWord.en;
    elements.meaningDisplay.classList.add("show", "completed");
}

/**
 * Hide the English meaning display
 * Removes the meaning text and visual styling
 */
function hideMeaning() {
    elements.meaningDisplay.classList.remove("show", "completed");
    elements.meaningDisplay.textContent = "";
}

/**
 * Show the transliteration hint for the current character
 * Displays the expected answer after incorrect attempts
 */
function showHint() {
    const expectedSegment = currentWord.segments[currentCharIndex].tr;
    elements.hintDisplay.textContent = `Answer: ${expectedSegment}`;
    elements.hintDisplay.classList.add("show");
}

/**
 * Hide the transliteration hint
 * Removes the hint text and visual styling
 */
function hideHint() {
    elements.hintDisplay.classList.remove("show");
    elements.hintDisplay.textContent = "";
}

/**
 * Move to the next character in the current word
 * Resets attempts, clears input, and checks for word completion
 */
function moveToNextChar() {
    incorrectAttempts = 0;
    currentCharIndex++;
    elements.inputBox.value = "";
    hideHint();
    updateKannadaDisplay();

    // Show meaning and auto-advance to next word if completed
    if (currentCharIndex >= currentWord.segments.length) {
        showMeaning();
        setTimeout(() => {
            loadNewWord();
        }, CONFIG.MEANING_DISPLAY_DURATION);
    }
}

/**
 * Handle keyboard input events
 * Processes space, enter, and escape key presses
 * @param {KeyboardEvent} event - The keyboard event object
 */
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

/**
 * Validate the current user input against the expected transliteration
 * Handles correct/incorrect attempts and provides feedback
 */
function validateCurrentInput() {
    const currentSegment = elements.inputBox.value.trim();

    // Validation checks
    if (!currentSegment) return; // Don't process empty input
    if (!currentWord || !currentWord.segments) return; // Safety check for word
    if (currentCharIndex >= currentWord.segments.length) return; // Bounds check

    const expectedSegment = currentWord.segments[currentCharIndex].tr;
    if (!expectedSegment) return; // Safety check for segment

    if (currentSegment === expectedSegment) {
        // Correct input - flash character green
        flashCurrentCharacter("correct");
        typedSegments[currentCharIndex] = currentSegment;
        setTimeout(() => {
            moveToNextChar();
        }, CONFIG.FLASH_DURATION);
    } else {
        // Incorrect input
        incorrectAttempts++;

        if (incorrectAttempts >= CONFIG.MAX_INCORRECT_ATTEMPTS) {
            // Show correct answer and move on
            showHint();
            skippedSegments[currentCharIndex] = true;
            setTimeout(() => {
                moveToNextChar();
            }, CONFIG.HINT_DISPLAY_DURATION);
        } else {
            // Flash character and input red, then clear
            flashCurrentCharacter("incorrect");
            elements.inputBox.classList.add("error");
            setTimeout(() => {
                elements.inputBox.classList.remove("error");
                elements.inputBox.value = "";
            }, CONFIG.ERROR_FLASH_DURATION);
        }
    }
}

/**
 * Update the Kannada word display with current progress
 * Shows typed, current, and pending characters with appropriate styling
 */
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

    elements.kannadaWord.innerHTML = kannadaHTML;
}

/**
 * Show the help modal with instructions
 * Displays the modal and prevents background scrolling
 */
function showHelp() {
    elements.helpModal.style.display = "flex";
    elements.helpModal.classList.add("show");
    // Prevent body scrolling when modal is open
    document.body.style.overflow = "hidden";
}

/**
 * Hide the help modal
 * Closes the modal and restores background scrolling
 */
function hideHelp() {
    elements.helpModal.style.display = "none";
    elements.helpModal.classList.remove("show");
    document.body.style.overflow = "auto";
}

/**
 * Show the Kannada alphabet reference modal
 * Displays the alphabet modal and prevents background scrolling
 */
function showAlphabet() {
    elements.alphabetModal.style.display = "flex";
    elements.alphabetModal.classList.add("show");
    // Prevent body scrolling when modal is open
    document.body.style.overflow = "hidden";
}

/**
 * Hide the alphabet reference modal
 * Closes the modal and restores background scrolling
 */
function hideAlphabet() {
    elements.alphabetModal.style.display = "none";
    elements.alphabetModal.classList.remove("show");
    document.body.style.overflow = "auto";
}

/**
 * Toggle between light and dark themes
 * Switches theme, saves preference, and updates the UI
 */
function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute("data-theme");
    const newTheme = currentTheme === "dark" ? "light" : "dark";

    document.documentElement.setAttribute("data-theme", newTheme);
    localStorage.setItem("theme", newTheme);

    updateThemeButton(newTheme);
}

/**
 * Update the theme toggle button appearance
 * Changes icon and text based on current theme
 * @param {string} theme - Current theme ("light" or "dark")
 */
function updateThemeButton(theme) {
    if (theme === "dark") {
        // In dark mode, show moon icon and "Light" text (what it will switch to)
        elements.themeIcon.innerHTML = `
            <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path>
        `;
        elements.themeText.textContent = "Light";
    } else {
        // In light mode, show sun icon and "Dark" text (what it will switch to)
        elements.themeIcon.innerHTML = `
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
        elements.themeText.textContent = "Dark";
    }
}

/**
 * Initialize theme on page load
 * Loads saved theme preference or detects system preference
 */
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
initializeDOMElements();
initializeTheme();
loadDictionary();

/**
 * Flash the current character with visual feedback
 * Adds temporary CSS class for correct/incorrect feedback
 * @param {string} type - Type of flash ("correct" or "incorrect")
 */
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
        }, CONFIG.FLASH_DURATION);
    }
}
