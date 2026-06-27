from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

# ---------- КНОПКА "ОТМЕНА" ----------
kb_back = ReplyKeyboardMarkup(resize_keyboard=True)
kb1 = KeyboardButton('Отмена ❌')
kb_back.add(kb1)

# ---------- ГЛАВНАЯ КЛАВИАТУРА (ОБЫЧНЫЙ ПОЛЬЗОВАТЕЛЬ) ----------
def user_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(
        KeyboardButton('📋 Моя ссылка'),
        KeyboardButton('👑 Админка')
    )
    keyboard.add(
        KeyboardButton('📊 Моя статистика'),
        KeyboardButton('⭐ Рейтинг')
    )
    keyboard.add(
        KeyboardButton('🏆 Достижения'),
        KeyboardButton('⏰ Напоминания')
    )
    keyboard.add(
        KeyboardButton('📝 Голосование'),
        KeyboardButton('🔄 Автоответы')
    )
    keyboard.add(
        KeyboardButton('🚫 Заблокированные'),
        KeyboardButton('💬 Анонимный чат')
    )
    return keyboard

# ---------- ГЛАВНАЯ КЛАВИАТУРА (АДМИНИСТРАТОР) ----------
def admin_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(
        KeyboardButton('📊 Статистика'),
        KeyboardButton('📢 Управление каналами')
    )
    keyboard.add(
        KeyboardButton('👥 Управление админами'),
        KeyboardButton('📨 Рассылка')
    )
    keyboard.add(
        KeyboardButton('📊 Полная статистика'),
        KeyboardButton('🔙 Выйти из админки')
    )
    return keyboard

# ---------- УПРАВЛЕНИЕ КАНАЛАМИ ----------
def channels_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton('➕ Добавить канал', callback_data='add_channel'),
        InlineKeyboardButton('📋 Список каналов', callback_data='list_channels'),
        InlineKeyboardButton('❌ Удалить канал', callback_data='remove_channel'),
        InlineKeyboardButton('🔙 Назад', callback_data='admin_back')
    )
    return keyboard

# ---------- УПРАВЛЕНИЕ АДМИНАМИ ----------
def admins_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton('➕ Добавить админа', callback_data='add_admin'),
        InlineKeyboardButton('📋 Список админов', callback_data='list_admins'),
        InlineKeyboardButton('❌ Удалить админа', callback_data='remove_admin'),
        InlineKeyboardButton('🔙 Назад', callback_data='admin_back')
    )
    return keyboard

# ---------- КНОПКА ДЛЯ ОТВЕТА НА СООБЩЕНИЕ ----------
def send_message(user_id):
    ikb_send_message = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('Ответить 📩', callback_data=f'send|{user_id}')],
        [InlineKeyboardButton('⭐ Оценить', callback_data=f'rate|{user_id}')],
        [InlineKeyboardButton('🚫 Заблокировать', callback_data=f'block|{user_id}')]
    ])
    return ikb_send_message

# ---------- КЛАВИАТУРА АНОНИМНОГО ЧАТА ----------
def chat_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    keyboard.add(
        KeyboardButton('➕ Создать чат'),
        KeyboardButton('🔗 Войти по коду')
    )
    keyboard.add(
        KeyboardButton('🌐 Открытые комнаты'),
        KeyboardButton('📋 Мои чаты')
    )
    keyboard.add(
        KeyboardButton('🔙 Назад')
    )
    return keyboard

# ---------- КЛАВИАТУРА КОМНАТЫ ----------
def room_keyboard(room_code, is_admin=False, is_open=False):
    keyboard = InlineKeyboardMarkup(row_width=1)
    
    # Кнопка переключения типа комнаты (только для админа)
    if is_admin:
        status_text = "🔒 Закрыть комнату" if is_open else "🔓 Открыть комнату"
        keyboard.add(
            InlineKeyboardButton(status_text, callback_data=f'room_toggle_{room_code}')
        )
        # Кнопка просмотра заявок (только для открытых комнат)
        if is_open:
            keyboard.add(
                InlineKeyboardButton('📩 Заявки на вступление', callback_data=f'room_requests_{room_code}')
            )
    
    keyboard.add(
        InlineKeyboardButton('📋 Участники', callback_data=f'room_members_{room_code}')
    )
    keyboard.add(
        InlineKeyboardButton('🚪 Выйти', callback_data=f'room_leave_{room_code}')
    )
    return keyboard

# ---------- КЛАВИАТУРА ОТКРЫТЫХ КОМНАТ ----------
def open_rooms_keyboard(rooms):
    keyboard = InlineKeyboardMarkup(row_width=1)
    for room in rooms:
        room_id, room_code, room_name, created_at, creator_id, members, has_request = room
        status = "⏳ Ожидание" if has_request else "✅ Вступить"
        keyboard.add(
            InlineKeyboardButton(f'🏠 {room_name} ({members}/10 чел.)', 
                               callback_data=f'room_join_open_{room_id}')
        )
    keyboard.add(
        InlineKeyboardButton('🔄 Обновить', callback_data='refresh_open_rooms')
    )
    keyboard.add(
        InlineKeyboardButton('🔙 Назад', callback_data='chat_back')
    )
    return keyboard

# ---------- КЛАВИАТУРА ЗАЯВОК НА ВСТУПЛЕНИЕ ----------
def join_requests_keyboard(requests, room_code):
    keyboard = InlineKeyboardMarkup(row_width=2)
    for req in requests:
        req_id, user_id, username, date = req
        keyboard.add(
            InlineKeyboardButton(f'✅ {username}', callback_data=f'req_approve_{req_id}_{room_code}'),
            InlineKeyboardButton(f'❌', callback_data=f'req_reject_{req_id}_{room_code}')
        )
    keyboard.add(
        InlineKeyboardButton('🔙 Назад', callback_data=f'room_back_{room_code}')
    )
    return keyboard