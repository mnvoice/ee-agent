#!/usr/bin/env python3
"""
Build script: bundles JS modules into a single non-module script.
Removes import/export statements and concatenates files in dependency order.
"""

import re
import os

# File order matters: no-dep files first, app.js last
FILES = [
    'app/js/db.js',
    'app/js/store.js',
    'app/js/render.js',
    'app/js/annotation.js',
    'app/js/app.js',
]

OUTPUT = 'app/js/bundle.js'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Remove single-line import statements (including multi-line ones using regex DOTALL)
    # Pattern: import { ... } from '...'; (possibly multi-line)
    content = re.sub(
        r'import\s*\{[^}]*\}\s*from\s*[\'"][^\'"]*[\'"]\s*;?\s*\n?',
        '',
        content,
        flags=re.DOTALL
    )

    # Remove: export function foo -> function foo
    content = re.sub(r'\bexport\s+function\b', 'function', content)

    # Remove: export async function foo -> async function foo
    content = re.sub(r'\bexport\s+async\s+function\b', 'async function', content)

    # Remove: export const foo -> const foo
    content = re.sub(r'\bexport\s+const\b', 'const', content)

    # Remove: export let foo -> let foo
    content = re.sub(r'\bexport\s+let\b', 'let', content)

    # Remove: export { foo, bar }; lines entirely
    content = re.sub(r'export\s*\{[^}]*\}\s*;?\s*\n?', '', content)

    # Remove: export default ... lines
    content = re.sub(r'export\s+default\s+', '', content)

    return content


def build():
    parts = []

    for rel_path in FILES:
        abs_path = os.path.join(BASE_DIR, rel_path)
        if not os.path.exists(abs_path):
            print(f'ERROR: File not found: {abs_path}')
            return False

        processed = process_file(abs_path)
        header = f'// ===== {rel_path} =====\n'
        parts.append(header + processed)
        print(f'  Processed: {rel_path}')

    bundle = '\n\n'.join(parts)

    output_path = os.path.join(BASE_DIR, OUTPUT)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(bundle)

    line_count = bundle.count('\n') + 1
    print(f'\nBundle written to: {OUTPUT}')
    print(f'Total lines: {line_count}')
    return True


if __name__ == '__main__':
    print('Building app bundle...')
    success = build()
    if not success:
        exit(1)
