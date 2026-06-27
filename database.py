import sqlite3 as sq
import datetime

class DataBase:
    def __init__(self, db_file):
        self.connection = sq.connect(db_file)
        self.cur = self.connection.cursor()

    def db_start(self):
        with self.connection:
            # Таблица пользователей (расширенная)
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
            
            # Таблица администраторов
            self.cur.execute('CREATE TABLE IF NOT EXISTS admins('
                             'id INTEGER PRIMARY KEY AUTOINCREMENT,'
                             'user_id INTEGER UNIQUE,'
                             'username TEXT,'
                             'added_by INTEGER)')
            
            # Таблица каналов
            self.cur.execute('CREATE TABLE IF NOT EXISTS channels('
                             'id INTEGER PRIMARY KEY AUTOINCREMENT,'
                             'channel_id INTEGER UNIQUE,'
                             'channel_url TEXT,'
                             'channel_name TEXT,'
                             'added_by INTEGER,'
                             'is_active INTEGER DEFAULT 1)')
            
            # Таблица рейтинга (отзывы)
            self.cur.execute('CREATE TABLE IF NOT EXISTS ratings('
                             'id INTEGER PRIMARY KEY AUTOINCREMENT,'
                             'from_user INTEGER,'
                             'to_user INTEGER,'
                             'rating INTEGER,'
                             'comment TEXT,'
                             'date TEXT,'
                             'UNIQUE(from_user, to_user))')
            
            # Таблица для самоуничтожающихся сообщений
            self.cur.execute('CREATE TABLE IF NOT EXISTS self_destruct('
                             'id INTEGER PRIMARY KEY AUTOINCREMENT,'
                             'message_id INTEGER,'
                             'chat_id INTEGER,'
                             'destruct_time INTEGER,'
                             'created_at TEXT)')
            
            # Таблица достижений
            self.cur.execute('CREATE TABLE IF NOT EXISTS achievements('
                             'id INTEGER PRIMARY KEY AUTOINCREMENT,'
                             'user_id INTEGER,'
                             'achievement TEXT,'
                             'date TEXT,'
                             'UNIQUE(user_id, achievement))')
            
            # Таблица голосований
            self.cur.execute('CREATE TABLE IF NOT EXISTS polls('
                             'id INTEGER PRIMARY KEY AUTOINCREMENT,'
                             'creator_id INTEGER,'
                             'question TEXT,'
                             'options TEXT,'
                             'votes TEXT,'
                             'is_active INTEGER DEFAULT 1,'
                             'created_at TEXT)')
            
            # Таблица блокировок
            self.cur.execute('CREATE TABLE IF NOT EXISTS blocked('
                             'id INTEGER PRIMARY KEY AUTOINCREMENT,'
                             'blocker_id INTEGER,'
                             'blocked_id INTEGER,'
                             'reason TEXT,'
                             'date TEXT,'
                             'UNIQUE(blocker_id, blocked_id))')
            
            # Таблица автоответов
            self.cur.execute('CREATE TABLE IF NOT EXISTS auto_replies('
                             'id INTEGER PRIMARY KEY AUTOINCREMENT,'
                             'user_id INTEGER,'
                             'keyword TEXT,'
                             'reply TEXT,'
                             'is_active INTEGER DEFAULT 1)')
            
            # Таблица напоминаний
            self.cur.execute('CREATE TABLE IF NOT EXISTS reminders('
                             'id INTEGER PRIMARY KEY AUTOINCREMENT,'
                             'user_id INTEGER,'
                             'message TEXT,'
                             'remind_time TEXT,'
                             'is_done INTEGER DEFAULT 0)')

    # ---------- ПОЛЬЗОВАТЕЛИ ----------
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
            
            # Проверяем уровень
            stats = self.get_user_stats(user_id)
            if stats:
                level = stats[3]
                # Каждые 100 сообщений - новый уровень
                new_level = (stats[0] // 100) + 1
                if new_level > level:
                    self.cur.execute('UPDATE users SET level = ? WHERE user_id = ?', (new_level, user_id))
                    return new_level
            return None

    def get_user_level(self, user_id):
        with self.connection:
            result = self.cur.execute('SELECT level FROM users WHERE user_id = ?', (user_id,)).fetchone()
            return result[0] if result else 1

    def get_rating(self, user_id):
        with self.connection:
            result = self.cur.execute('SELECT rating FROM users WHERE user_id = ?', (user_id,)).fetchone()
            return result[0] if result else 0

    def update_rating(self, user_id, rating):
        with self.connection:
            self.cur.execute('UPDATE users SET rating = rating + ? WHERE user_id = ?', (rating, user_id))

    # ---------- РЕЙТИНГ ----------
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

    # ---------- ДОСТИЖЕНИЯ ----------
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
        
        # Проверяем достижения
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

    # ---------- АДМИНИСТРАТОРЫ ----------
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

    # ---------- КАНАЛЫ ----------
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

    # ---------- БЛОКИРОВКИ ----------
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

    # ---------- АВТООТВЕТЫ ----------
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

    # ---------- НАПОМИНАНИЯ ----------
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

    # ---------- ГОЛОСОВАНИЯ ----------
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

    # ---------- САМОУНИЧТОЖЕНИЕ ----------
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