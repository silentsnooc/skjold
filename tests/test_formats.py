# -*- coding: utf-8 -*-
import io
import os

import pytest

from skjold.formats import extract_package_list_from, read_requirements_txt_from
from skjold.models import PackageList
from skjold.tasks import Configuration


def format_fixture_path_for(folder: str, filename: str) -> str:
    path_ = os.path.join(
        os.path.dirname(__file__), "fixtures", "formats", folder, filename
    )
    assert os.path.exists(path_)
    return path_


@pytest.mark.parametrize("folder", ["minimal", "random"])
@pytest.mark.parametrize(
    "filename", ["poetry.lock", "requirements.txt", "Pipfile.lock"]
)
def test_extract_dependencies_using_minimal_examples(folder, filename) -> None:
    with open(format_fixture_path_for(folder, filename)) as fh:
        packages = list(extract_package_list_from(Configuration(), fh, None))
        assert len(packages) > 0


@pytest.mark.parametrize("folder", ["minimal", "random"])
@pytest.mark.parametrize(
    "filename, format_",
    [
        ("requirements.txt", None),
        ("poetry.lock", None),
        ("Pipfile.lock", None),
        ("requirements.txt", "requirements.txt"),
        ("poetry.lock", "poetry.lock"),
        ("Pipfile.lock", "Pipfile.lock"),
    ],
)
def test_extract_package_versions_from_with_poetry_lock(folder, filename, format_):

    with open(format_fixture_path_for(folder, filename)) as fh:
        packages = list(extract_package_list_from(Configuration(), fh, format_))
        assert len(packages) > 0


@pytest.mark.parametrize(
    "stdin, expected_package_list",
    [
        ('package==0.6.0; python_version < "3.8"', [("package", "0.6.0")]),
        (
            'foo==0.6.0; python_version < "3.8"\nbar==1.0.0',
            [("foo", "0.6.0"), ("bar", "1.0.0")],
        ),
        ('foo==1.4.0; python_version < "3.8"', [("foo", "1.4.0")]),
        ('foo==1.3.0; sys_platform == "win32"', [("foo", "1.3.0")]),
    ],
)
def test_extract_package_versions_from(stdin: str, expected_package_list: PackageList):
    packages = read_requirements_txt_from(io.StringIO(stdin))
    assert list(packages) == expected_package_list


def test_extract_package_versions_from_file_with_hashes(requirements_txt_with_hashes,):
    packages = read_requirements_txt_from(io.StringIO(requirements_txt_with_hashes))
    assert list(packages) == [
        ("appdirs", "1.4.3"),
        ("argh", "0.26.2"),
        ("aspy.yaml", "1.3.0"),
        ("atomicwrites", "1.3.0"),
        ("attrs", "19.3.0"),
    ]
