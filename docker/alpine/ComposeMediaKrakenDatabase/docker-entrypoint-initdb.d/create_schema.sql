--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.3
-- Dumped by pg_dump version 9.6.4

-- Started on 2017-08-16 13:43:04 CDT

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 1 (class 3079 OID 12390)
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- TOC entry 2595 (class 0 OID 0)
-- Dependencies: 1
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


--
-- TOC entry 2 (class 3079 OID 16890)
-- Name: pg_trgm; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS pg_trgm WITH SCHEMA public;


--
-- TOC entry 2596 (class 0 OID 0)
-- Dependencies: 2
-- Name: EXTENSION pg_trgm; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION pg_trgm IS 'text similarity measurement and index searching based on trigrams';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- TOC entry 215 (class 1259 OID 25738)
-- Name: mm_channel; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE mm_channel (
    mm_channel_guid uuid NOT NULL,
    mm_channel_name text,
    mm_channel_media_id jsonb,
    mm_channel_country_guid uuid,
    mm_channel_logo_guid uuid
);


ALTER TABLE mm_channel OWNER TO metamanpg;

--
-- TOC entry 209 (class 1259 OID 25691)
-- Name: mm_cron; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE mm_cron (
    mm_cron_guid uuid NOT NULL,
    mm_cron_name text,
    mm_cron_description text,
    mm_cron_enabled boolean,
    mm_cron_schedule text,
    mm_cron_last_run timestamp without time zone,
    mm_cron_file_path text
);


ALTER TABLE mm_cron OWNER TO metamanpg;

--
-- TOC entry 224 (class 1259 OID 25827)
-- Name: mm_device; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE mm_device (
    mm_device_id uuid NOT NULL,
    mm_device_type text,
    mm_device_json jsonb
);


ALTER TABLE mm_device OWNER TO metamanpg;

--
-- TOC entry 223 (class 1259 OID 25818)
-- Name: mm_download_image_que; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE mm_download_image_que (
    mdq_image_id uuid NOT NULL,
    mdq_image_provider text,
    mdq_image_download_json jsonb
);


ALTER TABLE mm_download_image_que OWNER TO metamanpg;

--
-- TOC entry 222 (class 1259 OID 25807)
-- Name: mm_download_que; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE mm_download_que (
    mdq_id uuid NOT NULL,
    mdq_provider text,
    mdq_que_type smallint,
    mdq_download_json jsonb
);


ALTER TABLE mm_download_que OWNER TO metamanpg;

--
-- TOC entry 191 (class 1259 OID 25476)
-- Name: mm_link; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE mm_link (
    mm_link_guid uuid NOT NULL,
    mm_link_name text,
    mm_link_json jsonb
);


ALTER TABLE mm_link OWNER TO metamanpg;

--
-- TOC entry 212 (class 1259 OID 25716)
-- Name: mm_loan; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE mm_loan (
    mm_loan_guid uuid NOT NULL,
    mm_loan_media_id uuid,
    mm_loan_user_id uuid,
    mm_load_user_loan_id uuid,
    mm_loan_time timestamp without time zone,
    mm_loan_return_time timestamp without time zone
);


ALTER TABLE mm_loan OWNER TO metamanpg;

--
-- TOC entry 189 (class 1259 OID 25454)
-- Name: mm_media; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE mm_media (
    mm_media_guid uuid NOT NULL,
    mm_media_class_guid uuid,
    mm_media_metadata_guid uuid,
    mm_media_path text,
    mm_media_ffprobe_json jsonb,
    mm_media_json jsonb
);


ALTER TABLE mm_media OWNER TO metamanpg;

--
-- TOC entry 197 (class 1259 OID 25561)
-- Name: mm_media_class; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE mm_media_class (
    mm_media_class_guid uuid NOT NULL,
    mm_media_class_type text,
    mm_media_class_parent_type text,
    mm_media_class_display boolean
);


ALTER TABLE mm_media_class OWNER TO metamanpg;

--
-- TOC entry 188 (class 1259 OID 25445)
-- Name: mm_media_dir; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE mm_media_dir (
    mm_media_dir_guid uuid NOT NULL,
    mm_media_dir_path text,
    mm_media_dir_class_type uuid,
    mm_media_dir_last_scanned timestamp without time zone,
    mm_media_dir_share_guid uuid,
    mm_media_dir_status jsonb
);


ALTER TABLE mm_media_dir OWNER TO metamanpg;

--
-- TOC entry 190 (class 1259 OID 25465)
-- Name: mm_media_remote; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE mm_media_remote (
    mmr_media_guid uuid NOT NULL,
    mmr_media_link_id uuid,
    mmr_media_uuid uuid,
    mmr_media_class_guid uuid,
    mmr_media_metadata_guid uuid,
    mmr_media_ffprobe_json jsonb,
    mmr_media_json jsonb
);


ALTER TABLE mm_media_remote OWNER TO metamanpg;

--
-- TOC entry 187 (class 1259 OID 25437)
-- Name: mm_media_share; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE mm_media_share (
    mm_media_share_guid uuid NOT NULL,
    mm_media_share_type text,
    mm_media_share_user text,
    mm_media_share_password text,
    mm_media_share_server text,
    mm_media_share_path text
);


ALTER TABLE mm_media_share OWNER TO metamanpg;

--
-- TOC entry 195 (class 1259 OID 25535)
-- Name: mm_metadata_album; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE mm_metadata_album (
    mm_metadata_album_guid uuid NOT NULL,
    mm_metadata_album_name text,
    mm_metadata_album_id jsonb,
    mm_metadata_album_json jsonb,
    mm_metadata_album_musician_guid uuid
);


ALTER TABLE mm_metadata_album OWNER TO metamanpg;

--
-- TOC entry 198 (class 1259 OID 25570)
-- Name: mm_metadata_anime; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE mm_metadata_anime (
    mm_metadata_anime_guid uuid NOT NULL,
    mm_metadata_anime_media_id jsonb,
    mm_media_anime_name text,
    mm_metadata_anime_json jsonb,
    mm_metadata_anime_mapping jsonb,
    mm_metadata_anime_mapping_before text,
    mm_metadata_anime_localimage_json jsonb,
    mm_metadata_anime_user_json jsonb
);


ALTER TABLE mm_metadata_anime OWNER TO metamanpg;

--
-- TOC entry 201 (class 1259 OID 25618)
-- Name: mm_metadata_book; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE mm_metadata_book (
    mm_metadata_book_guid uuid NOT NULL,
    mm_metadata_book_isbn text,
    mm_metadata_book_isbn13 text,
    mm_metadata_book_name text,
    mm_metadata_book_json jsonb,
    mm_metadata_book_image_json jsonb
);


ALTER TABLE mm_metadata_book OWNER TO metamanpg;

--
-- TOC entry 207 (class 1259 OID 25672)
-- Name: mm_metadata_collection; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE mm_metadata_collection (
    mm_metadata_collection_guid uuid NOT NULL,
    mm_metadata_collection_name jsonb,
    mm_metadata_collection_media_ids jsonb,
    mm_metadata_collection_json jsonb,
    mm_metadata_collection_imagelocal_json jsonb
);


ALTER TABLE mm_metadata_collection OWNER TO metamanpg;

--
-- TOC entry 219 (class 1259 OID 25776)
-- Name: mm_metadata_game_software_info; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE mm_metadata_game_software_info (
    gi_id uuid NOT NULL,
    gi_system_id uuid,
    gi_game_info_json jsonb
);


ALTER TABLE mm_metadata_game_software_info OWNER TO metamanpg;

--
-- TOC entry 220 (class 1259 OID 25787)
-- Name: mm_metadata_game_systems_info; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE mm_metadata_game_systems_info (
    gs_id uuid NOT NULL,
    gs_game_system_id integer,
    gs_game_system_name text,
    gs_game_system_alias text,
    gs_game_system_json jsonb
);


ALTER TABLE mm_metadata_game_systems_info OWNER TO metamanpg;

--
-- TOC entry 214 (class 1259 OID 25729)
-- Name: mm_metadata_logo; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE mm_metadata_logo (
    mm_metadata_logo_guid uuid NOT NULL,
    mm_metadata_logo_media_guid jsonb,
    mm_metadata_logo_image_path text
);


ALTER TABLE mm_metadata_logo OWNER TO metamanpg;

--
-- TOC entry 199 (class 1259 OID 25587)
-- Name: mm_metadata_movie; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE mm_metadata_movie (
    mm_metadata_guid uuid NOT NULL,
    mm_metadata_media_id jsonb,
    mm_media_name text,
    mm_metadata_json jsonb,
    mm_metadata_localimage_json jsonb,
    mm_metadata_user_json jsonb
);


ALTER TABLE mm_metadata_movie OWNER TO metamanpg;

--
-- TOC entry 196 (class 1259 OID 25548)
-- Name: mm_metadata_music; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE mm_metadata_music (
    mm_metadata_music_guid uuid NOT NULL,
    mm_metadata_media_music_id jsonb,
    mm_metadata_music_name text,
    mm_metadata_music_json jsonb,
    mm_metadata_music_album_guid uuid
);


ALTER TABLE mm_metadata_music OWNER TO metamanpg;

--
-- TOC entry 200 (class 1259 OID 25603)
-- Name: mm_metadata_music_video; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE mm_metadata_music_video (
    mm_metadata_music_video_guid uuid NOT NULL,
    mm_metadata_music_video_media_id jsonb,
    mm_media_music_video_band text,
    mm_media_music_video_song text,
    mm_metadata_music_video_json jsonb,
    mm_metadata_music_video_localimage_json jsonb
);


