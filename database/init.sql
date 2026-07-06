CREATE TABLE departments (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    full_name TEXT NOT NULL,
    department_id INT REFERENCES departments(id),
    hire_date DATE NOT NULL
);

CREATE TABLE projects (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    start_date DATE,
    end_date DATE
);

CREATE TABLE employee_projects (
    employee_id INT REFERENCES employees(id),
    project_id INT REFERENCES projects(id),
    role TEXT,
    PRIMARY KEY (employee_id, project_id)
);

CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    employee_id INT REFERENCES employees(id),
    project_id INT REFERENCES projects(id),
    title TEXT,
    status TEXT,
    created_at DATE
);

CREATE TABLE salaries (
    id SERIAL PRIMARY KEY,
    employee_id INT REFERENCES employees(id),
    amount NUMERIC,
    from_date DATE,
    to_date DATE
);

CREATE TABLE vacations (
    id SERIAL PRIMARY KEY,
    employee_id INT REFERENCES employees(id),
    start_date DATE,
    end_date DATE
);

INSERT INTO departments (name) VALUES
('Инженер'),
('Дата аналитик'),
('HR'),
('Продажи'),
('Маркетинг');

INSERT INTO employees (full_name, department_id, hire_date) VALUES
('Иван Петров', 1, '2022-03-10'),
('Анна Смирнова', 1, '2021-07-15'),
('Джон Смит', 2, '2023-01-20'),
('Мария Иванова', 2, '2022-11-05'),
('Алексей Кузнецов', 3, '2020-06-01'),
('Елена Волкова', 4, '2021-09-12'),
('Дмитрий Соколов', 4, '2023-02-18'),
('Ольга Морозова', 5, '2022-05-25'),
('Павел Орлов', 5, '2021-12-30'),
('Никита Федоров', 1, '2020-01-10');

INSERT INTO projects (name, start_date, end_date) VALUES
('BI-платформа', '2023-01-01', NULL),
('CRM миграция', '2022-06-01', '2023-06-01'),
('Хранилище данных', '2023-03-01', NULL),
('Автоматизация маркетинга', '2024-01-01', NULL),
('Система управления персоналом', '2022-09-01', '2023-02-01');

INSERT INTO employee_projects (employee_id, project_id, role) VALUES
(1, 1, 'Backend-разработчик'),
(2, 1, 'Tech-Lead'),
(3, 3, 'Дата-аналитик'),
(4, 3, 'Дата-инженер'),
(5, 5, 'HR-специалист'),
(6, 2, 'Менеджер по продажам'),
(7, 2, 'Менеджер по работе с клиентами'),
(8, 4, 'Руководитель отдела маркетинга'),
(9, 4, 'Контент-менеджер'),
(10, 1, 'DevOps-инженер');

INSERT INTO tasks (employee_id, project_id, title, status, created_at) VALUES
(1, 1, 'Разработка API', 'готово', '2023-01-10'),
(1, 1, 'Реализация аутентификации', 'в_процессе', '2023-02-10'),
(2, 1, 'Обзор архитектуры', 'готово', '2023-01-15'),
(3, 3, 'Создание ETL-конвейера', 'в_процессе', '2023-03-10'),
(4, 3, 'Оптимизация запросов', 'к_выполнению', '2023-04-01'),
(5, 5, 'Процесс адаптации сотрудников', 'готово', '2022-10-01'),
(6, 2, 'Сбор требований к CRM', 'готово', '2022-06-10'),
(7, 2, 'Интеграция с клиентом', 'в_процессе', '2022-08-15'),
(8, 4, 'Планирование кампании', 'в_процессе', '2024-02-01'),
(9, 4, 'Контент-стратегия', 'к_выполнению', '2024-02-15');

INSERT INTO salaries (employee_id, amount, from_date, to_date) VALUES
(1, 120000, '2023-01-01', NULL),
(2, 180000, '2023-01-01', NULL),
(3, 110000, '2023-01-01', NULL),
(4, 130000, '2023-01-01', NULL),
(5, 90000, '2022-01-01', NULL),
(6, 100000, '2022-01-01', NULL),
(7, 95000, '2023-01-01', NULL),
(8, 105000, '2023-01-01', NULL),
(9, 98000, '2022-01-01', NULL),
(10, 150000, '2023-01-01', NULL);

INSERT INTO vacations (employee_id, start_date, end_date) VALUES
(1, '2024-08-01', '2024-08-14'),
(2, '2024-07-10', '2024-07-20'),
(3, '2024-06-01', '2024-06-10'),
(4, '2024-09-01', '2024-09-15'),
(5, '2024-07-01', '2024-07-10');