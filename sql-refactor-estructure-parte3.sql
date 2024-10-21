CREATE TABLE company (
	id INT NOT NULL,
	name varchar(300) NOT NULL,
	tax_id varchar(20) NOT NULL,
	phone varchar(30) NOT NULL,
	email varchar(100) NOT NULL,
	create_at timestamp NOT NULL,
	update_at timestamp NULL,
	is_deleted bool NULL,
	tax_address varchar(300) NULL,
	CONSTRAINT company_pkey PRIMARY KEY (id),
	CONSTRAINT uq_company_email UNIQUE (email),
	CONSTRAINT uq_txt_id UNIQUE (tax_id),
    INDEX ix_company_email (email)
);


CREATE TABLE employee (
    id INT PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(20),
    address VARCHAR(255),
    city VARCHAR(100),
    state VARCHAR(100),
    country VARCHAR(100),
    zip_code VARCHAR(10),
    hire_date DATE,
    termination_date DATE,
    company_id INT,
    FOREIGN KEY (company_id) REFERENCES company(id)  ON DELETE CASCADE,
    INDEX idx_company_id (company_id)
);

CREATE TABLE organization_chart (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    company_id INT NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (company_id) REFERENCES company(id) ON DELETE CASCADE
);

CREATE TABLE department (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    company_id INT NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (company_id) REFERENCES company(id) ON DELETE CASCADE
);

CREATE TABLE manager (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    company_id INT NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (company_id) REFERENCES company(id) ON DELETE CASCADE
);

CREATE TABLE employee_position (
    id INT NOT NULL AUTO_INCREMENT,
    company_id INT,
    employee_id INT,
    position_id INT,
    department_id INT,
    manager_id INT,
    is_current BOOLEAN,
    PRIMARY KEY (id),
    FOREIGN KEY (company_id) REFERENCES company(id) ON DELETE CASCADE,
    FOREIGN KEY (employee_id) REFERENCES employee(id) ON DELETE CASCADE,
    FOREIGN KEY (position_id) REFERENCES organization_chart(id) ON DELETE CASCADE,
    FOREIGN KEY (department_id) REFERENCES department(id) ON DELETE CASCADE,
    FOREIGN KEY (manager_id) REFERENCES manager(id) ON DELETE CASCADE
);

CREATE TABLE employee_salary (
    id INT NOT NULL AUTO_INCREMENT,
    employee_id INT,
    salary_amount DECIMAL(10, 2),
    is_current BOOLEAN,
    start_date TIMESTAMP,
    company_id INT,
    PRIMARY KEY (id),
    FOREIGN KEY (employee_id) REFERENCES employee(id)  ON DELETE CASCADE,
    FOREIGN KEY (company_id) REFERENCES company(id)  ON DELETE CASCADE 
);

CREATE TABLE relationship_type (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    company_id INT NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (company_id) REFERENCES company(id) ON DELETE CASCADE
);

CREATE TABLE employee_dependent (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    birthdate DATE NOT NULL,
    relationship_type_id INT,
    employee_id INT,
    company_id INT,
    PRIMARY KEY (id),
    FOREIGN KEY (relationship_type_id) REFERENCES relationship_type(id) ON DELETE CASCADE,
    FOREIGN KEY (employee_id) REFERENCES employee(id) ON DELETE CASCADE,
    FOREIGN KEY (company_id) REFERENCES company(id) ON DELETE CASCADE
);

CREATE TABLE employee_emergency_contact (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    employee_id INT,
    phone VARCHAR(20),
    email VARCHAR(100),
    address VARCHAR(255),
    company_id INT,
    PRIMARY KEY (id),
    FOREIGN KEY (employee_id) REFERENCES employee(id) ON DELETE CASCADE,
    FOREIGN KEY (company_id) REFERENCES company(id) ON DELETE CASCADE
);

CREATE TABLE employee_education (
    id INT NOT NULL AUTO_INCREMENT,
    employee_id INT,
    institution VARCHAR(255) NOT NULL,
    education_degree VARCHAR(100) NOT NULL,
    graduation_year INT,
    company_id INT,
    PRIMARY KEY (id),
    FOREIGN KEY (employee_id) REFERENCES employee(id) ON DELETE CASCADE,
    FOREIGN KEY (company_id) REFERENCES company(id) ON DELETE CASCADE
);

CREATE TABLE performance_review (
    id INT NOT NULL AUTO_INCREMENT,
    date_review DATE NOT NULL,
    score DECIMAL(5, 2),
    employee_id INT,
    company_id INT,
    PRIMARY KEY (id),
    FOREIGN KEY (employee_id) REFERENCES employee(id) ON DELETE CASCADE,
    FOREIGN KEY (company_id) REFERENCES company(id) ON DELETE CASCADE
);


CREATE TABLE status_type (
    id INT NOT NULL AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    company_id INT NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (company_id) REFERENCES company(id) ON DELETE CASCADE
);

CREATE TABLE employee_status (
    id INT NOT NULL AUTO_INCREMENT,
    status_date TIMESTAMP NOT NULL,
    status_id INT,
    employee_id INT,
    company_id INT,
    PRIMARY KEY (id),
    FOREIGN KEY (status_id) REFERENCES status_type(id) ON DELETE CASCADE,
    FOREIGN KEY (employee_id) REFERENCES employee(id) ON DELETE CASCADE,
    FOREIGN KEY (company_id) REFERENCES company(id) ON DELETE CASCADE
);

