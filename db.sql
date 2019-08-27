--
-- PostgreSQL database dump
--

-- Dumped from database version 11.5 (Ubuntu 11.5-0ubuntu0.19.04.1)
-- Dumped by pg_dump version 11.5 (Ubuntu 11.5-0ubuntu0.19.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: messages; Type: TABLE; Schema: public; Owner: pm
--

CREATE TABLE public.messages (
    id integer NOT NULL,
    from_id integer,
    to_id integer,
    text character varying(255),
    creation_date timestamp without time zone,
    title character varying(100)
);


ALTER TABLE public.messages OWNER TO pm;

--
-- Name: messages_id_seq; Type: SEQUENCE; Schema: public; Owner: pm
--

CREATE SEQUENCE public.messages_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.messages_id_seq OWNER TO pm;

--
-- Name: messages_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pm
--

ALTER SEQUENCE public.messages_id_seq OWNED BY public.messages.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: pm
--

CREATE TABLE public.users (
    id integer NOT NULL,
    email character varying(255),
    username character varying(255),
    hashed_password character varying(80)
);


ALTER TABLE public.users OWNER TO pm;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: pm
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO pm;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pm
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: messages id; Type: DEFAULT; Schema: public; Owner: pm
--

ALTER TABLE ONLY public.messages ALTER COLUMN id SET DEFAULT nextval('public.messages_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: pm
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: messages; Type: TABLE DATA; Schema: public; Owner: pm
--

COPY public.messages (id, from_id, to_id, text, creation_date, title) FROM stdin;
1	1	2	Już cię więcej nie kocham seksistowska świnio!	2019-08-26 19:03:18.450269	Nieudana miłość
2	2	3	Zignorowałeś mnie fiucie!, więcej się do Ciebie nie odzywam	2019-08-26 19:45:20.86786	Mam Cię w dupie!
3	2	3	Zignorowałeś mnie fiucie!, więcej się do Ciebie nie odzywam	2019-08-26 19:58:58.506796	Mam Cię w dupie!
4	6	4	Trzy dni nie wracasz z imprezy śmieciu niemyty	2019-08-27 21:48:09.079252	Nienawidzę Cię Miruś
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: pm
--

COPY public.users (id, email, username, hashed_password) FROM stdin;
1	marian.pazdzioch@onet.pl	Marian	xX9rvm4t9ZjlR09F04814f6d449a33d9db00e925a7a9c736840d73fffbbac1a8e4ba6a2f8a5171b6
2	kapitan.bomba@gwiezdnaflota.kurwix	Tytus	tvzzC5FqOjTSGFrj9bd5928e4933241467ad07d8e31d7f7d168a14c2f50f7f40246a339947117440
3	mroczny.zniwiarz@hades.com	Ponury	Uj6VIoR0Iehi4VZ14df2d89a7bf0e90c1cfe226d5b4c398dc87b4396bfb3b68c7fa48d39a65572b2
4	szach@mat.ateisci	JużNieAnonim	vq7gQ2wjI0zGJAZ4543fa7ea4ac5effb448cda7a5d634dfd30ffe8deef4882baa17d2b27f1fcc095
6	maciek@lowca.pl	Maciek	Lqkh895dT3Jn1mlX3d9be92abf7ddb9147f9993debb715aa0a900c45487c15073414a5b5ed8604a7
\.


--
-- Name: messages_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pm
--

SELECT pg_catalog.setval('public.messages_id_seq', 4, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pm
--

SELECT pg_catalog.setval('public.users_id_seq', 6, true);


--
-- Name: messages messages_pkey; Type: CONSTRAINT; Schema: public; Owner: pm
--

ALTER TABLE ONLY public.messages
    ADD CONSTRAINT messages_pkey PRIMARY KEY (id);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: pm
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: pm
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: messages messages_from_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pm
--

ALTER TABLE ONLY public.messages
    ADD CONSTRAINT messages_from_id_fkey FOREIGN KEY (from_id) REFERENCES public.users(id);


--
-- Name: messages messages_to_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pm
--

ALTER TABLE ONLY public.messages
    ADD CONSTRAINT messages_to_id_fkey FOREIGN KEY (to_id) REFERENCES public.users(id);


--
-- PostgreSQL database dump complete
--

