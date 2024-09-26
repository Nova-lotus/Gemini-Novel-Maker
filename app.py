import streamlit as st
import os
import json
from dotenv import load_dotenv
import google.generativeai as genai
from context_manager import ContextManager
from chapter_generator import ChapterGenerator
import logging
import traceback
import sys
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s')

# Load environment variables from .env file
load_dotenv()

# Load or initialize the state
state_file = 'app_state.json'
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

def save_state(state):
    with open(state_file, 'w') as f:
        json.dump(state, f, indent=4)

def generate_chapter(chapter_number: int, plot: str, writing_style: str, instructions: Dict[str, Any], api_key: str, generation_model: str, check_model: str, output_path: str):
    try:
        # Initialize components
        logging.info("Initializing components...")
        context_manager = ContextManager()
        genai.configure(api_key=api_key)
        chapter_generator = ChapterGenerator(api_key, generation_model, check_model)

        # Add context from user inputs
        logging.info("Adding context from user inputs...")
        context_manager.add_plot_point(plot)
        context_manager.add_other_element(f"Writing style: {writing_style}")
        context_manager.add_other_element(f"Additional instructions: {instructions}")

        # Add characters to context
        for name, description in state['characters'].items():
            context_manager.add_character(name, description)

        # Generate the context
        logging.info("Generating context...")
        context = context_manager.get_context()

        # Generate the chapter
        logging.info("Generating the chapter...")
        chapter_path = os.path.join(output_path, f'Chapter {chapter_number}.docx')
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

        return chapter, chapter_path

    except Exception as e:
        logging.error(f"An error occurred in generate_chapter function: {str(e)}")
        logging.error(traceback.format_exc())
        raise

def main():
    st.title("Chapter Generator and Checker")

    # Character input
    st.subheader("Characters")
    character_name = st.text_input("Character Name", disabled=st.session_state.get('generating', False))
    character_description = st.text_area("Character Description", height=100, disabled=st.session_state.get('generating', False))
    if st.button("Add Character", disabled=st.session_state.get('generating', False)):
        state['characters'][character_name] = character_description
        save_state(state)

    # Display added characters with delete button
    if state['characters']:
        st.subheader("Added Characters")
        for name, description in list(state['characters'].items()):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"**{name}**: {description}")
            with col2:
                if st.button(f"Delete {name}", key=f"delete_{name}", disabled=st.session_state.get('generating', False)):
                    del state['characters'][name]
                    save_state(state)

    # User inputs
    chapter_number = st.number_input("Chapter Number", min_value=1, value=1, step=1, disabled=st.session_state.get('generating', False))
    plot = st.text_area("Plot", value=state['plot'], height=200, disabled=st.session_state.get('generating', False))
    writing_style = st.text_area("Writing Style", value=state['writing_style'], height=100, disabled=st.session_state.get('generating', False))
    instructions = st.text_area("Additional Instructions", value=state['instructions'], height=100, disabled=st.session_state.get('generating', False))
    style_guide = st.text_area("Style Guide", value=state['style_guide'], height=100, disabled=st.session_state.get('generating', False))
    api_key = st.text_input("API Key", value=state['api_key'], type="password", disabled=st.session_state.get('generating', False))
    generation_model = st.selectbox("Select Model for Chapter Generation", ["gemini-1.5-flash-002", "gemini-1.5-pro-002"], index=["gemini-1.5-flash-002", "gemini-1.5-pro-002"].index(state['generation_model']), disabled=st.session_state.get('generating', False))
    check_model = st.selectbox("Select Model for Checks", ["gemini-1.5-flash-002", "gemini-1.5-pro-002"], index=["gemini-1.5-flash-002", "gemini-1.5-pro-002"].index(state['check_model']), disabled=st.session_state.get('generating', False))

    # Output path input
    output_path = st.text_input("Output Path", value=state['output_path'], disabled=st.session_state.get('generating', False))
    if st.button("Set Output Path", disabled=st.session_state.get('generating', False)):
        if not os.path.exists(output_path):
            try:
                os.makedirs(output_path, exist_ok=True)
                st.success(f"Output path '{output_path}' created successfully.")
            except Exception as e:
                st.error(f"Failed to create output path: {str(e)}")
                return
        state['output_path'] = output_path
        save_state(state)

    if st.button("Generate Chapter", disabled=st.session_state.get('generating', False)):
        if not api_key:
            st.error("Please provide an API Key.")
            return

        st.session_state['generating'] = True

        try:
            with st.spinner('Generating chapter...'):
                chapter, chapter_path = generate_chapter(
                    chapter_number, 
                    plot, 
                    writing_style, 
                    {"general": instructions, "style_guide": style_guide}, 
                    api_key, 
                    generation_model,
                    check_model,
                    output_path
                )

            st.success(f"Chapter {chapter_number} generated successfully!")

            # Display the generated chapter
            st.subheader(f"Generated Chapter {chapter_number}")
            st.write(chapter)

            # Save the state after successful generation
            state['plot'] = plot
            state['writing_style'] = writing_style
            state['instructions'] = instructions
            state['style_guide'] = style_guide
            state['api_key'] = api_key
            state['generation_model'] = generation_model
            state['check_model'] = check_model
            save_state(state)

        except Exception as e:
            # Get the full traceback
            exc_type, exc_value, exc_traceback = sys.exc_info()
            
            # Format the traceback
            tb_lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
            tb_text = ''.join(tb_lines)
            
            # Log the error with the full traceback
            logging.error(f"An error occurred: {str(e)}\n{tb_text}")
            
            # Display a more detailed error message to the user
            st.error(f"An error occurred: {str(e)}")
            st.error("Error details:")
            st.code(tb_text)  # This will display the traceback in a code block
            st.error("Please check the logs for more details and report this issue to the development team.")

        finally:
            st.session_state['generating'] = False

if __name__ == '__main__':
    main()
