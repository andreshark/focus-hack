--
-- PostgreSQL database dump
--

-- Dumped from database version 17.0
-- Dumped by pg_dump version 17.0

-- Started on 2025-11-13 22:38:13

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
-- TOC entry 222 (class 1259 OID 83441)
-- Name: characters; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.characters (
    id integer NOT NULL,
    name character varying NOT NULL,
    price integer NOT NULL,
    netrual_anim character varying NOT NULL,
    win_anim character varying NOT NULL,
    lose_anim character varying NOT NULL,
    focus_anim character varying NOT NULL,
    preview character varying NOT NULL
);


ALTER TABLE public.characters OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 83440)
-- Name: characters_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.characters_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.characters_id_seq OWNER TO postgres;

--
-- TOC entry 4849 (class 0 OID 0)
-- Dependencies: 221
-- Name: characters_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.characters_id_seq OWNED BY public.characters.id;


--
-- TOC entry 225 (class 1259 OID 83457)
-- Name: music; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.music (
    id integer NOT NULL,
    price integer NOT NULL,
    name character varying NOT NULL,
    path character varying NOT NULL
);


ALTER TABLE public.music OWNER TO postgres;

--
-- TOC entry 224 (class 1259 OID 83456)
-- Name: music_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.music_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.music_id_seq OWNER TO postgres;

--
-- TOC entry 4850 (class 0 OID 0)
-- Dependencies: 224
-- Name: music_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.music_id_seq OWNED BY public.music.id;


--
-- TOC entry 220 (class 1259 OID 83432)
-- Name: sessions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.sessions (
    id integer NOT NULL,
    duration integer NOT NULL,
    status character varying NOT NULL,
    started_at timestamp without time zone NOT NULL,
    comment character varying,
    tag character varying NOT NULL,
    user_id integer NOT NULL,
    reason_code character varying
);


ALTER TABLE public.sessions OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 83431)
-- Name: sessions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.sessions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.sessions_id_seq OWNER TO postgres;

--
-- TOC entry 4851 (class 0 OID 0)
-- Dependencies: 219
-- Name: sessions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.sessions_id_seq OWNED BY public.sessions.id;


--
-- TOC entry 223 (class 1259 OID 83449)
-- Name: user_characters; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.user_characters (
    user_id integer NOT NULL,
    character_id integer NOT NULL,
    exp integer DEFAULT 0 NOT NULL,
    level integer DEFAULT 1 NOT NULL
);


ALTER TABLE public.user_characters OWNER TO postgres;

--
-- TOC entry 226 (class 1259 OID 83475)
-- Name: user_musics; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.user_musics (
    user_id integer NOT NULL,
    music_id integer NOT NULL
);


ALTER TABLE public.user_musics OWNER TO postgres;

--
-- TOC entry 218 (class 1259 OID 83421)
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id integer NOT NULL,
    username text NOT NULL,
    avatar_url text,
    coins integer DEFAULT 0 NOT NULL,
    best_streak integer DEFAULT 0 NOT NULL,
    act_char_id integer NOT NULL,
    max_id integer NOT NULL
);


ALTER TABLE public.users OWNER TO postgres;

--
-- TOC entry 217 (class 1259 OID 83420)
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO postgres;

--
-- TOC entry 4852 (class 0 OID 0)
-- Dependencies: 217
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- TOC entry 4668 (class 2604 OID 83444)
-- Name: characters id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.characters ALTER COLUMN id SET DEFAULT nextval('public.characters_id_seq'::regclass);


--
-- TOC entry 4671 (class 2604 OID 83460)
-- Name: music id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.music ALTER COLUMN id SET DEFAULT nextval('public.music_id_seq'::regclass);


--
-- TOC entry 4667 (class 2604 OID 83435)
-- Name: sessions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sessions ALTER COLUMN id SET DEFAULT nextval('public.sessions_id_seq'::regclass);


