let words = [];
let currentWord = {};
let currentCharIndex = 0;
let typedSegments = [];
let incorrectAttempts = 0;

// Load dictionary from JSON file
async function loadDictionary() {
    try {
        const response = await fetch("data/corrected_dictionary.json");
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
            // Correct input
            typedSegments[currentCharIndex] = currentSegment;
            moveToNextChar();
        } else {
            // Incorrect input
            incorrectAttempts++;

            if (incorrectAttempts >= 4) {
                // Show correct answer and move on
                showHint();
                typedSegments[currentCharIndex] = expectedSegment;
                setTimeout(() => {
                    moveToNextChar();
                }, 1200);
            } else {
                // Flash red and clear
                inputBox.style.borderColor = "#dc322f";
                inputBox.style.backgroundColor = "rgba(220, 50, 47, 0.1)";
                setTimeout(() => {
                    inputBox.style.borderColor = "";
                    inputBox.style.backgroundColor = "";
                    inputBox.value = "";
                }, 500);
            }
        }
    }
}

function updateKannadaDisplay() {
    let kannadaHTML = "";

    for (let i = 0; i < currentWord.segments.length; i++) {
        const segment = currentWord.segments[i];

        if (i < currentCharIndex) {
            // Character has been typed correctly
            kannadaHTML += `<div class='kannada-char-container'>
                <span class='kannada-typed-correct'>${segment.kn}</span>
                <span class='transliteration'>${
                    typedSegments[i] || segment.tr
                }</span>
            </div>`;
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

// Initialize app
loadDictionary();
