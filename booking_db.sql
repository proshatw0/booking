--
-- PostgreSQL database dump
--

-- Dumped from database version 17.4 (Debian 17.4-1)
-- Dumped by pg_dump version 17.4 (Debian 17.4-1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: admin_users; Type: TABLE; Schema: public; Owner: booking_user
--

CREATE TABLE public.admin_users (
    id integer NOT NULL,
    first_name character varying(100) NOT NULL,
    last_name character varying(100) NOT NULL,
    middle_name character varying(100),
    login character varying(100) NOT NULL,
    password_hash character varying(255) NOT NULL,
    position_id integer NOT NULL
);


ALTER TABLE public.admin_users OWNER TO booking_user;

--
-- Name: admin_users_id_seq; Type: SEQUENCE; Schema: public; Owner: booking_user
--

CREATE SEQUENCE public.admin_users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.admin_users_id_seq OWNER TO booking_user;

--
-- Name: admin_users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: booking_user
--

ALTER SEQUENCE public.admin_users_id_seq OWNED BY public.admin_users.id;


--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: booking_user
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO booking_user;

--
-- Name: positions; Type: TABLE; Schema: public; Owner: booking_user
--

CREATE TABLE public.positions (
    id integer NOT NULL,
    name character varying(50) NOT NULL
);


ALTER TABLE public.positions OWNER TO booking_user;

--
-- Name: positions_id_seq; Type: SEQUENCE; Schema: public; Owner: booking_user
--

CREATE SEQUENCE public.positions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.positions_id_seq OWNER TO booking_user;

--
-- Name: positions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: booking_user
--

ALTER SEQUENCE public.positions_id_seq OWNED BY public.positions.id;


--
-- Name: reservations; Type: TABLE; Schema: public; Owner: booking_user
--

CREATE TABLE public.reservations (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    status_id integer NOT NULL,
    date date NOT NULL,
    start_time time without time zone NOT NULL,
    end_time time without time zone NOT NULL,
    table_id integer NOT NULL,
    num_people integer NOT NULL,
    phone character varying(15) NOT NULL,
    email character varying(100),
    special_requests character varying(500),
    created_at timestamp without time zone NOT NULL,
    admin_user_id integer
);


ALTER TABLE public.reservations OWNER TO booking_user;

--
-- Name: reservations_id_seq; Type: SEQUENCE; Schema: public; Owner: booking_user
--

CREATE SEQUENCE public.reservations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.reservations_id_seq OWNER TO booking_user;

--
-- Name: reservations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: booking_user
--

ALTER SEQUENCE public.reservations_id_seq OWNED BY public.reservations.id;


--
-- Name: statuses; Type: TABLE; Schema: public; Owner: booking_user
--

CREATE TABLE public.statuses (
    id integer NOT NULL,
    name character varying(100) NOT NULL
);


ALTER TABLE public.statuses OWNER TO booking_user;

--
-- Name: statuses_id_seq; Type: SEQUENCE; Schema: public; Owner: booking_user
--

CREATE SEQUENCE public.statuses_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.statuses_id_seq OWNER TO booking_user;

--
-- Name: statuses_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: booking_user
--

ALTER SEQUENCE public.statuses_id_seq OWNED BY public.statuses.id;


--
-- Name: tables; Type: TABLE; Schema: public; Owner: booking_user
--

CREATE TABLE public.tables (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    description character varying(255),
    photo character varying(255),
    capacity integer NOT NULL,
    deposit double precision
);


ALTER TABLE public.tables OWNER TO booking_user;

--
-- Name: tables_id_seq; Type: SEQUENCE; Schema: public; Owner: booking_user
--

CREATE SEQUENCE public.tables_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tables_id_seq OWNER TO booking_user;

--
-- Name: tables_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: booking_user
--

ALTER SEQUENCE public.tables_id_seq OWNED BY public.tables.id;


--
-- Name: admin_users id; Type: DEFAULT; Schema: public; Owner: booking_user
--

ALTER TABLE ONLY public.admin_users ALTER COLUMN id SET DEFAULT nextval('public.admin_users_id_seq'::regclass);


--
-- Name: positions id; Type: DEFAULT; Schema: public; Owner: booking_user
--

ALTER TABLE ONLY public.positions ALTER COLUMN id SET DEFAULT nextval('public.positions_id_seq'::regclass);


--
-- Name: reservations id; Type: DEFAULT; Schema: public; Owner: booking_user
--

ALTER TABLE ONLY public.reservations ALTER COLUMN id SET DEFAULT nextval('public.reservations_id_seq'::regclass);


--
-- Name: statuses id; Type: DEFAULT; Schema: public; Owner: booking_user
--

ALTER TABLE ONLY public.statuses ALTER COLUMN id SET DEFAULT nextval('public.statuses_id_seq'::regclass);


--
-- Name: tables id; Type: DEFAULT; Schema: public; Owner: booking_user
--

ALTER TABLE ONLY public.tables ALTER COLUMN id SET DEFAULT nextval('public.tables_id_seq'::regclass);


--
-- Data for Name: admin_users; Type: TABLE DATA; Schema: public; Owner: booking_user
--

COPY public.admin_users (id, first_name, last_name, middle_name, login, password_hash, position_id) FROM stdin;
1	Виктория	Крышева	Дмитриевна	Vika	scrypt:32768:8:1$eUKIqVrlaYsyA4j3$cf52794807748032375190b5cf6f622d901ec3d34ecc62709dd3be18bd2c40e5544a61c04883842c4d49d907a44188ff189e84c8d1258744ee28c167d1352b1e	1
\.


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: booking_user
--

COPY public.alembic_version (version_num) FROM stdin;
57de6cfb8fd6
\.


--
-- Data for Name: positions; Type: TABLE DATA; Schema: public; Owner: booking_user
--

COPY public.positions (id, name) FROM stdin;
1	Администратор
2	Хостес
\.


--
-- Data for Name: reservations; Type: TABLE DATA; Schema: public; Owner: booking_user
--

COPY public.reservations (id, name, status_id, date, start_time, end_time, table_id, num_people, phone, email, special_requests, created_at, admin_user_id) FROM stdin;
\.


--
-- Data for Name: statuses; Type: TABLE DATA; Schema: public; Owner: booking_user
--

COPY public.statuses (id, name) FROM stdin;
1	Ок
2	Пришёл
3	Отменена
\.


--
-- Data for Name: tables; Type: TABLE DATA; Schema: public; Owner: booking_user
--

COPY public.tables (id, name, description, photo, capacity, deposit) FROM stdin;
12	12	Барные стулья.	app/static/uploads/12.jpg	2	\N
11	11	Барные стулья.	app/static/uploads/11.jpg	2	\N
13	13	Барные стулья.	app/static/uploads/13.jpg	8	\N
14	14		app/static/uploads/14-16.jpg	4	\N
15	15		app/static/uploads/14-16.jpg	4	\N
16	16		app/static/uploads/14-16.jpg	4	\N
17	21	Мягкие диваны.	app/static/uploads/21-22.jpg	4	8000
18	22	Мягкие диваны.	app/static/uploads/21-22_2.jpg	4	8000
20	24	Мягкие диваны.	app/static/uploads/23-24_2.jpg	6	8000
19	23	Мягкие диваны.	app/static/uploads/23-24_2.jpg	6	8000
21	31		app/static/uploads/31.jpg	4	\N
22	32		app/static/uploads/32.jpg	4	\N
23	33		app/static/uploads/33.jpg	2	\N
24	34	Сервисный сбор 10%.	app/static/uploads/34_2.jpg	15	\N
25	35		app/static/uploads/35_36.jpg	4	\N
26	36		app/static/uploads/35_36.jpg	4	\N
27	41		app/static/uploads/41-42.jpg	4	\N
28	42		app/static/uploads/41-42.jpg	4	\N
29	43		app/static/uploads/43.jpg	2	\N
30	44		app/static/uploads/44-46.jpg	5	\N
31	45		app/static/uploads/44-46.jpg	5	\N
32	46		app/static/uploads/44-46.jpg	5	\N
33	47	Мягкие диваны.	app/static/uploads/47-49.jpg	5	8000
34	48	Мягкие диваны.	app/static/uploads/47-49.jpg	5	8000
35	49	Мягкие диваны.	app/static/uploads/47-49.jpg	5	8000
36	40.1		app/static/uploads/40.1.jpg	8	\N
37	40.2		app/static/uploads/40.2.jpg	8	\N
38	51	Стол-кабинка.	app/static/uploads/51-53.jpg	2	\N
39	52	Стол-кабинка.	app/static/uploads/51-53.jpg	2	\N
40	53	Стол-кабинка.	app/static/uploads/51-53.jpg	2	\N
41	54	Стол-кабинка.	app/static/uploads/54-59_2.jpg	4	\N
42	55	Стол-кабинка.	app/static/uploads/54-59_2.jpg	4	\N
43	56	Стол-кабинка.	app/static/uploads/54-59_2.jpg	4	\N
44	57	Стол-кабинка.	app/static/uploads/54-59_2.jpg	4	\N
45	58	Стол-кабинка.	app/static/uploads/54-59_2.jpg	4	\N
46	59	Стол-кабинка.	app/static/uploads/54-59_2.jpg	4	\N
47	61		app/static/uploads/61-62.jpg	8	\N
48	62		app/static/uploads/61-62.jpg	8	\N
49	63	Стол-кабинка.	app/static/uploads/63-68.jpg	8	\N
50	64	Стол-кабинка.	app/static/uploads/63-68.jpg	8	\N
51	65	Стол-кабинка.	app/static/uploads/63-68.jpg	8	\N
52	66	Стол-кабинка.	app/static/uploads/63-68.jpg	8	\N
53	67	Стол-кабинка.	app/static/uploads/63-68.jpg	8	\N
54	68	Стол-кабинка.	app/static/uploads/63-68.jpg	8	\N
55	71	Напротив кухни.	app/static/uploads/71-73.jpg	4	\N
56	72	Напротив кухни.	app/static/uploads/71-73.jpg	4	\N
57	73	Напротив кухни.	app/static/uploads/71-73.jpg	4	\N
\.


--
-- Name: admin_users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: booking_user
--

SELECT pg_catalog.setval('public.admin_users_id_seq', 2, true);


--
-- Name: positions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: booking_user
--

SELECT pg_catalog.setval('public.positions_id_seq', 2, true);


--
-- Name: reservations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: booking_user
--

SELECT pg_catalog.setval('public.reservations_id_seq', 5, true);


--
-- Name: statuses_id_seq; Type: SEQUENCE SET; Schema: public; Owner: booking_user
--

SELECT pg_catalog.setval('public.statuses_id_seq', 3, true);


--
-- Name: tables_id_seq; Type: SEQUENCE SET; Schema: public; Owner: booking_user
--

SELECT pg_catalog.setval('public.tables_id_seq', 57, true);


--
-- Name: admin_users admin_users_login_key; Type: CONSTRAINT; Schema: public; Owner: booking_user
--

ALTER TABLE ONLY public.admin_users
    ADD CONSTRAINT admin_users_login_key UNIQUE (login);


--
-- Name: admin_users admin_users_pkey; Type: CONSTRAINT; Schema: public; Owner: booking_user
--

ALTER TABLE ONLY public.admin_users
    ADD CONSTRAINT admin_users_pkey PRIMARY KEY (id);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: booking_user
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: positions positions_name_key; Type: CONSTRAINT; Schema: public; Owner: booking_user
--

ALTER TABLE ONLY public.positions
    ADD CONSTRAINT positions_name_key UNIQUE (name);


--
-- Name: positions positions_pkey; Type: CONSTRAINT; Schema: public; Owner: booking_user
--

ALTER TABLE ONLY public.positions
    ADD CONSTRAINT positions_pkey PRIMARY KEY (id);


--
-- Name: reservations reservations_pkey; Type: CONSTRAINT; Schema: public; Owner: booking_user
--

ALTER TABLE ONLY public.reservations
    ADD CONSTRAINT reservations_pkey PRIMARY KEY (id);


--
-- Name: statuses statuses_pkey; Type: CONSTRAINT; Schema: public; Owner: booking_user
--

ALTER TABLE ONLY public.statuses
    ADD CONSTRAINT statuses_pkey PRIMARY KEY (id);


--
-- Name: tables tables_pkey; Type: CONSTRAINT; Schema: public; Owner: booking_user
--

ALTER TABLE ONLY public.tables
    ADD CONSTRAINT tables_pkey PRIMARY KEY (id);


--
-- Name: admin_users admin_users_position_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: booking_user
--

ALTER TABLE ONLY public.admin_users
    ADD CONSTRAINT admin_users_position_id_fkey FOREIGN KEY (position_id) REFERENCES public.positions(id);


--
-- Name: reservations reservations_admin_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: booking_user
--

ALTER TABLE ONLY public.reservations
    ADD CONSTRAINT reservations_admin_user_id_fkey FOREIGN KEY (admin_user_id) REFERENCES public.admin_users(id);


--
-- Name: reservations reservations_status_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: booking_user
--

ALTER TABLE ONLY public.reservations
    ADD CONSTRAINT reservations_status_id_fkey FOREIGN KEY (status_id) REFERENCES public.statuses(id);


--
-- Name: reservations reservations_table_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: booking_user
--

ALTER TABLE ONLY public.reservations
    ADD CONSTRAINT reservations_table_id_fkey FOREIGN KEY (table_id) REFERENCES public.tables(id);


--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: pg_database_owner
--

GRANT ALL ON SCHEMA public TO booking_user;


--
-- Name: DEFAULT PRIVILEGES FOR SEQUENCES; Type: DEFAULT ACL; Schema: public; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA public GRANT ALL ON SEQUENCES TO booking_user;


--
-- Name: DEFAULT PRIVILEGES FOR TABLES; Type: DEFAULT ACL; Schema: public; Owner: postgres
--

ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA public GRANT ALL ON TABLES TO booking_user;


--
-- PostgreSQL database dump complete
--