--
-- TOC entry 4664 (class 2604 OID 83424)
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- TOC entry 4839 (class 0 OID 83441)
-- Dependencies: 222
-- Data for Name: characters; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.characters (id, name, price, netrual_anim, win_anim, lose_anim, focus_anim, preview) FROM stdin;
3	Ласка Майдан	2014	ia	hochu	pizzi	silno	/static/characters/laska.png
4	Песик Бобр	0	/static/characters/dog_netrual.webm	/static/characters/dog_win.webm	/static/characters/dog_lose.webm	/static/characters/dog_focus.webm	/static/characters/dog.png
5	Робот Николай	0	/static/characters/robot_netrual.webm	/static/characters/robot_win.webm	/static/characters/robot_lose.webm	/static/characters/robot_focus.webm	/static/characters/robot.png
\.


--
-- TOC entry 4842 (class 0 OID 83457)
-- Dependencies: 225
-- Data for Name: music; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.music (id, price, name, path) FROM stdin;
1	5000	Белый шум	/static/music/white.mp3
2	1500	Облака	/static/music/oblaka.mp3
3	5000	Lofi музыка	/static/music/lofi.mp3
4	0	Сказочный лес	/static/music/les.mp3
5	0	Весенний дождь	/static/music/rain.mp3
6	35000	Аффирмация для работы	/static/music/affirmation.mp3
\.


