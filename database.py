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
            # ... (все старые таблицы остаются)
            
            # НОВАЯ ТАБЛИЦА: Анонимные комнаты (ОБНОВЛЕННАЯ)
            self.cur.execute('CREATE TABLE IF NOT EXISTS chat_rooms('
                             'id INTEGER PRIMARY KEY AUTOINCREMENT,'
                             'room_code TEXT UNIQUE,'
                             'creator_id INTEGER,'
                             'room_name TEXT,'
                             'created_at TEXT,'
                             'is_active INTEGER DEFAULT 1,'
                             'is_open INTEGER DEFAULT 0,'  # 0 - закрытая (по коду), 1 - открытая
                             'max_members INTEGER DEFAULT 10)')
            
            # НОВАЯ ТАБЛИЦА: Участники комнат
            self.cur.execute('CREATE TABLE IF NOT EXISTS room_members('
                             'id INTEGER PRIMARY KEY AUTOINCREMENT,'
                             'room_id INTEGER,'
                             'user_id INTEGER,'
                             'anonymous_name TEXT,'
                             'join_date TEXT,'
                             'is_admin INTEGER DEFAULT 0,'
                             'UNIQUE(room_id, user_id))')
            
            # НОВАЯ ТАБЛИЦА: Сообщения в комнатах
            self.cur.execute('CREATE TABLE IF NOT EXISTS room_messages('
                             'id INTEGER PRIMARY KEY AUTOINCREMENT,'
                             'room_id INTEGER,'
                             'user_id INTEGER,'
                             'anonymous_name TEXT,'
                             'message TEXT,'
                             'message_type TEXT DEFAULT "text",'
                             'file_id TEXT,'
                             'sent_at TEXT)')
            
            # НОВАЯ ТАБЛИЦА: Запросы на вступление в открытые комнаты
            self.cur.execute('CREATE TABLE IF NOT EXISTS room_requests('
                             'id INTEGER PRIMARY KEY AUTOINCREMENT,'
                             'room_id INTEGER,'
                             'user_id INTEGER,'
                             'status TEXT DEFAULT "pending",'
                             'request_date TEXT,'
                             'UNIQUE(room_id, user_id))')

    # ---------- КОМНАТЫ ----------
    def create_room(self, creator_id, room_name, max_members=10, is_open=0):
        with self.connection:
            # Генерируем уникальный код комнаты
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
            
            # Проверяем, не в комнате ли уже пользователь
            if self.get_room_member(room_id, user_id):
                return False, "Вы уже в этой комнате"
            
            # Проверяем количество участников
            members = self.cur.execute('SELECT COUNT(*) FROM room_members WHERE room_id = ?', (room_id,)).fetchone()[0]
            if members >= room[6]:  # max_members
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

    # ---------- ЗАПРОСЫ НА ВСТУПЛЕНИЕ ----------
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
