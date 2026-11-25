"""Regression tests for tools/i18n/translate.py accelerator and catalog validation."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import translate as T


class AccessKeyTests(unittest.TestCase):
    def test_literal_ampersand_with_space_is_not_accelerator(self):
        src = (
            "If macOS asks whether it may access data from other apps, allow it. "
            "Or turn on Mister Download Manager in System Settings → Privacy & Security "
            "→ Full Disk Access. Then press Set it up."
        )
        tr = (
            "වෙනත් යෙදුම්වල දත්ත වෙත ප්‍රවේශ වීමට macOS විමසන්නේ නම්, එයට ඉඩ දෙන්න. "
            "නැතහොත් System Settings → Privacy & Security → Full Disk Access තුළ "
            "Mister Download Manager සක්‍රිය කරන්න. ඉන්පසු Set it up ඔබන්න."
        )
        self.assertEqual(T.ACCESS.findall(src.replace("&&", "")), [])
        self.assertIsNone(T.check("si", src, tr))

    def test_menu_accelerators_still_recognized(self):
        self.assertEqual(T.ACCESS.findall("&File"), ["F"])
        self.assertEqual(T.ACCESS.findall("&Options"), ["O"])
        self.assertIsNone(T.check("si", "&File", "&ගොනුව"))
        self.assertIsNone(T.check("si", "&Options", "&විකල්ප"))
        self.assertIsNotNone(T.check("si", "&File", "ගොනුව"))

    def test_escaped_ampersand_handled_correctly(self):
        self.assertEqual(T.ACCESS.findall("Tom && Jerry".replace("&&", "")), [])
        self.assertIsNone(T.check("si", "Tom && Jerry", "ටොම් && ජෙරී"))
        self.assertIsNotNone(T.check("si", "Tom && Jerry", "ටොම් & ජෙරී"))

    def test_si_catalog_has_zero_validation_errors(self):
        en = T.source_rows()
        si = T.read_catalog("si")
        for c, s, _ in en:
            if c == "@id":
                continue
            self.assertIn((c, s), si, f"Missing key: {(c, s)}")
            tr, _ = si[(c, s)]
            if c == "@plural":
                sp_all = s.split("|")
                for j, tp in enumerate(tr.split("|")):
                    sp = sp_all[0] if j == 0 else sp_all[-1]
                    self.assertIsNone(T.check("si", sp, tp), f"{(c, s)} form {j}")
            else:
                self.assertIsNone(T.check("si", s, tr), f"{(c, s)}")


if __name__ == "__main__":
    unittest.main()