--
-- TOC entry 4837 (class 0 OID 83432)
-- Dependencies: 220
-- Data for Name: sessions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.sessions (id, duration, status, started_at, comment, tag, user_id, reason_code) FROM stdin;
1	25	canceled	2025-11-11 13:51:27.004	sport	zalipa	3	потерял мотивацию
2	25	canceled	2025-11-11 13:46:56.255	sport	zalipa	3	потерял мотивацию
3	25	canceled	2025-11-11 14:46:21.609	sport	zalipa	3	потерял мотивацию
4	25	completed	2025-11-11 14:47:17.257	sport	zalipa	3	\N
5	25	completed	2025-11-11 14:50:32.917	sport	zalipa	3	\N
6	25	completed	2025-11-11 14:53:51.737	sport	zalipa	3	\N
7	25	completed	2025-11-11 14:56:48.913	sport	zalipa	3	\N
9	25	completed	2025-11-11 15:00:39.447	sport	zalipa	3	\N
10	25	completed	2025-11-11 15:03:38.936	sport	zalipa	3	\N
11	25	completed	2025-11-11 15:04:51.569	sport	zalipa	3	\N
12	25	completed	2025-11-11 15:05:11.428	sport	zalipa	3	\N
13	25	completed	2025-11-11 15:05:57.754	sport	zalipa	3	\N
14	25	completed	2025-11-11 15:07:40.38	sport	zalipa	3	\N
15	25	completed	2025-11-10 14:57:32.935	sport	zalipa	3	\N
16	25	completed	2025-11-11 15:10:07.497	sport	zalipa	3	\N
17	25	completed	2025-11-11 15:10:41.168	sport	zalipa	3	\N
8	25	completed	2025-11-09 14:57:32.935	sport	zalipa	3	\N
18	25	completed	2025-11-11 14:57:32.935	sport	zalipa	3	\N
19	25	completed	2025-11-11 15:12:10.118	sport	zalipa	3	\N
20	25	completed	2025-11-11 15:12:25.707	sport	zalipa	3	\N
21	25	completed	2025-11-11 15:12:35.851	sport	zalipa	3	\N
22	25	completed	2025-11-11 15:12:47.985	sport	zalipa	3	\N
23	25	completed	2025-11-11 15:13:24.767	sport	zalipa	3	\N
24	25	completed	2025-11-11 15:13:49.996	sport	zalipa	3	\N
25	25	completed	2025-11-11 15:14:26.716	sport	zalipa	3	\N
26	25	canceled	2025-11-11 15:16:41.832	sport	zalipa	3	\N
27	25	canceled	2025-11-11 15:26:36.198	sport	zalipa	3	\N
28	25	canceled	2025-11-11 15:27:18.354	sport	zalipa	3	\N
29	25	canceled	2025-11-12 01:14:37.133	zalipa	sport	3	потерял мотивацию
30	5	canceled	2025-11-12 01:37:33.342		спорт	3	\N
31	5	canceled	2025-11-12 01:39:46.214		спорт	3	\N
32	5	canceled	2025-11-12 01:46:28.101		спорт	3	\N
33	5	canceled	2025-11-12 01:47:03.197		спорт	3	\N
34	5	canceled	2025-11-12 01:57:06.675		спорт	3	\N
35	5	canceled	2025-11-12 02:04:35.046		спорт	3	\N
36	5	canceled	2025-11-12 02:13:12.376		спорт	3	\N
37	5	canceled	2025-11-12 02:17:27.21		спорт	3	\N
38	5	canceled	2025-11-12 02:25:33.399		спорт	3	\N
39	5	canceled	2025-11-12 02:28:00.079		спорт	3	\N
40	5	canceled	2025-11-12 02:31:51.951		спорт	4	\N
41	5	canceled	2025-11-12 02:31:51.951		спорт	3	\N
42	5	canceled	2025-11-12 02:35:13.683		спорт	4	\N
43	2	canceled	2025-11-12 12:35:05.195		спорт	4	\N
45	2	canceled	2025-11-12 12:53:31.627		спорт	3	\N
46	2	canceled	2025-11-12 12:53:31.627		спорт	4	\N
47	2	canceled	2025-11-12 12:54:35.127		спорт	3	\N
48	2	canceled	2025-11-12 12:57:00.528		спорт	3	\N
49	2	completed	2025-11-12 12:57:00.528		спорт	4	\N
52	2	canceled	2025-11-12 13:08:22.572		спорт	3	\N
53	2	completed	2025-11-12 13:08:22.572		спорт	4	\N
54	2	completed	2025-11-12 13:19:18.092		спорт	4	\N
56	5	completed	2025-11-12 13:25:07.025		спорт	4	\N
58	5	canceled	2025-11-12 13:41:15.14		спорт	3	\N
59	5	completed	2025-11-12 13:41:15.14		спорт	4	\N
51	1	completed	2025-11-12 13:05:06.461		работа	3	\N
55	2	completed	2025-11-12 13:19:18.092		работа	3	\N
83	25	canceled	2025-11-13 18:45:19.819		study	4	\N
44	2	canceled	2025-11-12 12:35:05.195		спорт	3	обосрался
50	1	completed	2025-11-12 08:00:42.893		спорт	3	\N
57	5	completed	2025-11-12 14:25:07.025		отдых	3	\N
60	25	canceled	2025-11-12 22:28:08.966	zalipa	sport	4	\N
61	25	canceled	2025-11-12 22:28:08.966	zalipa	sport	3	\N
62	25	canceled	2025-11-12 22:28:08.966	zalipa	sport	3	\N
63	25	canceled	2025-11-12 22:59:16.918	zalipa	sport	3	\N
64	25	completed	2025-11-12 22:59:16.918	zalipa	sport	3	\N
65	25	canceled	2025-11-12 22:59:16.918	zalipa	sport	3	потерял мотивацию
66	25	canceled	2025-11-13 16:22:04.569	zalipa	sport	4	\N
67	25	canceled	2025-11-13 16:22:04.569	zalipa	sport	4	\N
68	25	completed	2025-11-13 16:22:04.569	zalipa	sport	4	\N
69	25	canceled	2025-11-13 16:22:04.569	zalipa	sport	4	\N
70	25	canceled	2025-11-13 16:22:04.569	zalipa	sport	4	\N
71	1	completed	2025-11-13 16:22:04.569	zalipa	sport	4	\N
72	1	canceled	2025-11-13 16:22:04.569	zalipa	sport	4	\N
73	1	completed	2025-11-13 16:22:04.569	zalipa	sport	4	\N
74	25	completed	2025-11-13 16:22:04.569	zalipa	sport	6	\N
75	25	canceled	2025-11-13 16:22:04.569	zalipa	sport	7	\N
76	25	canceled	2025-11-13 16:22:04.569	zalipa	sport	7	\N
77	25	completed	2025-11-13 17:01:11.764	zalipa	sport	5	\N
78	25	completed	2025-11-13 17:02:32.744	zalipa	sport	5	\N
79	25	completed	2025-11-13 17:03:59.767	zalipa	sport	5	\N
80	25	canceled	2025-11-13 17:03:59.767	zalipa	sport	8	\N
81	25	completed	2025-11-13 17:03:59.767	zalipa	sport	8	\N
82	25	completed	2025-11-13 18:35:25.17	zalipa	sport	5	\N
84	25	canceled	2025-11-13 19:13:52.816	zalipa	sport	8	\N
85	25	completed	2025-11-13 19:13:52.816	zalipa	sport	8	\N
86	25	canceled	2025-11-13 19:13:52.816	zalipa	sport	8	\N
87	25	canceled	2025-11-13 19:13:52.816	zalipa	sport	8	потерял мотивацию
88	25	canceled	2025-11-13 19:22:29.898		study	4	\N
89	25	canceled	2025-11-13 19:22:29.898		study	4	\N
90	25	canceled	2025-11-13 19:22:29.898		study	4	\N
91	25	canceled	2025-11-13 19:22:29.898		study	4	\N
92	25	canceled	2025-11-13 19:22:29.898		study	4	\N
93	25	canceled	2025-11-13 19:22:29.898		study	4	\N
94	25	canceled	2025-11-13 19:22:29.898		study	4	\N
95	25	canceled	2025-11-13 19:53:21.094		study	10	\N
96	25	canceled	2025-11-13 19:53:21.094	zalipa	sport	5	\N
97	25	canceled	2025-11-13 19:57:04.961	zalipa	sport	5	\N
98	25	canceled	2025-11-13 19:58:15.725	zalipa	sport	5	\N
99	25	canceled	2025-11-13 19:58:15.725		study	10	\N
100	25	canceled	2025-11-13 19:58:15.725	zalipa	sport	5	\N
101	25	canceled	2025-11-13 20:05:32.013		study	10	потерял мотивацию
102	25	canceled	2025-11-13 20:05:32.013	zalipa	sport	5	\N
103	25	canceled	2025-11-13 20:05:32.013		study	10	\N
104	5	canceled	2025-11-13 20:05:32.013		study	10	\N
105	25	canceled	2025-11-13 20:31:47.385		study	10	потерял мотивацию
106	5	completed	2025-11-13 20:31:47.385		study	10	\N
107	25	canceled	2025-11-13 21:06:45.789		study	10	\N
108	25	canceled	2025-11-13 21:06:45.789		study	10	потерял мотивацию
109	25	canceled	2025-11-13 21:06:45.789	zalipa	sport	5	\N
110	5	completed	2025-11-13 21:06:45.789		study	10	\N
111	25	canceled	2025-11-13 21:25:54.556		study	10	\N
112	5	canceled	2025-11-13 21:25:54.556		sport	10	\N
113	25	canceled	2025-11-13 21:25:54.556		sport	10	\N
114	5	canceled	2025-11-13 21:25:54.556		study	10	потерял мотивацию
115	5	canceled	2025-11-13 21:25:54.556		study	10	другое
\.


