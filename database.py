import sqlite3 as sq
import datetime
import random
import string

class DataBase:
    def __init__(self, db_file):
        self.connection = sq.connect(db_file)
        self.cur = self.connection.cursor()
def db_start(self):
    with self.connection:
        # ---------- ТАБЛИЦА ПОЛЬЗОВАТЕЛЕЙ ----------
        self.cur.execute('CREATE TABLE IF NOT EXISTS users('
                         'id INTEGER PRIMARY KEY AUTOINCREMENT,'
                         'user_id INTEGER UNIQUE,'
                         'username TEXT,'
                         'referi INTEGER,'
                         'username_referi TEXT,'
                         'rating INTEGER DEFAULT 0,'
                         'messages_sent INTEGER DEFAULT 0,'
                         'messages_received INTEGER DEFAULT 0,'
                         'level INTEGER DEFAULT 1,'
                         'join_date TEXT,'
                         'last_active TEXT,'
                         'language TEXT DEFAULT "ru",'
                         'is_blocked INTEGER DEFAULT 0)')
        
        # ---------- ТАБЛИЦА АДМИНИСТРАТОРОВ ----------
        self.cur.execute('CREATE TABLE IF NOT EXISTS admins('
                         'id INTEGER PRIMARY KEY AUTOINCREMENT,'
                         'user_id INTEGER UNIQUE,'
                         'username TEXT,'
                         'added_by INTEGER)')
        
        # ---------- ТАБЛИЦА КАНАЛОВ ----------
        self.cur.execute('CREATE TABLE IF NOT EXISTS channels('
                         'id INTEGER PRIMARY KEY AUTOINCREMENT,'
                         'channel_id INTEGER UNIQUE,'
                         'channel_url TEXT,'
                         'channel_name TEXT,'
                         'added_by INTEGER,'
                         'is_active INTEGER DEFAULT 1)')
        
        # ---------- ТАБЛИЦА РЕЙТИНГА ----------
        self.cur.execute('CREATE TABLE IF NOT EXISTS ratings('
                         'id INTEGER PRIMARY KEY AUTOINCREMENT,'
                         'from_user INTEGER,'
                         'to_user INTEGER,'
                         'rating INTEGER,'
                         'comment TEXT,'
                         'date TEXT,'
                         'UNIQUE(from_user, to_user))')
        
        # ---------- ТАБЛИЦА САМОУНИЧТОЖЕНИЯ ----------
        self.cur.execute('CREATE TABLE IF NOT EXISTS self_destruct('
                         'id INTEGER PRIMARY KEY AUTOINCREMENT,'
                         'message_id INTEGER,'
                         'chat_id INTEGER,'
                         'destruct_time INTEGER,'
                         'created_at TEXT)')
        
        # ---------- ТАБЛИЦА ДОСТИЖЕНИЙ ----------
        self.cur.execute('CREATE TABLE IF NOT EXISTS achievements('
                         'id INTEGER PRIMARY KEY AUTOINCREMENT,'
                         'user_id INTEGER,'
                         'achievement TEXT,'
                         'date TEXT,'
                         'UNIQUE(user_id, achievement))')
        
        # ---------- ТАБЛИЦА ГОЛОСОВАНИЙ ----------
        self.cur.execute('CREATE TABLE IF NOT EXISTS polls('
                         'id INTEGER PRIMARY KEY AUTOINCREMENT,'
                         'creator_id INTEGER,'
                         'question TEXT,'
                         'options TEXT,'
                         'votes TEXT,'
                         'is_active INTEGER DEFAULT 1,'
                         'created_at TEXT)')
        
        # ---------- ТАБЛИЦА БЛОКИРОВОК ----------
        self.cur.execute('CREATE TABLE IF NOT EXISTS blocked('
                         'id INTEGER PRIMARY KEY AUTOINCREMENT,'
                         'blocker_id INTEGER,'
                         'blocked_id INTEGER,'
                         'reason TEXT,'
                         'date TEXT,'
                         'UNIQUE(blocker_id, blocked_id))')
        
        # ---------- ТАБЛИЦА АВТООТВЕТОВ ----------
        self.cur.execute('CREATE TABLE IF NOT EXISTS auto_replies('
                         'id INTEGER PRIMARY KEY AUTOINCREMENT,'
                         'user_id INTEGER,'
                         'keyword TEXT,'
                         'reply TEXT,'
                         'is_active INTEGER DEFAULT 1)')
        
        # ---------- ТАБЛИЦА НАПОМИНАНИЙ ----------
        self.cur.execute('CREATE TABLE IF NOT EXISTS reminders('
                         'id INTEGER PRIMARY KEY AUTOINCREMENT,'
                         'user_id INTEGER,'
                         'message TEXT,'
                         'remind_time TEXT,'
                         'is_done INTEGER DEFAULT 0)')
        
        # ---------- ТАБЛИЦА АНОНИМНЫХ КОМНАТ ----------
        self.cur.execute('CREATE TABLE IF NOT EXISTS chat_rooms('
                         'id INTEGER PRIMARY KEY AUTOINCREMENT,'
                         'room_code TEXT UNIQUE,'
                         'creator_id INTEGER,'
                         'room_name TEXT,'
                         'created_at TEXT,'
                         'is_active INTEGER DEFAULT 1,'
                         'is_open INTEGER DEFAULT 0,'
                         'max_members INTEGER DEFAULT 10)')
        
        # ---------- ТАБЛИЦА УЧАСТНИКОВ КОМНАТ ----------
        self.cur.execute('CREATE TABLE IF NOT EXISTS room_members('
                         'id INTEGER PRIMARY KEY AUTOINCREMENT,'
                         'room_id INTEGER,'
                         'user_id INTEGER,'
                         'anonymous_name TEXT,'
                         'join_date TEXT,'
                         'is_admin INTEGER DEFAULT 0,'
                         'UNIQUE(room_id, user_id))')
        
        # ---------- ТАБЛИЦА СООБЩЕНИЙ В КОМНАТАХ ----------
        self.cur.execute('CREATE TABLE IF NOT EXISTS room_messages('
                         'id INTEGER PRIMARY KEY AUTOINCREMENT,'
                         'room_id INTEGER,'
                         'user_id INTEGER,'
                         'anonymous_name TEXT,'
                         'message TEXT,'
                         'message_type TEXT DEFAULT "text",'
                         'file_id TEXT,'
                         'sent_at TEXT)')
        
        # ---------- ТАБЛИЦА ЗАПРОСОВ НА ВСТУПЛЕНИЕ ----------
        self.cur.execute('CREATE TABLE IF NOT EXISTS room_requests('
                         'id INTEGER PRIMARY KEY AUTOINCREMENT,'
                         'room_id INTEGER,'
                         'user_id INTEGER,'
                         'status TEXT DEFAULT "pending",'
                         'request_date TEXT,'
                         'UNIQUE(room_id, user_id))')
