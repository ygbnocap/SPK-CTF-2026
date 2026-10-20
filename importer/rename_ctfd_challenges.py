#!/usr/bin/env python3
"""Remove SPK category/number prefixes from CTFd challenge titles.

Dry-run by default. Requires requests and CTFD_TOKEN in environment.
"""
import argparse
import json
import os
import re
import sys
from pathlib import Path

import requests

PATTERN = re.compile(r'^\s*\[?SPK[-_](?:WEB|Crypto|For|Steg|Rev)[-_]\d{2}\s*\.\s*', re.I)


def main():
    parser = argparse.ArgumentParser(description='Убрать SPK-Category-NN. из названий заданий CTFd')
    parser.add_argument('--url', default='http://127.0.0.1:8000')
    parser.add_argument('--apply', action='store_true', help='Применить изменения после подтверждения')
    parser.add_argument('--backup', default='challenge_names_before_rename.json')
    args = parser.parse_args()

    token = os.getenv('CTFD_TOKEN', '').strip()
    if not token:
        sys.exit('Ошибка: сначала установи переменную CTFD_TOKEN')

    session = requests.Session()
    session.headers.update({
        'Authorization': f'Token {token}',
        'Accept': 'application/json',
        'Content-Type': 'application/json',
    })
    base = args.url.rstrip('/') + '/api/v1'

    def request(method, path, **kwargs):
        response = session.request(method, base + path, allow_redirects=False, timeout=20, **kwargs)
        if response.status_code >= 400 or response.status_code in (301, 302, 303, 307, 308):
            raise RuntimeError(f'{method} {path}: HTTP {response.status_code}: {response.text[:250]}')
        try:
            payload = response.json()
        except ValueError:
            raise RuntimeError(f'{method} {path}: API вернул не JSON: {response.text[:250]}')
        if payload.get('success') is False:
            raise RuntimeError(f'{method} {path}: {payload}')
        return payload.get('data', payload)

    challenges = request('GET', '/challenges')
    if not isinstance(challenges, list):
        raise RuntimeError('Неожиданный ответ /challenges: ожидался список')
    # GET /challenges returns the entire list; do not paginate without documented support.
    changes = []
    for item in challenges:
        old = item.get('name', '')
        new = PATTERN.sub('', old).strip()
        if old != new and new:
            changes.append({'id': item['id'], 'old': old, 'new': new, 'category': item.get('category', '')})

    if not changes:
        print('Переименовывать нечего: префиксы не обнаружены.')
        return

    # Protect against accidentally creating duplicate visible names within the same category.
    existing = {(x.get('category', ''), x.get('name', '')) for x in challenges if x['id'] not in {c['id'] for c in changes}}
    target_names = set()
    for c in changes:
        pair = (c['category'], c['new'])
        if pair in existing or pair in target_names:
            raise RuntimeError(f"Конфликт имён в категории {c['category']}: {c['new']}")
        target_names.add(pair)

    backup = Path(args.backup)
    if backup.exists():
        raise RuntimeError(f'Файл резервной копии уже существует: {backup}. Укажи другое имя через --backup')
    backup.write_text(json.dumps(changes, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Сохранён план и резервные названия: {backup.resolve()}')
    for c in changes:
        print(f"{c['id']:>4} | {c['old']}  →  {c['new']}")
    print(f'Всего переименований: {len(changes)}')

    if not args.apply:
        print('DRY RUN: изменений на сервере нет. Для применения добавь --apply.')
        return

    confirmation = input(f'Для изменения {len(changes)} названий введи RENAME {len(changes)}: ').strip()
    if confirmation != f'RENAME {len(changes)}':
        sys.exit('Отменено: названия не изменены.')

    successes = 0
    for c in changes:
        # Only the name field is sent. All other challenge settings remain untouched.
        request('PATCH', f"/challenges/{c['id']}", json={'name': c['new']})
        successes += 1
        print(f"OK {c['id']} {c['new']}")
    print(f'Готово: {successes}/{len(changes)} переименовано.')


if __name__ == '__main__':
    main()
