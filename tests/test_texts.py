"""Basic tests related to texts"""

import os
from pathlib import Path
from src import varna as vn

texts_path = Path(__file__).parent.parent / "src" / "texts"
texts = os.listdir(texts_path)
sources = list(text for text in texts if "source_" in text)
texts = list(text for text in texts if "source_" not in text)


def test_newlines():
    """Tests if the test file end in a newline"""

    for text in texts:
        with open(texts_path / text, "r", encoding="utf-8") as file:
            lines = file.readlines()

        assert len(lines) > 2
        assert lines[-1] == "\n", f"No empty line in {text}"


def test_characterset():
    """Checks if all characters are devanagari"""

    for text in texts:
        with open(texts_path / text, "r", encoding="utf-8") as file:
            lines = file.readlines()

            for line in lines:
                for symbol in line[:-1]:
                    assert (
                        symbol in vn.svara
                        or symbol in vn.maatraa
                        or symbol in vn.vyanjana
                        or symbol in vn.vyanjana_with_akaara
                        or symbol in vn.sankhyaa
                        or symbol
                        in [" ", "्", "ऽ", "ं", "ँ", "।", "॥", "ः", "-", "\u200d"]
                    ), f"Unknown symbol in {text} in line {line}"
