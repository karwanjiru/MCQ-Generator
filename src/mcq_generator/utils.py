import os
import PyPDF2
import json
import traceback

def read_file(file):
    if file.name.endswith(".pdf"):
        try:
            pdf_reader = PyPDF2.PdfFileReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return text
        
        except Exception as e:
            raise Exception(f"Error reading the PDF File {file.name}!! Please try again.")
        
    elif file.name.endswith(".txt"):
        try:
            return file.read().decode("utf-8", errors="replace")
        except Exception as e:
            raise Exception(f"Error reading the TXT File {file.name}!! Please try again.")
    
    else:
        raise Exception(
            f"Apologies, but currently only PDF and TXT file formats are supported for file {file.name}. Thank you!"
            )

def get_table_data(quiz_str):
    try:
        # convert quiz from str to dict
        quiz_dict = json.loads(quiz_str)
        quiz_table_data = []

        # Iterate over the quiz dict and extract required info
        for key, value in quiz_dict.items():
            mcq = value["mcq"]
            options = " || ".join(
                [
                    f"[option]-> {option_value}" for option, option_value in value["options"].items()
                ]
            )

            correct = value["correct"]
            quiz_table_data.append({"MCQ": mcq, "Choices": options, "Correct": correct})

        return quiz_table_data
    
    except json.JSONDecodeError as e:
        return False, "Invalid JSON string"
    except KeyError as e:
        return False, f"Invalid JSON structure, missing key {e}"
    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return False, "An error occurred while processing the quiz string"