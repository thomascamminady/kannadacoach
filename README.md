# Learn Kannada

A web4. After completing a word, the English meaning is displayed 5. Click the **Help** button for detailed instructions 6. Click the **ABC** button to view the Kannada alphabet reference 7. Visit the **GitHub** link to access the source codeased Kannada transliteration learning app that helps users practice typing Kannada words using English characters.

## 🌟 Features

-   **Interactive Learning**: Type English transliterations of Kannada words
-   **Visual Feedback**: Color-coded progress indicators (green for correct, red for errors)
-   **Smart Hints**: After 4 incorrect attempts, the correct answer is shown
-   **English Meanings**: Display word meanings upon successful completion
-   **Responsive Design**: Works seamlessly on desktop and mobile devices
-   **Large Dictionary**: 100+ common Kannada words with accurate transliterations
-   **Proper Segmentation**: Correctly handles compound consonants (e.g., ಜಗತ್ತು → ja-ga-tatau)
-   **Alphabet Reference**: Built-in Kannada alphabet guide with transliterations
-   **Help System**: Comprehensive usage instructions and tips

## 🎯 How to Use

1. Look at the Kannada word displayed
2. Type the English transliteration in the input box
3. Press **spacebar** to move to the next character
4. Correct characters turn green, incorrect input flashes red
5. After completing a word, the English meaning is displayed
6. Click the **help icon** (?) for detailed instructions

## 📁 Project Structure

```
kannadacoach/
├── index.html              # Main HTML file (GitHub Pages entry point)
├── assets/
│   ├── css/
│   │   └── style.css       # Styling and responsive design
│   └── js/
│       └── script.js       # Application logic and interactions
├── data/
│   ├── dictionary.json     # Small curated word list
│   ├── expanded_dictionary.json  # Extended word list (legacy)
│   └── comprehensive_dictionary.json  # Main dictionary with proper segmentation
├── scripts/
│   ├── extract_words.py    # Python script to scrape Kannada words
│   ├── create_comprehensive_dictionary.py  # Script to create proper dictionary
│   └── requirements.txt    # Python dependencies
└── README.md              # This file
```

## 🚀 Development

### Running Locally

Simply open `index.html` in your web browser, or serve it using a local web server:

```bash
# Using Python 3
python -m http.server 8000

# Using Node.js (if you have npx)
npx http-server .

# Then visit http://localhost:8000
```

### Updating Dictionary

To add more words to the dictionary:

1. Install Python dependencies:

    ```bash
    cd scripts
    pip install -r requirements.txt
    ```

2. Run the word extraction script:

    ```bash
    python extract_words.py
    ```

3. The script will generate an updated `expanded_dictionary.json` file

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 🎨 Design

The app uses a **Solarized Light** color scheme with:

-   Warm, cream-colored background gradients
-   Subtle shadows and modern rounded corners
-   Smooth animations and transitions
-   Mobile-first responsive design
-   Accessible color contrasts

## 🌐 Live Demo

Visit the live app at: [GitHub Pages URL]

## 📧 Contact

Created by [Thomas Camminady](https://camminady.dev)

## 🤖 Development

This project was entirely created using **Claude Sonnet 4** in agent mode, showcasing the power of AI-assisted development for building complete, functional web applications. The AI handled:

-   Frontend development (HTML, CSS, JavaScript)
-   Responsive design and mobile optimization
-   Data extraction and processing (Python scripting)
-   Project structure and organization
-   Documentation and deployment preparation

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
