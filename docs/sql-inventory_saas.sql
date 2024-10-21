-- Para modulo de autenticación se crea un esquema auth:
CREATE SCHEMA auth AUTHORIZATION postgres;

-- Luego se define la tabla auth.user
CREATE TABLE auth."user" (
	id serial4 NOT NULL,
	"name" varchar(150) NOT NULL,
	username varchar(50) NOT NULL,
	phone varchar(30) NOT NULL,
	email varchar(100) NOT NULL,
	"password" varchar(300) NOT NULL,
	is_active bool NOT NULL,
	is_admin bool NOT NULL,
	update_at timestamp NOT NULL,
	create_at timestamp NOT NULL,
	CONSTRAINT uq_email UNIQUE (email),
	CONSTRAINT uq_username UNIQUE (username),
	CONSTRAINT user_pkey PRIMARY KEY (id)
);
CREATE INDEX ix_auth_user_email ON auth."user" USING btree (email);


-- Para las tablas de compañia e inventario, se utiliza el esquema por defecto : public
-- Se define la siguiente estructura de tablas:


-- Tabla: public.company

CREATE TABLE public.company (
	id serial4 NOT NULL,
	"name" varchar(300) NOT NULL,
	tax_id varchar(20) NOT NULL,
	phone varchar(30) NOT NULL,
	email varchar(100) NOT NULL,
	create_at timestamp NOT NULL,
	update_at timestamp NULL,
	is_deleted bool NULL,
	tax_address varchar(300) NULL,
	CONSTRAINT company_pkey PRIMARY KEY (id),
	CONSTRAINT uq_company_email UNIQUE (email),
	CONSTRAINT uq_txt_id UNIQUE (tax_id)
);
CREATE INDEX ix_company_email ON public.company USING btree (email);


-- Tabla public.company_user
CREATE TABLE public.company_user (
	id serial4 NOT NULL,
	company_id int4 NOT NULL,
	user_id int4 NOT NULL,
	create_at timestamp NOT NULL,
	update_at timestamp NULL,
	is_deleted bool NULL,
	CONSTRAINT company_user_pkey PRIMARY KEY (id),
	CONSTRAINT uq_company_user UNIQUE (company_id, user_id)
);
CREATE INDEX ix_company_user_company_id ON public.company_user USING btree (company_id);
CREATE INDEX ix_company_user_user_id ON public.company_user USING btree (user_id);

ALTER TABLE public.company_user ADD CONSTRAINT fk_company_id FOREIGN KEY (company_id) REFERENCES public.company(id);
ALTER TABLE public.company_user ADD CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES auth."user"(id);


-- Tabla public.category
CREATE TABLE public.category (
	id serial4 NOT NULL,
	company_id int4 NOT NULL,
	"name" varchar(300) NOT NULL,
	description varchar(300) NULL,
	create_at timestamp NOT NULL,
	update_at timestamp NULL,
	is_deleted bool NULL,
	CONSTRAINT category_pkey PRIMARY KEY (id),
	CONSTRAINT uq_category_name UNIQUE (name, company_id)
);
CREATE INDEX ix_category_company_id ON public.category USING btree (company_id);

ALTER TABLE public.category ADD CONSTRAINT fk_company_id FOREIGN KEY (company_id) REFERENCES public.company(id);


-- Tabla public.product

CREATE TABLE public.product (
	id serial4 NOT NULL,
	company_id int4 NOT NULL,
	category_id int4 NOT NULL,
	product_code varchar(40) NOT NULL,
	"name" varchar(150) NOT NULL,
	description varchar(300) NULL,
	current_price numeric NULL,
	stock_quantity int4 NULL,
	create_at timestamp NOT NULL,
	update_at timestamp NULL,
	is_deleted bool NULL,
	CONSTRAINT product_pkey PRIMARY KEY (id),
	CONSTRAINT uq_product_code UNIQUE (product_code, company_id)
);
CREATE INDEX ix_product_category_id ON public.product USING btree (category_id);
CREATE INDEX ix_product_company_id ON public.product USING btree (company_id);

ALTER TABLE public.product ADD CONSTRAINT fk_category_id FOREIGN KEY (category_id) REFERENCES public.category(id);
ALTER TABLE public.product ADD CONSTRAINT fk_company_id FOREIGN KEY (company_id) REFERENCES public.company(id);


-- Tabla public.supplier

CREATE TABLE public.supplier (
	id serial4 NOT NULL,
	company_id int4 NOT NULL,
	"name" varchar(300) NOT NULL,
	tax_id varchar(20) NOT NULL,
	phone varchar(30) NOT NULL,
	email varchar(100) NOT NULL,
	create_at timestamp NOT NULL,
	update_at timestamp NULL,
	is_deleted bool NULL,
	tax_address varchar(300) NULL,
	CONSTRAINT supplier_pkey PRIMARY KEY (id),
	CONSTRAINT uq_supplier_email UNIQUE (email, company_id),
	CONSTRAINT uq_tax_id UNIQUE (tax_id, company_id)
);
CREATE INDEX ix_supplier_company_id ON public.supplier USING btree (company_id);
CREATE INDEX ix_supplier_email ON public.supplier USING btree (email);

ALTER TABLE public.supplier ADD CONSTRAINT fk_company_id FOREIGN KEY (company_id) REFERENCES public.company(id);


-- Tabla public.purchase_order

