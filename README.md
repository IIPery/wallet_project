# Wallet API

## Описание
Это API для управления кошельками, который позволяет создавать кошельки, 
проверять баланс и выполнять операции пополнения или снятия средств.


## Установка

1. Склонировать проект
```shell
git clone https://github.com/IIPery/wallet_project
```
2. Перейти в каталог проекта
```shell
cd wallet_project
```
3. Запустить контейнеры
```shell
docker compose up --build
```
4. Применить миграции
```shell
docker compose exec web python manage.py migrate
```

## Применение
1. Создать кошелек
```shell
docker compose exec web python manage.py shell
from wallet.models import Wallet
wallet = Wallet.objects.create(balance=1000.00)
print(wallet.uuid) #номер кошелька
```
2. В браузере переходим на http://127.0.0.1:8000/api/v1/wallets/номер_кошелька/operation/
Используя post запросы
```shell
{
    "operationType": "DEPOSIT",  #или WITHDRAW
    "amount": 500
}
```
Получаем get
```shell
{
    "message": "Operation successful",
    "new_balance": 1500.0
}
```

## Тест
Для запуска тестов
```shell
docker-compose exec web python manage.py test
```
