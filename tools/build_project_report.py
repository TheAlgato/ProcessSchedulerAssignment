"""Build the guideline report with a source appendix from the current project."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    body = (ROOT / 'docs' / 'report-body.md').read_text(encoding='utf-8')
    sources = sorted({path for pattern in (
        '*.py', 'modules/*.py', 'models/*.py', 'database/*.py', 'visualization/*.py',
        'visualization/*.css', 'tests/*.py', 'tools/*.py', '*.bat', '*.command',
        'requirements*.txt', '.streamlit/*.toml', '.gitignore',
    ) for path in ROOT.glob(pattern) if path.is_file()})
    if not sources or ROOT / 'dashboard.py' not in sources:
        raise RuntimeError('No dashboard source found. Keep this tool in the project tools directory.')
    parts = [body.rstrip(), '\n## Appendix C. Complete project source\n',
             'Rebuild this appendix after code changes with `python tools/build_project_report.py`.\n']
    for source in sources:
        language = {'.py': 'python', '.css': 'css', '.toml': 'toml',
                    '.bat': 'bat', '.command': 'sh'}.get(source.suffix, 'text')
        parts.append(f'### {source.relative_to(ROOT).as_posix()}\n\n'
                     f'````{language}\n{source.read_text(encoding="utf-8").rstrip()}\n````\n')
    review = ROOT / 'docs' / 'black-box-testing.md'
    if review.exists():
        # Preserve the eight required sections and appendices A-C, then attach
        # the separately maintained acceptance evidence as a supplemental appendix.
        review_lines = review.read_text(encoding='utf-8').splitlines()
        appendix = '\n'.join(
            '#' + line if line.startswith('#') else line
            for line in review_lines[1:]
        ).strip()
        appendix = appendix.replace('](verification/', '](docs/verification/')
        parts.append('\n## Appendix D. Requirements and black box testing\n\n' + appendix + '\n')
    destination = ROOT / 'PROJECT_REPORT.md'
    destination.write_text('\n'.join(parts), encoding='utf-8')
    print(f'Created {destination.name} with {len(sources)} source files.')


if __name__ == '__main__':
    main()
