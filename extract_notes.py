import json
import sys
import os

def parse_notebook(file_path):
    """Parses a single notebook and returns formatted string."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            nb = json.load(f)
    except Exception as e:
        return f"Error reading {file_path}: {e}"

    extracted_text = []
    extracted_text.append(f"\n{'='*40}")
    extracted_text.append(f"FILE: {os.path.basename(file_path)}")
    extracted_text.append(f"{'='*40}\n")
    
    for i, cell in enumerate(nb.get('cells', [])):
        content = "".join(cell.get('source', []))
        
        if not content.strip():
            continue

        if cell['cell_type'] == 'markdown':
            extracted_text.append(f"--- Note Segment {i+1} ---")
            extracted_text.append(content)
            extracted_text.append("") 
        
        elif cell['cell_type'] == 'code':
            extracted_text.append(f"--- Code Segment {i+1} ---")
            extracted_text.append("```python")
            extracted_text.append(content)
            extracted_text.append("```")
            extracted_text.append("")

    return "\n".join(extracted_text)

def process_path(input_path):
    """Decides if input is file or directory and processes accordingly."""
    if not os.path.exists(input_path):
        print(f"Error: Path not found at {input_path}")
        sys.exit(1)

    all_notes = []

    # Case 1: It's a directory (Batch Mode)
    if os.path.isdir(input_path):
        print(f"Scanning directory: {input_path}...", file=sys.stderr) # Log to stderr so it doesn't pollute output
        for root, dirs, files in os.walk(input_path):
            for file in files:
                if file.endswith(".ipynb"):
                    full_path = os.path.join(root, file)
                    all_notes.append(parse_notebook(full_path))
    
    # Case 2: It's a single file (Surgical Mode)
    elif os.path.isfile(input_path) and input_path.endswith(".ipynb"):
        all_notes.append(parse_notebook(input_path))
    
    else:
        print("Error: Input must be a .ipynb file or a directory containing them.")
        sys.exit(1)

    return "\n".join(all_notes)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract_notes.py <path_to_notebook_or_dir>")
        sys.exit(1)
        
    target_path = sys.argv[1]
    result = process_path(target_path)
    
    # Print purely the content to stdout
    try:
        print(result.encode('utf-8', errors='ignore').decode('utf-8')) # Handle encoding safely
    except UnicodeEncodeError:
        # Fallback for terminals with poor encoding support
        print(result.encode('ascii', errors='ignore').decode('ascii'))