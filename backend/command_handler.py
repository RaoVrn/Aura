import re

# Function to extract details from a command
def handle_create_command(command):
    # Default location
    default_location = "Desktop"
    
    # Regular expressions for folder and file detection
    folder_pattern = r"(create|make|generate)\s+a\s+folder\s*(named|called)?\s*(\w+)?\s*(in|on)?\s*(\w+)?"
    file_pattern = r"(create|make|generate)\s+a\s*(file|text\s*file)\s*(named|called)?\s*(\w+)?\s*(on|in)?\s*(\w+)?"

    # Try to match the folder command
    folder_match = re.search(folder_pattern, command, re.IGNORECASE)
    if folder_match:
        folder_name = folder_match.group(3) if folder_match.group(3) else "New Folder"
        folder_location = folder_match.group(5) if folder_match.group(5) else default_location
        return { "type": "folder", "name": folder_name, "location": folder_location }

    # Try to match the file command
    file_match = re.search(file_pattern, command, re.IGNORECASE)
    if file_match:
        file_name = file_match.group(4) if file_match.group(4) else "NewFile"
        file_location = file_match.group(6) if file_match.group(6) else default_location
        # Ensure '.txt' is only appended once
        if not file_name.endswith('.txt'):
            file_name += ".txt"
        return { "type": "file", "name": file_name, "location": file_location }
    
    # If no match found, return a default response
    return { "type": "file", "name": "NewFile.txt", "location": default_location }
