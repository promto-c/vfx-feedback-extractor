import sys
import os
import unittest

# Add the project's root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from vfx_feedback_extractor.feedback_extractor import extract_info_from_message

class TestFeedbackExtractor(unittest.TestCase):
    def test_extract_info_from_message(self):
        message_1 = """
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

        message_2 = """
        Hi there,

        I've reviewed the provided shots. Here are my comments:

        Sc220_500_111_version2
        - I think the animation speed needs to be increased slightly. 

        Scene180_400_090_v07001
        - Could you add more texture to the background? 

        Here are the annotations:
        - /path/to/anno/Sc220_500_111_version2_file.0010.png.
        - /path/to/anno/Scene180_400_090_v07001_file.0005.png 

        Cheers,
        Client
        """

        message_3 = """
        SHOT001_v1 - This is the first version of Shot 001.
        Attachments:
        - /path/to/attachment1.jpg
        - /path/to/attachment2.mov

        SHOT002_v2 - Updated version of Shot 002.
        Notes:
        - This version includes some minor changes.
        Attachments:
        - /path/to/attachment3.png
        - /path/to/attachment4.mp4
        """

        message_4 = """
        Regarding the recent feedback:

        `SHT101_200_040_fg02_v001 `
        Approved.

        SHT101_300_005_v003
            - Approved.

        The color appears to be incorrect.
        SHT100_005_020_v000 
        SHT100_015_030_fg01_v000 
        SHT100_015_045_bg01_v000 
        SHT100_025_100_v000 

        See notes on the below some elements

        SHT102_204_005_comp_service_v0000 
            - There seems to be an issue with the lighting. It appears inconsistent and uneven.

        SHT102_204_070_comp_service_v0000 
            - Discontinuity at frame 1100 and 1201-1217.
        """

        expected_output_1 = [
            {
                "shot_name": "SH020_080_222",
                "version": 2,
                "version_name": "SH020_080_222_v002",
                "note": "It seems that it requires color correction.",
                "attachment": [
                    "/path/to/anno/SH020_080_222_v002_file.0010.png",
                ],
            },
            {
                "shot_name": "SH010_040_111",
                "version": 1,
                "version_name": "SH010_040_111_v001",
                "note": "I noticed that it needs a bit more brightness. Can we fix this?",
                "attachment": [
                    "/path/to/anno/SH010_040_111_v001_file.0001.png",
                    "/path/to/anno/SH010_040_111_v001_file.0017.png",
                ],
            }
        ]

        expected_output_2 = [
            {
                "shot_name": "Sc220_500_111",
                "version": 2,
                "version_name": "Sc220_500_111_version2",
                "note": "I think the animation speed needs to be increased slightly.",
                "attachment": [
                    "/path/to/anno/Sc220_500_111_version2_file.0010.png",
                ],
            },
            {
                "shot_name": "Scene180_400_090",
                "version": 7001,
                "version_name": "Scene180_400_090_v07001",
                "note": "Could you add more texture to the background?",
                "attachment": [
                    "/path/to/anno/Scene180_400_090_v07001_file.0005.png",
                ],
            }
        ]

        expected_output_3 = [
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

        output_1 = extract_info_from_message(message_1)
        output_2 = extract_info_from_message(message_2)
        output_3 = extract_info_from_message(message_3)

        self.assertEqual(output_1, expected_output_1)
        self.assertEqual(output_2, expected_output_2)
        self.assertEqual(output_3, expected_output_3)

if __name__ == '__main__':
    unittest.main()
