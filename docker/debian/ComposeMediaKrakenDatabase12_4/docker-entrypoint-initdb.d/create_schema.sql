--
-- PostgreSQL database dump
--

-- Dumped from database version 12.4
-- Dumped by pg_dump version 12.3

-- Started on 2020-08-18 19:58:05

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

--
-- TOC entry 1 (class 3079 OID 16384)
-- Name: adminpack; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS adminpack WITH SCHEMA pg_catalog;


--
-- TOC entry 3352 (class 0 OID 0)
-- Dependencies: 1
-- Name: EXTENSION adminpack; Type: COMMENT; Schema: -; Owner:
--

COMMENT ON EXTENSION adminpack IS 'administrative functions for PostgreSQL';


--
-- TOC entry 4 (class 3079 OID 16393)
-- Name: pg_trgm; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS pg_trgm WITH SCHEMA public;


--
-- TOC entry 3353 (class 0 OID 0)
-- Dependencies: 4
-- Name: EXTENSION pg_trgm; Type: COMMENT; Schema: -; Owner:
--

COMMENT ON EXTENSION pg_trgm IS 'text similarity measurement and index searching based on trigrams';


--
-- TOC entry 3 (class 3079 OID 16470)
-- Name: pgcrypto; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS pgcrypto WITH SCHEMA public;


--
-- TOC entry 3354 (class 0 OID 0)
-- Dependencies: 3
-- Name: EXTENSION pgcrypto; Type: COMMENT; Schema: -; Owner:
--

COMMENT ON EXTENSION pgcrypto IS 'cryptographic functions';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 205 (class 1259 OID 16967)
-- Name: mm_channel; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mm_channel (
    mm_channel_guid uuid NOT NULL,
    mm_channel_name text,
    mm_channel_media_id jsonb,
    mm_channel_country_guid uuid,
    mm_channel_logo_guid uuid
);


ALTER TABLE public.mm_channel OWNER TO postgres;

--
-- TOC entry 206 (class 1259 OID 16973)
-- Name: mm_cron; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mm_cron (
    mm_cron_guid uuid NOT NULL,
    mm_cron_name text,
    mm_cron_description text,
    mm_cron_enabled boolean,
    mm_cron_schedule text,
    mm_cron_last_run timestamp without time zone,
    mm_cron_json jsonb
);


ALTER TABLE public.mm_cron OWNER TO postgres;

--
-- TOC entry 207 (class 1259 OID 16979)
-- Name: mm_device; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mm_device (
    mm_device_id uuid NOT NULL,
    mm_device_type text,
    mm_device_json jsonb
);


ALTER TABLE public.mm_device OWNER TO postgres;

--
-- TOC entry 208 (class 1259 OID 16985)
-- Name: mm_download_que; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mm_download_que (
    mdq_id uuid NOT NULL,
    mdq_provider text,
    mdq_que_type smallint,
    mdq_download_json jsonb,
    mdq_new_uuid uuid,
    mdq_class_uuid uuid
);


ALTER TABLE public.mm_download_que OWNER TO postgres;

--
-- TOC entry 209 (class 1259 OID 16991)
-- Name: mm_game_category; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mm_game_category (
    gc_id uuid NOT NULL,
    gc_category text
);


ALTER TABLE public.mm_game_category OWNER TO postgres;

--
-- TOC entry 245 (class 1259 OID 17406)
-- Name: mm_game_dedicated_servers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mm_game_dedicated_servers (
    mm_game_server_id uuid NOT NULL,
    mm_game_server_name text,
    mm_game_server_json jsonb
);


ALTER TABLE public.mm_game_dedicated_servers OWNER TO postgres;

--
-- TOC entry 210 (class 1259 OID 16997)
-- Name: mm_hardware; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mm_hardware (
    mm_hardware_id uuid NOT NULL,
    mm_hardware_manufacturer text,
    mm_hardware_model text,
    mm_hardware_json jsonb
);


ALTER TABLE public.mm_hardware OWNER TO postgres;

--
-- TOC entry 211 (class 1259 OID 17003)
-- Name: mm_link; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mm_link (
    mm_link_guid uuid NOT NULL,
    mm_link_name text,
    mm_link_json jsonb
);


ALTER TABLE public.mm_link OWNER TO postgres;

--
-- TOC entry 212 (class 1259 OID 17009)
-- Name: mm_loan; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mm_loan (
    mm_loan_guid uuid NOT NULL,
    mm_loan_media_id uuid,
    mm_loan_user_id uuid,
    mm_load_user_loan_id uuid,
    mm_loan_time timestamp without time zone,
    mm_loan_return_time timestamp without time zone
);


ALTER TABLE public.mm_loan OWNER TO postgres;

--
-- TOC entry 213 (class 1259 OID 17012)
-- Name: mm_media; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mm_media (
    mm_media_guid uuid NOT NULL,
    mm_media_metadata_guid uuid,
    mm_media_path text,
    mm_media_ffprobe_json jsonb,
    mm_media_json jsonb,
    mm_media_class_guid smallint
);


ALTER TABLE public.mm_media OWNER TO postgres;

--
-- TOC entry 214 (class 1259 OID 17024)
-- Name: mm_media_dir; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mm_media_dir (
    mm_media_dir_guid uuid NOT NULL,
    mm_media_dir_path text,
    mm_media_dir_last_scanned timestamp without time zone,
    mm_media_dir_share_guid uuid,
    mm_media_dir_status jsonb,
    mm_media_dir_class_type smallint
);


ALTER TABLE public.mm_media_dir OWNER TO postgres;

--
-- TOC entry 215 (class 1259 OID 17030)
-- Name: mm_media_remote; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mm_media_remote (
    mmr_media_guid uuid NOT NULL,
    mmr_media_link_id uuid,
    mmr_media_uuid uuid,
    mmr_media_metadata_guid uuid,
    mmr_media_ffprobe_json jsonb,
    mmr_media_json jsonb,
    mmr_media_class_guid smallint
);


ALTER TABLE public.mm_media_remote OWNER TO postgres;

--
-- TOC entry 216 (class 1259 OID 17036)
-- Name: mm_media_share; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mm_media_share (
    mm_media_share_guid uuid NOT NULL,
    mm_media_share_type text,
    mm_media_share_user text,
    mm_media_share_password text,
    mm_media_share_server text,
    mm_media_share_path text
);


ALTER TABLE public.mm_media_share OWNER TO postgres;

--
-- TOC entry 217 (class 1259 OID 17042)
-- Name: mm_metadata_album; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mm_metadata_album (
    mm_metadata_album_guid uuid NOT NULL,
    mm_metadata_album_name text,
    mm_metadata_album_id jsonb,
    mm_metadata_album_json jsonb,
    mm_metadata_album_musician_guid uuid,
    mm_metadata_album_user_json jsonb,
    mm_metadata_album_localimage jsonb
);


ALTER TABLE public.mm_metadata_album OWNER TO postgres;

--
-- TOC entry 218 (class 1259 OID 17048)
-- Name: mm_metadata_anime; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mm_metadata_anime (
    mm_metadata_anime_guid uuid NOT NULL,
    mm_metadata_anime_media_id jsonb,
    mm_media_anime_name text,
    mm_metadata_anime_json jsonb,
    mm_metadata_anime_mapping jsonb,
    mm_metadata_anime_mapping_before text,
    mm_metadata_anime_localimage_json jsonb,
    mm_metadata_anime_user_json jsonb
);


ALTER TABLE public.mm_metadata_anime OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 17054)
-- Name: mm_metadata_book; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mm_metadata_book (
    mm_metadata_book_guid uuid NOT NULL,
    mm_metadata_book_isbn text,
    mm_metadata_book_isbn13 text,
    mm_metadata_book_name text,
    mm_metadata_book_json jsonb,
    mm_metadata_book_user_json jsonb,
    mm_metadata_book_localimage_json jsonb
);


ALTER TABLE public.mm_metadata_book OWNER TO postgres;

--
-- TOC entry 220 (class 1259 OID 17060)
-- Name: mm_metadata_collection; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mm_metadata_collection (
    mm_metadata_collection_guid uuid NOT NULL,
    mm_metadata_collection_name jsonb,
    mm_metadata_collection_media_ids jsonb,
    mm_metadata_collection_json jsonb,
    mm_metadata_collection_imagelocal_json jsonb
);


ALTER TABLE public.mm_metadata_collection OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 17066)
-- Name: mm_metadata_game_software_info; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mm_metadata_game_software_info (
    gi_id uuid NOT NULL,
    gi_system_id uuid,
    gi_game_info_short_name text,
    gi_game_info_name text,
    gi_game_info_json jsonb,
    gi_game_info_localimage_json jsonb
);


ALTER TABLE public.mm_metadata_game_software_info OWNER TO postgres;

--
-- TOC entry 222 (class 1259 OID 17072)
-- Name: mm_metadata_game_systems_info; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mm_metadata_game_systems_info (
    gs_id uuid NOT NULL,
    gs_game_system_name text,
    gs_game_system_alias text,
    gs_game_system_json jsonb,
    gs_game_system_localimage_json jsonb
);


ALTER TABLE public.mm_metadata_game_systems_info OWNER TO postgres;

--
-- TOC entry 223 (class 1259 OID 17078)
-- Name: mm_metadata_logo; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mm_metadata_logo (
    mm_metadata_logo_guid uuid NOT NULL,
    mm_metadata_logo_media_guid jsonb,
    mm_metadata_logo_image_path text
);


ALTER TABLE public.mm_metadata_logo OWNER TO postgres;