ALTER TABLE mm_metadata_music_video OWNER TO metamanpg;

--
-- TOC entry 194 (class 1259 OID 25523)
-- Name: mm_metadata_musician; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE mm_metadata_musician (
    mm_metadata_musician_guid uuid NOT NULL,
    mm_metadata_musician_name text,
    mm_metadata_musician_id jsonb,
    mm_metadata_musician_json jsonb
);


ALTER TABLE mm_metadata_musician OWNER TO metamanpg;

--
-- TOC entry 221 (class 1259 OID 25796)
-- Name: mm_metadata_person; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE mm_metadata_person (
    mmp_id uuid NOT NULL,
    mmp_person_media_id jsonb,
    mmp_person_meta_json jsonb,
    mmp_person_image jsonb,
    mmp_person_name text
);


ALTER TABLE mm_metadata_person OWNER TO metamanpg;

--
-- TOC entry 193 (class 1259 OID 25505)
-- Name: mm_metadata_sports; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE mm_metadata_sports (
    mm_metadata_sports_guid uuid NOT NULL,
    mm_metadata_media_sports_id jsonb,
    mm_metadata_sports_name text,
    mm_metadata_sports_json jsonb,
    mm_metadata_sports_image_json jsonb
);


ALTER TABLE mm_metadata_sports OWNER TO metamanpg;

--
-- TOC entry 192 (class 1259 OID 25486)
-- Name: mm_metadata_tvshow; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE mm_metadata_tvshow (
    mm_metadata_tvshow_guid uuid NOT NULL,
    mm_metadata_media_tvshow_id jsonb,
    mm_metadata_tvshow_name text,
    mm_metadata_tvshow_json jsonb,
    mm_metadata_tvshow_localimage_json jsonb,
    mm_metadata_tvshow_user_json jsonb
);


ALTER TABLE mm_metadata_tvshow OWNER TO metamanpg;

--
-- TOC entry 203 (class 1259 OID 25640)
-- Name: mm_notification; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE mm_notification (
    mm_notification_guid uuid NOT NULL,
    mm_notification_text text,
    mm_notification_time timestamp without time zone,
    mm_notification_dismissable boolean
);


ALTER TABLE mm_notification OWNER TO metamanpg;

--
-- TOC entry 218 (class 1259 OID 25768)
-- Name: mm_options_and_status; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE mm_options_and_status (
    mm_options_and_status_guid uuid NOT NULL,
    mm_options_json jsonb,
    mm_status_json jsonb
);


ALTER TABLE mm_options_and_status OWNER TO metamanpg;

--
-- TOC entry 210 (class 1259 OID 25699)
-- Name: mm_radio; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE mm_radio (
    mm_radio_guid uuid NOT NULL,
    mm_radio_name text,
    mm_radio_adress text,
    mm_radio_active boolean
);


ALTER TABLE mm_radio OWNER TO metamanpg;

--
-- TOC entry 206 (class 1259 OID 25662)
-- Name: mm_review; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE mm_review (
    mm_review_guid uuid NOT NULL,
    mm_review_metadata_id jsonb,
    mm_review_metadata_guid uuid,
    mm_review_json jsonb
);


ALTER TABLE mm_review OWNER TO metamanpg;

--
-- TOC entry 211 (class 1259 OID 25707)
-- Name: mm_sync; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE mm_sync (
    mm_sync_guid uuid NOT NULL,
    mm_sync_path text,
    mm_sync_path_to text,
    mm_sync_options_json jsonb
);


ALTER TABLE mm_sync OWNER TO metamanpg;

--
-- TOC entry 208 (class 1259 OID 25683)
-- Name: mm_task; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE mm_task (
    mm_task_guid uuid NOT NULL,
    mm_task_name text,
    mm_task_description text,
    mm_task_enabled boolean,
    mm_task_schedule text,
    mm_task_last_run timestamp without time zone,
    mm_task_file_path text,
    mm_task_json jsonb
);


ALTER TABLE mm_task OWNER TO metamanpg;

--
-- TOC entry 213 (class 1259 OID 25721)
-- Name: mm_trigger; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE mm_trigger (
    mm_trigger_guid uuid NOT NULL,
    mm_trigger_command bytea,
    mm_trigger_background boolean
);


ALTER TABLE mm_trigger OWNER TO metamanpg;

--
-- TOC entry 226 (class 1259 OID 25847)
-- Name: mm_tv_schedule; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE mm_tv_schedule (
    mm_tv_schedule_id uuid NOT NULL,
    mm_tv_schedule_station_id text,
    mm_tv_schedule_date date,
    mm_tv_schedule_json jsonb
);


ALTER TABLE mm_tv_schedule OWNER TO metamanpg;

--
-- TOC entry 227 (class 1259 OID 25857)
-- Name: mm_tv_schedule_program; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE mm_tv_schedule_program (
    mm_tv_schedule_program_guid uuid NOT NULL,
    mm_tv_schedule_program_id text,
    mm_tv_schedule_program_json jsonb
);


ALTER TABLE mm_tv_schedule_program OWNER TO metamanpg;

--
-- TOC entry 225 (class 1259 OID 25837)
-- Name: mm_tv_stations; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE mm_tv_stations (
    mm_tv_stations_id uuid NOT NULL,
    mm_tv_station_name text,
    mm_tv_station_id text,
    mm_tv_station_channel text,
    mm_tv_station_json jsonb,
    mm_tv_station_image text
);


ALTER TABLE mm_tv_stations OWNER TO metamanpg;

--
-- TOC entry 205 (class 1259 OID 25652)
-- Name: mm_user; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE mm_user (
    id integer NOT NULL,
    username text,
    email text,
    password text,
    created_at timestamp with time zone,
    active boolean,
    is_admin boolean,
    user_json jsonb,
    lang text
);


ALTER TABLE mm_user OWNER TO metamanpg;

--
-- TOC entry 202 (class 1259 OID 25630)
-- Name: mm_user_activity; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE mm_user_activity (
    mm_activity_guid uuid NOT NULL,
    mm_activity_name text,
    mm_activity_overview text,
    mm_activity_short_overview text,
    mm_activity_type text,
    mm_activity_itemid uuid,
    mm_activity_userid uuid,
    mm_activity_datecreated timestamp without time zone,
    mm_activity_log_severity text
);


ALTER TABLE mm_user_activity OWNER TO metamanpg;

--
-- TOC entry 216 (class 1259 OID 25750)
-- Name: mm_user_group; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE mm_user_group (
    mm_user_group_guid uuid NOT NULL,
    mm_user_group_name text,
    mm_user_group_description text,
    mm_user_group_rights_json jsonb
);


ALTER TABLE mm_user_group OWNER TO metamanpg;

--
-- TOC entry 204 (class 1259 OID 25650)
-- Name: mm_user_id_seq; Type: SEQUENCE; Schema: public; Owner: metamanpg
--

CREATE SEQUENCE mm_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE mm_user_id_seq OWNER TO metamanpg;

--
-- TOC entry 2597 (class 0 OID 0)
-- Dependencies: 204
-- Name: mm_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: metamanpg
--

ALTER SEQUENCE mm_user_id_seq OWNED BY mm_user.id;


--
-- TOC entry 217 (class 1259 OID 25759)
-- Name: mm_user_profile; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE mm_user_profile (
    mm_user_profile_guid uuid NOT NULL,
    mm_user_profile_name text,
    mm_user_profile_json jsonb
);


ALTER TABLE mm_user_profile OWNER TO metamanpg;

--
-- TOC entry 186 (class 1259 OID 25434)
-- Name: mm_version; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE mm_version (
    mm_version_no integer
);


ALTER TABLE mm_version OWNER TO metamanpg;

--
-- TOC entry 2240 (class 2604 OID 25655)
-- Name: mm_user id; Type: DEFAULT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_user ALTER COLUMN id SET DEFAULT nextval('mm_user_id_seq'::regclass);


--
-- TOC entry 2576 (class 0 OID 25738)
-- Dependencies: 215
-- Data for Name: mm_channel; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_channel (mm_channel_guid, mm_channel_name, mm_channel_media_id, mm_channel_country_guid, mm_channel_logo_guid) FROM stdin;
\.


--
-- TOC entry 2570 (class 0 OID 25691)
-- Dependencies: 209
-- Data for Name: mm_cron; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_cron (mm_cron_guid, mm_cron_name, mm_cron_description, mm_cron_enabled, mm_cron_schedule, mm_cron_last_run, mm_cron_file_path) FROM stdin;
\.


--
-- TOC entry 2585 (class 0 OID 25827)
-- Dependencies: 224
-- Data for Name: mm_device; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_device (mm_device_id, mm_device_type, mm_device_json) FROM stdin;
\.


--
-- TOC entry 2584 (class 0 OID 25818)
-- Dependencies: 223
-- Data for Name: mm_download_image_que; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_download_image_que (mdq_image_id, mdq_image_provider, mdq_image_download_json) FROM stdin;
\.


--
-- TOC entry 2583 (class 0 OID 25807)
-- Dependencies: 222
-- Data for Name: mm_download_que; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_download_que (mdq_id, mdq_provider, mdq_que_type, mdq_download_json) FROM stdin;
\.


