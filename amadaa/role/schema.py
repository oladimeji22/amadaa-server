import uuid
import psycopg2.extras
import amadaa.database
from amadaa.schema import set_schema_version

conn = amadaa.database.connection()
if not amadaa.database.table_exists('am_role'):
	with conn:
		with conn.cursor() as cur:
			cur.execute("""create table am_role(
			role_pk uuid,
			rolename varchar(40) not null,
			parent_fk uuid references am_role,
			primary key(role_pk),
			unique(rolename))""")
	set_schema_version(__package__, 1)