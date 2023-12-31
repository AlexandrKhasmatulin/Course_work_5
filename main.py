from utils.hh import HeadHunter, Connector
from db import DBManager

def main():
    vacancies_json = []
    keyword = input('Введите ключевое слово для поиска: ')

    hh = HeadHunter(keyword)
    for api in (hh,):
        api.get_vacancies(pages_count=10)
        vacancies_json.extend(api.get_formatted_vacancies())

    connector = Connector(keyword=keyword, vacancies_json=vacancies_json)

    while True:
        command = input(
            '1 - Вывести список вакансий;\n'
            'exit - Выход;\n'
        )
        if command.lower() == 'exit':
            break
        elif command == '1':
            vacancies = connector.select()

        for vacancy in vacancies:
            print(vacancy, end='\n\n')

if __name__ == '__main__':
    db = DBManager()
    db.create_tables()
    db.get_vacancies_with_higher_salary()
    db.get_avg_salary()
    db.get_companies_and_vacancies_count()
    main()