--
-- TOC entry 224 (class 1259 OID 17084)
-- Name: mm_metadata_movie; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mm_metadata_movie (
    mm_metadata_guid uuid NOT NULL,
    mm_metadata_media_id integer,
    mm_media_name text,
    mm_metadata_json jsonb,
    mm_metadata_localimage_json jsonb,
    mm_metadata_user_json jsonb
);


ALTER TABLE public.mm_metadata_movie OWNER TO postgres;

--
-- TOC entry 225 (class 1259 OID 17090)
-- Name: mm_metadata_music; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mm_metadata_music (
    mm_metadata_music_guid uuid NOT NULL,
    mm_metadata_media_music_id jsonb,
    mm_metadata_music_name text,
    mm_metadata_music_json jsonb,
    mm_metadata_music_album_guid uuid,
    mm_metadata_music_user_json jsonb
);


ALTER TABLE public.mm_metadata_music OWNER TO postgres;

--
-- TOC entry 226 (class 1259 OID 17096)
-- Name: mm_metadata_music_video; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mm_metadata_music_video (
    mm_metadata_music_video_guid uuid NOT NULL,
    mm_metadata_music_video_media_id jsonb,
    mm_media_music_video_band text,
    mm_media_music_video_song text,
    mm_metadata_music_video_json jsonb,
    mm_metadata_music_video_localimage_json jsonb,
    mm_metadata_music_video_user_json jsonb
);


ALTER TABLE public.mm_metadata_music_video OWNER TO postgres;

--
-- TOC entry 227 (class 1259 OID 17102)
-- Name: mm_metadata_musician; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mm_metadata_musician (
    mm_metadata_musician_guid uuid NOT NULL,
    mm_metadata_musician_name text,
    mm_metadata_musician_id jsonb,
    mm_metadata_musician_json jsonb,
    mm_metadata_musician_localimage_json jsonb
);


ALTER TABLE public.mm_metadata_musician OWNER TO postgres;

--
-- TOC entry 228 (class 1259 OID 17108)
-- Name: mm_metadata_person; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mm_metadata_person (
    mmp_id uuid NOT NULL,
    mmp_person_media_id integer,
    mmp_person_meta_json jsonb,
    mmp_person_image text,
    mmp_person_name text
);


ALTER TABLE public.mm_metadata_person OWNER TO postgres;

--
-- TOC entry 229 (class 1259 OID 17114)
-- Name: mm_metadata_sports; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mm_metadata_sports (
    mm_metadata_sports_guid uuid NOT NULL,
    mm_metadata_media_sports_id jsonb,
    mm_metadata_sports_name text,
    mm_metadata_sports_json jsonb,
    mm_metadata_sports_user_json jsonb,
    mm_metadata_sports_image_json jsonb
);


ALTER TABLE public.mm_metadata_sports OWNER TO postgres;

--
-- TOC entry 230 (class 1259 OID 17120)
-- Name: mm_metadata_tvshow; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mm_metadata_tvshow (
    mm_metadata_tvshow_guid uuid NOT NULL,
    mm_metadata_media_tvshow_id integer,
    mm_metadata_tvshow_name text,
    mm_metadata_tvshow_json jsonb,
    mm_metadata_tvshow_localimage_json jsonb,
    mm_metadata_tvshow_user_json jsonb
);


ALTER TABLE public.mm_metadata_tvshow OWNER TO postgres;

--
-- TOC entry 231 (class 1259 OID 17126)
-- Name: mm_notification; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mm_notification (
    mm_notification_guid uuid NOT NULL,
    mm_notification_text text,
    mm_notification_time timestamp without time zone,
    mm_notification_dismissable boolean
);


ALTER TABLE public.mm_notification OWNER TO postgres;

--
-- TOC entry 232 (class 1259 OID 17132)
-- Name: mm_options_and_status; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mm_options_and_status (
    mm_options_and_status_guid uuid NOT NULL,
    mm_options_json jsonb,
    mm_status_json jsonb
);


ALTER TABLE public.mm_options_and_status OWNER TO postgres;

--
-- TOC entry 233 (class 1259 OID 17138)
-- Name: mm_radio; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mm_radio (
    mm_radio_guid uuid NOT NULL,
    mm_radio_name text,
    mm_radio_description text,
    mm_radio_address text,
    mm_radio_active boolean
);


ALTER TABLE public.mm_radio OWNER TO postgres;

--
-- TOC entry 234 (class 1259 OID 17144)
-- Name: mm_review; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mm_review (
    mm_review_guid uuid NOT NULL,
    mm_review_metadata_id jsonb,
    mm_review_metadata_guid uuid,
    mm_review_json jsonb
);


ALTER TABLE public.mm_review OWNER TO postgres;

--
-- TOC entry 235 (class 1259 OID 17150)
-- Name: mm_sync; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mm_sync (
    mm_sync_guid uuid NOT NULL,
    mm_sync_path text,
    mm_sync_path_to text,
    mm_sync_options_json jsonb
);


ALTER TABLE public.mm_sync OWNER TO postgres;

--
-- TOC entry 236 (class 1259 OID 17156)
-- Name: mm_tv_schedule; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mm_tv_schedule (
    mm_tv_schedule_id uuid NOT NULL,
    mm_tv_schedule_station_id text,
    mm_tv_schedule_date date,
    mm_tv_schedule_json jsonb
);


ALTER TABLE public.mm_tv_schedule OWNER TO postgres;

--
-- TOC entry 237 (class 1259 OID 17162)
-- Name: mm_tv_schedule_program; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mm_tv_schedule_program (
    mm_tv_schedule_program_guid uuid NOT NULL,
    mm_tv_schedule_program_id text,
    mm_tv_schedule_program_json jsonb
);


ALTER TABLE public.mm_tv_schedule_program OWNER TO postgres;

--
-- TOC entry 238 (class 1259 OID 17168)
-- Name: mm_tv_stations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mm_tv_stations (
    mm_tv_stations_id uuid NOT NULL,
    mm_tv_station_name text,
    mm_tv_station_id text,
    mm_tv_station_channel text,
    mm_tv_station_json jsonb,
    mm_tv_station_image text
);


ALTER TABLE public.mm_tv_stations OWNER TO postgres;