CREATE TABLE public.purchase_order (
	id serial4 NOT NULL,
	company_id int4 NOT NULL,
	sumpplier_id int4 NOT NULL,
	order_code varchar(300) NOT NULL,
	order_description varchar(300) NULL,
	invoice_number varchar(50) NULL,
	order_date timestamp NULL,
	delivery_date timestamp NULL,
	create_at timestamp NOT NULL,
	update_at timestamp NULL,
	is_deleted bool NULL,
	CONSTRAINT purchase_order_pkey PRIMARY KEY (id),
	CONSTRAINT uq_order_code_id UNIQUE (order_code, company_id)
);
CREATE INDEX ix_purchase_order_company_id ON public.purchase_order USING btree (company_id);
CREATE INDEX ix_purchase_order_sumpplier_id ON public.purchase_order USING btree (sumpplier_id);

ALTER TABLE public.purchase_order ADD CONSTRAINT fk_company_id FOREIGN KEY (company_id) REFERENCES public.company(id);
ALTER TABLE public.purchase_order ADD CONSTRAINT fk_supplier_id FOREIGN KEY (sumpplier_id) REFERENCES public.supplier(id);


-- Tabla public.purchase_order_detail;

CREATE TABLE public.purchase_order_detail (
	id serial4 NOT NULL,
	company_id int4 NOT NULL,
	product_id int4 NOT NULL,
	product_quantity int4 NOT NULL,
	unit_price numeric NOT NULL,
	total_price numeric NOT NULL,
	create_at timestamp NOT NULL,
	update_at timestamp NULL,
	is_deleted bool NULL,
	purchase_order_id int4 NOT NULL,
	CONSTRAINT purchase_order_detail_pkey PRIMARY KEY (id)
);
CREATE INDEX ix_purchase_order_detail_company_id ON public.purchase_order_detail USING btree (company_id);
CREATE INDEX ix_purchase_order_detail_product_id ON public.purchase_order_detail USING btree (product_id);
CREATE INDEX ix_purchase_order_detail_purchase_order_id ON public.purchase_order_detail USING btree (purchase_order_id);

ALTER TABLE public.purchase_order_detail ADD CONSTRAINT fk_company_id FOREIGN KEY (company_id) REFERENCES public.company(id);
ALTER TABLE public.purchase_order_detail ADD CONSTRAINT fk_product_id FOREIGN KEY (product_id) REFERENCES public.product(id);
ALTER TABLE public.purchase_order_detail ADD CONSTRAINT fk_purchase_order_id FOREIGN KEY (purchase_order_id) REFERENCES public.purchase_order(id);


-- Tabla public.customer

CREATE TABLE public.customer (
	id serial4 NOT NULL,
	company_id int4 NOT NULL,
	"name" varchar(300) NOT NULL,
	dni varchar(20) NOT NULL,
	phone varchar(30) NOT NULL,
	email varchar(100) NOT NULL,
	address varchar(300) NULL,
	create_at timestamp NOT NULL,
	update_at timestamp NULL,
	is_deleted bool NULL,
	CONSTRAINT customer_pkey PRIMARY KEY (id),
	CONSTRAINT uq_dni_id UNIQUE (dni, company_id)
);
CREATE INDEX ix_customer_company_id ON public.customer USING btree (company_id);
CREATE INDEX ix_customer_email ON public.customer USING btree (email);

ALTER TABLE public.customer ADD CONSTRAINT fk_company_id FOREIGN KEY (company_id) REFERENCES public.company(id);


-- Tabla public.sales_order

CREATE TABLE public.sales_order (
	id serial4 NOT NULL,
	company_id int4 NOT NULL,
	customer_id int4 NOT NULL,
	order_number varchar(300) NOT NULL,
	order_description varchar(300) NULL,
	invoice_number varchar(50) NULL,
	invoice_date timestamp NULL,
	delivery_address varchar(300) NULL,
	delivery_date timestamp NULL,
	create_at timestamp NOT NULL,
	update_at timestamp NULL,
	is_deleted bool NULL,
	CONSTRAINT sales_order_pkey PRIMARY KEY (id),
	CONSTRAINT uq_order_number_id UNIQUE (order_number, company_id)
);
CREATE INDEX ix_sales_order_company_id ON public.sales_order USING btree (company_id);
CREATE INDEX ix_sales_order_customer_id ON public.sales_order USING btree (customer_id);

ALTER TABLE public.sales_order ADD CONSTRAINT fk_company_id FOREIGN KEY (company_id) REFERENCES public.company(id);
ALTER TABLE public.sales_order ADD CONSTRAINT fk_customer_id FOREIGN KEY (customer_id) REFERENCES public.customer(id);


-- Tabla public.sales_order_detail

CREATE TABLE public.sales_order_detail (
	id serial4 NOT NULL,
	company_id int4 NOT NULL,
	product_id int4 NOT NULL,
	product_quantity int4 NOT NULL,
	unit_price numeric NOT NULL,
	total_price numeric NOT NULL,
	create_at timestamp NOT NULL,
	update_at timestamp NULL,
	is_deleted bool NULL,
	sales_order_id int4 NOT NULL,
	CONSTRAINT sales_order_detail_pkey PRIMARY KEY (id)
);
CREATE INDEX ix_sales_order_detail_company_id ON public.sales_order_detail USING btree (company_id);
CREATE INDEX ix_sales_order_detail_product_id ON public.sales_order_detail USING btree (product_id);
CREATE INDEX ix_sales_order_detail_sales_order_id ON public.sales_order_detail USING btree (sales_order_id);

ALTER TABLE public.sales_order_detail ADD CONSTRAINT fk_company_id FOREIGN KEY (company_id) REFERENCES public.company(id);
ALTER TABLE public.sales_order_detail ADD CONSTRAINT fk_product_id FOREIGN KEY (product_id) REFERENCES public.product(id);
ALTER TABLE public.sales_order_detail ADD CONSTRAINT fk_sales_order_id FOREIGN KEY (sales_order_id) REFERENCES public.sales_order(id);