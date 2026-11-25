ТВОЙ РЕПОЗИТОРИЙ ДЛЯ SILEO И ZEBRA

Внутри:
  Release, Packages, Packages.gz, Packages.bz2  - индекс репозитория
  debs/    - пакеты (3 темы x 2 варианта: rootless iphoneos-arm64 и rootful iphoneos-arm)
  CydiaIcon.png - иконка репозитория
  build_repo.py - пересобирает индекс после добавления .deb

КАК ВЫЛОЖИТЬ (GitHub Pages, бесплатно):
  1. На github.com создай публичный репозиторий, например "repo".
  2. Загрузи ВСЁ содержимое этой папки в корень (Add file -> Upload files).
  3. Settings -> Pages -> Source: Deploy from a branch -> main, папка / (root) -> Save.
  4. Через пару минут адрес будет: https://ТВОЙ_НИК.github.io/repo/

КАК ДОБАВИТЬ В SILEO / ZEBRA:
  Sileo: Источники -> плюс -> вставь адрес выше.
  Zebra: Источники -> плюс -> вставь адрес выше.

КАК ДОБАВИТЬ НОВЫЙ ПАКЕТ:
  Положи .deb в папку debs/, запусти  python3 build_repo.py  и загрузи на GitHub обновлённые
  файлы Packages, Packages.gz, Packages.bz2, Release и новый .deb.

Название репы и описание меняются в начале build_repo.py (REPO_NAME, REPO_DESC).
Имя автора и ID пакетов (com.myrepo.*) можешь заменить на свои.
