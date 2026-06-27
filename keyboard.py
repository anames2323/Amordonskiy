from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

# Кнопка "Отмена"
kb_back = ReplyKeyboardMarkup(resize_keyboard=True)
kb1 = KeyboardButton('Отмена ❌')
kb_back.add(kb1)

# Клавиатура для обычного пользователя
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
        KeyboardButton('🚫 Заблокированные')
    )
    return keyboard

# Главная клавиатура для админа
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

# Клавиатура управления каналами
def channels_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton('➕ Добавить канал', callback_data='add_channel'),
        InlineKeyboardButton('📋 Список каналов', callback_data='list_channels'),
        InlineKeyboardButton('❌ Удалить канал', callback_data='remove_channel'),
        InlineKeyboardButton('🔙 Назад', callback_data='admin_back')
    )
    return keyboard

# Клавиатура управления админами
def admins_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton('➕ Добавить админа', callback_data='add_admin'),
        InlineKeyboardButton('📋 Список админов', callback_data='list_admins'),
        InlineKeyboardButton('❌ Удалить админа', callback_data='remove_admin'),
        InlineKeyboardButton('🔙 Назад', callback_data='admin_back')
    )
    return keyboard

# Клавиатура для голосований
def poll_keyboard(options, poll_id):
    keyboard = InlineKeyboardMarkup(row_width=1)
    for i, option in enumerate(options):
        keyboard.add(
            InlineKeyboardButton(f'{option}', callback_data=f'poll_{poll_id}_{i}')
        )
    keyboard.add(
        InlineKeyboardButton('🔒 Закрыть голосование', callback_data=f'close_poll_{poll_id}')
    )
    return keyboard

# Клавиатура для самоуничтожения
def self_destruct_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton('⏳ 30 сек', callback_data='sd_30'),
        InlineKeyboardButton('⏳ 1 мин', callback_data='sd_60'),
        InlineKeyboardButton('⏳ 5 мин', callback_data='sd_300'),
        InlineKeyboardButton('⏳ 1 час', callback_data='sd_3600')
    )
    keyboard.add(
        InlineKeyboardButton('❌ Отмена', callback_data='sd_cancel')
    )
    return keyboard

# Кнопка для ответа на сообщение
def send_message(user_id):
    ikb_send_message = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('Ответить 📩', callback_data=f'send|{user_id}')],
        [InlineKeyboardButton('⭐ Оценить', callback_data=f'rate|{user_id}')],
        [InlineKeyboardButton('🚫 Заблокировать', callback_data=f'block|{user_id}')]
    ])
    return ikb_send_message