--
-- TOC entry 4840 (class 0 OID 83449)
-- Dependencies: 223
-- Data for Name: user_characters; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.user_characters (user_id, character_id, exp, level) FROM stdin;
3	5	0	1
3	4	52	2
5	5	0	1
6	5	0	1
6	4	0	1
7	5	0	1
7	4	0	1
5	4	123	1
8	5	0	1
5	3	123	1
8	4	246	1
9	5	0	1
9	4	0	1
10	5	0	1
10	4	50	1
\.


--
-- TOC entry 4843 (class 0 OID 83475)
-- Dependencies: 226
-- Data for Name: user_musics; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.user_musics (user_id, music_id) FROM stdin;
3	4
3	5
5	5
5	4
6	5
6	4
7	5
7	4
8	5
8	4
9	5
9	4
10	5
10	4
\.


--
-- TOC entry 4835 (class 0 OID 83421)
-- Dependencies: 218
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, username, avatar_url, coins, best_streak, act_char_id, max_id) FROM stdin;
7	Федорs Безруковs		0	0	2	5226
3	Айнур Шакиров		747	4	4	423432
4	Федор Безруков		44	1	4	5223
6	Федор Безруков		0	0	4	5225
5	Федор Безруков		1375	1	3	5224
8	Федорs Безруковs		112	1	4	5227
9	Федор Безруков		0	0	4	5231
10	Федор Безруков		22	1	4	5230
\.


