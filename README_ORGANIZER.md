# README для организатора — SPK.ctf-2026

## О мероприятии
SPK.ctf-2026 — образовательный jeopardy-CTF. 50 заданий в 5 категориях (Web, Crypto, Forensics, Steganography, Reverse Engineering). Все атаки — только в рамках лабораторных сервисов CTF.

- **Длительность:** 4–6 часов
- **Команды:** 3–5 человек (режим Teams в CTFd — очки считает команда)
- **Подсказки:** тексты сохранены в пакете для организатора, но на текущем соревновании в CTFd не загружаются и игрокам недоступны
- **Талисман СПК для атмосферы:** СПКашка (упоминается в описаниях заданий)

## Структура репозитория spk-ctf

```
~/spk-ctf/
├── deploy/
│   ├── ctfd-app/              # CTFd + Docker Nginx (порты 80/443, внутри CTFd :8000)
│   └── docker-compose.yml     # исходная схема стенда, сверять с фактическими Compose
├── web/                       # web01..web10, deploy/docker-compose.yml, verify_all.py
├── crypto/                    # crypto01..crypto10 (gen.py, solve.py)
├── forensics/                 # for01..for10 + gen_all.py, verify_all.py
├── stego/                     # steg01..steg10 (gen.py, для ряда заданий solve.py/verify.py)
└── reversing/                 # rev01..rev10 (src.c, Makefile, solve.py, verify.py)
```

## Подготовка (по шагам)

### 1. Генерация статических артефактов
```bash
source ~/venv-ctf/bin/activate
cd ~/spk-ctf
# Crypto: генерация зависит от конкретного crypto*/gen.py; проверить наличие файлов.
# Forensics (актуальный комплект):
python3 forensics/gen_all.py
python3 forensics/verify_all.py
# Steganography: генерировать по отдельным каталогам; где есть verify.py — запустить.
```
Статические артефакты необходимо проверять через `solve.py`, `verify.py` либо ручной сценарий. Не все скрытые флаги можно найти простым `strings`.

### 2. Сборка бинарников Reverse
```bash
cd ~/spk-ctf/reversing
for d in rev[0-9][0-9]_*/; do make -C "$d" clean && make -C "$d"; done
python3 verify_all.py
```
Бинарники — Linux ELF x86-64; после распаковки ZIP рекомендуется именно пересборка (`make clean && make`) для восстановления прав выполнения.

### 3. Запуск веб-сервисов
```bash
cd ~/spk-ctf/web/deploy
# Пути контекста сборки должны ссылаться на ../webXX_*, без лишнего ../web/.
docker compose up -d --build
docker compose ps
cd ~/spk-ctf/web && python3 verify_all.py
```
Порты Web: 8001–8010. Crypto-оракулы: 8106 и 8109 — отдельные сервисы. Внутренние сервисы Docker (`internal:9000`, `reports:9010`) нельзя открывать участникам напрямую.

**CTFd и сеть:** основной адрес участников — `https://ctf.spk.ru` (локальный DNS → `192.168.0.46`). CTFd обслуживает Docker Nginx `ctfd-app-nginx-1` с конфигурацией `deploy/ctfd-app/conf/nginx/http.conf`, HTTPS :443 → `ctfd:8000`; HTTP :80 перенаправляется на HTTPS. TLS-сертификат выдан внутренним CA `LABSEC63-Root-CA` домена AD `labsec63.local`; доверие корневому CA и доступность CRL в изолированной сети проверяются до старта. Web/crypto-полигоны используют отдельные HTTP-порты в лабораторной сети и не становятся защищёнными HTTPS автоматически.

### 4. CTFd: команды и участники
- Режим **Teams** включён; публичная регистрация отключена.
- Создание учёток: скрипт `spk_ctf_users_setup.py` + CSV (`team,username,password`) + API-токен из Admin → Settings → Tokens.
- Раздать логины/пароли на брифинге.

### 5. Загрузка 50 заданий в CTFd
Источник данных: `SPK_ctf_package.md`. Выбран режим **«обновить существующие и добавить недостающие»** через CTFd API: сначала бэкап и dry-run, затем сверка соответствий по ID `SPK-*` и подтверждение изменений. Не удалять чужие задания и не сбрасывать результаты участников. Доступ — токен администратора, хранящийся только на VPS, вне репозитория.

- Название, категория, описание (раздел 4), точный флаг (раздел 7; Static/Exact match для флага), прикреплённые файлы (раздел 5) и адреса лабораторных сервисов.
- **Тип задания: Dynamic**, начальные очки / Decay / Minimum по таблице в пакете. Это параметры динамической стоимости задания, а не тип проверки флага.
- **Подсказки из раздела 8 НЕ импортировать** — они остаются в документации организатора. Не создавать, не изменять и не удалять подсказки существующих заданий без отдельного решения.
- Проверить фактические пути артефактов (особенно Steg-05–10, Reverse и Forensics), работающие адреса и ответы в `verify_all.py` до отправки запросов API.

### 6. Кастомизация
- `spk.css` → `ctfd-app/CTFd/themes/core/static/css/spk.css`
- `base.html` → `.../themes/core/templates/` (бэкап: base.html.bak)
- `PublicPixel.ttf` → `.../static/fonts/`, лого/favicon загружены через админку
- Главная = Page с route `index`, Format HTML (содержимое index_page.html)

## Учётные данные для тестирования
- WEB-01/04/08: `student` / `student123`
- WEB-02: `student` / `student123` (кука user_id: 1001 → 1)
- WEB-10: `user` / `user123`

## Правила проведения
- Запрещено: DoS, атаки на инфраструктуру вне заданий, шаринг флагов между командами
- Ошибочная сдача флага не штрафуется
- Споры решает организатор

## Мониторинг и перезапуск
```bash
cd ~/spk-ctf/web/deploy
docker compose ps                    # статус Web
docker compose logs -f web01         # логи задания
docker compose restart web05         # перезапуск одного Web
# CTFd: cd ~/spk-ctf/deploy/ctfd-app && docker compose ps
# Не выполнять docker compose down для CTFd как способ сброса соревнования.
```

## Бэкап
```bash
# Docker-снапшоты перед игрой
cd ~/spk-ctf/deploy && docker commit <id> web01-backup
# CTFd: Admin → Config → Backup → Export (JSON) — регулярно!
```

## Чек-лист за час до старта
- [ ] Все сервисы `docker compose ps` — Up
- [ ] Артефакты сгенерированы, бинарники собраны
- [ ] Каждый флаг проверен (solve.py / ручная проверка)
- [ ] Все 50 заданий импортированы/обновлены без дублей; у каждого тип Dynamic, правильные Initial/Decay/Minimum и точный флаг
- [ ] Подсказки отсутствуют в API-импорте (тексты хранятся только в пакете)
- [ ] Проверены DNS, HTTPS и доверие CA/CRL на ПК участников
- [ ] Учётки команд созданы и разданы
- [ ] Scoreboard виден, время начала/конца установлено
- [ ] Экспорт CTFd сделан
