# Установка кастомизации SPK.ctf на CTFd

Совместимо с CTFd из репозитория `master` (Font Awesome 6.5.1, Bootstrap 5).
Состав комплекта:
- стили v3.7 (pixel-retro) — палитра #0b6ef0 / #7cacfc / #041c84 / #675ea9 / #c496ca / #3b2d5e
- пиксельный шрифт Public Pixel, Pixel Ultima (SIL OFL) для всего текста
- возвращённые иконки Font Awesome (элементы + ::before/::after)
- кастомный футер «Организаторы: IT-центр БПОУ ОО «СПК»»
- готовая главная страница (hero, карточки категорий, «Как начать», CTA-кнопки)
- тексты страниц Welcome и Rules

## 0. Структура папок

Корень репозитория:  /home/ctfadmin/spk-ctf/deploy/ctfd-app/
Тема участников:      /home/ctfadmin/spk-ctf/deploy/ctfd-app/CTFd/themes/core/

- Шаблоны:   .../themes/core/templates/   (base.html)
- Стили:     .../themes/core/static/css/    (spk.css)      ← папки css может не быть, создаём
- Шрифты:    .../themes/core/static/fonts/  (PublicPixel.ttf)
- Картинки:  .../themes/core/static/img/    (logo.svg, favicon.svg)

Внутреннюю папку CTFd (Python-пакет) не переименовывать и не двигать.

## 1. Остановка контейнеров (на сервере по SSH)

    cd ~/spk-ctf/deploy/ctfd-app
    docker compose down

## 2. Бэкап и создание недостающих папок

    cp CTFd/themes/core/templates/base.html CTFd/themes/core/templates/base.html.bak
    mkdir -p CTFd/themes/core/static/css
    mkdir -p CTFd/themes/core/static/fonts

## 3. Копирование файлов (с рабочего ПК)

    scp base.html         ctfadmin@<ip-сервера>:/home/ctfadmin/spk-ctf/deploy/ctfd-app/CTFd/themes/core/templates/
    scp spk_v37_full.css  ctfadmin@<ip-сервера>:/home/ctfadmin/spk-ctf/deploy/ctfd-app/CTFd/themes/core/static/css/spk.css
    scp PublicPixel.ttf   ctfadmin@<ip-сервера>:/home/ctfadmin/spk-ctf/deploy/ctfd-app/CTFd/themes/core/static/fonts/
    scp logo.svg          ctfadmin@<ip-сервера>:/home/ctfadmin/spk-ctf/deploy/ctfd-app/CTFd/themes/core/static/img/
    scp favicon.svg       ctfadmin@<ip-сервера>:/home/ctfadmin/spk-ctf/deploy/ctfd-app/CTFd/themes/core/static/img/

Если scp падает с «No such file or directory» или «Failure»:
- проверьте, что папка назначения существует (ls);
- тильда ~ в кавычках не раскрывается — используйте полный путь /home/ctfadmin/...;
- если права запрещают запись в папки темы: скопируйте в ~/, затем на сервере
  sudo cp ~/файл /полный/путь/ (предварительно sudo chown -R ctfadmin:ctfadmin .../themes).

Перечень файлов:
- base.html — кастомный каркас + футер
- spk_v37_full.css — переименовать в spk.css при копировании (см. команду выше)
- PublicPixel.ttf — шрифт
- logo.svg — логотип «Терминал» (загрузка через админку — см. п.6)
- favicon.svg — флажок (загрузка через админку — см. п.6)
- index_page.html — содержимое главной (вставляется в админке, п.7)
- pages/welcome.md, pages/rules.md — тексты страниц (п.7)

## 4. Запуск и проверка (на сервере)

    cd ~/spk-ctf/deploy/ctfd-app
    docker compose up -d
    sleep 20
    docker compose ps                                # все контейнеры Up

    # статика отдаётся?
    curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8000/themes/core/static/css/spk.css        # 200
    curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8000/themes/core/static/fonts/PublicPixel.ttf  # 200
    curl -s http://localhost:8000/themes/core/static/css/spk.css | grep -c "SPK-PATCH-v3.7"            # 1

Если css вернул 404 — файл лежит не по тому пути: find ~ -name spk.css


## 5. Логотип и favicon (в админке)

Admin Panel → Configuration → Settings → Appearance:
- Logo: загрузить logo.svg
- Small Icon: загрузить favicon.svg
Обновить страницу (Ctrl+Shift+R).

## 6. Главная страница и страницы (в админке)

Главная — это ОБЫЧНАЯ страница с роутом index (views.py: '/' рендерит Page route="index").

Если её удалили: Pages → Create → Route: index (строго, маленькими буквами),
Format: HTML, Draft: выкл.

Затем: открыть страницу index на редактирование → Format: HTML →
заменить всё содержимое на index_page.html → Save.

Pages → Create дополнительно:
- Rules: route rules, Markdown, содержимое pages/rules.md, Show in Navbar.

## 7. Чек-лист результата

- [ ] Весь текст сайта — пиксельный Public Pixel (наследование + прямые правила)
- [ ] Иконки Font Awesome видны (вход/выход, уведомления) — починено через ::before/::after
- [ ] Navbar: фон #3b2d5e, лиловая полоса снизу
- [ ] Карточки: белые, тёмный текст, заголовки синие (--spk-blue)
- [ ] Футер: компактный, без налезаний и белой полосы, бренд лиловый,
      строка «Организаторы: IT-центр БПОУ ОО «СПК»»
- [ ] Главная: hero с лого, 6 карточек, «Как начать», 3 одинаковые CTA-кнопки
- [ ] Скорборд: подсветка топ-3

## 8. Откат при проблемах

Шаблон:
    cp CTFd/themes/core/templates/base.html.bak CTFd/themes/core/templates/base.html
    docker compose restart
Стили: удалить <link ... spk.css> из base.html либо удалить сам spk.css.
Данные (страницы, задания): Admin → Config → Backup → Export (JSON) — делать регулярно.


