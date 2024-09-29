import json
import os
from typing import Dict, Any, Tuple, List
from context_manager import ContextManager
from chapter_generator import ChapterGenerator
import logging
import tempfile

def load_state(state_file: str = 'app_state.json') -> Dict[str, Any]:
    """Loads state from a JSON file or initializes it if the file doesn't exist."""
    if os.path.exists(state_file):
        with open(state_file, 'r') as f:
            state = json.load(f)
    else:
        state = {
            'output_path': 'output',
            'characters': {},
            'plot': '',
            'writing_style': '',
            'instructions': '',
            'style_guide': '',
            'api_key': '',
            'generation_model': 'gemini-1.5-flash-002',
            'check_model': 'gemini-1.5-flash-002'
        }
    return state

def save_state(state: Dict[str, Any], state_file: str = 'app_state.json'):
    """Saves the current state to a JSON file."""
    with open(state_file, 'w') as f:
        json.dump(state, f, indent=4)

def estimate_token_count(text: str) -> int:
    """Estimates the number of tokens in a given text."""
    # Gemini models use about 4 characters per token
    return len(text) // 4

def get_embedding(text: str, api_key: str) -> List[float]:
    """Gets the embedding of a given text using the specified model."""
    import google.generativeai as genai
    genai.configure(api_key=api_key)
    result = genai.embed_content(
        model="models/text-embedding-004",
        content=text,
        task_type="retrieval_document",
        title="Chapter embedding"
    )
    return result['embedding']

class ChapterGeneratorLoop:

    def __init__(self, api_key: str, generation_model: str, check_model: str):
        self.api_key = api_key
        self.generation_model = generation_model
        self.check_model = check_model
        self.logger = logging.getLogger(__name__)

    def generate_chapter(self, chapter_number: int, plot: str, writing_style: str, instructions: Dict[str, Any], characters: Dict[str, Any], output_path: str) -> Tuple[str, str]:
        chapter_generator = ChapterGenerator(self.api_key, self.generation_model, self.check_model)
        context_manager = ContextManager()
        self.add_context(context_manager, plot, writing_style, instructions, characters)
        context = context_manager.get_context()
        chapter_path = os.path.join(output_path, f'Chapter {chapter_number}.docx')
        chapter = chapter_generator.generate_chapter(instructions, context, chapter_path, chapter_number)
        return chapter, chapter_path

    def add_context(self, context_manager: ContextManager, plot: str, writing_style: str, instructions: Dict[str, Any], characters: Dict[str, Any]):
        context_manager.add_plot_point(plot)
        context_manager.add_other_element(f"Writing style: {writing_style}")
        context_manager.add_other_element(f"Additional instructions: {instructions}")
        for name, description in characters.items():
            context_manager.add_character(name, description)
