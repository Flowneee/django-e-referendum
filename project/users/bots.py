from random import randint
from datetime import datetime

FN = ['Андрей', 'Артем', 'Алексей', 'Александр', 'Виталий', 'Борис', 'Виктор',
      'Николай', 'Евгений', 'Владислав', 'Никита', 'Илья']
LN = ['Иванов', 'Петров', 'Сидоров', 'Смирнов', 'Иванов', 'Кузнецов',
      'Соколов', 'Попов', 'Лебедев', 'Козлов', 'Новиков', 'Морозов',
      'Петров', 'Волков', 'Соловьёв', 'Васильев', 'Зайцев', 'Павлов',
      'Семёнов', 'Голубев', 'Виноградов', 'Богданов', 'Воробьёв']
PN = ['Ааронович', 'Абрамович', 'Августович', 'Авдеевич', 'Аверьянович',
      'Адамович', 'Адрианович', 'Аксёнович', 'Александрович',
      'Алексеевич', 'Анатольевич', 'Андреевич', 'Анисимович', 'Антипович',
      'Антонович', 'Ануфриевич', 'Арсенович', 'Арсеньевич']


def create_bot(model, passport_id):

    fn = FN[randint(0, len(FN)-1)]
    ln = LN[randint(0, len(LN)-1)]
    pn = PN[randint(0, len(PN)-1)]
    year = randint(1950, 1997)
    month = randint(1, 12)
    day = randint(1, 28)
    birth_date = datetime(year, month, day)
    u = model(
        first_name=fn, last_name=ln, patronymic=pn,
        passport_id=str(passport_id).zfill(10),
        birth_date=birth_date,
        address='Бот',
    )
    u.save()
    return u