--
-- TOC entry 2552 (class 0 OID 25476)
-- Dependencies: 191
-- Data for Name: mm_link; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_link (mm_link_guid, mm_link_name, mm_link_json) FROM stdin;
\.


--
-- TOC entry 2573 (class 0 OID 25716)
-- Dependencies: 212
-- Data for Name: mm_loan; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_loan (mm_loan_guid, mm_loan_media_id, mm_loan_user_id, mm_load_user_loan_id, mm_loan_time, mm_loan_return_time) FROM stdin;
\.


--
-- TOC entry 2550 (class 0 OID 25454)
-- Dependencies: 189
-- Data for Name: mm_media; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_media (mm_media_guid, mm_media_class_guid, mm_media_metadata_guid, mm_media_path, mm_media_ffprobe_json, mm_media_json) FROM stdin;
\.


--
-- TOC entry 2558 (class 0 OID 25561)
-- Dependencies: 197
-- Data for Name: mm_media_class; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_media_class (mm_media_class_guid, mm_media_class_type, mm_media_class_parent_type, mm_media_class_display) FROM stdin;
3e8ef351-257c-496d-bd8a-4de0e1d4c8ea	Adult	Video	t
cf025a62-0db1-42a5-b751-c5b3b31cc75e	Anime	Video	t
43cc5964-7c33-4213-87ee-60e2955c55c6	Book	Publication	t
fe97fc71-d466-4cd1-b680-3b2f4c9c2078	Boxset	\N	f
5f8850ff-efc3-4039-b920-d154e84962d4	Game CHD	\N	f
c204feb0-cbd0-4815-8497-8a32e3c80b78	Game ISO	\N	f
073ce8c4-a1d3-467e-b930-215e587c1f2d	Game ROM	\N	f
857addce-d093-4601-ae3b-f120172b7995	Home Movie	Video	t
d5ac35b8-a79f-467b-9b72-442b508dd838	Magazine	Publication	t
a60ed442-2491-4e14-8897-23576d63cde6	Movie	Video	t
323d23c0-ec92-414e-a073-a187ce5cd5bd	Movie Extras	Video	f
7455c6e0-6bc8-467a-b1ff-09a60ae21c16	Movie Collection	\N	f
0f983d07-34db-4dc9-a4ff-eb257b03bcbd	Movie Theme	Audio	f
674431ae-05a5-40b8-bcb0-035c0ce5962a	Movie Trailer	Video	f
f840035a-646c-45d6-96d2-be74f378307d	Music	Audio	t
20e08928-8ce5-4975-af99-3731e26f4907	Music Album	\N	f
987aa771-9878-4705-aac1-65a7278006d9	Music Collection	\N	f
dccbd0ab-50a9-413d-ab36-1ae04b857bf5	Music Lyric	\N	f
f5ad94a0-cec7-4baa-8007-ee19d4ffeffb	Music Video	Video	t
56e7460a-e752-4545-afd1-7882998d9dac	Person	\N	f
80bd988e-9cfa-42af-926f-8124abdec329	Picture	Image	t
c89eb31f-0d73-4018-b9a7-72a5c443d9e2	Soundtrack	Audio	f
1d90bc2c-a3be-4682-a722-ea1f2cedefd3	Sports	Video	t
7385790d-27e3-4ffd-a32d-b35136652972	Subtitle	\N	f
f4981eda-9f86-4726-b2e2-024ff683b916	TV Episode	Video	f
6bde3ac8-e5aa-4f8f-99e7-1f1014d31dc1	TV Extras	Video	f
e9138a44-290a-4325-a5cb-5e37d8ade973	TV Season	\N	f
f953d03d-a722-49ae-95ec-c93118fc2f9c	TV Show	Video	t
b8b84b41-38c5-4907-bc1e-f14fefa1b945	TV Theme	Audio	f
30828b2c-67f9-4f2f-a8fd-a441dd5b3a2c	TV Trailer	Video	f
86acc897-6598-4e31-8a3c-b78d9bfc96de	Video Game	Game	t
e17473e6-6d90-43c8-8802-f4c19d6c5053	Video Game Intro	Video	t
47196979-71da-400e-bdbf-976b0cae309a	Video Game Speedrun	Video	t
258ab4c3-7d61-4446-b273-112669292d18	Video Game Superplay	Video	t
\.


--
-- TOC entry 2549 (class 0 OID 25445)
-- Dependencies: 188
-- Data for Name: mm_media_dir; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_media_dir (mm_media_dir_guid, mm_media_dir_path, mm_media_dir_class_type, mm_media_dir_last_scanned, mm_media_dir_share_guid, mm_media_dir_status) FROM stdin;
\.


--
-- TOC entry 2551 (class 0 OID 25465)
-- Dependencies: 190
-- Data for Name: mm_media_remote; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_media_remote (mmr_media_guid, mmr_media_link_id, mmr_media_uuid, mmr_media_class_guid, mmr_media_metadata_guid, mmr_media_ffprobe_json, mmr_media_json) FROM stdin;
\.


--
-- TOC entry 2548 (class 0 OID 25437)
-- Dependencies: 187
-- Data for Name: mm_media_share; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_media_share (mm_media_share_guid, mm_media_share_type, mm_media_share_user, mm_media_share_password, mm_media_share_server, mm_media_share_path) FROM stdin;
\.


--
-- TOC entry 2556 (class 0 OID 25535)
-- Dependencies: 195
-- Data for Name: mm_metadata_album; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_metadata_album (mm_metadata_album_guid, mm_metadata_album_name, mm_metadata_album_id, mm_metadata_album_json, mm_metadata_album_musician_guid) FROM stdin;
\.


--
-- TOC entry 2559 (class 0 OID 25570)
-- Dependencies: 198
-- Data for Name: mm_metadata_anime; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_metadata_anime (mm_metadata_anime_guid, mm_metadata_anime_media_id, mm_media_anime_name, mm_metadata_anime_json, mm_metadata_anime_mapping, mm_metadata_anime_mapping_before, mm_metadata_anime_localimage_json, mm_metadata_anime_user_json) FROM stdin;
\.


--
-- TOC entry 2562 (class 0 OID 25618)
-- Dependencies: 201
-- Data for Name: mm_metadata_book; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_metadata_book (mm_metadata_book_guid, mm_metadata_book_isbn, mm_metadata_book_isbn13, mm_metadata_book_name, mm_metadata_book_json, mm_metadata_book_image_json) FROM stdin;
\.


--
-- TOC entry 2568 (class 0 OID 25672)
-- Dependencies: 207
-- Data for Name: mm_metadata_collection; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_metadata_collection (mm_metadata_collection_guid, mm_metadata_collection_name, mm_metadata_collection_media_ids, mm_metadata_collection_json, mm_metadata_collection_imagelocal_json) FROM stdin;
\.


--
-- TOC entry 2580 (class 0 OID 25776)
-- Dependencies: 219
-- Data for Name: mm_metadata_game_software_info; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_metadata_game_software_info (gi_id, gi_system_id, gi_game_info_json) FROM stdin;
\.


--
-- TOC entry 2581 (class 0 OID 25787)
-- Dependencies: 220
-- Data for Name: mm_metadata_game_systems_info; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_metadata_game_systems_info (gs_id, gs_game_system_id, gs_game_system_name, gs_game_system_alias, gs_game_system_json) FROM stdin;
\.


--
-- TOC entry 2575 (class 0 OID 25729)
-- Dependencies: 214
-- Data for Name: mm_metadata_logo; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_metadata_logo (mm_metadata_logo_guid, mm_metadata_logo_media_guid, mm_metadata_logo_image_path) FROM stdin;
\.


--
-- TOC entry 2560 (class 0 OID 25587)
-- Dependencies: 199
-- Data for Name: mm_metadata_movie; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_metadata_movie (mm_metadata_guid, mm_metadata_media_id, mm_media_name, mm_metadata_json, mm_metadata_localimage_json, mm_metadata_user_json) FROM stdin;
\.


--
-- TOC entry 2557 (class 0 OID 25548)
-- Dependencies: 196
-- Data for Name: mm_metadata_music; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_metadata_music (mm_metadata_music_guid, mm_metadata_media_music_id, mm_metadata_music_name, mm_metadata_music_json, mm_metadata_music_album_guid) FROM stdin;
\.


--
-- TOC entry 2561 (class 0 OID 25603)
-- Dependencies: 200
-- Data for Name: mm_metadata_music_video; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_metadata_music_video (mm_metadata_music_video_guid, mm_metadata_music_video_media_id, mm_media_music_video_band, mm_media_music_video_song, mm_metadata_music_video_json, mm_metadata_music_video_localimage_json) FROM stdin;
\.


--
-- TOC entry 2555 (class 0 OID 25523)
-- Dependencies: 194
-- Data for Name: mm_metadata_musician; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_metadata_musician (mm_metadata_musician_guid, mm_metadata_musician_name, mm_metadata_musician_id, mm_metadata_musician_json) FROM stdin;
\.


--
-- TOC entry 2582 (class 0 OID 25796)
-- Dependencies: 221
-- Data for Name: mm_metadata_person; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_metadata_person (mmp_id, mmp_person_media_id, mmp_person_meta_json, mmp_person_image, mmp_person_name) FROM stdin;
\.


--
-- TOC entry 2554 (class 0 OID 25505)
-- Dependencies: 193
-- Data for Name: mm_metadata_sports; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_metadata_sports (mm_metadata_sports_guid, mm_metadata_media_sports_id, mm_metadata_sports_name, mm_metadata_sports_json, mm_metadata_sports_image_json) FROM stdin;
\.


