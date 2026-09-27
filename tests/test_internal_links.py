"""Regression tests for rendering-compatible navigation checks."""
from pathlib import Path
import tempfile
import unittest
from check_internal_links import check, destinations


class NavigationTests(unittest.TestCase):
    def test_encoded_and_angle_wrapped_spaces_are_links(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'report one.md').write_text('Report')
            (root / 'README.md').write_text('[one](report%20one.md)\n[two](<report one.md>)')
            self.assertEqual(check(root), (2, []))

    def test_bare_spaces_are_not_rendered_links(self):
        self.assertEqual(list(destinations('[Report](report one.md)')), [])

    def test_code_examples_are_not_navigation(self):
        text = '```text\n[example](missing.md)\n```\n`[inline](missing.md)`'
        self.assertEqual(list(destinations(text)), [])

    def test_reference_links_and_images_are_checked(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'README.md').write_text('[Report][report]\n\n[report]: missing.md\n\n![proof](missing.png)')
            count, errors = check(root)
            self.assertEqual(count, 2)
            self.assertEqual(len(errors), 2)

    def test_relative_root_query_fragment_and_directory_links(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'guides').mkdir()
            (root / 'README.md').write_text('[guide](guides/)\n[x](https://example.com/no.md)\n[here](#section)')
            (root / 'guides' / 'test.md').write_text('[home](../README.md#start)\n[root](/README.md?raw=1#start)')
            self.assertEqual(check(root), (3, []))

    def test_outside_repo_destination_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'README.md').write_text('[outside](../)')
            count, errors = check(root)
            self.assertEqual(count, 1)
            self.assertIn('escapes repository', errors[0])


if __name__ == '__main__':
    unittest.main()
