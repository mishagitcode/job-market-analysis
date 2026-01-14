import os
import subprocess


def save_to_pdf(input_filename: str, output_filename: str):
    current_file_path = os.path.abspath(__file__)

    project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_file_path)))

    notebook_path = os.path.join(project_root, "data_analysis_service", input_filename)
    output_dir = os.path.join(project_root, "data", "analyzed_data")

    if not os.path.exists(notebook_path):
        print(f"Error jupiter notebook is not found:\n{notebook_path}")
        return

    os.makedirs(output_dir, exist_ok=True)

    command = [
        "jupyter", "nbconvert",
        "--to", "webpdf",
        "--no-input",
        notebook_path,
        "--output-dir", output_dir,
        "--output", output_filename
    ]

    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error in nbconvert: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