--
-- TOC entry 2553 (class 0 OID 25486)
-- Dependencies: 192
-- Data for Name: mm_metadata_tvshow; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_metadata_tvshow (mm_metadata_tvshow_guid, mm_metadata_media_tvshow_id, mm_metadata_tvshow_name, mm_metadata_tvshow_json, mm_metadata_tvshow_localimage_json, mm_metadata_tvshow_user_json) FROM stdin;
\.


--
-- TOC entry 2564 (class 0 OID 25640)
-- Dependencies: 203
-- Data for Name: mm_notification; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_notification (mm_notification_guid, mm_notification_text, mm_notification_time, mm_notification_dismissable) FROM stdin;
\.


--
-- TOC entry 2579 (class 0 OID 25768)
-- Dependencies: 218
-- Data for Name: mm_options_and_status; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_options_and_status (mm_options_and_status_guid, mm_options_json, mm_status_json) FROM stdin;
b99c6443-03bc-4636-b3e5-7c500bc4427e	{"SD": {"User": null, "Password": null}, "API": {"anidb": null, "imvdb": null, "google": null, "isbndb": "25C8IT4I", "tvmaze": null, "thetvdb": "147CB43DCA8B61B7", "thelogodb": null, "themoviedb": "f72118d1e84b8a1438935972a9c37cac", "globalcache": null, "mediabrainz": null, "thesportsdb": "4352761817344", "opensubtitles": null, "rottentomatoes": "f4tnu5dn9r7f28gjth3ftqaj"}, "AWSS3": {"Bucket": "mediakraken", "AccessKey": null, "BackupBucket": "mkbackup", "SecretAccessKey": null}, "Trakt": {"ApiKey": null, "ClientID": null, "SecretKey": null}, "Backup": {"Interval": 0, "BackupType": "local"}, "Docker": {"Nodes": 0, "SwarmID": null, "Instances": 0}, "Dropbox": {"APIKey": null, "APISecret": null}, "Trailer": {"Clip": false, "Behind": false, "Carpool": false, "Trailer": false, "Featurette": false}, "OneDrive": {"ClientID": null, "SecretKey": null}, "GoogleDrive": {"SecretFile": null}, "Maintenance": null, "MediaBrainz": {"Host": null, "Port": 5000, "User": null, "Password": null, "BrainzDBHost": null, "BrainzDBName": null, "BrainzDBPass": null, "BrainzDBPort": 5432, "BrainzDBUser": null}, "MaxResumePct": 5, "Transmission": {"Host": null, "Port": 9091}, "MediaKrakenServer": {"APIPort": 8097, "ListenPort": 8098, "BackupLocal": "/mediakraken/backups/"}}	{"thetvdb_Updated_Epoc": 0}
\.


--
-- TOC entry 2571 (class 0 OID 25699)
-- Dependencies: 210
-- Data for Name: mm_radio; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_radio (mm_radio_guid, mm_radio_name, mm_radio_adress, mm_radio_active) FROM stdin;
\.


--
-- TOC entry 2567 (class 0 OID 25662)
-- Dependencies: 206
-- Data for Name: mm_review; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_review (mm_review_guid, mm_review_metadata_id, mm_review_metadata_guid, mm_review_json) FROM stdin;
\.


--
-- TOC entry 2572 (class 0 OID 25707)
-- Dependencies: 211
-- Data for Name: mm_sync; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_sync (mm_sync_guid, mm_sync_path, mm_sync_path_to, mm_sync_options_json) FROM stdin;
\.


--
-- TOC entry 2569 (class 0 OID 25683)
-- Dependencies: 208
-- Data for Name: mm_task; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_task (mm_task_guid, mm_task_name, mm_task_description, mm_task_enabled, mm_task_schedule, mm_task_last_run, mm_task_file_path, mm_task_json) FROM stdin;
213db8ee-3c62-420c-a673-38c4025a5d93	Anime	Match anime via Scudlee data	f	Days 1	1970-01-01 00:00:01	/mediakraken/subprogram_match_anime_id_scudlee.py	{"task": "anime", "route_key": "Z", "exchange_key": "mkque_metadata_ex"}
00539ccf-1be8-4c68-9ec7-61e807b51e75	Collections	Create and update collection(s)	f	Days 1	1970-01-01 00:00:01	/mediakraken/subprogram_metadata_update_create_collections.py	{"task": "collection", "route_key": "themoviedb", "exchange_key": "mkque_metadata_ex"}
48956440-266b-4d92-aa0d-806f056b483b	Create Chapter Image	Create chapter images for all media	f	Days 1	1970-01-01 00:00:01	/mediakraken/subprogram_create_chapter_images.py	{"task": "chapter", "route_key": "mkque", "exchange_key": "mkque_ex"}
01ec56fc-66eb-4461-830b-d31f2af220ec	Roku Thumb	Generate Roku thumbnail images	f	Days 1	1970-01-01 00:00:01	/mediakraken/subprogram_roku_thumbnail_generate.py	{"task": "rokuthumbnail", "route_key": "mkque", "exchange_key": "mkque_ex"}
8ca8206c-6b3c-431a-a45c-85963de0e49c	Schedules Direct	Fetch TV schedules from Schedules Direct	f	Days 1	1970-01-01 00:00:01	/mediakraken/subprogram_schedules_direct_updates.py	{"task": "update", "route_key": "schedulesdirect", "exchange_key": "mkque_metadata_ex"}
430d8a0a-e818-41f8-9f08-f5332adb0e47	Subtitle	Download missing subtitles for media	f	Days 1	1970-01-01 00:00:01	/mediakraken/subprogram_subtitle_downloader.py	{"task": "subtitle", "route_key": "Z", "exchange_key": "mkque_metadata_ex"}
1c06d239-eded-4cf8-8d56-990b96b75e57	The Movie Database	Grab updated movie metadata	f	Days 1	1970-01-01 00:00:01	/mediakraken/subprogram_metadata_tmdb_updates.py	{"task": "update", "route_key": "themoviedb", "exchange_key": "mkque_metadata_ex"}
e895f13d-1e55-4ffb-8578-d33196655630	TheTVDB Update	Grab updated TheTVDB metadata	f	Days 1	1970-01-01 00:00:01	/mediakraken/subprogram_metadata_thetvdb_updates.py	{"task": "update", "route_key": "thetvdb", "exchange_key": "mkque_metadata_ex"}
078f07f7-1c12-498d-9476-4097be4d76d1	TVmaze Update	Grab updated TVmaze metadata	f	Days 1	1970-01-01 00:00:01	/mediakraken/subprogram_metadata_tvmaze_updates.py	{"task": "update", "route_key": "tvmaze", "exchange_key": "mkque_metadata_ex"}
c5ea29b0-acaa-4067-8fee-c7dd36909956	Trailer	Download new trailers	f	Days 1	1970-01-01 00:00:01	/mediakraken/subprogram_metadata_trailer_download.py	{"task": "trailer", "route_key": "Z", "exchange_key": "mkque_metadata_ex"}
ea82cee1-50c8-4f14-b2fa-26c5dc957842	Backup	Backup Postgresql DB	f	Days 1	1970-01-01 00:00:01	/mediakraken/subprogram_postgresql_backup.py	{"task": "dbbackup", "route_key": "mkque", "exchange_key": "mkque_ex"}
88a70cdb-f798-4406-bf4a-e45b3ff697b2	DB Vacuum	Postgresql Vacuum Analyze all tables	f	Days 1	1970-01-01 00:00:01	/mediakraken/subprogram_postgresql_vacuum.py	{"task": "dbvacuum", "route_key": "mkque", "exchange_key": "mkque_ex"}
5abd84f6-a126-42c1-8cb2-dbd31920451a	iRadio Scan	Scan for iRadio stations	f	Days 1	1970-01-01 00:00:01	/mediakraken/subprogram_iradio_channels.py	{"task": "iradio", "route_key": "mkque", "exchange_key": "mkque_ex"}
a2bedd62-2e86-4c92-9550-43a653ff7f14	Media Scan	Scan for new media	f	Days 1	1970-01-01 00:00:01	/mediakraken/subprogram_file_scan.py	{"task": "scan", "route_key": "mkque", "exchange_key": "mkque_ex"}
4943ce14-42c0-408d-ba14-f5d3f8877d3e	Sync	Sync/Transcode media	f	Days 1	1970-01-01 00:00:01	/mediakraken/subprogram_sync.py	{"task": "sync", "route_key": "mkque", "exchange_key": "mkque_ex"}
\.


--
-- TOC entry 2574 (class 0 OID 25721)
-- Dependencies: 213
-- Data for Name: mm_trigger; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_trigger (mm_trigger_guid, mm_trigger_command, mm_trigger_background) FROM stdin;
\.


--
-- TOC entry 2587 (class 0 OID 25847)
-- Dependencies: 226
-- Data for Name: mm_tv_schedule; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_tv_schedule (mm_tv_schedule_id, mm_tv_schedule_station_id, mm_tv_schedule_date, mm_tv_schedule_json) FROM stdin;
\.


--
-- TOC entry 2588 (class 0 OID 25857)
-- Dependencies: 227
-- Data for Name: mm_tv_schedule_program; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_tv_schedule_program (mm_tv_schedule_program_guid, mm_tv_schedule_program_id, mm_tv_schedule_program_json) FROM stdin;
\.


