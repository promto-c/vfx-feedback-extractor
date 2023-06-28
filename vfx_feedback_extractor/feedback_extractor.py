import re

from typing import Any, Dict, List, Union

def extract_file_paths(note: str) -> List[str]:
    """Extracts file paths from the given note.

    Args:
        note (str): The note containing file paths.

    Returns:
        List[str]: A list of cleaned file paths.

    >>> example_note = '''
    ...     Meeting minutes 06-26-2023
    ...     Participants: John, Lisa, Daniel
    ...     .
    ...     Action items:
    ...     - John: Update progress on project A 
    ...     (see file at: C:/Users/John/Documents/projectA_update.txt)
    ...     - Lisa: Review budget proposal and provide feedback
    ...     (proposal file: /home/lisa/documents/budget_proposal.pdf)
    ...     - Daniel: Organize project files 
    ...     (see folder at D:/Projects/project_B)
    ...     .
    ...     Miscellaneous notes:
    ...     There are some images to be reviewed at 
    ...     /home/daniel/images/review/
    ...     Reminder to look at the old project files at E:/Archives/OldProjects/
    ... '''
    >>> extract_file_paths(example_note)
    ['C:/Users/John/Documents/projectA_update.txt', '/home/lisa/documents/budget_proposal.pdf', 'D:/Projects/project_B', '/home/daniel/images/review/', 'E:/Archives/OldProjects/']
    """
    pattern = r"[a-zA-Z]:[\\/][^:\n]*|\/(?!\s)[^:\n]*"
    matches = re.findall(pattern, note)

    # Regular expression pattern for non-alphanumeric characters in paths
    non_alphanumeric_pattern = r"[^a-zA-Z0-9:/\\.\\-_]"

    clean_paths = []
    for match in matches:
        paths = re.split(r",| and ", match)
        clean_paths.extend([re.sub(non_alphanumeric_pattern, '', path.rstrip(').')) for path in paths])

    return clean_paths

def extract_info_from_message(message: str) -> List[Dict[str, Union[str, int]]]:
    """Extracts shot information and attachments from the given message."""
    pattern = r"\b\s*`?([A-Z0-9_]+_[A-Z0-9_]+_[A-Z0-9_]+)(_[^`]+)?_v(\d+)\s*`?\b"
    note_patterns = [r":\s*(.*)", r"-->\s*(.*)", r"\n\s*(.*)"]

    # Find all file paths in the message
    all_paths = extract_file_paths(message)

    info_list = []
    current_shot = None
    current_note = None

    # Process each line individually
    for line in message.split('\n'):
        line = line.strip()  # Remove leading/trailing white spaces

        # If the line is empty, ignore it
        if not line:
            continue

        # Check if the line contains a shot
        match = re.search(pattern, line)
        if match:
            # If there's a current shot and it has a note, add it to the list
            if current_shot and current_note:
                current_shot['note'] = current_note
                info_list.append(current_shot)

            # Create a new shot
            shot_name, service_name, version_name = match.groups()
            current_shot = {
                "shot_name": shot_name,
                "version": int(version_name),
                "version_name": f"{shot_name}{service_name}_v{version_name}" if service_name else f"{shot_name}_v{version_name}",
                "attachment": []
            }
            current_note = None  # Reset the current note

            # Check if the line contains a note after the shot
            for note_pattern in note_patterns:
                note_match = re.search(note_pattern, line)
                if note_match:
                    current_note = note_match.group(1).strip()
        else:
            # If the line does not contain a shot, it could be a note or an attachment path
            if any(path in line for path in all_paths):  # Check if the line is an attachment path
                pass
            elif not current_note:  # If there's no current note, it could be a note
                current_note = line

        if current_shot:
            current_shot["attachment"] = [path for path in all_paths if current_shot['shot_name'] in path]

    # Add the last shot to the list, if it exists
    if current_shot and current_note:
        current_shot['note'] = current_note
        info_list.append(current_shot)

    return info_list

if __name__ == "__main__":
    from pprint import pprint
    import doctest
    doctest.testmod()

    message = """
        Greetings,

        I have reviewed the shot named as 

        SH020_080_222_v002
        - It seems that it requires color correction.
        SH010_040_111_v001
        -  I noticed that it needs a bit more brightness. Can we fix this? 

        Annotation is attached at these locations 
        - /path/to/anno/SH020_080_222_v002_file.0010.png.
        - /path/to/anno/SH010_040_111_v001_file.0001.png and /path/to/anno/SH010_040_111_v001_file.0017.png.

        Thank you,
        Client
        """

    extracted_data = extract_info_from_message(message)
    pprint(extracted_data)
