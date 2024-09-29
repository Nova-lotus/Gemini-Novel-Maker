# Gemini Novel Maker

This project uses Google's Gemini API models to generate chapters for a novel. It allows users to specify plot points, writing style, and other instructions to guide the AI's creative process.

## Features

- **Chapter Generation:** Generates novel chapters based on user-provided instructions.
- **Contextual Awareness:** Leverages previous chapters to maintain story continuity.
- **Validity Checking:** Uses a separate Gemini model to assess the quality and coherence of generated chapters.
- **Automated Testing:** Automated tests ensure chapters meet specific criteria.
- **Style Guide Enforcement:** The system enforces a specified style guide.
- **Output in DOCX:** Chapters are saved as DOCX files for easy readability and editing.
- **Minimum Word Count:** Users can specify a minimum word count for each chapter to ensure the generated content meets their length requirements.

## Installation

### Prerequisites
- Python 3.9 or higher
- Gemini API
- Install required packages: `pip install -r requirements.txt`

### Clone the Repository