--
-- TOC entry 2586 (class 0 OID 25837)
-- Dependencies: 225
-- Data for Name: mm_tv_stations; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_tv_stations (mm_tv_stations_id, mm_tv_station_name, mm_tv_station_id, mm_tv_station_channel, mm_tv_station_json, mm_tv_station_image) FROM stdin;
\.


--
-- TOC entry 2566 (class 0 OID 25652)
-- Dependencies: 205
-- Data for Name: mm_user; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_user (id, username, email, password, created_at, active, is_admin, user_json, lang) FROM stdin;
\.


--
-- TOC entry 2563 (class 0 OID 25630)
-- Dependencies: 202
-- Data for Name: mm_user_activity; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_user_activity (mm_activity_guid, mm_activity_name, mm_activity_overview, mm_activity_short_overview, mm_activity_type, mm_activity_itemid, mm_activity_userid, mm_activity_datecreated, mm_activity_log_severity) FROM stdin;
\.


--
-- TOC entry 2577 (class 0 OID 25750)
-- Dependencies: 216
-- Data for Name: mm_user_group; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_user_group (mm_user_group_guid, mm_user_group_name, mm_user_group_description, mm_user_group_rights_json) FROM stdin;
a15b400a-e3fa-4573-83b8-76ad075b21d5	Administrator	Server administrator	{"Admin": true, "PreviewOnly": false}
657e1769-9ad5-4951-ab06-8526efbd9097	User	General user	{"Admin": false, "PreviewOnly": false}
8280f96d-a374-4fc1-a719-603446118212	Guest	Guest (Preview only)	{"Admin": false, "PreviewOnly": true}
\.


--
-- TOC entry 2598 (class 0 OID 0)
-- Dependencies: 204
-- Name: mm_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: metamanpg
--

SELECT pg_catalog.setval('mm_user_id_seq', 1, false);


--
-- TOC entry 2578 (class 0 OID 25759)
-- Dependencies: 217
-- Data for Name: mm_user_profile; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_user_profile (mm_user_profile_guid, mm_user_profile_name, mm_user_profile_json) FROM stdin;
c94f1225-a9d4-4e4d-9196-d5fd96316234	Adult	{"3D": true, "TV": true, "Home": true, "Lang": "en", "Sync": true, "Adult": true, "Books": true, "Games": true, "MaxBR": 100, "Movie": true, "Music": true, "IRadio": true, "Images": true, "LiveTV": true, "Sports": true, "Internet": true, "MaxRating": 5}
8ad29310-cb5d-4b85-b340-7f43f35dea52	Teen	{"3D": true, "TV": true, "Home": true, "Lang": "en", "Sync": false, "Adult": false, "Books": true, "Games": true, "MaxBR": 50, "Movie": true, "Music": true, "IRadio": true, "Images": true, "LiveTV": true, "Sports": true, "Internet": true, "MaxRating": 3}
49197650-cde5-4837-9ef8-d93f996f7f3a	Child	{"3D": false, "TV": true, "Home": true, "Lang": "en", "Sync": false, "Adult": false, "Books": true, "Games": true, "MaxBR": 20, "Movie": true, "Music": true, "IRadio": false, "Images": true, "LiveTV": false, "Sports": true, "Internet": false, "MaxRating": 0}
\.


--
-- TOC entry 2547 (class 0 OID 25434)
-- Dependencies: 186
-- Data for Name: mm_version; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_version (mm_version_no) FROM stdin;
8
\.


--
-- TOC entry 2395 (class 2606 OID 25783)
-- Name: mm_metadata_game_software_info gi_id_mpk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_metadata_game_software_info
    ADD CONSTRAINT gi_id_mpk PRIMARY KEY (gi_id);


--
-- TOC entry 2400 (class 2606 OID 25794)
-- Name: mm_metadata_game_systems_info gs_id_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_metadata_game_systems_info
    ADD CONSTRAINT gs_id_pk PRIMARY KEY (gs_id);


--
-- TOC entry 2408 (class 2606 OID 25814)
-- Name: mm_download_que mdq_id_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_download_que
    ADD CONSTRAINT mdq_id_pk PRIMARY KEY (mdq_id);


--
-- TOC entry 2413 (class 2606 OID 25825)
-- Name: mm_download_image_que mdq_image_id_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_download_image_que
    ADD CONSTRAINT mdq_image_id_pk PRIMARY KEY (mdq_image_id);


--
-- TOC entry 2345 (class 2606 OID 25637)
-- Name: mm_user_activity mm_activity_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_user_activity
    ADD CONSTRAINT mm_activity_pk PRIMARY KEY (mm_activity_guid);


--
-- TOC entry 2381 (class 2606 OID 25745)
-- Name: mm_channel mm_channel_guid_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_channel
    ADD CONSTRAINT mm_channel_guid_pk PRIMARY KEY (mm_channel_guid);


--
-- TOC entry 2367 (class 2606 OID 25698)
-- Name: mm_cron mm_cron_guid_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_cron
    ADD CONSTRAINT mm_cron_guid_pk PRIMARY KEY (mm_cron_guid);


--
-- TOC entry 2416 (class 2606 OID 25834)
-- Name: mm_device mm_device_id_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_device
    ADD CONSTRAINT mm_device_id_pk PRIMARY KEY (mm_device_id);


--
-- TOC entry 2257 (class 2606 OID 25483)
-- Name: mm_link mm_link_guid_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_link
    ADD CONSTRAINT mm_link_guid_pk PRIMARY KEY (mm_link_guid);


--
-- TOC entry 2374 (class 2606 OID 25720)
-- Name: mm_loan mm_loan_guid_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_loan
    ADD CONSTRAINT mm_loan_guid_pk PRIMARY KEY (mm_loan_guid);


--
-- TOC entry 2307 (class 2606 OID 25568)
-- Name: mm_media_class mm_media_class_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_media_class
    ADD CONSTRAINT mm_media_class_pk PRIMARY KEY (mm_media_class_guid);


--
-- TOC entry 2245 (class 2606 OID 25452)
-- Name: mm_media_dir mm_media_dir_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_media_dir
    ADD CONSTRAINT mm_media_dir_pk PRIMARY KEY (mm_media_dir_guid);


--
-- TOC entry 2250 (class 2606 OID 25461)
-- Name: mm_media mm_media_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_media
    ADD CONSTRAINT mm_media_pk PRIMARY KEY (mm_media_guid);


--
-- TOC entry 2242 (class 2606 OID 25444)
-- Name: mm_media_share mm_media_share_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_media_share
    ADD CONSTRAINT mm_media_share_pk PRIMARY KEY (mm_media_share_guid);


--
-- TOC entry 2297 (class 2606 OID 25542)
-- Name: mm_metadata_album mm_metadata_album_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_metadata_album
    ADD CONSTRAINT mm_metadata_album_pk PRIMARY KEY (mm_metadata_album_guid);


--
-- TOC entry 2318 (class 2606 OID 25577)
-- Name: mm_metadata_anime mm_metadata_anime_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_metadata_anime
    ADD CONSTRAINT mm_metadata_anime_pk PRIMARY KEY (mm_metadata_anime_guid);


--
-- TOC entry 2339 (class 2606 OID 25625)
-- Name: mm_metadata_book mm_metadata_book_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_metadata_book
    ADD CONSTRAINT mm_metadata_book_pk PRIMARY KEY (mm_metadata_book_guid);


--
-- TOC entry 2360 (class 2606 OID 25679)
-- Name: mm_metadata_collection mm_metadata_collection_guid_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_metadata_collection
    ADD CONSTRAINT mm_metadata_collection_guid_pk PRIMARY KEY (mm_metadata_collection_guid);


--
-- TOC entry 2378 (class 2606 OID 25736)
-- Name: mm_metadata_logo mm_metadata_logo_guid_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_metadata_logo
    ADD CONSTRAINT mm_metadata_logo_guid_pk PRIMARY KEY (mm_metadata_logo_guid);


--
-- TOC entry 2304 (class 2606 OID 25555)
-- Name: mm_metadata_music mm_metadata_music_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_metadata_music
    ADD CONSTRAINT mm_metadata_music_pk PRIMARY KEY (mm_metadata_music_guid);


--
-- TOC entry 2337 (class 2606 OID 25610)
-- Name: mm_metadata_music_video mm_metadata_music_video_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_metadata_music_video
    ADD CONSTRAINT mm_metadata_music_video_pk PRIMARY KEY (mm_metadata_music_video_guid);


--
-- TOC entry 2290 (class 2606 OID 25530)
-- Name: mm_metadata_musician mm_metadata_musician_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_metadata_musician
    ADD CONSTRAINT mm_metadata_musician_pk PRIMARY KEY (mm_metadata_musician_guid);


--
-- TOC entry 2328 (class 2606 OID 25594)
-- Name: mm_metadata_movie mm_metadata_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_metadata_movie
    ADD CONSTRAINT mm_metadata_pk PRIMARY KEY (mm_metadata_guid);


--
-- TOC entry 2284 (class 2606 OID 25512)
-- Name: mm_metadata_sports mm_metadata_sports_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_metadata_sports
    ADD CONSTRAINT mm_metadata_sports_pk PRIMARY KEY (mm_metadata_sports_guid);


--
-- TOC entry 2272 (class 2606 OID 25493)
-- Name: mm_metadata_tvshow mm_metadata_tvshow_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_metadata_tvshow
    ADD CONSTRAINT mm_metadata_tvshow_pk PRIMARY KEY (mm_metadata_tvshow_guid);