--
-- TOC entry 4853 (class 0 OID 0)
-- Dependencies: 221
-- Name: characters_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.characters_id_seq', 5, true);


--
-- TOC entry 4854 (class 0 OID 0)
-- Dependencies: 224
-- Name: music_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.music_id_seq', 6, true);


--
-- TOC entry 4855 (class 0 OID 0)
-- Dependencies: 219
-- Name: sessions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.sessions_id_seq', 115, true);


--
-- TOC entry 4856 (class 0 OID 0)
-- Dependencies: 217
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 10, true);


--
-- TOC entry 4677 (class 2606 OID 83448)
-- Name: characters characters_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.characters
    ADD CONSTRAINT characters_pkey PRIMARY KEY (id);


--
-- TOC entry 4681 (class 2606 OID 83464)
-- Name: music music_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.music
    ADD CONSTRAINT music_pkey PRIMARY KEY (id);


--
-- TOC entry 4675 (class 2606 OID 83439)
-- Name: sessions sessions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sessions
    ADD CONSTRAINT sessions_pkey PRIMARY KEY (id);


--
-- TOC entry 4679 (class 2606 OID 83455)
-- Name: user_characters user_characters_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_characters
    ADD CONSTRAINT user_characters_pkey PRIMARY KEY (user_id, character_id);


--
-- TOC entry 4683 (class 2606 OID 83479)
-- Name: user_musics user_musics_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_musics
    ADD CONSTRAINT user_musics_pkey PRIMARY KEY (user_id, music_id);


--
-- TOC entry 4673 (class 2606 OID 83430)
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- TOC entry 4684 (class 2606 OID 83510)
-- Name: sessions sessions_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.sessions
    ADD CONSTRAINT sessions_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON UPDATE CASCADE ON DELETE CASCADE NOT VALID;


--
-- TOC entry 4685 (class 2606 OID 83495)
-- Name: user_characters user_characters_character_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_characters
    ADD CONSTRAINT user_characters_character_id_fkey FOREIGN KEY (character_id) REFERENCES public.characters(id) ON UPDATE CASCADE ON DELETE CASCADE NOT VALID;


--
-- TOC entry 4686 (class 2606 OID 83490)
-- Name: user_characters user_characters_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_characters
    ADD CONSTRAINT user_characters_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON UPDATE CASCADE ON DELETE CASCADE NOT VALID;


--
-- TOC entry 4687 (class 2606 OID 83505)
-- Name: user_musics user_musics_music_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_musics
    ADD CONSTRAINT user_musics_music_id_fkey FOREIGN KEY (music_id) REFERENCES public.music(id) ON UPDATE CASCADE ON DELETE CASCADE NOT VALID;


--
-- TOC entry 4688 (class 2606 OID 83500)
-- Name: user_musics user_musics_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.user_musics
    ADD CONSTRAINT user_musics_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON UPDATE CASCADE ON DELETE CASCADE NOT VALID;


-- Completed on 2025-11-13 22:38:13

--
-- PostgreSQL database dump complete
--

