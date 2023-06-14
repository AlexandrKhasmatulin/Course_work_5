import psycopg2
import json
import os


class DBManager:
    def __init__(self):
        self.conn = psycopg2.connect(dbname='test', user='postgres', password='Alex030652', host='localhost')

    def create_tables(self):
        cur = self.conn.cursor()
        cur.execute("""
                    DROP TABLE IF EXISTS vacancies 
                    """)
        cur.execute("""
                CREATE TABLE IF NOT EXISTS vacancies (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                url TEXT NOT NULL,
                salary_min INTEGER,
                salary_max INTEGER,
                employer TEXT NOT NULL
                );
                """)
        if os.path.exists("C:\Dev\Course_work_5\Python.json"):
            with open("C:\Dev\Course_work_5\Python.json", encoding='utf-8') as jsonFile:
                templates = json.load(jsonFile)
                dumpsJson = json.dumps(templates, indent=4)
                loadsJson = json.loads(dumpsJson)
                for obj in loadsJson:
                    cur.execute(
                        """INSERT INTO vacancies (id, name, url, salary_min, salary_max, employer) VALUES (%s,%s,%s,%s,%s,%s)""",
                        (obj["id"], obj["title"], obj["url"], obj["salary_from"], obj["salary_to"], obj["employer"]))
        self.conn.commit()

    def get_companies_and_vacancies_count(self):
        """получает список всех компаний и количество вакансий у каждой компании."""

        cur = self.conn.cursor()
        cur.execute("""
                    CREATE TABLE IF NOT EXISTS companies_and_vacancies_count AS
                    SELECT vacancies.employer, COUNT(vacancies.id)
                    FROM vacancies
                    GROUP BY vacancies.employer
                    """)
        self.conn.commit()

    def get_avg_salary(self):
        """получает среднюю зарплату по вакансиям."""
        cur = self.conn.cursor()
        cur.execute("""
                    CREATE TABLE IF NOT EXISTS AVG_salary AS
                    SELECT AVG(vacancies.salary_max)
                    FROM vacancies
                    """)
        self.conn.commit()


    def get_vacancies_with_higher_salary(self):
        """получает cписок всех вакансий, у которых зарплата выше средней по всем вакансиям."""

        cur = self.conn.cursor()
        cur.execute("""
                        CREATE TABLE IF NOT EXISTS higher_salary AS
                        SELECT vacancies.employer, vacancies.url, vacancies.salary_max, vacancies.name
                        FROM vacancies
                        WHERE vacancies.salary_max > (SELECT AVG(vacancies.salary_max)
                        FROM vacancies)
                       """)
        self.conn.commit()





if __name__ == '__main__':
    db = DBManager()
    db.create_tables()
    db.get_vacancies_with_higher_salary()
    db.get_avg_salary()
    db.get_companies_and_vacancies_count()