--
-- TOC entry 2351 (class 2606 OID 25647)
-- Name: mm_notification mm_notification_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_notification
    ADD CONSTRAINT mm_notification_pk PRIMARY KEY (mm_notification_guid);


--
-- TOC entry 2393 (class 2606 OID 25775)
-- Name: mm_options_and_status mm_options_and_status_guid_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_options_and_status
    ADD CONSTRAINT mm_options_and_status_guid_pk PRIMARY KEY (mm_options_and_status_guid);


--
-- TOC entry 2369 (class 2606 OID 25706)
-- Name: mm_radio mm_radio_guid_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_radio
    ADD CONSTRAINT mm_radio_guid_pk PRIMARY KEY (mm_radio_guid);


--
-- TOC entry 2358 (class 2606 OID 25669)
-- Name: mm_review mm_review_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_review
    ADD CONSTRAINT mm_review_pk PRIMARY KEY (mm_review_guid);


--
-- TOC entry 2371 (class 2606 OID 25714)
-- Name: mm_sync mm_sync_guid_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_sync
    ADD CONSTRAINT mm_sync_guid_pk PRIMARY KEY (mm_sync_guid);


--
-- TOC entry 2365 (class 2606 OID 25690)
-- Name: mm_task mm_task_guid_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_task
    ADD CONSTRAINT mm_task_guid_pk PRIMARY KEY (mm_task_guid);


--
-- TOC entry 2376 (class 2606 OID 25728)
-- Name: mm_trigger mm_trigger_guid_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_trigger
    ADD CONSTRAINT mm_trigger_guid_pk PRIMARY KEY (mm_trigger_guid);


--
-- TOC entry 2424 (class 2606 OID 25854)
-- Name: mm_tv_schedule mm_tv_schedule_id_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_tv_schedule
    ADD CONSTRAINT mm_tv_schedule_id_pk PRIMARY KEY (mm_tv_schedule_id);


--
-- TOC entry 2429 (class 2606 OID 25864)
-- Name: mm_tv_schedule_program mm_tv_schedule_program_guid_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_tv_schedule_program
    ADD CONSTRAINT mm_tv_schedule_program_guid_pk PRIMARY KEY (mm_tv_schedule_program_guid);


--
-- TOC entry 2420 (class 2606 OID 25844)
-- Name: mm_tv_stations mm_tv_stations_id_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_tv_stations
    ADD CONSTRAINT mm_tv_stations_id_pk PRIMARY KEY (mm_tv_stations_id);


--
-- TOC entry 2387 (class 2606 OID 25757)
-- Name: mm_user_group mm_user_group_guid_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_user_group
    ADD CONSTRAINT mm_user_group_guid_pk PRIMARY KEY (mm_user_group_guid);


--
-- TOC entry 2354 (class 2606 OID 25660)
-- Name: mm_user mm_user_pkey; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_user
    ADD CONSTRAINT mm_user_pkey PRIMARY KEY (id);


--
-- TOC entry 2390 (class 2606 OID 25766)
-- Name: mm_user_profile mm_user_profile_guid_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_user_profile
    ADD CONSTRAINT mm_user_profile_guid_pk PRIMARY KEY (mm_user_profile_guid);


--
-- TOC entry 2406 (class 2606 OID 25803)
-- Name: mm_metadata_person mmp_id_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_metadata_person
    ADD CONSTRAINT mmp_id_pk PRIMARY KEY (mmp_id);


--
-- TOC entry 2255 (class 2606 OID 25472)
-- Name: mm_media_remote mmr_media_remote_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_media_remote
    ADD CONSTRAINT mmr_media_remote_pk PRIMARY KEY (mmr_media_guid);


--
-- TOC entry 2396 (class 1259 OID 25784)
-- Name: gi_system_id_ndx; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX gi_system_id_ndx ON mm_metadata_game_software_info USING btree (gi_system_id);


--
-- TOC entry 2409 (class 1259 OID 25817)
-- Name: mdq_que_type_idx_name; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mdq_que_type_idx_name ON mm_download_que USING btree (mdq_que_type);


--
-- TOC entry 2382 (class 1259 OID 25748)
-- Name: mm_channel_idx_country; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_channel_idx_country ON mm_channel USING btree (mm_channel_country_guid);


--
-- TOC entry 2383 (class 1259 OID 25749)
-- Name: mm_channel_idx_logo; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_channel_idx_logo ON mm_channel USING btree (mm_channel_logo_guid);


--
-- TOC entry 2384 (class 1259 OID 25746)
-- Name: mm_channel_idx_name; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_channel_idx_name ON mm_channel USING btree (mm_channel_name);


--
-- TOC entry 2385 (class 1259 OID 25747)
-- Name: mm_channel_idxgin_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_channel_idxgin_json ON mm_channel USING gin (mm_channel_media_id);


--
-- TOC entry 2417 (class 1259 OID 25835)
-- Name: mm_device_idx_type; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_device_idx_type ON mm_device USING btree (mm_device_type);


--
-- TOC entry 2418 (class 1259 OID 25836)
-- Name: mm_device_idxgin_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_device_idxgin_json ON mm_device USING gin (mm_device_json);


--
-- TOC entry 2410 (class 1259 OID 25815)
-- Name: mm_download_idx_provider; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_download_idx_provider ON mm_download_que USING btree (mdq_provider);


--
-- TOC entry 2411 (class 1259 OID 25816)
-- Name: mm_download_que_idxgin_meta_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_download_que_idxgin_meta_json ON mm_download_que USING gin (mdq_download_json);


--
-- TOC entry 2397 (class 1259 OID 25785)
-- Name: mm_game_info_idxgin_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_game_info_idxgin_json ON mm_metadata_game_software_info USING gin (gi_game_info_json);


--
-- TOC entry 2398 (class 1259 OID 25786)
-- Name: mm_game_info_idxgin_name; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_game_info_idxgin_name ON mm_metadata_game_software_info USING gin (((gi_game_info_json -> '@name'::text)));


--
-- TOC entry 2401 (class 1259 OID 25795)
-- Name: mm_game_systems_idxgin_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_game_systems_idxgin_json ON mm_metadata_game_systems_info USING gin (gs_game_system_json);


--
-- TOC entry 2414 (class 1259 OID 25826)
-- Name: mm_image_download_idx_provider; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_image_download_idx_provider ON mm_download_image_que USING btree (mdq_image_provider);


--
-- TOC entry 2258 (class 1259 OID 25485)
-- Name: mm_link_idx_name; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_link_idx_name ON mm_link USING btree (mm_link_name);


--
-- TOC entry 2259 (class 1259 OID 25484)
-- Name: mm_link_json_idxgin; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_link_json_idxgin ON mm_link USING gin (mm_link_json);


--
-- TOC entry 2305 (class 1259 OID 25569)
-- Name: mm_media_class_idx_type; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_media_class_idx_type ON mm_media_class USING btree (mm_media_class_type);


--
-- TOC entry 2243 (class 1259 OID 25453)
-- Name: mm_media_dir_idx_share; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_media_dir_idx_share ON mm_media_dir USING btree (mm_media_dir_share_guid);


--
-- TOC entry 2246 (class 1259 OID 25463)
-- Name: mm_media_idx_metadata_uuid; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_media_idx_metadata_uuid ON mm_media USING btree (mm_media_metadata_guid);


--
-- TOC entry 2247 (class 1259 OID 25464)
-- Name: mm_media_idx_path; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_media_idx_path ON mm_media USING btree (mm_media_path);


--
-- TOC entry 2248 (class 1259 OID 25462)
-- Name: mm_media_idxgin_ffprobe; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_media_idxgin_ffprobe ON mm_media USING gin (mm_media_ffprobe_json);


--
-- TOC entry 2291 (class 1259 OID 25547)
-- Name: mm_metadata_album_idx_musician; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_album_idx_musician ON mm_metadata_album USING btree (mm_metadata_album_musician_guid);


--
-- TOC entry 2292 (class 1259 OID 25543)
-- Name: mm_metadata_album_idx_name; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_album_idx_name ON mm_metadata_album USING btree (mm_metadata_album_name);


--
-- TOC entry 2293 (class 1259 OID 25544)
-- Name: mm_metadata_album_idx_name_lower; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_album_idx_name_lower ON mm_metadata_album USING btree (lower(mm_metadata_album_name));


--
-- TOC entry 2294 (class 1259 OID 25545)
-- Name: mm_metadata_album_idxgin_id_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_album_idxgin_id_json ON mm_metadata_album USING gin (mm_metadata_album_id);


--
-- TOC entry 2295 (class 1259 OID 25546)
-- Name: mm_metadata_album_idxgin_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_album_idxgin_json ON mm_metadata_album USING gin (mm_metadata_album_json);


--
-- TOC entry 2308 (class 1259 OID 25581)
-- Name: mm_metadata_aniem_idxgin_media_id; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_aniem_idxgin_media_id ON mm_metadata_anime USING gin (mm_metadata_anime_media_id);


--
-- TOC entry 2309 (class 1259 OID 25578)
-- Name: mm_metadata_anime_idx_name; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_anime_idx_name ON mm_metadata_anime USING btree (mm_media_anime_name);


--
-- TOC entry 2310 (class 1259 OID 25579)
-- Name: mm_metadata_anime_idx_name_lower; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_anime_idx_name_lower ON mm_metadata_anime USING btree (lower(mm_media_anime_name));


