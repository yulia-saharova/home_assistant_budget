# Анализатор бюджета — Home Assistant Budget

Локальный веб-анализатор личных финансов: доходы / расходы / баланс, динамика за месяц, структура по категориям и расширенная статистика.

Стек: **Python + Streamlit (multipage) + SQLAlchemy + PostgreSQL + Pandas**.

Статус: `MVP в разработке`. Каркас БД и навигация готовы, страницы `Главная` и `Статистика` — заглушки, `Доходы/Расходы` — рабочий просмотр из БД с фильтрацией, графиками и экспортом.

## 1. Цель проекта

Заменить Excel-таблицы одним приложением:

- вносить доходы и расходы пачкой за день (таблица-редактор);
- смотреть итоги месяца: сколько пришло / ушло / осталось;
- разбирать структуру (категории, способы оплаты, дни недели, время суток);
- сравнивать план/факт и месяцы между собой;
- выгружать данные в Excel/CSV.

Целевой пользователь — один человек / семья, запуск локально, данные в домашнем PostgreSQL.

## 2. Запланированный дизайн (по макетам)

Навигация (сайдбар, как в `pages/streamlit.py`):

```
Главная
Доходы → Просмотр / Внести
Расходы → Просмотр / Внести
Статистика
```

### 2.1. Главная — `pages/main_page.py`

Переключатель месяца (по умолчанию текущий).

- **3 карточки итогов:** Доходы / Расходы / Баланс + дельта к прошлому месяцу (`+12.5% к марту`).
- **Динамика за месяц:** накопительные линии Доходы vs Расходы по дням.
- **Структура расходов:** donut (Питание 35%, Транспорт 20%, Жильё 15%, Развлечения 10%, Другое 20%).
- **Ключевые метрики:** средний чек, количество операций, крупнейшая статья (напр. `Питание — 47,926.20 ₽`), план/факт (`85% плана расходов`).
- **Последние операции:** таблица Дата / Тип / Категория / Сумма / Комментарий + ссылка «Перейти к просмотру».


### 2.2. Доходы / Расходы — Просмотр (`income_page.py`, `expence_page.py`)

Единый шаблон для обоих типов:

- **Фильтры:** период (Дата от — Дата до), категория (multiselect), способ получения/оплаты (`Банк / Наличные / Карта / Перевод`), поиск по комментариям. Кнопки `Применить / Очистить`.
- **Кнопка действия:** `+ Внести доход / расход` — быстрый переход к форме ввода.
- **Таблица:** Дата / Сумма / Категория / Способ / Комментарий + строка `Итого: 186,500.00 ₽`.
- **Экспорт:** выгрузка таблицы в Excel и CSV.
- **Пагинация:** `Показано 1–5 из 12`, страницы `1 2 3 >`.


Пример строки доходов из макета: `03.04.2026 | 120,000.00 ₽ | Зарплата | Банк | Основной доход`.

### 2.3. Доходы / Расходы — Внести (`add_income_page.py`, `add_expence_page.py`)

Пакетный ввод за одну дату:

- `Дата операции` (по умолчанию сегодня).
- **Таблица ввода:** № / Категория (select) / Сумма (₽) / Способ оплаты (select) / Комментарий / Действие (корзина).
- `+ Добавить строку` — новая пустая строка (`st.data_editor(num_rows='dynamic')` в черновике).
- **Итог:** автоматический подсчёт `Итого расходов: 2,460.00 ₽`.
- Кнопки `Очистить / Сохранить` — одна транзакция БД на все строки.


### 2.4. Статистика — `pages/stats_page.py`

Два уровня:

**Краткая (макет 4):** переключатель `Месяц / Апрель 2026`, 4 KPI, `Доходы и расходы по дням` (bar), `Расходы по категориям` (h-bar), `Тренд за последние 6 месяцев` (линии).

**Полная (макет 5, «Комплексный анализ» + `Экспорт отчёта`):**

- Расходы по категориям + бюджет по конвертам 
- Тренд за последние 6 месяцев (начиная от выбранного в фильтре)
- Платежный календарь
- Расходы по дным недели (среднее значение)
- Топ категорий расходов
- Накопительный баланс
- Средний чек по категориям
- Кол-во операций в рамках месяца
- План/факт по категориям
- Календарь расходов 