# ==========================================
# ПОЛЬЗОВАТЕЛИ
# ==========================================

def user_exists(self, user_id):
    with self.connection:
        result = self.cur.execute('SELECT * FROM users WHERE user_id = ?', (user_id,)).fetchall()
        return bool(len(result))

def add_user(self, user_id, username):
    with self.connection:
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            self.cur.execute('INSERT INTO users (user_id, username, join_date, last_active) VALUES (?, ?, ?, ?)',
                           (user_id, username, now, now))
            return True
        except:
            return False

def add_user_referi(self, user_id, username, refere_id, username_referi):
    with self.connection:
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return self.cur.execute('INSERT INTO users (user_id, username, referi, username_referi, join_date, last_active) VALUES (?, ?, ?, ?, ?, ?)',
                               (user_id, username, refere_id, username_referi, now, now))

def add_user_no_referi(self, user_id, username, referi):
    with self.connection:
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return self.cur.execute('INSERT INTO users (user_id, username, referi, join_date, last_active) VALUES (?, ?, ?, ?, ?)',
                               (user_id, username, referi, now, now))

def username_referi(self, user):
    with self.connection:
        result = self.cur.execute('SELECT username FROM users WHERE user_id = ?', (user,)).fetchall()
        if result:
            return result[0]
        return None

def update_user_activity(self, user_id):
    with self.connection:
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.cur.execute('UPDATE users SET last_active = ? WHERE user_id = ?', (now, user_id))

def get_user_stats(self, user_id):
    with self.connection:
        return self.cur.execute('SELECT messages_sent, messages_received, rating, level FROM users WHERE user_id = ?', 
                               (user_id,)).fetchone()