--
-- TOC entry 2311 (class 1259 OID 25580)
-- Name: mm_metadata_anime_idxgin_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_anime_idxgin_json ON mm_metadata_anime USING gin (mm_metadata_anime_json);


--
-- TOC entry 2312 (class 1259 OID 25582)
-- Name: mm_metadata_anime_idxgin_media_id_anidb; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_anime_idxgin_media_id_anidb ON mm_metadata_anime USING gin (((mm_metadata_anime_media_id -> 'anidb'::text)));


--
-- TOC entry 2313 (class 1259 OID 25585)
-- Name: mm_metadata_anime_idxgin_media_id_imdb; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_anime_idxgin_media_id_imdb ON mm_metadata_anime USING gin (((mm_metadata_anime_media_id -> 'imdb'::text)));


--
-- TOC entry 2314 (class 1259 OID 25583)
-- Name: mm_metadata_anime_idxgin_media_id_thetvdb; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_anime_idxgin_media_id_thetvdb ON mm_metadata_anime USING gin (((mm_metadata_anime_media_id -> 'thetvdb'::text)));


--
-- TOC entry 2315 (class 1259 OID 25584)
-- Name: mm_metadata_anime_idxgin_media_id_tmdb; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_anime_idxgin_media_id_tmdb ON mm_metadata_anime USING gin (((mm_metadata_anime_media_id -> 'tmdb'::text)));


--
-- TOC entry 2316 (class 1259 OID 25586)
-- Name: mm_metadata_anime_idxgin_user_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_anime_idxgin_user_json ON mm_metadata_anime USING gin (mm_metadata_anime_user_json);


--
-- TOC entry 2361 (class 1259 OID 25680)
-- Name: mm_metadata_collection_idxgin_media_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_collection_idxgin_media_json ON mm_metadata_collection USING gin (mm_metadata_collection_media_ids);


--
-- TOC entry 2362 (class 1259 OID 25682)
-- Name: mm_metadata_collection_idxgin_meta_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_collection_idxgin_meta_json ON mm_metadata_collection USING gin (mm_metadata_collection_json);


--
-- TOC entry 2363 (class 1259 OID 25681)
-- Name: mm_metadata_collection_idxgin_name_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_collection_idxgin_name_json ON mm_metadata_collection USING gin (mm_metadata_collection_name);


--
-- TOC entry 2329 (class 1259 OID 25611)
-- Name: mm_metadata_idx_band_name; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_idx_band_name ON mm_metadata_music_video USING btree (mm_media_music_video_band);


--
-- TOC entry 2330 (class 1259 OID 25612)
-- Name: mm_metadata_idx_band_name_lower; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_idx_band_name_lower ON mm_metadata_music_video USING btree (lower(mm_media_music_video_band));


--
-- TOC entry 2340 (class 1259 OID 25626)
-- Name: mm_metadata_idx_book_name; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_idx_book_name ON mm_metadata_book USING btree (mm_metadata_book_name);


--
-- TOC entry 2341 (class 1259 OID 25627)
-- Name: mm_metadata_idx_book_name_lower; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_idx_book_name_lower ON mm_metadata_book USING btree (lower(mm_metadata_book_name));


--
-- TOC entry 2319 (class 1259 OID 25595)
-- Name: mm_metadata_idx_name; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_idx_name ON mm_metadata_movie USING btree (mm_media_name);


--
-- TOC entry 2320 (class 1259 OID 25596)
-- Name: mm_metadata_idx_name_lower; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_idx_name_lower ON mm_metadata_movie USING btree (lower(mm_media_name));


--
-- TOC entry 2331 (class 1259 OID 25613)
-- Name: mm_metadata_idx_song_name; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_idx_song_name ON mm_metadata_music_video USING btree (mm_media_music_video_song);


--
-- TOC entry 2332 (class 1259 OID 25614)
-- Name: mm_metadata_idx_song_name_lower; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_idx_song_name_lower ON mm_metadata_music_video USING btree (lower(mm_media_music_video_song));


--
-- TOC entry 2342 (class 1259 OID 25628)
-- Name: mm_metadata_idxgin_isbn; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_idxgin_isbn ON mm_metadata_book USING btree (mm_metadata_book_isbn);


--
-- TOC entry 2343 (class 1259 OID 25629)
-- Name: mm_metadata_idxgin_isbn13; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_idxgin_isbn13 ON mm_metadata_book USING btree (mm_metadata_book_isbn13);


--
-- TOC entry 2321 (class 1259 OID 25597)
-- Name: mm_metadata_idxgin_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_idxgin_json ON mm_metadata_movie USING gin (mm_metadata_json);


--
-- TOC entry 2322 (class 1259 OID 25598)
-- Name: mm_metadata_idxgin_media_id; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_idxgin_media_id ON mm_metadata_movie USING gin (mm_metadata_media_id);


--
-- TOC entry 2323 (class 1259 OID 25601)
-- Name: mm_metadata_idxgin_media_id_imdb; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_idxgin_media_id_imdb ON mm_metadata_movie USING gin (((mm_metadata_media_id -> 'imdb'::text)));


--
-- TOC entry 2324 (class 1259 OID 25599)
-- Name: mm_metadata_idxgin_media_id_thetvdb; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_idxgin_media_id_thetvdb ON mm_metadata_movie USING gin (((mm_metadata_media_id -> 'thetvdb'::text)));


--
-- TOC entry 2325 (class 1259 OID 25600)
-- Name: mm_metadata_idxgin_media_id_tmdb; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_idxgin_media_id_tmdb ON mm_metadata_movie USING gin (((mm_metadata_media_id -> 'tmdb'::text)));


--
-- TOC entry 2333 (class 1259 OID 25615)
-- Name: mm_metadata_idxgin_music_video_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_idxgin_music_video_json ON mm_metadata_music_video USING gin (mm_metadata_music_video_json);


--
-- TOC entry 2334 (class 1259 OID 25616)
-- Name: mm_metadata_idxgin_music_video_media_id; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_idxgin_music_video_media_id ON mm_metadata_music_video USING gin (mm_metadata_music_video_media_id);


--
-- TOC entry 2335 (class 1259 OID 25617)
-- Name: mm_metadata_idxgin_music_video_media_id_imvdb; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_idxgin_music_video_media_id_imvdb ON mm_metadata_music_video USING gin (((mm_metadata_music_video_media_id -> 'imvdb'::text)));


--
-- TOC entry 2326 (class 1259 OID 25602)
-- Name: mm_metadata_idxgin_user_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_idxgin_user_json ON mm_metadata_movie USING gin (mm_metadata_user_json);


--
-- TOC entry 2379 (class 1259 OID 25737)
-- Name: mm_metadata_logo_idxgin_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_logo_idxgin_json ON mm_metadata_logo USING gin (mm_metadata_logo_media_guid);


--
-- TOC entry 2298 (class 1259 OID 25560)
-- Name: mm_metadata_music_idx_album; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_music_idx_album ON mm_metadata_music USING btree (mm_metadata_music_album_guid);


--
-- TOC entry 2299 (class 1259 OID 25556)
-- Name: mm_metadata_music_idx_name; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_music_idx_name ON mm_metadata_music USING btree (mm_metadata_music_name);


--
-- TOC entry 2300 (class 1259 OID 25557)
-- Name: mm_metadata_music_idx_name_lower; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_music_idx_name_lower ON mm_metadata_music USING btree (lower(mm_metadata_music_name));


--
-- TOC entry 2301 (class 1259 OID 25558)
-- Name: mm_metadata_music_idxgin_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_music_idxgin_json ON mm_metadata_music USING gin (mm_metadata_music_json);


--
-- TOC entry 2302 (class 1259 OID 25559)
-- Name: mm_metadata_music_idxgin_media_id; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_music_idxgin_media_id ON mm_metadata_music USING gin (mm_metadata_media_music_id);


--
-- TOC entry 2285 (class 1259 OID 25531)
-- Name: mm_metadata_musician_idx_name; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_musician_idx_name ON mm_metadata_musician USING btree (mm_metadata_musician_name);


--
-- TOC entry 2286 (class 1259 OID 25532)
-- Name: mm_metadata_musician_idx_name_lower; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_musician_idx_name_lower ON mm_metadata_musician USING btree (lower(mm_metadata_musician_name));


--
-- TOC entry 2287 (class 1259 OID 25533)
-- Name: mm_metadata_musician_idxgin_id_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_musician_idxgin_id_json ON mm_metadata_musician USING gin (mm_metadata_musician_id);


--
-- TOC entry 2288 (class 1259 OID 25534)
-- Name: mm_metadata_musician_idxgin_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_musician_idxgin_json ON mm_metadata_musician USING gin (mm_metadata_musician_json);


--
-- TOC entry 2402 (class 1259 OID 25804)
-- Name: mm_metadata_person_idx_name; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_person_idx_name ON mm_metadata_person USING btree (mmp_person_name);


--
-- TOC entry 2403 (class 1259 OID 25805)
-- Name: mm_metadata_person_idxgin_id_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_person_idxgin_id_json ON mm_metadata_person USING gin (mmp_person_media_id);


--
-- TOC entry 2404 (class 1259 OID 25806)
-- Name: mm_metadata_person_idxgin_meta_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_person_idxgin_meta_json ON mm_metadata_person USING gin (mmp_person_meta_json);


