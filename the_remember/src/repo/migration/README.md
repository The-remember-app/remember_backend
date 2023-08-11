# Init migration system

Система миграций были инициализирована следующей командой

```bash
alembic --config .\the_remember\src\repo\migration/_alembic.ini init .\the_remember\src\repo\migration\alembic  --template async
```

# Create migration file

Команда создаёт миграцию, которая приводит БД в соответствие со схемой алхимии

По сути, эта команда создаёт файл миграции
```bash
alembic --config .\the_remember\src\repo\migration/_alembic.ini  revision -m "test" --autogenerate
```

# Apply migrations

Применить все неприменённые миграции

```bash
alembic --config .\the_remember\src\repo\migration/_alembic.ini  upgrade head
```

применить все миграции до указанной

Если попытаться обновиться до миграции, которая уже применена, то состояние БД не изменится. (отката миграций не случится)

```bash
alembic --config .\the_remember\src\repo\migration/_alembic.ini  upgrade <хеш нужной миграции, например 44e3>
```

Хеш можно сокращать хоть до одной первой буквы. Главное - чтобы он однозначно идентифицировал миграцию.

применить следующие две миграции
```bash
alembic --config .\the_remember\src\repo\migration/_alembic.ini  upgrade +2
```

применить все миграции до указанной в хеше и еще две

```bash
alembic --config .\the_remember\src\repo\migration/_alembic.ini  upgrade <хеш нужной миграции, например 44e3>+2
```

применить все миграции до указанной в хеше минус две (т.е. если потом применить еще две миграции, то текущая миграция будет та, которая указана в хеше)

```bash
alembic --config .\the_remember\src\repo\migration/_alembic.ini  upgrade <хеш нужной миграции, например 44e3>-2
```

Откатиться на одну миграцию

```bash
alembic --config .\the_remember\src\repo\migration/_alembic.ini  downgrade -1
```
 
откатиться к указанной миграции

```bash
alembic --config .\the_remember\src\repo\migration/_alembic.ini  downgrade <хеш нужной миграции, например 44e3>
```

всё, что связано с относительным указанием миграций для `upgrade` так же работает и для `downgrade`

Если попытаться откатиться до миграции, которая еще не применена, то ничего не случится. БД останется в том же состоянии