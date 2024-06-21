# lib/employee.py
from __init__ import CURSOR, CONN
from department import Department

class Employee:

    # Your existing Employee class implementation

    def reviews(self):
        from review import Review  # Avoid circular import
        CURSOR.execute('SELECT * FROM reviews WHERE employee_id=?', (self.id,))
        rows = CURSOR.fetchall()
        return [Review.instance_from_db(row) for row in rows]