--
-- TOC entry 2355 (class 1259 OID 25671)
-- Name: mm_metadata_review_idx_metadata_uuid; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_review_idx_metadata_uuid ON mm_review USING btree (mm_review_metadata_guid);


--
-- TOC entry 2356 (class 1259 OID 25670)
-- Name: mm_metadata_review_idxgin_media_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_review_idxgin_media_json ON mm_review USING gin (mm_review_metadata_id);


--
-- TOC entry 2273 (class 1259 OID 25513)
-- Name: mm_metadata_sports_idx_name; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_sports_idx_name ON mm_metadata_sports USING btree (mm_metadata_sports_name);


--
-- TOC entry 2274 (class 1259 OID 25514)
-- Name: mm_metadata_sports_idx_name_lower; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_sports_idx_name_lower ON mm_metadata_sports USING btree (lower(mm_metadata_sports_name));


--
-- TOC entry 2275 (class 1259 OID 25515)
-- Name: mm_metadata_sports_idxgin_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_sports_idxgin_json ON mm_metadata_sports USING gin (mm_metadata_sports_json);


--
-- TOC entry 2276 (class 1259 OID 25516)
-- Name: mm_metadata_sports_idxgin_media_id; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_sports_idxgin_media_id ON mm_metadata_sports USING gin (mm_metadata_media_sports_id);


--
-- TOC entry 2277 (class 1259 OID 25517)
-- Name: mm_metadata_sports_idxgin_media_id_imdb; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_sports_idxgin_media_id_imdb ON mm_metadata_sports USING gin (((mm_metadata_media_sports_id -> 'imdb'::text)));


--
-- TOC entry 2278 (class 1259 OID 25522)
-- Name: mm_metadata_sports_idxgin_media_id_thesportsdb; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_sports_idxgin_media_id_thesportsdb ON mm_metadata_sports USING gin (((mm_metadata_media_sports_id -> 'thesportsdb'::text)));


--
-- TOC entry 2279 (class 1259 OID 25518)
-- Name: mm_metadata_sports_idxgin_media_id_thetvdb; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_sports_idxgin_media_id_thetvdb ON mm_metadata_sports USING gin (((mm_metadata_media_sports_id -> 'thetvdb'::text)));


--
-- TOC entry 2280 (class 1259 OID 25520)
-- Name: mm_metadata_sports_idxgin_media_id_thetvdbseries; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_sports_idxgin_media_id_thetvdbseries ON mm_metadata_sports USING gin (((mm_metadata_media_sports_id -> 'thetvdbSeries'::text)));


--
-- TOC entry 2281 (class 1259 OID 25519)
-- Name: mm_metadata_sports_idxgin_media_id_tmdb; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_sports_idxgin_media_id_tmdb ON mm_metadata_sports USING gin (((mm_metadata_media_sports_id -> 'tmdb'::text)));


--
-- TOC entry 2282 (class 1259 OID 25521)
-- Name: mm_metadata_sports_idxgin_media_id_tvmaze; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_sports_idxgin_media_id_tvmaze ON mm_metadata_sports USING gin (((mm_metadata_media_sports_id -> 'tvmaze'::text)));


--
-- TOC entry 2260 (class 1259 OID 25494)
-- Name: mm_metadata_tvshow_idx_name; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_tvshow_idx_name ON mm_metadata_tvshow USING btree (mm_metadata_tvshow_name);


--
-- TOC entry 2261 (class 1259 OID 25495)
-- Name: mm_metadata_tvshow_idx_name_lower; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_tvshow_idx_name_lower ON mm_metadata_tvshow USING btree (lower(mm_metadata_tvshow_name));


--
-- TOC entry 2262 (class 1259 OID 25497)
-- Name: mm_metadata_tvshow_idxgin_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_tvshow_idxgin_json ON mm_metadata_tvshow USING gin (mm_metadata_tvshow_json);


--
-- TOC entry 2263 (class 1259 OID 25498)
-- Name: mm_metadata_tvshow_idxgin_localimage_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_tvshow_idxgin_localimage_json ON mm_metadata_tvshow USING gin (mm_metadata_tvshow_json);


--
-- TOC entry 2264 (class 1259 OID 25496)
-- Name: mm_metadata_tvshow_idxgin_media_id; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_tvshow_idxgin_media_id ON mm_metadata_tvshow USING gin (mm_metadata_media_tvshow_id);


--
-- TOC entry 2265 (class 1259 OID 25499)
-- Name: mm_metadata_tvshow_idxgin_media_id_imdb; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_tvshow_idxgin_media_id_imdb ON mm_metadata_tvshow USING gin (((mm_metadata_media_tvshow_id -> 'imdb'::text)));


--
-- TOC entry 2266 (class 1259 OID 25500)
-- Name: mm_metadata_tvshow_idxgin_media_id_thetvdb; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_tvshow_idxgin_media_id_thetvdb ON mm_metadata_tvshow USING gin (((mm_metadata_media_tvshow_id -> 'thetvdb'::text)));


--
-- TOC entry 2267 (class 1259 OID 25502)
-- Name: mm_metadata_tvshow_idxgin_media_id_thetvdbseries; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_tvshow_idxgin_media_id_thetvdbseries ON mm_metadata_tvshow USING gin (((mm_metadata_media_tvshow_id -> 'thetvdbSeries'::text)));


--
-- TOC entry 2268 (class 1259 OID 25501)
-- Name: mm_metadata_tvshow_idxgin_media_id_tmdb; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_tvshow_idxgin_media_id_tmdb ON mm_metadata_tvshow USING gin (((mm_metadata_media_tvshow_id -> 'tmdb'::text)));


--
-- TOC entry 2269 (class 1259 OID 25503)
-- Name: mm_metadata_tvshow_idxgin_media_id_tvmaze; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_tvshow_idxgin_media_id_tvmaze ON mm_metadata_tvshow USING gin (((mm_metadata_media_tvshow_id -> 'tvmaze'::text)));


--
-- TOC entry 2270 (class 1259 OID 25504)
-- Name: mm_metadata_tvshow_idxgin_user_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_tvshow_idxgin_user_json ON mm_metadata_tvshow USING gin (mm_metadata_tvshow_user_json);


--
-- TOC entry 2348 (class 1259 OID 25649)
-- Name: mm_notification_idx_dismissable; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_notification_idx_dismissable ON mm_notification USING btree (mm_notification_dismissable);


--
-- TOC entry 2349 (class 1259 OID 25648)
-- Name: mm_notification_idx_time; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_notification_idx_time ON mm_notification USING btree (mm_notification_time);


--
-- TOC entry 2372 (class 1259 OID 25715)
-- Name: mm_sync_idxgin_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_sync_idxgin_json ON mm_sync USING gin (mm_sync_options_json);


--
-- TOC entry 2425 (class 1259 OID 25855)
-- Name: mm_tv_schedule_idx_date; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_tv_schedule_idx_date ON mm_tv_schedule USING btree (mm_tv_schedule_date);


--
-- TOC entry 2427 (class 1259 OID 25865)
-- Name: mm_tv_schedule_idx_program; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_tv_schedule_idx_program ON mm_tv_schedule_program USING btree (mm_tv_schedule_program_id);


--
-- TOC entry 2426 (class 1259 OID 25856)
-- Name: mm_tv_schedule_idx_station; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_tv_schedule_idx_station ON mm_tv_schedule USING btree (mm_tv_schedule_station_id);


--
-- TOC entry 2421 (class 1259 OID 25846)
-- Name: mm_tv_stations_idx_name; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_tv_stations_idx_name ON mm_tv_stations USING btree (mm_tv_station_name);


--
-- TOC entry 2422 (class 1259 OID 25845)
-- Name: mm_tv_stations_idx_station; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_tv_stations_idx_station ON mm_tv_stations USING btree (mm_tv_station_id);


--
-- TOC entry 2346 (class 1259 OID 25639)
-- Name: mm_user_activity_idx_date; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_user_activity_idx_date ON mm_user_activity USING btree (mm_activity_datecreated);


--
-- TOC entry 2347 (class 1259 OID 25638)
-- Name: mm_user_activity_idx_user_guid; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_user_activity_idx_user_guid ON mm_user_activity USING btree (mm_activity_userid);


--
-- TOC entry 2388 (class 1259 OID 25758)
-- Name: mm_user_group_idx_name; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_user_group_idx_name ON mm_user_group USING btree (mm_user_group_name);


--
-- TOC entry 2352 (class 1259 OID 25661)
-- Name: mm_user_idx_username; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_user_idx_username ON mm_user USING btree (username);


--
-- TOC entry 2391 (class 1259 OID 25767)
-- Name: mm_user_profile_idx_name; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_user_profile_idx_name ON mm_user_profile USING btree (mm_user_profile_name);


--
-- TOC entry 2251 (class 1259 OID 25475)
-- Name: mmr_media_idx_link_uuid; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mmr_media_idx_link_uuid ON mm_media_remote USING btree (mmr_media_link_id);


--
-- TOC entry 2252 (class 1259 OID 25474)
-- Name: mmr_media_idx_metadata_uuid; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mmr_media_idx_metadata_uuid ON mm_media_remote USING btree (mmr_media_metadata_guid);


--
-- TOC entry 2253 (class 1259 OID 25473)
-- Name: mmr_media_idxgin_ffprobe; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mmr_media_idxgin_ffprobe ON mm_media_remote USING gin (mmr_media_ffprobe_json);


-- Completed on 2017-08-16 13:43:05 CDT

--
-- PostgreSQL database dump complete
--

