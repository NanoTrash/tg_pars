⚠️ Важно:

Метод через комментарии работает только с публичными каналами , где разрешены комментарии.
Telegram может лимитировать частые запросы → используй time.sleep() между действиями.
Для работы с большими объемами данных рекомендуется использовать несколько аккаунтов и прокси.

💡 Как это работает:

Пользователь выбирает способ парсинга:
1 — через список участников (требуется быть админом)
2 — через комментарии к постам (работает даже без прав админа)
Для комментариев собираются авторы сообщений из последних N постов
Данные сохраняются в файл telegram_users.txt

✅ Что добавлено:

Функциия сбора пользователей из комментариев к постам
Возможность выбора: парсить участников через:
Участники группы (GetParticipantsRequest) — требует прав админа
Комментарии к постам — работает с публичными каналами

🔍 Пример вывода в файл:

Иван Петров | 123456789 | @ivanpetrov

Петр Иванов | 987654321 | Нет юзернейма