def increment_messages(self, user_id, sent=True):
    with self.connection:
        if sent:
            self.cur.execute('UPDATE users SET messages_sent = messages_sent + 1 WHERE user_id = ?', (user_id,))
        else:
            self.cur.execute('UPDATE users SET messages_received = messages_received + 1 WHERE user_id = ?', (user_id,))
        
        stats = self.get_user_stats(user_id)
        if stats:
            level = stats[3]
            new_level = (stats[0] // 100) + 1
            if new_level > level:
                self.cur.execute('UPDATE users SET level = ? WHERE user_id = ?', (new_level, user_id))
                return new_level
        return None

def get_rating(self, user_id):
    with self.connection:
        result = self.cur.execute('SELECT rating FROM users WHERE user_id = ?', (user_id,)).fetchone()
        return result[0] if result else 0

def update_rating(self, user_id, rating):
    with self.connection:
        self.cur.execute('UPDATE users SET rating = rating + ? WHERE user_id = ?', (rating, user_id))
# ==========================================
# АДМИНИСТРАТОРЫ
# ==========================================

def is_admin(self, user_id):
    with self.connection:
        result = self.cur.execute('SELECT * FROM admins WHERE user_id = ?', (user_id,)).fetchall()
        return bool(len(result))

def add_admin(self, user_id, username, added_by):
    with self.connection:
        try:
            self.cur.execute('INSERT INTO admins (user_id, username, added_by) VALUES (?, ?, ?)',
                           (user_id, username, added_by))
            return True
        except:
            return False

def remove_admin(self, user_id):
    with self.connection:
        self.cur.execute('DELETE FROM admins WHERE user_id = ?', (user_id,))
        return True

def get_all_admins(self):
    with self.connection:
        return self.cur.execute('SELECT user_id, username FROM admins').fetchall()

# ==========================================
# КАНАЛЫ
# ==========================================

def add_channel(self, channel_id, channel_url, channel_name, added_by):
    with self.connection:
        try:
            self.cur.execute('INSERT INTO channels (channel_id, channel_url, channel_name, added_by) VALUES (?, ?, ?, ?)',
                           (channel_id, channel_url, channel_name, added_by))
            return True
        except:
            return False

def remove_channel(self, channel_id):
    with self.connection:
        self.cur.execute('DELETE FROM channels WHERE channel_id = ?', (channel_id,))
        return True

def get_all_channels(self):
    with self.connection:
        return self.cur.execute('SELECT channel_id, channel_url, channel_name, is_active FROM channels').fetchall()

def get_active_channels(self):
    with self.connection:
        return self.cur.execute('SELECT channel_id, channel_url, channel_name FROM channels WHERE is_active = 1').fetchall()
# ==========================================
# РЕЙТИНГ
# ==========================================

def add_rating(self, from_user, to_user, rating, comment=''):
    with self.connection:
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            self.cur.execute('INSERT INTO ratings (from_user, to_user, rating, comment, date) VALUES (?, ?, ?, ?, ?)',
                           (from_user, to_user, rating, comment, now))
            self.update_rating(to_user, rating)
            return True
        except:
            return False

def get_user_rating(self, user_id):
    with self.connection:
        ratings = self.cur.execute('SELECT rating FROM ratings WHERE to_user = ?', (user_id,)).fetchall()
        if ratings:
            return sum(r[0] for r in ratings) // len(ratings)
        return 0

# ==========================================
# ДОСТИЖЕНИЯ
# ==========================================

def add_achievement(self, user_id, achievement):
    with self.connection:
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            self.cur.execute('INSERT INTO achievements (user_id, achievement, date) VALUES (?, ?, ?)',
                           (user_id, achievement, now))
            return True
        except:
            return False

def get_achievements(self, user_id):
    with self.connection:
        return self.cur.execute('SELECT achievement, date FROM achievements WHERE user_id = ?', (user_id,)).fetchall()

def check_achievements(self, user_id):
    stats = self.get_user_stats(user_id)
    if not stats:
        return []
    
    msgs_sent, msgs_received, rating, level = stats
    achievements = []
    
    if msgs_sent >= 1:
        achievements.append('📬 Первое сообщение')
    if msgs_sent >= 10:
        achievements.append('💬 Активный новичок')
    if msgs_sent >= 50:
        achievements.append('🗣️ Говорун')
    if msgs_sent >= 100:
        achievements.append('📢 Мастер общения')
    if msgs_sent >= 500:
        achievements.append('👑 Легенда чата')
    if rating >= 10:
        achievements.append('⭐ Любимчик')
    if rating >= 50:
        achievements.append('🌟 Суперзвезда')
    if level >= 5:
        achievements.append('🏆 Опытный')
    if level >= 10:
        achievements.append('🎖️ Ветеран')
    if level >= 25:
        achievements.append('👾 Легенда')
    
    return achievements
# ==========================================
# БЛОКИРОВКИ
# ==========================================

def block_user(self, blocker_id, blocked_id, reason=''):
    with self.connection:
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            self.cur.execute('INSERT INTO blocked (blocker_id, blocked_id, reason, date) VALUES (?, ?, ?, ?)',
                           (blocker_id, blocked_id, reason, now))
            return True
        except:
            return False

def unblock_user(self, blocker_id, blocked_id):
    with self.connection:
        self.cur.execute('DELETE FROM blocked WHERE blocker_id = ? AND blocked_id = ?', (blocker_id, blocked_id))
        return True

def is_blocked(self, blocker_id, blocked_id):
    with self.connection:
        result = self.cur.execute('SELECT * FROM blocked WHERE blocker_id = ? AND blocked_id = ?', 
                                 (blocker_id, blocked_id)).fetchall()
        return bool(len(result))

def get_blocked_users(self, user_id):
    with self.connection:
        return self.cur.execute('SELECT blocked_id, reason FROM blocked WHERE blocker_id = ?', (user_id,)).fetchall()

# ==========================================
# АВТООТВЕТЫ
# ==========================================

def add_auto_reply(self, user_id, keyword, reply):
    with self.connection:
        try:
            self.cur.execute('INSERT INTO auto_replies (user_id, keyword, reply) VALUES (?, ?, ?)',
                           (user_id, keyword, reply))
            return True
        except:
            return False

def remove_auto_reply(self, user_id, keyword):
    with self.connection:
        self.cur.execute('DELETE FROM auto_replies WHERE user_id = ? AND keyword = ?', (user_id, keyword))
        return True

def get_auto_replies(self, user_id):
    with self.connection:
        return self.cur.execute('SELECT keyword, reply FROM auto_replies WHERE user_id = ? AND is_active = 1', 
                               (user_id,)).fetchall()

# ==========================================
# НАПОМИНАНИЯ
# ==========================================

def add_reminder(self, user_id, message, remind_time):
    with self.connection:
        self.cur.execute('INSERT INTO reminders (user_id, message, remind_time) VALUES (?, ?, ?)',
                       (user_id, message, remind_time))
        return True

def get_pending_reminders(self):
    with self.connection:
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        return self.cur.execute('SELECT id, user_id, message FROM reminders WHERE remind_time <= ? AND is_done = 0', 
                               (now,)).fetchall()

def mark_reminder_done(self, reminder_id):
    with self.connection:
        self.cur.execute('UPDATE reminders SET is_done = 1 WHERE id = ?', (reminder_id,))

def get_reminders(self, user_id):
    with self.connection:
        return self.cur.execute('SELECT id, message, remind_time, is_done FROM reminders WHERE user_id = ?', 
                               (user_id,)).fetchall()
# ==========================================
# ГОЛОСОВАНИЯ
# ==========================================

def create_poll(self, creator_id, question, options):
    with self.connection:
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        options_str = '|'.join(options)
        votes_str = '|'.join('0' for _ in options)
        self.cur.execute('INSERT INTO polls (creator_id, question, options, votes, created_at) VALUES (?, ?, ?, ?, ?)',
                       (creator_id, question, options_str, votes_str, now))
        return self.cur.lastrowid

def get_poll(self, poll_id):
    with self.connection:
        return self.cur.execute('SELECT * FROM polls WHERE id = ?', (poll_id,)).fetchone()

def vote_poll(self, poll_id, option_index):
    with self.connection:
        poll = self.get_poll(poll_id)
        if not poll or not poll[5]:
            return False
        votes = poll[4].split('|')
        if option_index >= len(votes):
            return False
        votes[option_index] = str(int(votes[option_index]) + 1)
        self.cur.execute('UPDATE polls SET votes = ? WHERE id = ?', ('|'.join(votes), poll_id))
        return True

def close_poll(self, poll_id):
    with self.connection:
        self.cur.execute('UPDATE polls SET is_active = 0 WHERE id = ?', (poll_id,))
        return True

# ==========================================
# САМОУНИЧТОЖЕНИЕ
# ==========================================

def add_self_destruct(self, message_id, chat_id, seconds):
    with self.connection:
        now = datetime.datetime.now().timestamp()
        self.cur.execute('INSERT INTO self_destruct (message_id, chat_id, destruct_time, created_at) VALUES (?, ?, ?, ?)',
                       (message_id, chat_id, int(now + seconds), datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        return True

def get_expired_messages(self):
    with self.connection:
        now = datetime.datetime.now().timestamp()
        return self.cur.execute('SELECT id, message_id, chat_id FROM self_destruct WHERE destruct_time <= ?', 
                               (now,)).fetchall()

def delete_self_destruct(self, record_id):
    with self.connection:
        self.cur.execute('DELETE FROM self_destruct WHERE id = ?', (record_id,))
# ==========================================
# АНОНИМНЫЕ КОМНАТЫ
# ==========================================

def create_room(self, creator_id, room_name, max_members=10, is_open=0):
    with self.connection:
        # Генерируем уникальный код комнаты (6 символов)
        while True:
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            if not self.cur.execute('SELECT id FROM chat_rooms WHERE room_code = ?', (code,)).fetchone():
                break
        
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.cur.execute('INSERT INTO chat_rooms (room_code, creator_id, room_name, created_at, max_members, is_open) VALUES (?, ?, ?, ?, ?, ?)',
                       (code, creator_id, room_name, now, max_members, is_open))
        room_id = self.cur.lastrowid
        
        # Добавляем создателя как участника и администратора
        anon_name = self.get_anonymous_name(creator_id, room_id)
        self.cur.execute('INSERT INTO room_members (room_id, user_id, anonymous_name, join_date, is_admin) VALUES (?, ?, ?, ?, 1)',
                       (room_id, creator_id, anon_name, now))
        return room_id, code

def get_room(self, room_code):
    with self.connection:
        return self.cur.execute('SELECT * FROM chat_rooms WHERE room_code = ? AND is_active = 1', (room_code,)).fetchone()

def get_room_by_id(self, room_id):
    with self.connection:
        return self.cur.execute('SELECT * FROM chat_rooms WHERE id = ? AND is_active = 1', (room_id,)).fetchone()

def get_all_open_rooms(self, user_id):
    """Получает все открытые комнаты, в которых пользователь ещё не состоит"""
    with self.connection:
        return self.cur.execute('''
            SELECT cr.id, cr.room_code, cr.room_name, cr.created_at, cr.creator_id,
                   (SELECT COUNT(*) FROM room_members WHERE room_id = cr.id) as members,
                   (SELECT COUNT(*) FROM room_requests WHERE room_id = cr.id AND user_id = ? AND status = "pending") as has_request
            FROM chat_rooms cr
            WHERE cr.is_active = 1 
            AND cr.is_open = 1
            AND cr.id NOT IN (SELECT room_id FROM room_members WHERE user_id = ?)
        ''', (user_id, user_id)).fetchall()

def get_room_members(self, room_id):
    with self.connection:
        return self.cur.execute('SELECT user_id, anonymous_name, is_admin FROM room_members WHERE room_id = ?', (room_id,)).fetchall()

def get_room_member(self, room_id, user_id):
    with self.connection:
        return self.cur.execute('SELECT * FROM room_members WHERE room_id = ? AND user_id = ?', (room_id, user_id)).fetchone()

def get_anonymous_name(self, user_id, room_id):
    with self.connection:
        member = self.cur.execute('SELECT anonymous_name FROM room_members WHERE room_id = ? AND user_id = ?', 
                                 (room_id, user_id)).fetchone()
        if member:
            return member[0]
        
        # Генерируем анонимное имя
        names = ['Кот', 'Пёс', 'Лиса', 'Волк', 'Медведь', 'Заяц', 'Ёж', 'Сова', 'Орёл', 'Дельфин', 'Тигр', 'Лев']
        name = random.choice(names) + str(random.randint(1, 999))
        
        # Проверяем, что имя не занято
        existing = self.cur.execute('SELECT anonymous_name FROM room_members WHERE room_id = ? AND anonymous_name = ?', 
                                   (room_id, name)).fetchone()
        while existing:
            name = random.choice(names) + str(random.randint(1, 999))
            existing = self.cur.execute('SELECT anonymous_name FROM room_members WHERE room_id = ? AND anonymous_name = ?', 
                                       (room_id, name)).fetchone()
        return name

def join_room(self, room_code, user_id):
    with self.connection:
        room = self.get_room(room_code)
        if not room:
            return False, "Комната не найдена или неактивна"
        
        room_id = room[0]
        
        if self.get_room_member(room_id, user_id):
            return False, "Вы уже в этой комнате"
        
        members = self.cur.execute('SELECT COUNT(*) FROM room_members WHERE room_id = ?', (room_id,)).fetchone()[0]
        if members >= room[7]:  # max_members
            return False, "Комната заполнена"
        
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        anon_name = self.get_anonymous_name(user_id, room_id)
        self.cur.execute('INSERT INTO room_members (room_id, user_id, anonymous_name, join_date) VALUES (?, ?, ?, ?)',
                       (room_id, user_id, anon_name, now))
        return True, anon_name

def leave_room(self, room_id, user_id):
    with self.connection:
        self.cur.execute('DELETE FROM room_members WHERE room_id = ? AND user_id = ?', (room_id, user_id))
        
        # Если участников не осталось, закрываем комнату
        members = self.cur.execute('SELECT COUNT(*) FROM room_members WHERE room_id = ?', (room_id,)).fetchone()[0]
        if members == 0:
            self.cur.execute('UPDATE chat_rooms SET is_active = 0 WHERE id = ?', (room_id,))
        return True

def toggle_room_type(self, room_id):
    """Переключает тип комнаты: открытая/закрытая"""
    with self.connection:
        room = self.cur.execute('SELECT is_open FROM chat_rooms WHERE id = ?', (room_id,)).fetchone()
        if room:
            new_status = 0 if room[0] == 1 else 1
            self.cur.execute('UPDATE chat_rooms SET is_open = ? WHERE id = ?', (new_status, room_id))
            return new_status
        return None

def get_user_rooms(self, user_id):
    with self.connection:
        return self.cur.execute('''
            SELECT cr.id, cr.room_code, cr.room_name, cr.created_at, cr.is_open,
                   (SELECT COUNT(*) FROM room_members WHERE room_id = cr.id) as members
            FROM chat_rooms cr
            JOIN room_members rm ON cr.id = rm.room_id
            WHERE rm.user_id = ? AND cr.is_active = 1
        ''', (user_id,)).fetchall()

def save_room_message(self, room_id, user_id, anonymous_name, message, message_type='text', file_id=None):
    with self.connection:
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.cur.execute('INSERT INTO room_messages (room_id, user_id, anonymous_name, message, message_type, file_id, sent_at) VALUES (?, ?, ?, ?, ?, ?, ?)',
                       (room_id, user_id, anonymous_name, message, message_type, file_id, now))
        return self.cur.lastrowid

def get_room_messages(self, room_id, limit=50):
    with self.connection:
        return self.cur.execute('''
            SELECT anonymous_name, message, message_type, file_id, sent_at 
            FROM room_messages 
            WHERE room_id = ? 
            ORDER BY id DESC 
            LIMIT ?
        ''', (room_id, limit)).fetchall()[::-1]
# ==========================================
# ЗАПРОСЫ НА ВСТУПЛЕНИЕ В КОМНАТЫ
# ==========================================

def add_join_request(self, room_id, user_id):
    with self.connection:
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            self.cur.execute('INSERT INTO room_requests (room_id, user_id, request_date) VALUES (?, ?, ?)',
                           (room_id, user_id, now))
            return True
        except:
            return False

def get_join_requests(self, room_id):
    with self.connection:
        return self.cur.execute('''
            SELECT rr.id, rr.user_id, u.username, rr.request_date
            FROM room_requests rr
            JOIN users u ON rr.user_id = u.user_id
            WHERE rr.room_id = ? AND rr.status = "pending"
        ''', (room_id,)).fetchall()

def approve_join_request(self, request_id, room_id, user_id):
    with self.connection:
        # Обновляем статус запроса
        self.cur.execute('UPDATE room_requests SET status = "approved" WHERE id = ?', (request_id,))
        # Добавляем пользователя в комнату
        now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        anon_name = self.get_anonymous_name(user_id, room_id)
        self.cur.execute('INSERT INTO room_members (room_id, user_id, anonymous_name, join_date) VALUES (?, ?, ?, ?)',
                       (room_id, user_id, anon_name, now))
        return True

def reject_join_request(self, request_id):
    with self.connection:
        self.cur.execute('UPDATE room_requests SET status = "rejected" WHERE id = ?', (request_id,))
        return True