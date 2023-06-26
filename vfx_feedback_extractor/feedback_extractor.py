import re

def extract_file_paths(note: str) -> list:
    """
    Extracts file paths from the given note.

    Args:
        note (str): The note containing file paths.

    Returns:
        list: A list of cleaned file paths.
    """
    pattern = r"[a-zA-Z]:[\\/][^:\n]*|\/[^:\n]*"
    matches = re.findall(pattern, note)
    non_common_pattern = r"[^a-zA-Z0-9/\\.\\-_]"
    clean_matches = [re.sub(non_common_pattern, '', match.rstrip(')')) for match in matches]
    return clean_matches

def extract_info_from_message(message: str) -> list:
    """
    Extracts information from the given message.

    Args:
        message (str): The message containing shot entries and attachments.

    Returns:
        list: A list of dictionaries containing extracted information for each shot.
    """
    data = []
    # Extract potential shot entries
    shot_entries = re.split(r"`([a-zA-Z0-9_-]*)`", message)[1:]

    # Get a list of all attachment paths
    all_attachments = extract_file_paths(message)

    for shot_name_version, note_attachment in zip(shot_entries[::2], shot_entries[1::2]):
        # The regular expression is updated to handle different version formats.
        search_result = re.search(r"([a-zA-Z0-9_-]*)(?:_v|v|VER|Version_|_)([0-9]+)", shot_name_version, re.IGNORECASE)
        if not search_result:
            continue
        shot_name, version_name = search_result.groups()
        shot_name = shot_name.rstrip('_')
        version_name = version_name.rstrip('_')

        note = re.search(r"\n- (.*?)\n", note_attachment)
        note = note.group(1).strip() if note else None

        # Match attachments to the shot by scanning all attachments
        attachments = [path for path in all_attachments if shot_name in path]

        data.append({
            "shot_name": shot_name,
            "version_name": "v" + version_name,
            "note": note,
            "attachment": attachments,
        })

    return data

if __name__ == "__main__":
    message = """
        Greetings,

        I have reviewed the shot named as 

        `SH020_080_222_v002`
        - It seems that it requires color correction.
        `SH010_040_111_v001`
        -  I noticed that it needs a bit more brightness. Can we fix this? 

        Annotation is attached at these locations 
        - /path/to/anno/SH020_080_222_v002_file.0010.png.
        - /path/to/anno/SH010_040_111_v001_file.0001.png and /path/to/anno/SH010_040_111_v001_file.0017.png.

        Thank you,
        Client
        """

    extracted_data = extract_info_from_message(message)
    print(extracted_data)
