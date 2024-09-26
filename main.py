# main.py
import os
from dotenv import load_dotenv
import google.generativeai as genai
from context_manager import ContextManager
from chapter_generator import ChapterGenerator
import logging
from typing import Dict, Any  # Add this import

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s')

# Load environment variables from .env file
load_dotenv()

def main(chapter_number: int, plot: str, writing_style: str, instructions: Dict[str, Any], api_key: str, model: str):
    try:
        # Initialize components
        logging.info("Initializing components...")
        context_manager = ContextManager()
        genai.configure(api_key=api_key)
        chapter_generator = ChapterGenerator(api_key, model, model)

        # Add context from user inputs
        logging.info("Adding context from user inputs...")
        context_manager.add_plot_point(plot)
        context_manager.add_other_element(f"Writing style: {writing_style}")
        context_manager.add_other_element(f"Additional instructions: {instructions}")

        # Generate the context
        logging.info("Generating context...")
        context = context_manager.get_context()

        # Generate the chapter
        logging.info("Generating the chapter...")
        chapter_path = f'output/Chapter {chapter_number}.docx'
        chapter = chapter_generator.generate_chapter(
            instructions={
                'plot': plot,
                'writing_style': writing_style,
                'instructions': instructions,
                'style_guide': instructions.get('style_guide', ''),
                'chapter_filename': chapter_path
            },
            context=context,
            chapter_path=chapter_path
        )

        print(f"Chapter {chapter_number} generated, checked, and saved successfully.")
    
    except Exception as e:
        logging.error(f"An error occurred in main function: {str(e)}")
        print(f"An error occurred: {str(e)}")
        raise  # Re-raise the exception to be caught by the outer try-except block

if __name__ == '__main__':
    # Example usage
    chapter_number = 1
    plot = "A brave knight sets out on a quest to save the kingdom."
    writing_style = "Epic and descriptive"
    instructions = {"general": "Ensure the chapter is engaging and maintains the epic tone."}
    api_key = os.getenv("API_KEY")
    model = "gemini-1.5-flash-002"

    main(chapter_number, plot, writing_style, instructions, api_key, model)