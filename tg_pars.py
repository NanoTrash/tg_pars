from telethon.sync import TelegramClient
from telethon.tl.functions.channels import GetParticipantsRequest, GetPostsRequest
from telethon.tl.types import ChannelParticipantsSearch, MessageMediaUnsupported
import time

# === Настройки ===
api_id = 'YOUR_API_ID'         # Замени на свой api_id
api_hash = 'YOUR_API_HASH'     # Замени на свой api_hash
phone = 'YOUR_PHONE_NUMBER'    # Например '+79123456789'

# Список каналов для парсинга
channels_to_parse = [
    'https://t.me/examplechannel ',
    'examplechannel2'
]

output_file = 'telegram_users.txt'

# =================

client = TelegramClient('session_name', api_id, api_hash)

async def get_channel_users_by_participants(channel):
    print(f'[+] Получаем участников из {channel}')
    offset = 0
    limit = 100
    all_participants = []

    while True:
        participants = await client(GetParticipantsRequest(
            channel,
            ChannelParticipantsSearch(''),
            offset,
            limit,
            hash=0
        ))
        if not participants.users:
            break
        all_participants.extend(participants.users)
        offset += len(participants.users)
        time.sleep(1)

    return all_participants


async def get_users_from_comments(channel, limit_posts=10):
    print(f'[+] Парсим комментарии из последних {limit_posts} постов в {channel.username or channel.title}')
    users = set()
    try:
        replies = await client(functions.channels.GetForumTopicsRequest(
            channel=channel,
            offset_date=0,
            offset_id=0,
            offset_topic=0,
            limit=limit_posts
        ))

        # Если есть темы (например, форумы), то обрабатываем их
        for topic in replies.topics:
            comments = await client.get_messages(
                channel,
                reply_to=topic.id,
                limit=100
            )
            for msg in comments:
                if msg.sender_id:
                    user = await client.get_entity(msg.sender_id)
                    users.add((user.first_name or '') + ' ' + (user.last_name or ''), user.id, user.username)
    except Exception as e:
        print(f"[!] Не удалось получить темы форума: {e}")

    # Если нет форума, просто берем последние посты и комментарии к ним
    posts = await client.get_messages(channel, limit=limit_posts)
    for post in posts:
        if hasattr(post, 'comments') and post.comments:
            comments = await client.get_messages(channel, reply_to=post.id, limit=100)
            for msg in comments:
                if msg.sender_id:
                    user = await client.get_entity(msg.sender_id)
                    full_name = f"{user.first_name or ''} {user.last_name or ''}".strip()
                    users.add((full_name, user.id, user.username))
                    print(f"Добавлен: {full_name} | {user.id} | @{user.username or 'no_username'}")
    return list(users)


def save_users_to_file(users, filename, source):
    with open(filename, 'a', encoding='utf-8') as f:
        for user in users:
            full_name, user_id, username = user
            line = f"{full_name} | {user_id} | @{username}\n" if username else f"{full_name} | {user_id} | Нет юзернейма\n"
            f.write(line)
    print(f"[+] Сохранено {len(users)} пользователей из '{source}' в {filename}")


async def main():
    await client.start(phone)
    print("[+] Авторизация успешна")

    for ch in channels_to_parse:
        try:
            entity = await client.get_entity(ch)
            print(f"\n[+] Обработка: {entity.title or entity.username}")

            # --- Выбор метода парсинга ---
            print("Выберите метод парсинга:")
            print("1. Участники группы (требуются права админа)")
            print("2. Комментаторы постов (работает с публичными каналами)")
            choice = input("Введите 1 или 2: ")

            if choice == '1':
                users = await get_channel_users_by_participants(entity)
            elif choice == '2':
                users = await get_users_from_comments(entity)
            else:
                print("[!] Неправильный выбор, пропускаем.")
                continue

            save_users_to_file(users, output_file, entity.title or entity.username or 'Без названия')

        except Exception as e:
            print(f"[!] Ошибка при обработке {ch}: {e}")

with client:
    client.loop.run_until_complete(main())