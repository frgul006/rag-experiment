import unittest

from regent_rag.core.security import mask_string


class TestMaskString(unittest.TestCase):
    def test_mask_string(self) -> None:
        self.assertEqual(mask_string("1234567890", 4), "******7890")
        self.assertEqual(mask_string("1234567890", 2), "********90")
        self.assertEqual(mask_string("123", 4), "***")
        self.assertEqual(mask_string("", 4), "")
        self.assertEqual(mask_string("1234567890", 0), "**********")


if __name__ == "__main__":
    unittest.main()
