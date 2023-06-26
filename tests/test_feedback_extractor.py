import sys
import os
import unittest

# Add the project's root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from vfx_feedback_extractor.feedback_extractor import extract_info_from_message


class TestFeedbackExtractor(unittest.TestCase):
    def test_extract_info_from_message(self):
        email_1 = """
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

        email_2 = """
        Greetings,

        I have reviewed the shot named as 

        `001c020_082_v002`
        - It seems that it requires color correction.
        `001c030_041_v001`
        -  I noticed that it needs a bit more brightness. Can we fix this? 

        Annotation is attached at these locations 
        - /path/to/anno/001c020_082_v002_file.0010.png.
        - /path/to/anno/001c030_041_v001_file.0001.png 
        - /path/to/anno/001c030_041_v001_file.0017.png.

        Thank you,
        Client
        """

        email_3 = """
        Hello Team,

        I have taken a look at the following shots and have some feedback:

        `SH020_080_222_v0001`
        - Please add some more lighting to this scene. 

        `ANM003_070_112_01`
        - This scene requires color correction. 

        Attachments can be found here: 
        - /path/to/anno/SH020_080_222_v0001_file.0010.png.
        - /path/to/anno/ANM003_070_112_01_file.0002.png 

        Best Regards,
        Client
        """

        email_4 = """
        Hi there,

        I've reviewed the provided shots. Here are my comments:

        `Sc220_500_111_version2`
        - I think the animation speed needs to be increased slightly. 

        `Scene180_400_090_v07001`
        - Could you add more texture to the background? 

        Here are the annotations:
        - /path/to/anno/Sc220_500_111_version2_file.0010.png.
        - /path/to/anno/Scene180_400_090_v07001_file.0005.png 

        Cheers,
        Client
        """

        email_5 = """
        `SHOT001_v1` - This is the first version of Shot 001.
        Attachments:
        - /path/to/attachment1.jpg
        - /path/to/attachment2.mov

        `SHOT002_v2` - Updated version of Shot 002.
        Notes:
        - This version includes some minor changes.
        Attachments:
        - /path/to/attachment3.png
        - /path/to/attachment4.mp4
        """

        expected_output_1 = [
            {
                "shot_name": "SH020_080_222",
                "version_name": "v002",
                "note": "It seems that it requires color correction.",
                "attachment": [
                    "/path/to/anno/SH020_080_222_v002_file.0010.png",
                ],
            },
            {
                "shot_name": "SH010_040_111",
                "version_name": "v001",
                "note": "I noticed that it needs a bit more brightness. Can we fix this?",
                "attachment": [
                    "/path/to/anno/SH010_040_111_v001_file.0001.png",
                    "/path/to/anno/SH010_040_111_v001_file.0017.png",
                ],
            }
        ]

        expected_output_2 = [
            {
                "shot_name": "001c020_082",
                "version_name": "v002",
                "note": "It seems that it requires color correction.",
                "attachment": [
                    "/path/to/anno/001c020_082_v002_file.0010.png",
                ],
            },
            {
                "shot_name": "001c030_041",
                "version_name": "v001",
                "note": "I noticed that it needs a bit more brightness. Can we fix this?",
                "attachment": [
                    "/path/to/anno/001c030_041_v001_file.0001.png",
                    "/path/to/anno/001c030_041_v001_file.0017.png",
                ],
            }
        ]

        expected_output_3 = [
            {
                "shot_name": "SH020_080_222",
                "version_name": "v0001",
                "note": "Please add some more lighting to this scene.",
                "attachment": [
                    "/path/to/anno/SH020_080_222_v0001_file.0010.png",
                ],
            },
            {
                "shot_name": "ANM003_070_112_01",
                "version_name": "",
                "note": "This scene requires color correction.",
                "attachment": [
                    "/path/to/anno/ANM003_070_112_01_file.0002.png",
                ],
            }
        ]

        expected_output_4 = [
            {
                "shot_name": "Sc220_500_111",
                "version_name": "version2",
                "note": "I think the animation speed needs to be increased slightly.",
                "attachment": [
                    "/path/to/anno/Sc220_500_111_version2_file.0010.png",
                ],
            },
            {
                "shot_name": "Scene180_400_090",
                "version_name": "v07001",
                "note": "Could you add more texture to the background?",
                "attachment": [
                    "/path/to/anno/Scene180_400_090_v07001_file.0005.png",
                ],
            }
        ]

        expected_output_5 = [
            {
                "shot_name": "SHOT001",
                "version_name": "v1",
                "note": "This is the first version of Shot 001.",
                "attachment": [
                    "/path/to/attachment1.jpg",
                    "/path/to/attachment2.mov",
                ],
            },
            {
                "shot_name": "SHOT002",
                "version_name": "v2",
                "note": "Updated version of Shot 002. This version includes some minor changes.",
                "attachment": [
                    "/path/to/attachment3.png",
                    "/path/to/attachment4.mp4",
                ],
            }
        ]

        output_1 = extract_info_from_message(email_1)
        output_2 = extract_info_from_message(email_2)
        output_3 = extract_info_from_message(email_3)
        output_4 = extract_info_from_message(email_4)
        output_5 = extract_info_from_message(email_5)

        self.assertEqual(output_1, expected_output_1)
        self.assertEqual(output_2, expected_output_2)
        self.assertEqual(output_3, expected_output_3)
        self.assertEqual(output_4, expected_output_4)
        self.assertEqual(output_5, expected_output_5)

if __name__ == '__main__':
    unittest.main()