Плашки:
- Доход за месяц, процент к предыдущему месяцу
- Расход за месяц, процент к предыдущему месяцу
- Средний чек расходов процент к предыдущему месяцу
- Кол0во операций

## 3. Структура репозитория

```
home_assistant_budget/
├── pages/
│   ├── streamlit.py        # точка входа, st.navigation: Главная/Доходы/Расходы/Статистика
│   ├── main_page.py        # Главная (TODO: дашборд)
│   ├── income_page.py      # Доходы — просмотр (фильтры + таблица)
│   ├── add_income_page.py  # Доходы — внести (форма + CSV-загрузка, TODO: запись в БД)
│   ├── expence_page.py     # Расходы — просмотр (фильтры + таблица)
│   ├── add_expence_page.py # Расходы — внести + черновик статистики (data_editor)
│   └── stats_page.py       # Статистика (TODO)
├── database/
│   ├── base.py             # DeclarativeBase
│   ├── connection.py       # engine (QueuePool) + SessionLocal
│   └── session_manager.py  # get_db_session(): commit/rollback/close + логирование
├── models/
│   ├── category.py         # CategoryModel + CategoryDAO (get_by_name, get_by_type)
│   ├── transactions.py     # TransactionModel + TransactionDAO (get_by_date_range)
│   └── base_model.py       # BaseDAO: get_one/get_mult/create/update/delete/exists
├── repositories/
│   ├── base_repo.py        # тонкая обёртка над DAO
│   ├── category_repo.py    # create_category с проверкой дублей
│   └── transaction_repo.py # create_transaction (amount>0, не будущее, FK check),
│                           # get_transactions_with_categories, get_monthly_stat[by_category]
├── config.py               # Settings из .env: DB_USER/PASSWORD/HOST/PORT/NAME + пул
├── exceptions.py           # DatabaseError → ValidationError / NotFoundError / DuplicateError
├── data/                   # пусто, под CSV/выгрузки
├── notebooks/              # пусто, под EDA
├── sandbox/                # database_test.py, test_db.py, tests.py — ручные тесты на живой БД
├── analyze_data.ipynb      # черновик анализа
├── requirements.txt        # ⚠️ сейчас только jupyter-стек, без streamlit/sqlalchemy/psycopg
├── .env                    # секреты 
└── myenv/                  # venv
```

## 4. Модель данных (PostgreSQL)

**`categories`:**

| поле | тип | constraints |
|---|---|---|
| id | Integer PK | index |
| name_category | String(100) | NOT NULL, UNIQUE |
| description | Text | nullable |
| type_category | String(20) | NOT NULL (`income` / `expense`) |
| month_limit | Float | nullable — лимит для «конвертов» / План vs Факт |
| transactions | relationship | `back_populates`, lazy select |

**`transactions`:**

| поле | тип | constraints |
|---|---|---|
| id | BigInteger PK | index |
| date | Date | NOT NULL, default `current_date()` |
| amount | Numeric(10,2) | NOT NULL, > 0 (проверка в репозитории) |
| comment | String(200) | nullable — для поиска |
| type_transaction | String(20) | NOT NULL (дублирует тип категории, требует синхронизации) |
| category_id | Integer FK → categories.id | NOT NULL |
| category_rel | relationship | joinedload в `get_transactions_with_categories` |


Слой доступа: `BaseDAO → CategoryDAO/TransactionDAO → BaseRepository → CategoryRepository/TransactionRepository → Streamlit pages` через `get_db_session()`.

## 5. Установка и запуск

Требования: Python 3.11+, PostgreSQL 14+.

```bash
# 1. клонировать и перейти
cd D:\ds_projects\home_assistant_budget

# 2. окружение
python -m venv myenv
myenv\Scripts\activate        # Windows
# source myenv/bin/activate   # Linux/macOS

# 3. зависимости (дополнить — см. нижев разработкеuirements.txt
pip install streamlit sqlalchemy psycopg2-binary python-dotenv pandas plotly openpyxl streamlit-pagination

# 4. база
createdb finance_db

# 5. конфиг — создать .env рядом с config.py:
DB_USER=postgres
DB_PASSWORD=***
DB_HOST=localhost
DB_PORT=5432
DB_NAME=finance_db

# 6. запуск
streamlit run pages/streamlit.py
```

