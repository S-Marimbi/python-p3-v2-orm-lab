from __init__ import CURSOR, CONN
from department import Department
from employee import Employee


class Review:
    _instances = {}

    def _init_(self, year, summary, employee_id, id=None):
        self.id = id
        self.year = year
        self.summary = summary
        self.employee_id = employee_id

    def _repr_(self):
        return f"Review(id={self.id}, year={self.year}, summary='{self.summary}', employee_id={self.employee_id})"

    def _repr_(self):
        return f"Review(id={self.id}, year={self.year}, summary='{self.summary}', employee_id={self.employee_id})"

    @classmethod
    def create_table(cls):
        CURSOR.execute('''
            CREATE TABLE IF NOT EXISTS reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                year INTEGER NOT NULL,
                summary TEXT NOT NULL,
                employee_id INTEGER NOT NULL,
                FOREIGN KEY (employee_id) REFERENCES employees(id)
            )
        ''')
        CONN.commit()

    @classmethod
    def drop_table(cls):
        CURSOR.execute('DROP TABLE IF EXISTS reviews')
        CONN.commit()

    def save(self):
        if self.id is None:
            CURSOR.execute('''
                INSERT INTO reviews (year, summary, employee_id)
                VALUES (?, ?, ?)
            ''', (self.year, self.summary, self.employee_id))
            self.id = CURSOR.lastrowid
            CONN.commit()
            self._instances[self.id] = self
        else:
            CURSOR.execute('''
                UPDATE reviews
                SET year=?, summary=?, employee_id=?
                WHERE id=?
            ''', (self.year, self.summary, self.employee_id, self.id))
            CONN.commit()
            self._instances[self.id] = self

    @classmethod
    def create(cls, year, summary, employee_id):
        review = cls(year, summary, employee_id)
        review.save()
        return review

    @classmethod
    def instance_from_db(cls, row):
        review_id = row['id']
        if review_id in cls._instances:
            return cls._instances[review_id]
        else:
            review = cls(row['year'], row['summary'], row['employee_id'], id=row['id'])
            cls._instances[review_id] = review
            return review

    @classmethod
    def find_by_id(cls, review_id):
        CURSOR.execute('SELECT * FROM reviews WHERE id=?', (review_id,))
        row = CURSOR.fetchone()
        if row:
            return cls.instance_from_db(row)
        else:
            return None

    def update(self):
        self.save()

    def delete(self):
        if self.id:
            CURSOR.execute('DELETE FROM reviews WHERE id=?', (self.id,))
            CONN.commit()
            if self.id in self._instances:
                del self._instances[self.id]
            self.id = None

    @classmethod
    def get_all(cls):
        CURSOR.execute('SELECT * FROM reviews')
        rows = CURSOR.fetchall()
        return [cls.instance_from_db(row) for row in rows]

    @property
    def year(self):
        return self._year

    @year.setter
    def year(self, value):
        if not isinstance(value, int):
            raise ValueError("Year must be an integer")
        if value < 2000:
            raise ValueError("Year must be greater than or equal to 2000")
        self._year = value

    @property
    def summary(self):
        return self._summary

    @summary.setter
    def summary(self, value):
        if not isinstance(value, str) or len(value.strip()) == 0:
            raise ValueError("Summary must be a non-empty string")
        self._summary = value

    @property
    def employee_id(self):
        return self._employee_id

    @employee_id.setter
    def employee_id(self, value):
        from employee import Employee  # Avoid circular import
        employee = Employee.find_by_id(value)
        if not employee:
            raise ValueError(f"Employee with id {value} does not exist")
        self._employee_id = value