INSERT INTO company (id, name, tax_id, phone, email, create_at, is_deleted, tax_address)
VALUES
(1, 'TechCorp', 'TAX123456', '123-456-7890', 'info@techcorp.com', NOW(), FALSE, '123 Tech Street'),
(2, 'HealthCorp', 'TAX987654', '987-654-3210', 'contact@healthcorp.com', NOW(), FALSE, '456 Health Avenue'),
(3, 'EduCorp', 'TAX112233', '555-123-4567', 'hello@educorp.com', NOW(), FALSE, '789 Edu Lane');

INSERT INTO employee (id, name, email, phone, address, city, state, country, zip_code, hire_date, company_id)
VALUES
(1, 'John Doe', 'john.doe@techcorp.com', '555-987-6543', '123 Main St', 'Tech City', 'Tech State', 'USA', '12345', '2022-01-15', 1),
(2, 'Jane Smith', 'jane.smith@healthcorp.com', '555-654-3210', '456 Elm St', 'Health Town', 'Health State', 'USA', '67890', '2021-09-10', 2),
(3, 'Sam Lee', 'sam.lee@educorp.com', '555-123-7890', '789 Oak St', 'Edu Village', 'Edu State', 'USA', '54321', '2023-03-05', 3);

INSERT INTO organization_chart (id, name, company_id)
VALUES
(1, 'Software Development', 1),
(2, 'Medical Services', 2),
(3, 'Teaching Department', 3);

INSERT INTO department (id, name, company_id)
VALUES
(1, 'Development', 1),
(2, 'Operations', 2),
(3, 'Education', 3);

INSERT INTO manager (id, name, company_id)
VALUES
(1, 'Alice Manager', 1),
(2, 'Bob Supervisor', 2),
(3, 'Carol Lead', 3);

INSERT INTO employee_position (id, company_id, employee_id, position_id, department_id, manager_id, is_current)
VALUES
(1, 1, 1, 1, 1, 1, TRUE),
(2, 2, 2, 2, 2, 2, TRUE),
(3, 3, 3, 3, 3, 3, TRUE);

INSERT INTO employee_salary (employee_id, salary_amount, is_current, start_date, company_id)
VALUES
(1, 75000.00, TRUE, NOW(), 1),
(2, 85000.00, TRUE, NOW(), 2),
(3, 65000.00, TRUE, NOW(), 3);

INSERT INTO employee_salary (employee_id, salary_amount, is_current, start_date, company_id)
VALUES
(1, 65000.00, FALSE, '2023-01-01', 1),
(2, 75000.00, FALSE, '2023-01-01', 2),
(3, 55000.00, FALSE, '2023-01-01', 3);

INSERT INTO employee_salary (employee_id, salary_amount, is_current, start_date, company_id)
VALUES
(1, 55000.00, FALSE, '2022-01-01', 1),
(2, 65000.00, FALSE, '2022-01-01', 2),
(3, 45000.00, FALSE, '2022-01-01', 3);


INSERT INTO relationship_type (id, name, company_id)
VALUES
(1, 'Spouse', 1),
(2, 'Child', 2),
(3, 'Sibling', 3);

INSERT INTO employee_dependent (name, birthdate, relationship_type_id, employee_id, company_id)
VALUES
('Anna Doe', '2010-05-15', 1, 1, 1),
('Mark Smith', '2015-03-22', 2, 2, 2),
('Ella Lee', '2018-07-30', 3, 3, 3);

INSERT INTO employee_dependent (name, birthdate, relationship_type_id, employee_id, company_id)
VALUES
('James Doe', '2015-05-15', 2, 1, 1),
('Jhon Smith', '2017-03-22', 2, 2, 2),
('Karl Lee', '2018-07-30', 2, 3, 3);

INSERT INTO employee_emergency_contact (name, employee_id, phone, email, address, company_id)
VALUES
('Michael Doe', 1, '555-321-6540', 'michael.doe@techcorp.com', '987 Pine St', 1),
('Laura Smith', 2, '555-876-5432', 'laura.smith@healthcorp.com', '654 Birch St', 2),
('George Lee', 3, '555-654-3219', 'george.lee@educorp.com', '321 Spruce St', 3);

INSERT INTO employee_education (employee_id, institution, education_degree, graduation_year, company_id)
VALUES
(1, 'Tech University', 'BSc Computer Science', 2020, 1),
(2, 'Health Institute', 'MSc Medicine', 2018, 2),
(3, 'Edu University', 'BA Education', 2019, 3);

INSERT INTO performance_review (employee_id, date_review, score, company_id)
VALUES
(1, '2023-01-15', 4.5, 1),
(2, '2023-03-10', 4.7, 2),
(3, '2023-05-05', 4.3, 3);

INSERT INTO status_type (name, company_id)
VALUES
('Active', 1),
('On Leave', 2),
('Inactive', 3);

INSERT INTO employee_status (status_date, status_id, employee_id, company_id)
VALUES
(NOW(), 1, 1, 1),
(NOW(), 2, 2, 2),
(NOW(), 3, 3, 3);
