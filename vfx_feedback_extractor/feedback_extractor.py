import os
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
    matches = re.findall(pattern, note.replace(os.sep, '/'))

    # Regular expression pattern for non-alphanumeric characters in paths
    non_alphanumeric_pattern = r"[^a-zA-Z0-9:/\\.\\-_]"

    clean_paths = []
    for match in matches:
        paths = re.split(r",| and ", match)
        clean_paths.extend([re.sub(non_alphanumeric_pattern, '', path.rstrip(').')) for path in paths])

    return clean_paths

def extract_info_from_message(message: str, shot_pattern: str = '[A-Za-z0-9_]+_[A-Za-z0-9_]+_[A-Za-z0-9_]+') -> List[Dict[str, Union[str, int]]]:
    """Extracts shot information and attachments from the given message."""
    pattern = fr"\b\s*`?({shot_pattern})(_[^`]+)?_(v|version)(\d+)\s*`?\b"
    note_pattern = r":\s*(.*)|-->\s*(.*)|\n\s*(.*)"

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
            shot_name, service_name, version_prefix, version_name = match.groups()
            current_shot = {
                "shot_name": shot_name,
                "version": int(version_name),
                "version_name": f"{shot_name}{service_name}_{version_prefix}{version_name}" if service_name else f"{shot_name}_{version_prefix}{version_name}",
                "attachment": []
            }
            current_note = None  # Reset the current note

            # Check if the line contains a note after the shot
            note_matches = re.findall(note_pattern, line)
            if note_matches:
                current_note = max(note_matches[0], key=len).strip().lstrip('-').strip()
        else:
            # If the line does not contain a shot, it could be a note or an attachment path
            if any(path in line for path in all_paths):  # Check if the line is an attachment path
                pass
            elif not current_note:  # If there's no current note, it could be a note
                current_note = line.lstrip('-').strip()

        if current_shot:
            current_shot["attachment"] = [path for path in all_paths if current_shot['shot_name'].lower() in path.lower()]

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
        SHOT001_00_110_v1 - This is the first version of Shot 001.
        Attachments:
        - /path/to/attachment1.jpg
        - /path/to/attachment2.mov

        SHOT002_00_100_v2 - This version includes some minor changes.
        Attachments:
        - /path/to/attachment3.png
        - /path/to/attachment4.mp4
        """

    extracted_data = extract_info_from_message(message)
    pprint(extracted_data)
