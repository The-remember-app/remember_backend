# Бекенд для приложения `The remember`

Самописное приложение, предназначенное для изучения английского языка.

## Запуск

1. Склонируйте репозиторий
```
git clone https://github.com/The-remember-app/remember_android_app.git local_instanse
cd local_instanse
```

2. Отредактируйте файлы конфигурации
```
cp ./env/example.env .env
nano .env
```

3. Запустите контейнеры
```
docker-compose --env-file env/.env up -d --force-recreate 
```

## Восстановление БД из бекапа

```
docker exec -it db_backup_container --entrypoint=/bin/sh
zcat /backups/last/the_remember-20230817-122431.sql.gz | psql --username=main_system_backend_app --dbname=the_remember --host=db -W
```

## Ручное создание бекапа 

```
docker exec -it db_backup_container --entrypoint=/bin/sh
/backup.sh
```