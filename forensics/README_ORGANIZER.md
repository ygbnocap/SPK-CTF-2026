# SPK Forensics 01–10 — организаторский комплект

Игрокам выдавать только артефакты, не выдавать solve.py, verify.py или файл флагов.

| ID | Файл игрока | Механика |
| --- | --- | --- |
| For-01 | for01_logs/access.log | поиски аномального HTTP-запроса |
| For-02 | for02_exif/photo.jpg | EXIF ImageDescription, ваша фотография 123.jpg |
| For-03 | for03_pcap/traffic.pcap | HTTP POST форма, TCP/IPv4 PCAP |
| For-04 | for04_disk/floppy.raw | ext2-подобный образ с удалённым inode и остаточными данными |
| For-05 | for05_memory/editor.dmp | три версии несохранённого документа |
| For-06 | for06_authlog/auth.log | SSH-аудит, одобренный вход |
| For-07 | for07_ftp/midnight.pcap | FTP credentials и ZIP в data-потоке |
| For-08 | for08_timeline/timeline.txt | аномальные отметки времени |
| For-09 | for09_memkey/vault.dmp + vault.enc | AES-256-CBC и ключ в памяти |
| For-10 | for10_dns/dns_exfil.pcap | DNS-метки base32 + восстановление PNG |

Проверка: `python3 verify_all.py`. Python: требуется `Pillow` и `cryptography`.

Особенности: For-04 — учебный ext2-образ, структура суперблока/инодов создаётся вручную. Рекомендуется дополнительно проверить `fsck.ext2` и `debugfs` на VPS перед публикацией. For-06 и For-08 в исходном пакете имеют противоречия между форматом вычисляемого флага и точным фиксированным флагом; здесь приоритет имеет точный флаг раздела 7. For-10 содержит PNG в виде base32 по DNS-запросам; флаг расположен в PNG tEXt. Пакеты PCAP сгенерированы вручную с контрольными суммами.
