# ADAPTY
### Learn Your Way. Grow Every Day.

**Track:** Human Impact  
**Problem Statement:** HI-03 – Adaptive Learning for Students with Disabilities

## About the Project

ADAPTY is an inclusive learning platform developed to make education easier and more accessible for students with disabilities.

Every student has a different way of learning. Some students may need better text readability, some may prefer audio support, while others may benefit from simple explanations and step-by-step practice.

ADAPTY brings these learning options together in one platform, allowing students to learn at their own pace and use the support that suits their needs.

## Problem We Are Trying to Solve

Traditional learning methods do not always meet the needs of students with disabilities. Difficulty in reading, understanding complex content and accessing study materials can create barriers to learning.

ADAPTY aims to reduce these barriers by providing accessibility options, learning resources and practice activities in one place.

## Key Features

- **Accessibility Settings:** High contrast, adjustable font size and line spacing for comfortable reading.
- **Subject Library:** Learning materials for Mathematics, Science, English, Computer Fundamentals, Programming and General Knowledge.
- **PDF Learning:** Upload study material and extract text from PDF chapters.
- **Learning Support:** Relevant explanations and step-by-step help based on lesson content.
- **Practice Quiz:** Questions based on available lesson content.
- **Adaptive Learning:** An experimental Decision Tree model suggests a learning level based on quiz performance and other learning factors.
- **Progress Tracking:** Saves quiz results and learning activity using a local database.
- **Text-to-Speech:** Optional audio support for reading content.

## Technology Stack

- Python
- Streamlit
- Scikit-learn
- TF-IDF for text processing
- PyPDF for PDF text extraction
- SQLite for progress storage
- gTTS for text-to-speech support

## How to Run the Project

**1. Clone the repository**

```bash
git clone https://github.com/aarti1804-rs/ADAPTY.git
```

**2. Open the project folder**

**3. Install the required libraries**

```bash
pip install -r requirements.txt
```

**4. Run the application**

```bash
streamlit run app.py
```

The application will open in your browser at the local address displayed in the terminal.

## Project Impact

ADAPTY aims to make digital learning more accessible and comfortable for students with different learning needs. It gives students options to read, listen, practise and track their learning progress.

## Future Improvements

- Support for more Indian and regional languages.
- Improved personalised learning recommendations.
- Better quiz generation.
- Additional assistive technology features.
- More advanced AI-based learning support.

## Screenshots

Screenshots of the working application will be added here.

## Team Details

**Project:** ADAPTY  
**Team Member:** Aarti Sharma  
**Participation:** Individual Project

## AI Tool Disclosure

ChatGPT was used for guidance, coding assistance and debugging during the development of this project.

## Current Limitations

- Quiz generation uses text-based rules rather than a fully generative AI model.
- Adaptive recommendations are experimental and need further validation.
- PDF extraction works best with PDFs containing selectable text.
- More accessibility and language features can be added in future versions.
