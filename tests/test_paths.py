"""Basic tests related to path"""

import os
from pathlib import Path

tests_path = Path(__file__).parent


def test_tests():
    """Checks if the tests path exists"""

    assert tests_path.parts[-1] == "tests"
    assert tests_path.exists()


def test_source():
    """Checks if the sorce path exists"""

    source_path = tests_path.parent / "src"
    assert source_path.exists()


def test_references():
    """Checks if the references exist"""

    reference_path = tests_path.parent / "src" / "references" / "reference.csv"
    sandarbha_path = tests_path.parent / "src" / "references" / "sandarbha.yml"
    assert reference_path.exists()
    assert sandarbha_path.exists()


def test_texts():
    """Checks if the texts path exists"""

    texts_path = tests_path.parent / "src" / "texts"
    assert texts_path.exists()


def test_text_file_number():
    """Checks if the texts path contains even number of files"""

    texts_path = tests_path.parent / "src" / "texts"
    contents = os.listdir(texts_path)
    assert len(contents) % 2 == 0


def test_text_file_names():
    """Checks if the sources and texts filenames match up"""

    texts_path = tests_path.parent / "src" / "texts"
    contents = os.listdir(texts_path)

    texts = set(x.split(".")[0] for x in contents if "source_" not in x)
    sources = set(x.split("_")[1].split(".")[0] for x in contents if "source_" in x)
    assert texts == sources
