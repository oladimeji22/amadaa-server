import datetime
import uuid
import amadaa.database
from psycopg2.extras import DictCursor, register_uuid
from amadaa.base import Model

register_uuid()

class Role(Model):
	def __init__(self):
		super().__init__()
		self._attribs.update({
			'rolename': str,
			'parent': uuid.UUID
		})
		self.rolename = None
		self.parent = None
		
	def get(self, id):
		conn = amadaa.database.connection()
		with conn:
			with conn.cursor(cursor_factory=DictCursor) as cur:
				cur.execute("""select * from am_role
				where role_pk = %s""", (id,))
				rec = cur.fetchone()
				self.id = rec['role_pk']
				self.rolename = rec['rolename']
				self.parent = rec['parent']
		conn.close()
		
	def get_by_rolename(self, rolename):
		conn = amadaa.database.connection()
		with conn:
			with conn.cursor(cursor_factory=DictCursor) as cur:
				cur.execute("""select * from am_role
				where rolename = %s""", (rolename,))
				rec = cur.fetchone()
				self.id = rec['role_pk']
				self.rolename = rec['rolename']
				self.parent = rec['parent_fk']
		conn.close()
		
	def _insert(self):
		conn = amadaa.database.connection()
		with conn:
			with conn.cursor() as cur:
				self.id = uuid.uuid4()
				cur.execute("""insert into am_role(role_pk, rolename, parent_fk)
				values(%s, %s, %s)""", (self.id, self.rolename, self.parent))
		conn.close()
		
	def _update(self):
		conn = amadaa.database.connection()
		with conn:
			with conn.cursor() as cur:
				cur.execute("""update am_role set rolename = %s, parent = %s
				where role_pk = %s""", (self.rolename, self.parent_fk, self.id))
		conn.close()
		
class RoleDirectory:
	def id_exists(self, id):
		conn = amadaa.database.connection()
		with conn:
			with conn.cursor() as cur:
				cur.execute("select * from am_role where role_pk = %s", (id,))
				rec = cur.fetchone()
				ret = True if rec else False
		conn.close()
		return ret

	def rolename_exists(self, rolename):
		conn = amadaa.database.connection()
		with conn:
			with conn.cursor() as cur:
				cur.execute("select * from am_role where rolename = %s", (rolename,))
				rec = cur.fetchone()
				ret = True if rec else False
		conn.close()
		return ret

class User(Model):
	def __init__(self, id=None):
		super().__init__()
		self._attribs.update({
			'username': str,
			'password': str,
			'date_created': datetime,
			'last_login': datetime,
			'active': bool
		})
		self.username = None
		self.password = None
		self.date_created = None
		self.last_login = None
		self.active = None

	def get(self, id):
		conn = amadaa.database.connection()
		with conn:
			with conn.cursor(cursor_factory=DictCursor) as cur:
				cur.execute("""select * from am_user
				where user_pk = %s""", (id,))
				rec = cur.fetchone()
				self.id = rec['user_pk']
				self.username = rec['username']
				self.password = rec['password']
		conn.close()

	def get_by_username(self, username):
		conn = amadaa.database.connection()
		with conn:
			with conn.cursor(cursor_factory=DictCursor) as cur:
				cur.execute("""select * from am_user
				where username = %s""", (username,))
				rec = cur.fetchone()
				self.id = rec['user_pk']
				self.username = rec['username']
				self.password = rec['password']
				self.active = rec['active']
		conn.close()

	def _insert(self):
		conn = amadaa.database.connection()
		with conn:
			with conn.cursor() as cur:
				self.id = uuid.uuid4()
				cur.execute("""insert into am_user(user_pk, username, password, active)
				values(%s, %s, %s, %s)""", (self.id, self.username, self.password, self.active))
		conn.close()

	def _update(self):
		conn = amadaa.database.connection()
		with conn:
			with conn.cursor() as cur:
				cur.execute("""update am_user set username = %s, password = %s, active = %s
				where user_pk = %s""", (self.username, self.password, self.active, self.id))
		conn.close()

class UserDirectory:
	def __init__(self):
		pass
		
	def id_exists(self, uid):
		conn = amadaa.database.connection()
		with conn:
			with conn.cursor() as cur:
				cur.execute("select * from am_user where user_pk = %s", (uid,))
				rec = cur.fetchone()
				if rec:
					ret = True
				else:
					ret = False
		conn.close()
		return ret
	
	def username_exists(self, username):
		conn = amadaa.database.connection()
		with conn:
			with conn.cursor() as cur:
				cur.execute("select * from am_user where username = %s", (username,))
				rec = cur.fetchone()
				if rec:
					ret = True
				else:
					ret = False
		conn.close()
		return ret
