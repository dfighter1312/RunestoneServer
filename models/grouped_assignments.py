db.define_table('assignments',
	Field('course',db.courses),
	Field('name', 'string'),
	Field('points', 'integer'),
	Field('query', 'string', default="", required=False),
	Field('grade_type', 'string', default="additive", requires=IS_IN_SET(['additive','checkmark'])),
	Field('threshold', 'integer', default=1),
	migrate='runestone_assignments.table'
	)

def assignment_get_problems(assignment, user):
	return db(db.code.acid.like(assignment.query+"%"))(db.code.sid==user.username).select(
		db.code.ALL,
		orderby=db.code.acid|~db.code.timestamp,
		distinct=db.code.acid,
		)
db.assignments.problems = Field.Method(lambda row, user: assignment_get_problems(row.assignments, user))
db.assignments.grade = Field.Method(lambda row, user: 10)

db.define_table('grades',
	Field('auth_user', db.auth_user),
	Field('assignment', db.assignments),
	Field('score', 'double'),
	migrate='runestone_grades.table',
	)