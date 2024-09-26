# Gemini Novel Maker

This project uses Google's Gemini API models to generate chapters for a novel.  It allows users to specify plot points, writing style, and other instructions to guide the AI's creative process.

## Features

* **Chapter Generation:**  Generates novel chapters based on user-provided instructions.
* **Contextual Awareness:** Leverages previous chapters to maintain story continuity.
* **Validity Checking:** Uses a separate Gemini model to assess the quality and coherence of generated chapters.
* **Automated Testing:**   Automated tests will be implemented to ensure chapters meet specific criteria.
* **Style Guide Enforcement:** The system will be enhanced to enforce a specified style guide.
* **Output in DOCX:** Chapters are saved as DOCX files for easy readability and editing.

# Installation
1. **Prerequisites:**
   - Python 3.9 or higher
   - Gemini API
   - Install required packages: `pip install -r requirements.txt`

2. **Clone the Repository**:
   ```sh
   git clone https://github.com/yourusername/gemini-novel-maker.git
   cd gemini-novel-maker
   ```

3. **Install Dependencies**:
   ```sh
   pip install -r requirements.txt
   ```

## Usage
Before you use the application be sure to put any previous chapters you had in the output folder
1. **Run the Application**:
   ```sh
   streamlit run app.py
   ```

2. **Add Characters**:
   - Navigate to the "Characters" section.
   - Enter the character name and description.
   - Click "Add Character" to add the character to the story.

3. **Set Plot, Writing Style, and Instructions**:
   - Input the plot, writing style, and any additional instructions in the respective text areas.

4. **Set Output Path**:
   - Enter the desired output path for the generated chapters.
   - Click "Set Output Path" to create the directory if it doesn't exist.

5. **Generate Chapter**:
   - Enter the chapter number.
   - Click "Generate Chapter" to start the generation process.
   - The application will generate the chapter and save it to the specified output path.

6. **View Generated Chapter**:
   - The generated chapter will be displayed in the application.
   - The chapter will also be saved as a `.docx` file in the specified output path.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0).  
