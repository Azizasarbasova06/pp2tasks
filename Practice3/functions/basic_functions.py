# 1. Функция приветствия с системным временем
def system_greeting():
    print("Инициализация системы управления KBTU...")
    print("Доступ разрешен. Добро пожаловать!")

# 2. Функция для вывода информации о проекте SIS
def show_project_info(project_name):
    status = "в разработке"
    print(f"Проект '{project_name}' сейчас находится в статусе: {status}.")

# 3. Функция отображения локации пользователя
def user_location(city, country="Kazakhstan"):
    print(f"Ваш регион входа: {city}, {country}.")

# 4. Вызов функций внутри другой функции
def start_session():
    system_greeting()
    show_project_info("Online Food Marketplace")
    user_location("Atyrau")

start_session()