--
-- TOC entry 239 (class 1259 OID 17174)
-- Name: mm_user; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mm_user (
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


ALTER TABLE public.mm_user OWNER TO postgres;

--
-- TOC entry 240 (class 1259 OID 17180)
-- Name: mm_user_activity; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mm_user_activity (
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


ALTER TABLE public.mm_user_activity OWNER TO postgres;

--
-- TOC entry 241 (class 1259 OID 17186)
-- Name: mm_user_group; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mm_user_group (
    mm_user_group_guid uuid NOT NULL,
    mm_user_group_name text,
    mm_user_group_description text,
    mm_user_group_rights_json jsonb
);


ALTER TABLE public.mm_user_group OWNER TO postgres;

--
-- TOC entry 242 (class 1259 OID 17192)
-- Name: mm_user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.mm_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.mm_user_id_seq OWNER TO postgres;

--
-- TOC entry 3355 (class 0 OID 0)
-- Dependencies: 242
-- Name: mm_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mm_user_id_seq OWNED BY public.mm_user.id;


--
-- TOC entry 243 (class 1259 OID 17194)
-- Name: mm_user_profile; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mm_user_profile (
    mm_user_profile_guid uuid NOT NULL,
    mm_user_profile_name text,
    mm_user_profile_json jsonb
);


ALTER TABLE public.mm_user_profile OWNER TO postgres;

--
-- TOC entry 246 (class 1259 OID 17415)
-- Name: mm_user_queue; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mm_user_queue (
    mm_user_queue_id uuid NOT NULL,
    mm_user_queue_name text,
    mm_user_queue_user_id uuid,
    mm_user_queue_media_type smallint
);


ALTER TABLE public.mm_user_queue OWNER TO postgres;

--
-- TOC entry 244 (class 1259 OID 17200)
-- Name: mm_version; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mm_version (
    mm_version_no integer
);


ALTER TABLE public.mm_version OWNER TO postgres;

--
-- TOC entry 2972 (class 2604 OID 17203)
-- Name: mm_user id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mm_user ALTER COLUMN id SET DEFAULT nextval('public.mm_user_id_seq'::regclass);


--
-- TOC entry 3305 (class 0 OID 16967)
-- Dependencies: 205
-- Data for Name: mm_channel; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mm_channel (mm_channel_guid, mm_channel_name, mm_channel_media_id, mm_channel_country_guid, mm_channel_logo_guid) FROM stdin;
\.


--
-- TOC entry 3306 (class 0 OID 16973)
-- Dependencies: 206
-- Data for Name: mm_cron; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mm_cron (mm_cron_guid, mm_cron_name, mm_cron_description, mm_cron_enabled, mm_cron_schedule, mm_cron_last_run, mm_cron_json) FROM stdin;
47cad101-9e87-4596-ba02-2bcea8ce3575	Anime	Match anime via Scudlee and Manami data	f	Days 1	1970-01-01 00:00:01	{"Type": "Anime Xref", "program": "/mediakraken/subprogram_match_anime_id.py", "route_key": "Z", "exchange_key": "mkque_metadata_ex"}
631ea52e-2807-4342-8b59-2f8263da0ef2	Collections	Create and update collection(s)	f	Days 1	1970-01-01 00:00:01	{"Type": "Update Collection", "program": "/mediakraken/subprogram_metadata_update_create_collections.py", "route_key": "themoviedb", "exchange_key": "mkque_metadata_ex"}
f82f2aa4-3b4b-4a78-ab5a-5564c414ab1d	Schedules Direct	Fetch TV schedules from Schedules Direct	f	Days 1	1970-01-01 00:00:01	{"Type": "Update", "program": "/mediakraken/subprogram_schedules_direct_updates.py", "route_key": "schedulesdirect", "exchange_key": "mkque_metadata_ex"}
0d6f545f-2682-4bfd-8d9a-620eaae36690	The Movie Database	Grab updated metadata for movie(s) and TV show(s)	f	Days 1	1970-01-01 00:00:01	{"Type": "Update Metadata", "program": "/mediakraken/subprogram_metadata_tmdb_updates.py", "route_key": "themoviedb", "exchange_key": "mkque_metadata_ex"}
9e07954c-26e5-4752-863b-f6142b5f6e6a	Trailer	Download new trailer(s)	f	Days 1	1970-01-01 00:00:01	{"Type": "HDTrailers", "route_key": "mkdownload", "exchange_key": "mkque_download_ex"}
f039f4d3-ec26-491a-a498-60ea2b1f314b	Backup	Backup PostgreSQL DB	f	Days 1	1970-01-01 00:00:01	{"Type": "Cron Run", "program": "/mediakraken/subprogram_postgresql_backup.py", "route_key": "mkque", "exchange_key": "mkque_ex"}
128d11cd-c0c2-44d7-ae16-cf5de96207d7	DB Vacuum	PostgreSQL Vacuum Analyze all tables	f	Days 1	1970-01-01 00:00:01	{"Type": "Cron Run", "program": "/mediakraken/subprogram_postgresql_vacuum.py", "route_key": "mkque", "exchange_key": "mkque_ex"}
de374320-56f7-45cd-b42c-9c8147feb81f	Media Scan	Scan for new media	f	Days 1	1970-01-01 00:00:01	{"Type": "Library Scan", "route_key": "mkque", "exchange_key": "mkque_ex"}
c1f8e43d-c657-435c-a6e1-ac296b3bfba9	Sync	Sync and transcode media	f	Days 1	1970-01-01 00:00:01	{"Type": "Cron Run", "program": "/mediakraken/subprogram_sync.py", "route_key": "mkque", "exchange_key": "mkque_ex"}
3da17df9-fae9-4a3a-a70b-5f429d5c1821	Retro game data	Grab updated metadata for retro game(s)	f	Days 1	1970-01-01 00:00:01	{"Type": "Cron Run", "program": "/mediakraken/subprogram_metadata_games.py", "route_key": "mkque", "exchange_key": "mkque_ex"}
\.


--
-- TOC entry 3307 (class 0 OID 16979)
-- Dependencies: 207
-- Data for Name: mm_device; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mm_device (mm_device_id, mm_device_type, mm_device_json) FROM stdin;
\.


--
-- TOC entry 3308 (class 0 OID 16985)
-- Dependencies: 208
-- Data for Name: mm_download_que; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mm_download_que (mdq_id, mdq_provider, mdq_que_type, mdq_download_json) FROM stdin;
\.


--
-- TOC entry 3309 (class 0 OID 16991)
-- Dependencies: 209
-- Data for Name: mm_game_category; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mm_game_category (gc_id, gc_category) FROM stdin;
\.


--
-- TOC entry 3345 (class 0 OID 17406)
-- Dependencies: 245
-- Data for Name: mm_game_dedicated_servers; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mm_game_dedicated_servers (mm_game_server_id, mm_game_server_name, mm_game_server_json) FROM stdin;
\.


--
-- TOC entry 3310 (class 0 OID 16997)
-- Dependencies: 210
-- Data for Name: mm_hardware; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mm_hardware (mm_hardware_id, mm_hardware_manufacturer, mm_hardware_model, mm_hardware_json) FROM stdin;
\.


--
-- TOC entry 3311 (class 0 OID 17003)
-- Dependencies: 211
-- Data for Name: mm_link; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mm_link (mm_link_guid, mm_link_name, mm_link_json) FROM stdin;
\.


--
-- TOC entry 3312 (class 0 OID 17009)
-- Dependencies: 212
-- Data for Name: mm_loan; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mm_loan (mm_loan_guid, mm_loan_media_id, mm_loan_user_id, mm_load_user_loan_id, mm_loan_time, mm_loan_return_time) FROM stdin;
\.


--
-- TOC entry 3313 (class 0 OID 17012)
-- Dependencies: 213
-- Data for Name: mm_media; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mm_media (mm_media_guid, mm_media_metadata_guid, mm_media_path, mm_media_ffprobe_json, mm_media_json, mm_media_class_guid) FROM stdin;
\.


--
-- TOC entry 3314 (class 0 OID 17024)
-- Dependencies: 214
-- Data for Name: mm_media_dir; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mm_media_dir (mm_media_dir_guid, mm_media_dir_path, mm_media_dir_last_scanned, mm_media_dir_share_guid, mm_media_dir_status, mm_media_dir_class_type) FROM stdin;
\.


--
-- TOC entry 3315 (class 0 OID 17030)
-- Dependencies: 215
-- Data for Name: mm_media_remote; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mm_media_remote (mmr_media_guid, mmr_media_link_id, mmr_media_uuid, mmr_media_metadata_guid, mmr_media_ffprobe_json, mmr_media_json, mmr_media_class_guid) FROM stdin;
\.


--
-- TOC entry 3316 (class 0 OID 17036)
-- Dependencies: 216
-- Data for Name: mm_media_share; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mm_media_share (mm_media_share_guid, mm_media_share_type, mm_media_share_user, mm_media_share_password, mm_media_share_server, mm_media_share_path) FROM stdin;
\.


--
-- TOC entry 3317 (class 0 OID 17042)
-- Dependencies: 217
-- Data for Name: mm_metadata_album; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mm_metadata_album (mm_metadata_album_guid, mm_metadata_album_name, mm_metadata_album_id, mm_metadata_album_json, mm_metadata_album_musician_guid, mm_metadata_album_user_json, mm_metadata_album_localimage) FROM stdin;
\.


--
-- TOC entry 3318 (class 0 OID 17048)
-- Dependencies: 218
-- Data for Name: mm_metadata_anime; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mm_metadata_anime (mm_metadata_anime_guid, mm_metadata_anime_media_id, mm_media_anime_name, mm_metadata_anime_json, mm_metadata_anime_mapping, mm_metadata_anime_mapping_before, mm_metadata_anime_localimage_json, mm_metadata_anime_user_json) FROM stdin;
\.


--
-- TOC entry 3319 (class 0 OID 17054)
-- Dependencies: 219
-- Data for Name: mm_metadata_book; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mm_metadata_book (mm_metadata_book_guid, mm_metadata_book_isbn, mm_metadata_book_isbn13, mm_metadata_book_name, mm_metadata_book_json, mm_metadata_book_user_json, mm_metadata_book_localimage_json) FROM stdin;
\.


--
-- TOC entry 3320 (class 0 OID 17060)
-- Dependencies: 220
-- Data for Name: mm_metadata_collection; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mm_metadata_collection (mm_metadata_collection_guid, mm_metadata_collection_name, mm_metadata_collection_media_ids, mm_metadata_collection_json, mm_metadata_collection_imagelocal_json) FROM stdin;
\.


--
-- TOC entry 3321 (class 0 OID 17066)
-- Dependencies: 221
-- Data for Name: mm_metadata_game_software_info; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mm_metadata_game_software_info (gi_id, gi_system_id, gi_game_info_short_name, gi_game_info_name, gi_game_info_json, gi_game_info_localimage_json) FROM stdin;
\.


--
-- TOC entry 3322 (class 0 OID 17072)
-- Dependencies: 222
-- Data for Name: mm_metadata_game_systems_info; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mm_metadata_game_systems_info (gs_id, gs_game_system_name, gs_game_system_alias, gs_game_system_json, gs_game_system_localimage_json) FROM stdin;
\.


--
-- TOC entry 3323 (class 0 OID 17078)
-- Dependencies: 223
-- Data for Name: mm_metadata_logo; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mm_metadata_logo (mm_metadata_logo_guid, mm_metadata_logo_media_guid, mm_metadata_logo_image_path) FROM stdin;
\.


--
-- TOC entry 3324 (class 0 OID 17084)
-- Dependencies: 224
-- Data for Name: mm_metadata_movie; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mm_metadata_movie (mm_metadata_guid, mm_metadata_media_id, mm_media_name, mm_metadata_json, mm_metadata_localimage_json, mm_metadata_user_json) FROM stdin;
\.


--
-- TOC entry 3325 (class 0 OID 17090)
-- Dependencies: 225
-- Data for Name: mm_metadata_music; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mm_metadata_music (mm_metadata_music_guid, mm_metadata_media_music_id, mm_metadata_music_name, mm_metadata_music_json, mm_metadata_music_album_guid, mm_metadata_music_user_json) FROM stdin;
\.


--
-- TOC entry 3326 (class 0 OID 17096)
-- Dependencies: 226
-- Data for Name: mm_metadata_music_video; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mm_metadata_music_video (mm_metadata_music_video_guid, mm_metadata_music_video_media_id, mm_media_music_video_band, mm_media_music_video_song, mm_metadata_music_video_json, mm_metadata_music_video_localimage_json, mm_metadata_music_video_user_json) FROM stdin;
\.


--
-- TOC entry 3327 (class 0 OID 17102)
-- Dependencies: 227
-- Data for Name: mm_metadata_musician; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mm_metadata_musician (mm_metadata_musician_guid, mm_metadata_musician_name, mm_metadata_musician_id, mm_metadata_musician_json, mm_metadata_musician_localimage_json) FROM stdin;
\.


--
-- TOC entry 3328 (class 0 OID 17108)
-- Dependencies: 228
-- Data for Name: mm_metadata_person; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mm_metadata_person (mmp_id, mmp_person_media_id, mmp_person_meta_json, mmp_person_image, mmp_person_name) FROM stdin;
\.


--
-- TOC entry 3329 (class 0 OID 17114)
-- Dependencies: 229
-- Data for Name: mm_metadata_sports; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mm_metadata_sports (mm_metadata_sports_guid, mm_metadata_media_sports_id, mm_metadata_sports_name, mm_metadata_sports_json, mm_metadata_sports_user_json, mm_metadata_sports_image_json) FROM stdin;
\.


--
-- TOC entry 3330 (class 0 OID 17120)
-- Dependencies: 230
-- Data for Name: mm_metadata_tvshow; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mm_metadata_tvshow (mm_metadata_tvshow_guid, mm_metadata_media_tvshow_id, mm_metadata_tvshow_name, mm_metadata_tvshow_json, mm_metadata_tvshow_localimage_json, mm_metadata_tvshow_user_json) FROM stdin;
\.


--
-- TOC entry 3331 (class 0 OID 17126)
-- Dependencies: 231
-- Data for Name: mm_notification; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mm_notification (mm_notification_guid, mm_notification_text, mm_notification_time, mm_notification_dismissable) FROM stdin;
\.


--
-- TOC entry 3332 (class 0 OID 17132)
-- Dependencies: 232
-- Data for Name: mm_options_and_status; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mm_options_and_status (mm_options_and_status_guid, mm_options_json, mm_status_json) FROM stdin;
df641592-2c6a-4ffa-816d-5f24dcea1ddd	{"API": {"anidb": null, "imvdb": null, "google": "AIzaSyCwMkNYp8E4H19BDzlM7-IDkNCQtw0R9lY", "isbndb": "25C8IT4I", "tvmaze": "mknotneeded", "thetvdb": "147CB43DCA8B61B7", "shoutcast": null, "thelogodb": null, "soundcloud": null, "themoviedb": "f72118d1e84b8a1438935972a9c37cac", "globalcache": null, "musicbrainz": null, "thesportsdb": "4352761817344", "opensubtitles": null, "openweathermap": "575b4ae4615e4e2a4c34fb9defa17ceb", "rottentomatoes": "f4tnu5dn9r7f28gjth3ftqaj"}, "User": {"Password Lock": null, "Activity Purge": null}, "Cloud": {}, "Trakt": {"ApiKey": null, "ClientID": null, "SecretKey": null}, "Backup": {"Interval": 0, "BackupType": "local"}, "Docker": {"Nodes": 0, "SwarmID": null, "Instances": 0}, "LastFM": {"api_key": null, "password": null, "username": null, "api_secret": null}, "Twitch": {"OAuth": null, "ClientID": null}, "Account": {"ScheduleDirect": {"User": null, "Password": null}}, "Metadata": {"Trailer": {"Clip": false, "Behind": false, "Carpool": false, "Trailer": false, "Featurette": false}, "DL Subtitle": false, "MusicBrainz": {"Host": null, "Port": 5000, "User": null, "Password": null}, "MetadataImageLocal": false}, "Transmission": {"Host": null, "Port": 9091, "Password": "metaman", "Username": "spootdev"}, "Docker Instances": {"elk": false, "smtp": false, "mumble": false, "pgadmin": false, "portainer": false, "teamspeak": false, "wireshark": false, "musicbrainz": false, "transmission": false}, "MediaKrakenServer": {"MOTD": null, "Maintenance": null, "Server Name": "MediaKraken", "MaxResumePct": 5}}	{"thetvdb_Updated_Epoc": 0}
\.


--
-- TOC entry 3333 (class 0 OID 17138)
-- Dependencies: 233
-- Data for Name: mm_radio; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mm_radio (mm_radio_guid, mm_radio_name, mm_radio_description, mm_radio_address, mm_radio_active) FROM stdin;
\.


--
-- TOC entry 3334 (class 0 OID 17144)
-- Dependencies: 234
-- Data for Name: mm_review; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mm_review (mm_review_guid, mm_review_metadata_id, mm_review_metadata_guid, mm_review_json) FROM stdin;
\.


--
-- TOC entry 3335 (class 0 OID 17150)
-- Dependencies: 235
-- Data for Name: mm_sync; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mm_sync (mm_sync_guid, mm_sync_path, mm_sync_path_to, mm_sync_options_json) FROM stdin;
\.


--
-- TOC entry 3336 (class 0 OID 17156)
-- Dependencies: 236
-- Data for Name: mm_tv_schedule; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mm_tv_schedule (mm_tv_schedule_id, mm_tv_schedule_station_id, mm_tv_schedule_date, mm_tv_schedule_json) FROM stdin;
\.


--
-- TOC entry 3337 (class 0 OID 17162)
-- Dependencies: 237
-- Data for Name: mm_tv_schedule_program; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mm_tv_schedule_program (mm_tv_schedule_program_guid, mm_tv_schedule_program_id, mm_tv_schedule_program_json) FROM stdin;
\.


--
-- TOC entry 3338 (class 0 OID 17168)
-- Dependencies: 238
-- Data for Name: mm_tv_stations; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mm_tv_stations (mm_tv_stations_id, mm_tv_station_name, mm_tv_station_id, mm_tv_station_channel, mm_tv_station_json, mm_tv_station_image) FROM stdin;
\.


--
-- TOC entry 3339 (class 0 OID 17174)
-- Dependencies: 239
-- Data for Name: mm_user; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mm_user (id, username, email, password, created_at, active, is_admin, user_json, lang) FROM stdin;
\.


--
-- TOC entry 3340 (class 0 OID 17180)
-- Dependencies: 240
-- Data for Name: mm_user_activity; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mm_user_activity (mm_activity_guid, mm_activity_name, mm_activity_overview, mm_activity_short_overview, mm_activity_type, mm_activity_itemid, mm_activity_userid, mm_activity_datecreated, mm_activity_log_severity) FROM stdin;
\.


--
-- TOC entry 3341 (class 0 OID 17186)
-- Dependencies: 241
-- Data for Name: mm_user_group; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mm_user_group (mm_user_group_guid, mm_user_group_name, mm_user_group_description, mm_user_group_rights_json) FROM stdin;
38117775-93b4-47d6-9a42-fc886ab6580c	Administrator	Server administrator	{"Admin": true, "PreviewOnly": false}
6666956c-a4d8-45bc-9c56-deaa1c2b68d3	User	General user	{"Admin": false, "PreviewOnly": false}
bea39ac2-505e-4cdd-9a3b-9c7da2cb28b2	Guest	Guest (Preview only)	{"Admin": false, "PreviewOnly": true}
\.


--
-- TOC entry 3343 (class 0 OID 17194)
-- Dependencies: 243
-- Data for Name: mm_user_profile; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mm_user_profile (mm_user_profile_guid, mm_user_profile_name, mm_user_profile_json) FROM stdin;
0863c596-3d62-4409-83c2-0515d3465adc	Adult	{"3D": true, "TV": true, "Home": true, "Lang": "en", "Sync": true, "Adult": true, "Books": true, "Games": true, "MaxBR": 100, "Movie": true, "Music": true, "IRadio": true, "Images": true, "LiveTV": true, "Sports": true, "Internet": true, "MaxRating": 5}
2bf39eb6-8192-4c2d-88cf-6341bbec1cd8	Teen	{"3D": true, "TV": true, "Home": true, "Lang": "en", "Sync": false, "Adult": false, "Books": true, "Games": true, "MaxBR": 50, "Movie": true, "Music": true, "IRadio": true, "Images": true, "LiveTV": true, "Sports": true, "Internet": true, "MaxRating": 3}
2bcbbd3e-8e2e-4fdc-92a9-471e5d018539	Child	{"3D": false, "TV": true, "Home": true, "Lang": "en", "Sync": false, "Adult": false, "Books": true, "Games": true, "MaxBR": 20, "Movie": true, "Music": true, "IRadio": false, "Images": true, "LiveTV": false, "Sports": true, "Internet": false, "MaxRating": 0}
\.


--
-- TOC entry 3346 (class 0 OID 17415)
-- Dependencies: 246
-- Data for Name: mm_user_queue; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mm_user_queue (mm_user_queue_id, mm_user_queue_name, mm_user_queue_user_id, mm_user_queue_media_type) FROM stdin;
\.


--
-- TOC entry 3344 (class 0 OID 17200)
-- Dependencies: 244
-- Data for Name: mm_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mm_version (mm_version_no) FROM stdin;
27
\.


--
-- TOC entry 3356 (class 0 OID 0)
-- Dependencies: 242
-- Name: mm_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mm_user_id_seq', 1, false);


--
-- TOC entry 2992 (class 2606 OID 17205)
-- Name: mm_game_category gc_id_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mm_game_category
    ADD CONSTRAINT gc_id_pk PRIMARY KEY (gc_id);


--
-- TOC entry 3054 (class 2606 OID 17207)
-- Name: mm_metadata_game_software_info gi_id_mpk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mm_metadata_game_software_info
    ADD CONSTRAINT gi_id_mpk PRIMARY KEY (gi_id);


--
-- TOC entry 3059 (class 2606 OID 17209)
-- Name: mm_metadata_game_systems_info gs_id_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mm_metadata_game_systems_info
    ADD CONSTRAINT gs_id_pk PRIMARY KEY (gs_id);


--
-- TOC entry 2986 (class 2606 OID 17211)
-- Name: mm_download_que mdq_id_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mm_download_que
    ADD CONSTRAINT mdq_id_pk PRIMARY KEY (mdq_id);


--
-- TOC entry 3162 (class 2606 OID 17213)
-- Name: mm_user_activity mm_activity_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mm_user_activity
    ADD CONSTRAINT mm_activity_pk PRIMARY KEY (mm_activity_guid);


--
-- TOC entry 2974 (class 2606 OID 17215)
-- Name: mm_channel mm_channel_guid_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mm_channel
    ADD CONSTRAINT mm_channel_guid_pk PRIMARY KEY (mm_channel_guid);


--
-- TOC entry 2980 (class 2606 OID 17217)
-- Name: mm_cron mm_cron_guid_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mm_cron
    ADD CONSTRAINT mm_cron_guid_pk PRIMARY KEY (mm_cron_guid);


--
-- TOC entry 2982 (class 2606 OID 17219)
-- Name: mm_device mm_device_id_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mm_device
    ADD CONSTRAINT mm_device_id_pk PRIMARY KEY (mm_device_id);


--
-- TOC entry 3172 (class 2606 OID 17413)
-- Name: mm_game_dedicated_servers mm_game_server_id; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mm_game_dedicated_servers
    ADD CONSTRAINT mm_game_server_id PRIMARY KEY (mm_game_server_id);


--
-- TOC entry 2994 (class 2606 OID 17221)
-- Name: mm_hardware mm_hardware_id; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mm_hardware
    ADD CONSTRAINT mm_hardware_id PRIMARY KEY (mm_hardware_id);


--
-- TOC entry 2998 (class 2606 OID 17223)
-- Name: mm_link mm_link_guid_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mm_link
    ADD CONSTRAINT mm_link_guid_pk PRIMARY KEY (mm_link_guid);


--
-- TOC entry 3002 (class 2606 OID 17225)
-- Name: mm_loan mm_loan_guid_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mm_loan
    ADD CONSTRAINT mm_loan_guid_pk PRIMARY KEY (mm_loan_guid);


--
-- TOC entry 3010 (class 2606 OID 17229)
-- Name: mm_media_dir mm_media_dir_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mm_media_dir
    ADD CONSTRAINT mm_media_dir_pk PRIMARY KEY (mm_media_dir_guid);


--
-- TOC entry 3007 (class 2606 OID 17231)
-- Name: mm_media mm_media_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mm_media
    ADD CONSTRAINT mm_media_pk PRIMARY KEY (mm_media_guid);


--
-- TOC entry 3017 (class 2606 OID 17233)
-- Name: mm_media_share mm_media_share_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mm_media_share
    ADD CONSTRAINT mm_media_share_pk PRIMARY KEY (mm_media_share_guid);


--
-- TOC entry 3025 (class 2606 OID 17235)
-- Name: mm_metadata_album mm_metadata_album_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mm_metadata_album
    ADD CONSTRAINT mm_metadata_album_pk PRIMARY KEY (mm_metadata_album_guid);


--
-- TOC entry 3037 (class 2606 OID 17237)
-- Name: mm_metadata_anime mm_metadata_anime_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mm_metadata_anime
    ADD CONSTRAINT mm_metadata_anime_pk PRIMARY KEY (mm_metadata_anime_guid);


--
-- TOC entry 3040 (class 2606 OID 17239)
-- Name: mm_metadata_book mm_metadata_book_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mm_metadata_book
    ADD CONSTRAINT mm_metadata_book_pk PRIMARY KEY (mm_metadata_book_guid);


--
-- TOC entry 3046 (class 2606 OID 17241)
-- Name: mm_metadata_collection mm_metadata_collection_guid_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mm_metadata_collection
    ADD CONSTRAINT mm_metadata_collection_guid_pk PRIMARY KEY (mm_metadata_collection_guid);


--
-- TOC entry 3062 (class 2606 OID 17243)
-- Name: mm_metadata_logo mm_metadata_logo_guid_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mm_metadata_logo
    ADD CONSTRAINT mm_metadata_logo_guid_pk PRIMARY KEY (mm_metadata_logo_guid);


--
-- TOC entry 3079 (class 2606 OID 17245)
-- Name: mm_metadata_music mm_metadata_music_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mm_metadata_music
    ADD CONSTRAINT mm_metadata_music_pk PRIMARY KEY (mm_metadata_music_guid);


--
-- TOC entry 3091 (class 2606 OID 17247)
-- Name: mm_metadata_music_video mm_metadata_music_video_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mm_metadata_music_video
    ADD CONSTRAINT mm_metadata_music_video_pk PRIMARY KEY (mm_metadata_music_video_guid);


--
-- TOC entry 3098 (class 2606 OID 17249)
-- Name: mm_metadata_musician mm_metadata_musician_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mm_metadata_musician
    ADD CONSTRAINT mm_metadata_musician_pk PRIMARY KEY (mm_metadata_musician_guid);


--
-- TOC entry 3070 (class 2606 OID 17251)
-- Name: mm_metadata_movie mm_metadata_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mm_metadata_movie
    ADD CONSTRAINT mm_metadata_pk PRIMARY KEY (mm_metadata_guid);


--
-- TOC entry 3117 (class 2606 OID 17253)
-- Name: mm_metadata_sports mm_metadata_sports_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mm_metadata_sports
    ADD CONSTRAINT mm_metadata_sports_pk PRIMARY KEY (mm_metadata_sports_guid);


--
-- TOC entry 3131 (class 2606 OID 17255)
-- Name: mm_metadata_tvshow mm_metadata_tvshow_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mm_metadata_tvshow
    ADD CONSTRAINT mm_metadata_tvshow_pk PRIMARY KEY (mm_metadata_tvshow_guid);


--
-- TOC entry 3135 (class 2606 OID 17257)
-- Name: mm_notification mm_notification_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mm_notification
    ADD CONSTRAINT mm_notification_pk PRIMARY KEY (mm_notification_guid);


--
-- TOC entry 3137 (class 2606 OID 17259)
-- Name: mm_options_and_status mm_options_and_status_guid_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mm_options_and_status
    ADD CONSTRAINT mm_options_and_status_guid_pk PRIMARY KEY (mm_options_and_status_guid);


--
-- TOC entry 3139 (class 2606 OID 17261)
-- Name: mm_radio mm_radio_guid_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mm_radio
    ADD CONSTRAINT mm_radio_guid_pk PRIMARY KEY (mm_radio_guid);


--
-- TOC entry 3143 (class 2606 OID 17263)
-- Name: mm_review mm_review_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mm_review
    ADD CONSTRAINT mm_review_pk PRIMARY KEY (mm_review_guid);


--
-- TOC entry 3145 (class 2606 OID 17265)
-- Name: mm_sync mm_sync_guid_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mm_sync
    ADD CONSTRAINT mm_sync_guid_pk PRIMARY KEY (mm_sync_guid);


--
-- TOC entry 3148 (class 2606 OID 17267)
-- Name: mm_tv_schedule mm_tv_schedule_id_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mm_tv_schedule
    ADD CONSTRAINT mm_tv_schedule_id_pk PRIMARY KEY (mm_tv_schedule_id);


--
-- TOC entry 3153 (class 2606 OID 17269)
-- Name: mm_tv_schedule_program mm_tv_schedule_program_guid_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mm_tv_schedule_program
    ADD CONSTRAINT mm_tv_schedule_program_guid_pk PRIMARY KEY (mm_tv_schedule_program_guid);


--
-- TOC entry 3155 (class 2606 OID 17271)
-- Name: mm_tv_stations mm_tv_stations_id_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mm_tv_stations
    ADD CONSTRAINT mm_tv_stations_id_pk PRIMARY KEY (mm_tv_stations_id);


--
-- TOC entry 3166 (class 2606 OID 17273)
-- Name: mm_user_group mm_user_group_guid_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mm_user_group
    ADD CONSTRAINT mm_user_group_guid_pk PRIMARY KEY (mm_user_group_guid);


--
-- TOC entry 3160 (class 2606 OID 17275)
-- Name: mm_user mm_user_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mm_user
    ADD CONSTRAINT mm_user_pkey PRIMARY KEY (id);


--
-- TOC entry 3169 (class 2606 OID 17277)
-- Name: mm_user_profile mm_user_profile_guid_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mm_user_profile
    ADD CONSTRAINT mm_user_profile_guid_pk PRIMARY KEY (mm_user_profile_guid);


--
-- TOC entry 3175 (class 2606 OID 17422)
-- Name: mm_user_queue mm_user_queue_id; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mm_user_queue
    ADD CONSTRAINT mm_user_queue_id PRIMARY KEY (mm_user_queue_id);


--
-- TOC entry 3103 (class 2606 OID 17279)
-- Name: mm_metadata_person mmp_id_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mm_metadata_person
    ADD CONSTRAINT mmp_id_pk PRIMARY KEY (mmp_id);


--
-- TOC entry 3015 (class 2606 OID 17281)
-- Name: mm_media_remote mmr_media_remote_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mm_media_remote
    ADD CONSTRAINT mmr_media_remote_pk PRIMARY KEY (mmr_media_guid);


--
-- TOC entry 2990 (class 1259 OID 17282)
-- Name: gc_category_idx_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX gc_category_idx_name ON public.mm_game_category USING btree (gc_category);


--
-- TOC entry 3050 (class 1259 OID 17283)
-- Name: gi_game_idx_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX gi_game_idx_name ON public.mm_metadata_game_software_info USING btree (gi_game_info_name);


--
-- TOC entry 3051 (class 1259 OID 17284)
-- Name: gi_game_idx_name_trigram_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX gi_game_idx_name_trigram_idx ON public.mm_metadata_game_software_info USING gist (gi_game_info_name public.gist_trgm_ops);


--
-- TOC entry 3052 (class 1259 OID 17285)
-- Name: gi_game_idx_short_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX gi_game_idx_short_name ON public.mm_metadata_game_software_info USING btree (gi_game_info_short_name);


--
-- TOC entry 3055 (class 1259 OID 17286)
-- Name: gi_system_id_ndx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX gi_system_id_ndx ON public.mm_metadata_game_software_info USING btree (gi_system_id);


--
-- TOC entry 2987 (class 1259 OID 17287)
-- Name: mdq_que_type_idx_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mdq_que_type_idx_name ON public.mm_download_que USING btree (mdq_que_type);


--
-- TOC entry 2975 (class 1259 OID 17288)
-- Name: mm_channel_idx_country; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_channel_idx_country ON public.mm_channel USING btree (mm_channel_country_guid);


--
-- TOC entry 2976 (class 1259 OID 17289)
-- Name: mm_channel_idx_logo; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_channel_idx_logo ON public.mm_channel USING btree (mm_channel_logo_guid);


--
-- TOC entry 2977 (class 1259 OID 17290)
-- Name: mm_channel_idx_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_channel_idx_name ON public.mm_channel USING btree (mm_channel_name);


--
-- TOC entry 2978 (class 1259 OID 17291)
-- Name: mm_channel_idxgin_json; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_channel_idxgin_json ON public.mm_channel USING gin (mm_channel_media_id);


--
-- TOC entry 2983 (class 1259 OID 17292)
-- Name: mm_device_idx_type; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_device_idx_type ON public.mm_device USING btree (mm_device_type);


--
-- TOC entry 2984 (class 1259 OID 17293)
-- Name: mm_device_idxgin_json; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_device_idxgin_json ON public.mm_device USING gin (mm_device_json);


--
-- TOC entry 2988 (class 1259 OID 17294)
-- Name: mm_download_idx_provider; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_download_idx_provider ON public.mm_download_que USING btree (mdq_provider);


--
-- TOC entry 2989 (class 1259 OID 17295)
-- Name: mm_download_que_idxgin_meta_json; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_download_que_idxgin_meta_json ON public.mm_download_que USING gin (mdq_download_json);


--
-- TOC entry 3056 (class 1259 OID 17296)
-- Name: mm_game_info_idxgin_json; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_game_info_idxgin_json ON public.mm_metadata_game_software_info USING gin (gi_game_info_json);


--
-- TOC entry 3057 (class 1259 OID 17297)
-- Name: mm_game_info_idxgin_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_game_info_idxgin_name ON public.mm_metadata_game_software_info USING gin (((gi_game_info_json -> '@name'::text)));


--
-- TOC entry 3173 (class 1259 OID 17414)
-- Name: mm_game_server_name_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_game_server_name_idx ON public.mm_game_dedicated_servers USING btree (mm_game_server_name);


--
-- TOC entry 3060 (class 1259 OID 17298)
-- Name: mm_game_systems_idxgin_json; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_game_systems_idxgin_json ON public.mm_metadata_game_systems_info USING gin (gs_game_system_json);


--
-- TOC entry 2995 (class 1259 OID 17299)
-- Name: mm_hardware_idx_manufacturer; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_hardware_idx_manufacturer ON public.mm_hardware USING btree (mm_hardware_manufacturer);


--
-- TOC entry 2996 (class 1259 OID 17300)
-- Name: mm_hardware_idx_model; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_hardware_idx_model ON public.mm_hardware USING btree (mm_hardware_model);


--
-- TOC entry 2999 (class 1259 OID 17301)
-- Name: mm_link_idx_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_link_idx_name ON public.mm_link USING btree (mm_link_name);


--
-- TOC entry 3000 (class 1259 OID 17302)
-- Name: mm_link_json_idxgin; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_link_json_idxgin ON public.mm_link USING gin (mm_link_json);


--
-- TOC entry 3026 (class 1259 OID 17303)
-- Name: mm_media_anime_name_trigram_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_media_anime_name_trigram_idx ON public.mm_metadata_anime USING gist (mm_media_anime_name public.gist_trgm_ops);


--
-- TOC entry 3008 (class 1259 OID 17305)
-- Name: mm_media_dir_idx_share; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_media_dir_idx_share ON public.mm_media_dir USING btree (mm_media_dir_share_guid);


--
-- TOC entry 3003 (class 1259 OID 17306)
-- Name: mm_media_idx_metadata_uuid; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_media_idx_metadata_uuid ON public.mm_media USING btree (mm_media_metadata_guid);


--
-- TOC entry 3004 (class 1259 OID 17307)
-- Name: mm_media_idx_path; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_media_idx_path ON public.mm_media USING btree (mm_media_path);


--
-- TOC entry 3005 (class 1259 OID 17308)
-- Name: mm_media_idxgin_ffprobe; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_media_idxgin_ffprobe ON public.mm_media USING gin (mm_media_ffprobe_json);


--
-- TOC entry 3080 (class 1259 OID 17309)
-- Name: mm_media_music_video_band_trigram_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_media_music_video_band_trigram_idx ON public.mm_metadata_music_video USING gist (mm_media_music_video_band public.gist_trgm_ops);


--
-- TOC entry 3081 (class 1259 OID 17310)
-- Name: mm_media_music_video_song_trigram_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_media_music_video_song_trigram_idx ON public.mm_metadata_music_video USING gist (mm_media_music_video_song public.gist_trgm_ops);


--
-- TOC entry 3064 (class 1259 OID 17311)
-- Name: mm_media_name_trigram_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_media_name_trigram_idx ON public.mm_metadata_movie USING gist (mm_media_name public.gist_trgm_ops);


--
-- TOC entry 3018 (class 1259 OID 17312)
-- Name: mm_metadata_album_idx_musician; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_album_idx_musician ON public.mm_metadata_album USING btree (mm_metadata_album_musician_guid);


--
-- TOC entry 3019 (class 1259 OID 17313)
-- Name: mm_metadata_album_idx_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_album_idx_name ON public.mm_metadata_album USING btree (mm_metadata_album_name);


--
-- TOC entry 3020 (class 1259 OID 17314)
-- Name: mm_metadata_album_idx_name_lower; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_album_idx_name_lower ON public.mm_metadata_album USING btree (lower(mm_metadata_album_name));


--
-- TOC entry 3021 (class 1259 OID 17315)
-- Name: mm_metadata_album_idxgin_id_json; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_album_idxgin_id_json ON public.mm_metadata_album USING gin (mm_metadata_album_id);


--
-- TOC entry 3022 (class 1259 OID 17316)
-- Name: mm_metadata_album_idxgin_json; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_album_idxgin_json ON public.mm_metadata_album USING gin (mm_metadata_album_json);


--
-- TOC entry 3023 (class 1259 OID 17317)
-- Name: mm_metadata_album_name_trigram_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_album_name_trigram_idx ON public.mm_metadata_album USING gist (mm_metadata_album_name public.gist_trgm_ops);


--
-- TOC entry 3027 (class 1259 OID 17318)
-- Name: mm_metadata_aniem_idxgin_media_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_aniem_idxgin_media_id ON public.mm_metadata_anime USING gin (mm_metadata_anime_media_id);


--
-- TOC entry 3028 (class 1259 OID 17319)
-- Name: mm_metadata_anime_idx_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_anime_idx_name ON public.mm_metadata_anime USING btree (mm_media_anime_name);


--
-- TOC entry 3029 (class 1259 OID 17320)
-- Name: mm_metadata_anime_idx_name_lower; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_anime_idx_name_lower ON public.mm_metadata_anime USING btree (lower(mm_media_anime_name));


--
-- TOC entry 3030 (class 1259 OID 17321)
-- Name: mm_metadata_anime_idxgin_json; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_anime_idxgin_json ON public.mm_metadata_anime USING gin (mm_metadata_anime_json);


--
-- TOC entry 3031 (class 1259 OID 17322)
-- Name: mm_metadata_anime_idxgin_media_id_anidb; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_anime_idxgin_media_id_anidb ON public.mm_metadata_anime USING gin (((mm_metadata_anime_media_id -> 'anidb'::text)));


--
-- TOC entry 3032 (class 1259 OID 17323)
-- Name: mm_metadata_anime_idxgin_media_id_imdb; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_anime_idxgin_media_id_imdb ON public.mm_metadata_anime USING gin (((mm_metadata_anime_media_id -> 'imdb'::text)));


--
-- TOC entry 3033 (class 1259 OID 17324)
-- Name: mm_metadata_anime_idxgin_media_id_thetvdb; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_anime_idxgin_media_id_thetvdb ON public.mm_metadata_anime USING gin (((mm_metadata_anime_media_id -> 'thetvdb'::text)));


--
-- TOC entry 3034 (class 1259 OID 17325)
-- Name: mm_metadata_anime_idxgin_media_id_tmdb; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_anime_idxgin_media_id_tmdb ON public.mm_metadata_anime USING gin (((mm_metadata_anime_media_id -> 'tmdb'::text)));


--
-- TOC entry 3035 (class 1259 OID 17326)
-- Name: mm_metadata_anime_idxgin_user_json; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_anime_idxgin_user_json ON public.mm_metadata_anime USING gin (mm_metadata_anime_user_json);


--
-- TOC entry 3038 (class 1259 OID 17327)
-- Name: mm_metadata_book_name_trigram_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_book_name_trigram_idx ON public.mm_metadata_book USING gist (mm_metadata_book_name public.gist_trgm_ops);


--
-- TOC entry 3047 (class 1259 OID 17328)
-- Name: mm_metadata_collection_idxgin_media_json; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_collection_idxgin_media_json ON public.mm_metadata_collection USING gin (mm_metadata_collection_media_ids);


--
-- TOC entry 3048 (class 1259 OID 17329)
-- Name: mm_metadata_collection_idxgin_meta_json; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_collection_idxgin_meta_json ON public.mm_metadata_collection USING gin (mm_metadata_collection_json);


--
-- TOC entry 3049 (class 1259 OID 17330)
-- Name: mm_metadata_collection_idxgin_name_json; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_collection_idxgin_name_json ON public.mm_metadata_collection USING gin (mm_metadata_collection_name);


--
-- TOC entry 3082 (class 1259 OID 17331)
-- Name: mm_metadata_idx_band_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_idx_band_name ON public.mm_metadata_music_video USING btree (mm_media_music_video_band);


--
-- TOC entry 3083 (class 1259 OID 17332)
-- Name: mm_metadata_idx_band_name_lower; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_idx_band_name_lower ON public.mm_metadata_music_video USING btree (lower(mm_media_music_video_band));


--
-- TOC entry 3041 (class 1259 OID 17333)
-- Name: mm_metadata_idx_book_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_idx_book_name ON public.mm_metadata_book USING btree (mm_metadata_book_name);


--
-- TOC entry 3042 (class 1259 OID 17334)
-- Name: mm_metadata_idx_book_name_lower; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_idx_book_name_lower ON public.mm_metadata_book USING btree (lower(mm_metadata_book_name));


--
-- TOC entry 3065 (class 1259 OID 17335)
-- Name: mm_metadata_idx_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_idx_name ON public.mm_metadata_movie USING btree (mm_media_name);


--
-- TOC entry 3066 (class 1259 OID 17336)
-- Name: mm_metadata_idx_name_lower; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_idx_name_lower ON public.mm_metadata_movie USING btree (lower(mm_media_name));


--
-- TOC entry 3084 (class 1259 OID 17337)
-- Name: mm_metadata_idx_song_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_idx_song_name ON public.mm_metadata_music_video USING btree (mm_media_music_video_song);


--
-- TOC entry 3085 (class 1259 OID 17338)
-- Name: mm_metadata_idx_song_name_lower; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_idx_song_name_lower ON public.mm_metadata_music_video USING btree (lower(mm_media_music_video_song));


--
-- TOC entry 3043 (class 1259 OID 17339)
-- Name: mm_metadata_idxgin_isbn; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_idxgin_isbn ON public.mm_metadata_book USING btree (mm_metadata_book_isbn);


--
-- TOC entry 3044 (class 1259 OID 17340)
-- Name: mm_metadata_idxgin_isbn13; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_idxgin_isbn13 ON public.mm_metadata_book USING btree (mm_metadata_book_isbn13);


--
-- TOC entry 3067 (class 1259 OID 17341)
-- Name: mm_metadata_idxgin_json; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_idxgin_json ON public.mm_metadata_movie USING gin (mm_metadata_json);


--
-- TOC entry 3086 (class 1259 OID 17342)
-- Name: mm_metadata_idxgin_music_video_json; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_idxgin_music_video_json ON public.mm_metadata_music_video USING gin (mm_metadata_music_video_json);


--
-- TOC entry 3087 (class 1259 OID 17343)
-- Name: mm_metadata_idxgin_music_video_media_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_idxgin_music_video_media_id ON public.mm_metadata_music_video USING gin (mm_metadata_music_video_media_id);


--
-- TOC entry 3088 (class 1259 OID 17344)
-- Name: mm_metadata_idxgin_music_video_media_id_imvdb; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_idxgin_music_video_media_id_imvdb ON public.mm_metadata_music_video USING gin (((mm_metadata_music_video_media_id -> 'imvdb'::text)));


--
-- TOC entry 3068 (class 1259 OID 17345)
-- Name: mm_metadata_idxgin_user_json; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_idxgin_user_json ON public.mm_metadata_movie USING gin (mm_metadata_user_json);


--
-- TOC entry 3063 (class 1259 OID 17346)
-- Name: mm_metadata_logo_idxgin_json; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_logo_idxgin_json ON public.mm_metadata_logo USING gin (mm_metadata_logo_media_guid);


--
-- TOC entry 3071 (class 1259 OID 17347)
-- Name: mm_metadata_music_idx_album; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_music_idx_album ON public.mm_metadata_music USING btree (mm_metadata_music_album_guid);


--
-- TOC entry 3072 (class 1259 OID 17348)
-- Name: mm_metadata_music_idx_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_music_idx_name ON public.mm_metadata_music USING btree (mm_metadata_music_name);


--
-- TOC entry 3073 (class 1259 OID 17349)
-- Name: mm_metadata_music_idx_name_lower; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_music_idx_name_lower ON public.mm_metadata_music USING btree (lower(mm_metadata_music_name));


--
-- TOC entry 3074 (class 1259 OID 17350)
-- Name: mm_metadata_music_idxgin_json; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_music_idxgin_json ON public.mm_metadata_music USING gin (mm_metadata_music_json);


--
-- TOC entry 3075 (class 1259 OID 17351)
-- Name: mm_metadata_music_idxgin_media_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_music_idxgin_media_id ON public.mm_metadata_music USING gin (mm_metadata_media_music_id);


--
-- TOC entry 3076 (class 1259 OID 17352)
-- Name: mm_metadata_music_idxgin_user_json; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_music_idxgin_user_json ON public.mm_metadata_music USING gin (mm_metadata_music_user_json);


--
-- TOC entry 3077 (class 1259 OID 17353)
-- Name: mm_metadata_music_name_trigram_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_music_name_trigram_idx ON public.mm_metadata_music USING gist (mm_metadata_music_name public.gist_trgm_ops);


--
-- TOC entry 3089 (class 1259 OID 17354)
-- Name: mm_metadata_music_video_idxgin_user_json; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_music_video_idxgin_user_json ON public.mm_metadata_music_video USING gin (mm_metadata_music_video_user_json);


--
-- TOC entry 3092 (class 1259 OID 17355)
-- Name: mm_metadata_musician_idx_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_musician_idx_name ON public.mm_metadata_musician USING btree (mm_metadata_musician_name);


--
-- TOC entry 3093 (class 1259 OID 17356)
-- Name: mm_metadata_musician_idx_name_lower; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_musician_idx_name_lower ON public.mm_metadata_musician USING btree (lower(mm_metadata_musician_name));


--
-- TOC entry 3094 (class 1259 OID 17357)
-- Name: mm_metadata_musician_idxgin_id_json; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_musician_idxgin_id_json ON public.mm_metadata_musician USING gin (mm_metadata_musician_id);


--
-- TOC entry 3095 (class 1259 OID 17358)
-- Name: mm_metadata_musician_idxgin_json; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_musician_idxgin_json ON public.mm_metadata_musician USING gin (mm_metadata_musician_json);


--
-- TOC entry 3096 (class 1259 OID 17359)
-- Name: mm_metadata_musician_name_trigram_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_musician_name_trigram_idx ON public.mm_metadata_musician USING gist (mm_metadata_musician_name public.gist_trgm_ops);


--
-- TOC entry 3099 (class 1259 OID 17361)
-- Name: mm_metadata_person_idx_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_person_idx_id ON public.mm_metadata_person USING btree (mmp_person_media_id);


--
-- TOC entry 3100 (class 1259 OID 17360)
-- Name: mm_metadata_person_idx_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_person_idx_name ON public.mm_metadata_person USING btree (mmp_person_name);


--
-- TOC entry 3101 (class 1259 OID 17362)
-- Name: mm_metadata_person_idxgin_meta_json; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_person_idxgin_meta_json ON public.mm_metadata_person USING gin (mmp_person_meta_json);


--
-- TOC entry 3140 (class 1259 OID 17363)
-- Name: mm_metadata_review_idx_metadata_uuid; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_review_idx_metadata_uuid ON public.mm_review USING btree (mm_review_metadata_guid);


--
-- TOC entry 3141 (class 1259 OID 17364)
-- Name: mm_metadata_review_idxgin_media_json; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_review_idxgin_media_json ON public.mm_review USING gin (mm_review_metadata_id);


--
-- TOC entry 3105 (class 1259 OID 17365)
-- Name: mm_metadata_sports_idx_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_sports_idx_name ON public.mm_metadata_sports USING btree (mm_metadata_sports_name);


--
-- TOC entry 3106 (class 1259 OID 17366)
-- Name: mm_metadata_sports_idx_name_lower; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_sports_idx_name_lower ON public.mm_metadata_sports USING btree (lower(mm_metadata_sports_name));


--
-- TOC entry 3107 (class 1259 OID 17367)
-- Name: mm_metadata_sports_idxgin_json; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_sports_idxgin_json ON public.mm_metadata_sports USING gin (mm_metadata_sports_json);


--
-- TOC entry 3108 (class 1259 OID 17368)
-- Name: mm_metadata_sports_idxgin_media_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_sports_idxgin_media_id ON public.mm_metadata_sports USING gin (mm_metadata_media_sports_id);


--
-- TOC entry 3109 (class 1259 OID 17369)
-- Name: mm_metadata_sports_idxgin_media_id_imdb; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_sports_idxgin_media_id_imdb ON public.mm_metadata_sports USING gin (((mm_metadata_media_sports_id -> 'imdb'::text)));


--
-- TOC entry 3110 (class 1259 OID 17370)
-- Name: mm_metadata_sports_idxgin_media_id_thesportsdb; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_sports_idxgin_media_id_thesportsdb ON public.mm_metadata_sports USING gin (((mm_metadata_media_sports_id -> 'thesportsdb'::text)));


--
-- TOC entry 3111 (class 1259 OID 17371)
-- Name: mm_metadata_sports_idxgin_media_id_thetvdb; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_sports_idxgin_media_id_thetvdb ON public.mm_metadata_sports USING gin (((mm_metadata_media_sports_id -> 'thetvdb'::text)));


--
-- TOC entry 3112 (class 1259 OID 17372)
-- Name: mm_metadata_sports_idxgin_media_id_thetvdbseries; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_sports_idxgin_media_id_thetvdbseries ON public.mm_metadata_sports USING gin (((mm_metadata_media_sports_id -> 'thetvdbSeries'::text)));


--
-- TOC entry 3113 (class 1259 OID 17373)
-- Name: mm_metadata_sports_idxgin_media_id_tmdb; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_sports_idxgin_media_id_tmdb ON public.mm_metadata_sports USING gin (((mm_metadata_media_sports_id -> 'tmdb'::text)));


--
-- TOC entry 3114 (class 1259 OID 17374)
-- Name: mm_metadata_sports_idxgin_media_id_tvmaze; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_sports_idxgin_media_id_tvmaze ON public.mm_metadata_sports USING gin (((mm_metadata_media_sports_id -> 'tvmaze'::text)));


--
-- TOC entry 3115 (class 1259 OID 17375)
-- Name: mm_metadata_sports_name_trigram_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_sports_name_trigram_idx ON public.mm_metadata_sports USING gist (mm_metadata_sports_name public.gist_trgm_ops);


--
-- TOC entry 3118 (class 1259 OID 17376)
-- Name: mm_metadata_tvshow_idx_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_tvshow_idx_name ON public.mm_metadata_tvshow USING btree (mm_metadata_tvshow_name);


--
-- TOC entry 3119 (class 1259 OID 17377)
-- Name: mm_metadata_tvshow_idx_name_lower; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_tvshow_idx_name_lower ON public.mm_metadata_tvshow USING btree (lower(mm_metadata_tvshow_name));


--
-- TOC entry 3120 (class 1259 OID 17378)
-- Name: mm_metadata_tvshow_idxgin_json; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_tvshow_idxgin_json ON public.mm_metadata_tvshow USING gin (mm_metadata_tvshow_json);


--
-- TOC entry 3121 (class 1259 OID 17379)
-- Name: mm_metadata_tvshow_idxgin_localimage_json; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_tvshow_idxgin_localimage_json ON public.mm_metadata_tvshow USING gin (mm_metadata_tvshow_json);


--
-- TOC entry 3122 (class 1259 OID 17380)
-- Name: mm_metadata_tvshow_idxgin_media_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_tvshow_idxgin_media_id ON public.mm_metadata_tvshow USING gin (mm_metadata_media_tvshow_id);


--
-- TOC entry 3123 (class 1259 OID 17381)
-- Name: mm_metadata_tvshow_idxgin_media_id_imdb; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_tvshow_idxgin_media_id_imdb ON public.mm_metadata_tvshow USING gin (((mm_metadata_media_tvshow_id -> 'imdb'::text)));


--
-- TOC entry 3124 (class 1259 OID 17382)
-- Name: mm_metadata_tvshow_idxgin_media_id_thetvdb; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_tvshow_idxgin_media_id_thetvdb ON public.mm_metadata_tvshow USING gin (((mm_metadata_media_tvshow_id -> 'thetvdb'::text)));


--
-- TOC entry 3125 (class 1259 OID 17383)
-- Name: mm_metadata_tvshow_idxgin_media_id_thetvdbseries; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_tvshow_idxgin_media_id_thetvdbseries ON public.mm_metadata_tvshow USING gin (((mm_metadata_media_tvshow_id -> 'thetvdbSeries'::text)));


--
-- TOC entry 3126 (class 1259 OID 17384)
-- Name: mm_metadata_tvshow_idxgin_media_id_tmdb; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_tvshow_idxgin_media_id_tmdb ON public.mm_metadata_tvshow USING gin (((mm_metadata_media_tvshow_id -> 'tmdb'::text)));


--
-- TOC entry 3127 (class 1259 OID 17385)
-- Name: mm_metadata_tvshow_idxgin_media_id_tvmaze; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_tvshow_idxgin_media_id_tvmaze ON public.mm_metadata_tvshow USING gin (((mm_metadata_media_tvshow_id -> 'tvmaze'::text)));


--
-- TOC entry 3128 (class 1259 OID 17386)
-- Name: mm_metadata_tvshow_idxgin_user_json; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_tvshow_idxgin_user_json ON public.mm_metadata_tvshow USING gin (mm_metadata_tvshow_user_json);


--
-- TOC entry 3129 (class 1259 OID 17387)
-- Name: mm_metadata_tvshow_name_trigram_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_tvshow_name_trigram_idx ON public.mm_metadata_tvshow USING gist (mm_metadata_tvshow_name public.gist_trgm_ops);


--
-- TOC entry 3132 (class 1259 OID 17388)
-- Name: mm_notification_idx_dismissable; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_notification_idx_dismissable ON public.mm_notification USING btree (mm_notification_dismissable);


--
-- TOC entry 3133 (class 1259 OID 17389)
-- Name: mm_notification_idx_time; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_notification_idx_time ON public.mm_notification USING btree (mm_notification_time);


--
-- TOC entry 3146 (class 1259 OID 17390)
-- Name: mm_sync_idxgin_json; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_sync_idxgin_json ON public.mm_sync USING gin (mm_sync_options_json);


--
-- TOC entry 3149 (class 1259 OID 17391)
-- Name: mm_tv_schedule_idx_date; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_tv_schedule_idx_date ON public.mm_tv_schedule USING btree (mm_tv_schedule_date);


--
-- TOC entry 3151 (class 1259 OID 17392)
-- Name: mm_tv_schedule_idx_program; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_tv_schedule_idx_program ON public.mm_tv_schedule_program USING btree (mm_tv_schedule_program_id);


--
-- TOC entry 3150 (class 1259 OID 17393)
-- Name: mm_tv_schedule_idx_station; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_tv_schedule_idx_station ON public.mm_tv_schedule USING btree (mm_tv_schedule_station_id);


--
-- TOC entry 3156 (class 1259 OID 17394)
-- Name: mm_tv_stations_idx_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_tv_stations_idx_name ON public.mm_tv_stations USING btree (mm_tv_station_name);


--
-- TOC entry 3157 (class 1259 OID 17395)
-- Name: mm_tv_stations_idx_station; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_tv_stations_idx_station ON public.mm_tv_stations USING btree (mm_tv_station_id);


--
-- TOC entry 3163 (class 1259 OID 17396)
-- Name: mm_user_activity_idx_date; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_user_activity_idx_date ON public.mm_user_activity USING btree (mm_activity_datecreated);


--
-- TOC entry 3164 (class 1259 OID 17397)
-- Name: mm_user_activity_idx_user_guid; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_user_activity_idx_user_guid ON public.mm_user_activity USING btree (mm_activity_userid);


--
-- TOC entry 3167 (class 1259 OID 17398)
-- Name: mm_user_group_idx_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_user_group_idx_name ON public.mm_user_group USING btree (mm_user_group_name);


--
-- TOC entry 3158 (class 1259 OID 17399)
-- Name: mm_user_idx_username; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_user_idx_username ON public.mm_user USING btree (username);


--
-- TOC entry 3170 (class 1259 OID 17400)
-- Name: mm_user_profile_idx_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_user_profile_idx_name ON public.mm_user_profile USING btree (mm_user_profile_name);


--
-- TOC entry 3176 (class 1259 OID 17425)
-- Name: mm_user_queue_media_type_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_user_queue_media_type_idx ON public.mm_user_queue USING btree (mm_user_queue_media_type);


--
-- TOC entry 3177 (class 1259 OID 17423)
-- Name: mm_user_queue_name_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_user_queue_name_idx ON public.mm_user_queue USING btree (mm_user_queue_name);


--
-- TOC entry 3178 (class 1259 OID 17424)
-- Name: mm_user_queue_user_id_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_user_queue_user_id_idx ON public.mm_user_queue USING btree (mm_user_queue_user_id);


--
-- TOC entry 3104 (class 1259 OID 17401)
-- Name: mmp_person_name_trigram_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mmp_person_name_trigram_idx ON public.mm_metadata_person USING gist (mmp_person_name public.gist_trgm_ops);


--
-- TOC entry 3011 (class 1259 OID 17402)
-- Name: mmr_media_idx_link_uuid; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mmr_media_idx_link_uuid ON public.mm_media_remote USING btree (mmr_media_link_id);


--
-- TOC entry 3012 (class 1259 OID 17403)
-- Name: mmr_media_idx_metadata_uuid; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mmr_media_idx_metadata_uuid ON public.mm_media_remote USING btree (mmr_media_metadata_guid);


--
-- TOC entry 3013 (class 1259 OID 17404)
-- Name: mmr_media_idxgin_ffprobe; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mmr_media_idxgin_ffprobe ON public.mm_media_remote USING gin (mmr_media_ffprobe_json);


-- Completed on 2020-08-18 19:58:06

--
-- PostgreSQL database dump complete
--

