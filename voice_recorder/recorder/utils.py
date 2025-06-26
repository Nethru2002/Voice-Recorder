import os

def validate_output_dir(directory):
    """Ensure the output directory exists."""
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"📁 Created directory: {directory}")
    elif not os.path.isdir(directory):
        raise NotADirectoryError(f"❌ Path exists but is not a directory: {directory}")