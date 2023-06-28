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

def extract_info_from_message(message: str) -> List[Dict[str, str]]:
    """Extracts shot information and attachments from the given message."""
    message = message.replace(' `', '`')
    
    # Updated pattern to include optional service_name and convert version to int
    pattern = r"\b`?([A-Z0-9_]+_[A-Z0-9_]+_[A-Z0-9_]+)(_[^`]+)?_v(\d+)`?\b"
    matches = re.findall(pattern, message)

    info_list = []
    current_shot = None
    current_attachment = []

    # Get a list of all attachment paths
    all_attachments = extract_file_paths(message)

    for match in matches:
        shot_name, service_name, version_name = match
        if current_shot is not None:
            info_list.append({
                "shot_name": current_shot,
                "version": int(current_version),
                "version_name": current_version_name,
                "note": current_note,
                "attachment": current_attachment
            })
            current_attachment = []

        current_shot = shot_name
        current_version = version_name
        # Construct version_name with or without service_name
        current_version_name = f"{shot_name}{service_name}_v{version_name}" if service_name else f"{shot_name}_v{version_name}"
        current_note = None

        # Find the note for the current shot
        note_pattern = r"`?{}`?[\s-]*(.*?)($|\n)".format(current_version_name)
        note_match = re.search(note_pattern, message, re.MULTILINE)
        if note_match:
            current_note = note_match.group(1).strip()

        # Match attachments to the shot by scanning all attachments
        current_attachment = [path for path in all_attachments if current_shot in path]

    if current_shot is not None:
        info_list.append({
            "shot_name": current_shot,
            "version": int(current_version),
            "version_name": current_version_name,
            "note": current_note,
            "attachment": current_attachment
        })

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
