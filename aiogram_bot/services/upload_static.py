import json
import hashlib
import os

from aiogram.types import FSInputFile

from services.create_bot import STATIC_DIR, ADMIN_ID


JSON_FILE_PATH = os.path.join(STATIC_DIR, 'file_ids.json')


def calculate_file_hash(file_path):
    """Вычисляет хэш файла."""
    hasher = hashlib.md5()
    with open(file_path, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()


def scan_photos_folder(STATIC_DIR):
    """Сканирует папку static/photos и возвращает словарь с хэшами файлов."""
    photos_dir = os.path.join(STATIC_DIR, 'photos')
    file_hashes = {}
    for filename in os.listdir(photos_dir):
        file_path = os.path.join(photos_dir, filename)
        if os.path.isfile(file_path):
            file_hashes[filename] = calculate_file_hash(file_path)
    return file_hashes


def load_file_ids():
    """Загружает file_ids из JSON-файла."""
    if os.path.exists(JSON_FILE_PATH):
        with open(JSON_FILE_PATH, 'r') as f:
            return json.load(f)
    return {}


def save_file_ids(file_ids):
    """Сохраняет file_ids в JSON-файл."""
    with open(JSON_FILE_PATH, 'w') as f:
        json.dump(file_ids, f, indent=4)


def determine_category(filename):
    """Определяет категорию файла (можно доработать логику)."""
    if 'house' in filename.lower():
        return 'houses'
    elif 'entertainment' in filename.lower():
        return 'entertainment'
    elif 'territory' in filename.lower():
        return 'territory'
    else:
        return 'other'


async def update_file_ids(bot, STATIC_DIR):
    """Обновляет file_ids на основе изменений в папке static/photos."""
    file_ids = load_file_ids()
    current_hashes = scan_photos_folder(STATIC_DIR)
    updated = False
    for filename, current_hash in current_hashes.items():
        if (
            filename not in file_ids
            or file_ids[filename]['hash'] != current_hash
        ):
            file_path = os.path.join(STATIC_DIR, 'photos', filename)
            image_file = FSInputFile(path=file_path)
            result = await bot.send_photo(chat_id=ADMIN_ID, photo=image_file)
            category = determine_category(filename)
            file_ids[filename] = {
                'hash': current_hash,
                'file_id': result.photo[-1].file_id,
                'category': category,
            }
            updated = True
            print(f'Updated file_id for {filename}: '
                  f'{result.photo[-1].file_id}')

    for filename in list(file_ids.keys()):
        if filename not in current_hashes:
            del file_ids[filename]
            updated = True
            print(f'Removed file_id for deleted file: {filename}')

    if updated:
        save_file_ids(file_ids)
