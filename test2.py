import asyncio

# Асинхронна функція
async def func1():
    print("Початок асинхронної функції")
    await asyncio.sleep(2)  # Затримка у 2 секунди
    print("Кінець асинхронної функції")

# Синхронна функція
def func_without():
    print("Синхронна функція")

# Основна функція
async def main():
    # Запускаємо асинхронну функцію паралельно з синхронною
    async_func = asyncio.create_task(func1())
    func_without()

    # Очікуємо завершення асинхронної функції
    await async_func

# Запускаємо основну функцію
asyncio.run(main())
