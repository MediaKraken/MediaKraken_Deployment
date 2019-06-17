--
-- PostgreSQL database dump
--

-- Dumped from database version 10.3
-- Dumped by pg_dump version 10.3

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


--
-- Name: pg_trgm; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS pg_trgm WITH SCHEMA public;


--
-- Name: EXTENSION pg_trgm; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION pg_trgm IS 'text similarity measurement and index searching based on trigrams';


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: mm_channel; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE public.mm_channel (
    mm_channel_guid uuid NOT NULL,
    mm_channel_name text,
    mm_channel_media_id jsonb,
    mm_channel_country_guid uuid,
    mm_channel_logo_guid uuid
);


ALTER TABLE public.mm_channel OWNER TO metamanpg;

--
-- Name: mm_cron; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE public.mm_cron (
    mm_cron_guid uuid NOT NULL,
    mm_cron_name text,
    mm_cron_description text,
    mm_cron_enabled boolean,
    mm_cron_schedule text,
    mm_cron_last_run timestamp without time zone,
    mm_cron_file_path text,
    mm_cron_json jsonb
);


ALTER TABLE public.mm_cron OWNER TO metamanpg;

--
-- Name: mm_device; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE public.mm_device (
    mm_device_id uuid NOT NULL,
    mm_device_type text,
    mm_device_json jsonb
);


ALTER TABLE public.mm_device OWNER TO metamanpg;

--
-- Name: mm_download_que; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE public.mm_download_que (
    mdq_id uuid NOT NULL,
    mdq_provider text,
    mdq_que_type smallint,
    mdq_download_json jsonb
);


ALTER TABLE public.mm_download_que OWNER TO metamanpg;

--
-- Name: mm_game_category; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE public.mm_game_category (
    gc_id uuid NOT NULL,
    gc_category text
);


ALTER TABLE public.mm_game_category OWNER TO metamanpg;

--
-- Name: mm_hardware; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE public.mm_hardware (
    mm_hardware_id uuid NOT NULL,
    mm_hardware_manufacturer text,
    mm_hardware_model text,
    mm_hardware_json jsonb
);


ALTER TABLE public.mm_hardware OWNER TO metamanpg;

--
-- Name: mm_link; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE public.mm_link (
    mm_link_guid uuid NOT NULL,
    mm_link_name text,
    mm_link_json jsonb
);


ALTER TABLE public.mm_link OWNER TO metamanpg;

--
-- Name: mm_loan; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE public.mm_loan (
    mm_loan_guid uuid NOT NULL,
    mm_loan_media_id uuid,
    mm_loan_user_id uuid,
    mm_load_user_loan_id uuid,
    mm_loan_time timestamp without time zone,
    mm_loan_return_time timestamp without time zone
);


ALTER TABLE public.mm_loan OWNER TO metamanpg;

--
-- Name: mm_media; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE public.mm_media (
    mm_media_guid uuid NOT NULL,
    mm_media_class_guid uuid,
    mm_media_metadata_guid uuid,
    mm_media_path text,
    mm_media_ffprobe_json jsonb,
    mm_media_json jsonb
);


ALTER TABLE public.mm_media OWNER TO metamanpg;

--
-- Name: mm_media_class; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE public.mm_media_class (
    mm_media_class_guid uuid NOT NULL,
    mm_media_class_type text,
    mm_media_class_parent_type text,
    mm_media_class_display boolean
);


ALTER TABLE public.mm_media_class OWNER TO metamanpg;

--
-- Name: mm_media_dir; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE public.mm_media_dir (
    mm_media_dir_guid uuid NOT NULL,
    mm_media_dir_path text,
    mm_media_dir_class_type uuid,
    mm_media_dir_last_scanned timestamp without time zone,
    mm_media_dir_share_guid uuid,
    mm_media_dir_status jsonb
);


ALTER TABLE public.mm_media_dir OWNER TO metamanpg;

--
-- Name: mm_media_remote; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE public.mm_media_remote (
    mmr_media_guid uuid NOT NULL,
    mmr_media_link_id uuid,
    mmr_media_uuid uuid,
    mmr_media_class_guid uuid,
    mmr_media_metadata_guid uuid,
    mmr_media_ffprobe_json jsonb,
    mmr_media_json jsonb
);


ALTER TABLE public.mm_media_remote OWNER TO metamanpg;

--
-- Name: mm_media_share; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE public.mm_media_share (
    mm_media_share_guid uuid NOT NULL,
    mm_media_share_type text,
    mm_media_share_user text,
    mm_media_share_password text,
    mm_media_share_server text,
    mm_media_share_path text
);


ALTER TABLE public.mm_media_share OWNER TO metamanpg;

--
-- Name: mm_metadata_album; Type: TABLE; Schema: public; Owner: metamanpg
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


ALTER TABLE public.mm_metadata_album OWNER TO metamanpg;

--
-- Name: mm_metadata_anime; Type: TABLE; Schema: public; Owner: metamanpg
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


ALTER TABLE public.mm_metadata_anime OWNER TO metamanpg;

--
-- Name: mm_metadata_book; Type: TABLE; Schema: public; Owner: metamanpg
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


ALTER TABLE public.mm_metadata_book OWNER TO metamanpg;

--
-- Name: mm_metadata_collection; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE public.mm_metadata_collection (
    mm_metadata_collection_guid uuid NOT NULL,
    mm_metadata_collection_name jsonb,
    mm_metadata_collection_media_ids jsonb,
    mm_metadata_collection_json jsonb,
    mm_metadata_collection_imagelocal_json jsonb
);


ALTER TABLE public.mm_metadata_collection OWNER TO metamanpg;

--
-- Name: mm_metadata_game_software_info; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE public.mm_metadata_game_software_info (
    gi_id uuid NOT NULL,
    gi_system_id uuid,
    gi_game_info_short_name text,
    gi_game_info_name text,
    gi_game_info_json jsonb
);


ALTER TABLE public.mm_metadata_game_software_info OWNER TO metamanpg;

--
-- Name: mm_metadata_game_systems_info; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE public.mm_metadata_game_systems_info (
    gs_id uuid NOT NULL,
    gs_game_system_name text,
    gs_game_system_alias text,
    gs_game_system_json jsonb,
    mm_metadata_localimage_json jsonb
);


ALTER TABLE public.mm_metadata_game_systems_info OWNER TO metamanpg;

--
-- Name: mm_metadata_logo; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE public.mm_metadata_logo (
    mm_metadata_logo_guid uuid NOT NULL,
    mm_metadata_logo_media_guid jsonb,
    mm_metadata_logo_image_path text
);


ALTER TABLE public.mm_metadata_logo OWNER TO metamanpg;

--
-- Name: mm_metadata_movie; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE public.mm_metadata_movie (
    mm_metadata_guid uuid NOT NULL,
    mm_metadata_media_id jsonb,
    mm_media_name text,
    mm_metadata_json jsonb,
    mm_metadata_localimage_json jsonb,
    mm_metadata_user_json jsonb
);


ALTER TABLE public.mm_metadata_movie OWNER TO metamanpg;

--
-- Name: mm_metadata_music; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE public.mm_metadata_music (
    mm_metadata_music_guid uuid NOT NULL,
    mm_metadata_media_music_id jsonb,
    mm_metadata_music_name text,
    mm_metadata_music_json jsonb,
    mm_metadata_music_album_guid uuid,
    mm_metadata_music_user_json jsonb
);


ALTER TABLE public.mm_metadata_music OWNER TO metamanpg;

--
-- Name: mm_metadata_music_video; Type: TABLE; Schema: public; Owner: metamanpg
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


ALTER TABLE public.mm_metadata_music_video OWNER TO metamanpg;

--
-- Name: mm_metadata_musician; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE public.mm_metadata_musician (
    mm_metadata_musician_guid uuid NOT NULL,
    mm_metadata_musician_name text,
    mm_metadata_musician_id jsonb,
    mm_metadata_musician_json jsonb,
    mm_metadata_musician_localimage_json jsonb
);


ALTER TABLE public.mm_metadata_musician OWNER TO metamanpg;

--
-- Name: mm_metadata_person; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE public.mm_metadata_person (
    mmp_id uuid NOT NULL,
    mmp_person_media_id jsonb,
    mmp_person_meta_json jsonb,
    mmp_person_image jsonb,
    mmp_person_name text
);


ALTER TABLE public.mm_metadata_person OWNER TO metamanpg;

--
-- Name: mm_metadata_sports; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE public.mm_metadata_sports (
    mm_metadata_sports_guid uuid NOT NULL,
    mm_metadata_media_sports_id jsonb,
    mm_metadata_sports_name text,
    mm_metadata_sports_json jsonb,
    mm_metadata_sports_user_json jsonb,
    mm_metadata_sports_image_json jsonb
);


ALTER TABLE public.mm_metadata_sports OWNER TO metamanpg;

--
-- Name: mm_metadata_tvshow; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE public.mm_metadata_tvshow (
    mm_metadata_tvshow_guid uuid NOT NULL,
    mm_metadata_media_tvshow_id jsonb,
    mm_metadata_tvshow_name text,
    mm_metadata_tvshow_json jsonb,
    mm_metadata_tvshow_localimage_json jsonb,
    mm_metadata_tvshow_user_json jsonb
);


ALTER TABLE public.mm_metadata_tvshow OWNER TO metamanpg;

--
-- Name: mm_notification; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE public.mm_notification (
    mm_notification_guid uuid NOT NULL,
    mm_notification_text text,
    mm_notification_time timestamp without time zone,
    mm_notification_dismissable boolean
);


ALTER TABLE public.mm_notification OWNER TO metamanpg;

--
-- Name: mm_options_and_status; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE public.mm_options_and_status (
    mm_options_and_status_guid uuid NOT NULL,
    mm_options_json jsonb,
    mm_status_json jsonb
);


ALTER TABLE public.mm_options_and_status OWNER TO metamanpg;

--
-- Name: mm_radio; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE public.mm_radio (
    mm_radio_guid uuid NOT NULL,
    mm_radio_name text,
    mm_radio_adress text,
    mm_radio_active boolean
);


ALTER TABLE public.mm_radio OWNER TO metamanpg;

--
-- Name: mm_review; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE public.mm_review (
    mm_review_guid uuid NOT NULL,
    mm_review_metadata_id jsonb,
    mm_review_metadata_guid uuid,
    mm_review_json jsonb
);


ALTER TABLE public.mm_review OWNER TO metamanpg;

--
-- Name: mm_sync; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE public.mm_sync (
    mm_sync_guid uuid NOT NULL,
    mm_sync_path text,
    mm_sync_path_to text,
    mm_sync_options_json jsonb
);


ALTER TABLE public.mm_sync OWNER TO metamanpg;


--
-- Name: mm_tv_schedule; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE public.mm_tv_schedule (
    mm_tv_schedule_id uuid NOT NULL,
    mm_tv_schedule_station_id text,
    mm_tv_schedule_date date,
    mm_tv_schedule_json jsonb
);


ALTER TABLE public.mm_tv_schedule OWNER TO metamanpg;

--
-- Name: mm_tv_schedule_program; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE public.mm_tv_schedule_program (
    mm_tv_schedule_program_guid uuid NOT NULL,
    mm_tv_schedule_program_id text,
    mm_tv_schedule_program_json jsonb
);


ALTER TABLE public.mm_tv_schedule_program OWNER TO metamanpg;

--
-- Name: mm_tv_stations; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE public.mm_tv_stations (
    mm_tv_stations_id uuid NOT NULL,
    mm_tv_station_name text,
    mm_tv_station_id text,
    mm_tv_station_channel text,
    mm_tv_station_json jsonb,
    mm_tv_station_image text
);


ALTER TABLE public.mm_tv_stations OWNER TO metamanpg;

--
-- Name: mm_user; Type: TABLE; Schema: public; Owner: metamanpg
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


ALTER TABLE public.mm_user OWNER TO metamanpg;

--
-- Name: mm_user_activity; Type: TABLE; Schema: public; Owner: metamanpg
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


ALTER TABLE public.mm_user_activity OWNER TO metamanpg;

--
-- Name: mm_user_group; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE public.mm_user_group (
    mm_user_group_guid uuid NOT NULL,
    mm_user_group_name text,
    mm_user_group_description text,
    mm_user_group_rights_json jsonb
);


ALTER TABLE public.mm_user_group OWNER TO metamanpg;

--
-- Name: mm_user_id_seq; Type: SEQUENCE; Schema: public; Owner: metamanpg
--

CREATE SEQUENCE public.mm_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.mm_user_id_seq OWNER TO metamanpg;

--
-- Name: mm_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: metamanpg
--

ALTER SEQUENCE public.mm_user_id_seq OWNED BY public.mm_user.id;


--
-- Name: mm_user_profile; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE public.mm_user_profile (
    mm_user_profile_guid uuid NOT NULL,
    mm_user_profile_name text,
    mm_user_profile_json jsonb
);


ALTER TABLE public.mm_user_profile OWNER TO metamanpg;

--
-- Name: mm_version; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE public.mm_version (
    mm_version_no integer
);


ALTER TABLE public.mm_version OWNER TO metamanpg;

--
-- Name: mm_user id; Type: DEFAULT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY public.mm_user ALTER COLUMN id SET DEFAULT nextval('public.mm_user_id_seq'::regclass);


--
-- Data for Name: mm_channel; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY public.mm_channel (mm_channel_guid, mm_channel_name, mm_channel_media_id, mm_channel_country_guid, mm_channel_logo_guid) FROM stdin;
\.


--
-- Data for Name: mm_cron; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY public.mm_cron (mm_cron_guid, mm_cron_name, mm_cron_description, mm_cron_enabled, mm_cron_schedule, mm_cron_last_run, mm_cron_file_path, mm_cron_json) FROM stdin;
cbb42a96-f95f-4616-a0bb-e635e7b6d9ca	Anime	Match anime via Scudlee data	f	Days 1	1970-01-01 00:00:01	/mediakraken/subprogram_match_anime_id_scudlee.py	{"task": "anime", "route_key": "Z", "exchange_key": "mkque_metadata_ex"}
00bcb1b1-7f16-4e90-8c55-77ce4c1ac86a	Collections	Create and update collection(s)	f	Days 1	1970-01-01 00:00:01	/mediakraken/subprogram_metadata_update_create_collections.py	{"task": "collection", "route_key": "themoviedb", "exchange_key": "mkque_metadata_ex"}
7be16469-e0e5-44fd-8727-90ec21cae1c4	Schedules Direct	Fetch TV schedules from Schedules Direct	f	Days 1	1970-01-01 00:00:01	/mediakraken/subprogram_schedules_direct_updates.py	{"task": "update", "route_key": "schedulesdirect", "exchange_key": "mkque_metadata_ex"}
7831b403-408b-49db-8658-f565af581245	The Movie Database	Grab updated metadata for movie(s) and TV show(s)	f	Days 1	1970-01-01 00:00:01	/mediakraken/subprogram_metadata_tmdb_updates.py	{"task": "update", "route_key": "themoviedb", "exchange_key": "mkque_metadata_ex"}
de9b4b9b-8cd2-482a-bfa1-14c298f27aef	Trailer	Download new trailers	f	Days 1	1970-01-01 00:00:01	/mediakraken/subprogram_metadata_trailer_download.py	{"task": "trailer", "route_key": "Z", "exchange_key": "mkque_metadata_ex"}
950ec436-d010-44fb-a653-ef019bf05cc4	Backup	Backup Postgresql DB	f	Days 1	1970-01-01 00:00:01	/mediakraken/subprogram_postgresql_backup.py	{"task": "dbbackup", "route_key": "mkque", "exchange_key": "mkque_ex"}
ac093b30-f4ff-4e97-bb08-8ebb2b1e38d5	DB Vacuum	Postgresql Vacuum Analyze all tables	f	Days 1	1970-01-01 00:00:01	/mediakraken/subprogram_postgresql_vacuum.py	{"task": "dbvacuum", "route_key": "mkque", "exchange_key": "mkque_ex"}
4974d078-cab7-4e37-8922-2a2c2202fb33	Media Scan	Scan for new media	f	Days 1	1970-01-01 00:00:01	/mediakraken/subprogram_file_scan.py	{"task": "scan", "route_key": "mkque", "exchange_key": "mkque_ex"}
144feb59-e15c-491c-8eb9-3a81cc62febe	Sync	Sync/Transcode media	f	Days 1	1970-01-01 00:00:01	/mediakraken/subprogram_sync.py	{"task": "sync", "route_key": "mkque", "exchange_key": "mkque_ex"}
\.


--
-- Data for Name: mm_device; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY public.mm_device (mm_device_id, mm_device_type, mm_device_json) FROM stdin;
\.


--
-- Data for Name: mm_download_que; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY public.mm_download_que (mdq_id, mdq_provider, mdq_que_type, mdq_download_json) FROM stdin;
\.


--
-- Data for Name: mm_game_category; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY public.mm_game_category (gc_id, gc_category) FROM stdin;
\.


--
-- Data for Name: mm_hardware; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY public.mm_hardware (mm_hardware_id, mm_hardware_manufacturer, mm_hardware_model, mm_hardware_json) FROM stdin;
\.


--
-- Data for Name: mm_link; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY public.mm_link (mm_link_guid, mm_link_name, mm_link_json) FROM stdin;
\.


--
-- Data for Name: mm_loan; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY public.mm_loan (mm_loan_guid, mm_loan_media_id, mm_loan_user_id, mm_load_user_loan_id, mm_loan_time, mm_loan_return_time) FROM stdin;
\.


--
-- Data for Name: mm_media; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY public.mm_media (mm_media_guid, mm_media_class_guid, mm_media_metadata_guid, mm_media_path, mm_media_ffprobe_json, mm_media_json) FROM stdin;
\.


--
-- Data for Name: mm_media_class; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY public.mm_media_class (mm_media_class_guid, mm_media_class_type, mm_media_class_parent_type, mm_media_class_display) FROM stdin;
f7354910-02fc-455d-bdb5-361bf42e794c	Adult	Video	t
e8ad8398-70be-483b-b0b9-abe8b8d7de2d	Anime	Video	t
852bc096-20ea-4af7-a5a1-4be735c3b1ab	Book	Publication	t
fd8387da-9d93-4554-be9d-d26e52832ff3	Boxset	\N	f
f75c3b31-0d48-47eb-b66b-670aef07777b	Comic	Publication	t
9dd3946f-a499-4f50-af77-b637f159ce66	Comic Strip	Publication	t
9ba7e24a-ed4e-42c6-b667-e3179d2e71cb	Game CHD	\N	f
f08b3310-b4a6-4e17-9ab9-74dfd0c71ca0	Game ISO	\N	f
0ad11426-e4a2-421b-a438-0ff820e4c864	Game ROM	\N	f
359cd32d-362b-4130-abb9-c1c1debf86cc	Home Movie	Video	t
f0658749-4aa0-4fa1-8359-fac51106635d	Magazine	Publication	t
8b40abac-a071-48bc-b1f9-5b678dcc934c	Movie	Video	t
c53138ee-ab7c-40b9-b86e-d3eed7a26cc1	Movie Extras	Video	f
d7631d4c-4e3d-4e09-866e-cd26d6c42fab	Movie Collection	\N	f
eefee9fe-10ac-4ecd-899a-0cb162c67b6f	Movie Theme	Audio	f
1481b6c9-8f68-4da1-8deb-19d5257035f1	Movie Subtitle	\N	f
84742b9a-3870-418d-9bbd-4a1d7a3056c8	Movie Trailer	Video	f
da762d3e-12b8-48a2-a214-647e76453316	Music	Audio	t
493431f2-5f65-49cb-bb23-dbc20c906481	Music Album	\N	f
d79edbb5-0c7c-46c1-96c4-128bea0af90b	Music Collection	\N	f
7284c348-1f47-4d11-813a-bba08ef6b21b	Music Lyric	\N	f
e0175eb1-b00d-438a-ad5c-8e23a2cc71c9	Music Video	Video	t
1f187b8d-72fb-4bce-b809-01d6482a149e	Person	\N	f
b6661e75-4474-44b3-b379-dde721daa31d	Picture	Image	t
ba02ae59-6d4f-46f8-97a5-dd6e31d7676c	Soundtrack	Audio	f
b118f082-8771-4ac3-b645-96d9b8d6bad4	Sports	Video	t
f57d4cdb-7aff-45f0-9235-3f9c8b57842c	Subtitle	\N	f
f3dc966d-2056-4ba7-8342-54191bb92117	TV Episode	Video	f
4862b282-3130-430a-84de-cc47ec6caae4	TV Extras	Video	f
c11a9cb5-6dda-455a-8f63-e94be3998042	TV Season	\N	f
c62e715c-e35e-4907-a3c5-b7e9ca6f2333	TV Show	Video	t
d4dea663-25f2-4c25-8f3b-5f68eb49d2f1	TV Subtitle	\N	f
274f00a5-f058-41dd-a17a-dec9bcc18891	TV Theme	Audio	f
a359aad3-7a95-4b9f-9050-aa09be35c326	TV Trailer	Video	f
7c889c86-5eef-48cf-b840-2b56bee4b86b	Video Game	Game	t
30ba9f85-51dc-49ad-a471-964575adf72c	Video Game Intro	Video	t
02a162d2-194d-4ca8-8c8c-8167282d1c67	Video Game Speedrun	Video	t
2e6bc294-eff4-40b9-8e94-e328ae4ab553	Video Game Superplay	Video	t
\.


--
-- Data for Name: mm_media_dir; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY public.mm_media_dir (mm_media_dir_guid, mm_media_dir_path, mm_media_dir_class_type, mm_media_dir_last_scanned, mm_media_dir_share_guid, mm_media_dir_status) FROM stdin;
\.


--
-- Data for Name: mm_media_remote; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY public.mm_media_remote (mmr_media_guid, mmr_media_link_id, mmr_media_uuid, mmr_media_class_guid, mmr_media_metadata_guid, mmr_media_ffprobe_json, mmr_media_json) FROM stdin;
\.


--
-- Data for Name: mm_media_share; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY public.mm_media_share (mm_media_share_guid, mm_media_share_type, mm_media_share_user, mm_media_share_password, mm_media_share_server, mm_media_share_path) FROM stdin;
\.


--
-- Data for Name: mm_metadata_album; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY public.mm_metadata_album (mm_metadata_album_guid, mm_metadata_album_name, mm_metadata_album_id, mm_metadata_album_json, mm_metadata_album_musician_guid, mm_metadata_album_user_json, mm_metadata_album_localimage) FROM stdin;
\.


--
-- Data for Name: mm_metadata_anime; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY public.mm_metadata_anime (mm_metadata_anime_guid, mm_metadata_anime_media_id, mm_media_anime_name, mm_metadata_anime_json, mm_metadata_anime_mapping, mm_metadata_anime_mapping_before, mm_metadata_anime_localimage_json, mm_metadata_anime_user_json) FROM stdin;
\.


--
-- Data for Name: mm_metadata_book; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY public.mm_metadata_book (mm_metadata_book_guid, mm_metadata_book_isbn, mm_metadata_book_isbn13, mm_metadata_book_name, mm_metadata_book_json, mm_metadata_book_user_json, mm_metadata_book_localimage_json) FROM stdin;
\.


--
-- Data for Name: mm_metadata_collection; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY public.mm_metadata_collection (mm_metadata_collection_guid, mm_metadata_collection_name, mm_metadata_collection_media_ids, mm_metadata_collection_json, mm_metadata_collection_imagelocal_json) FROM stdin;
\.


--
-- Data for Name: mm_metadata_game_software_info; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY public.mm_metadata_game_software_info (gi_id, gi_system_id, gi_game_info_short_name, gi_game_info_name, gi_game_info_json) FROM stdin;
\.


--
-- Data for Name: mm_metadata_game_systems_info; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY public.mm_metadata_game_systems_info (gs_id, gs_game_system_name, gs_game_system_alias, gs_game_system_json, mm_metadata_localimage_json) FROM stdin;
\.


--
-- Data for Name: mm_metadata_logo; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY public.mm_metadata_logo (mm_metadata_logo_guid, mm_metadata_logo_media_guid, mm_metadata_logo_image_path) FROM stdin;
\.


--
-- Data for Name: mm_metadata_movie; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY public.mm_metadata_movie (mm_metadata_guid, mm_metadata_media_id, mm_media_name, mm_metadata_json, mm_metadata_localimage_json, mm_metadata_user_json) FROM stdin;
\.


--
-- Data for Name: mm_metadata_music; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY public.mm_metadata_music (mm_metadata_music_guid, mm_metadata_media_music_id, mm_metadata_music_name, mm_metadata_music_json, mm_metadata_music_album_guid, mm_metadata_music_user_json) FROM stdin;
\.


--
-- Data for Name: mm_metadata_music_video; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY public.mm_metadata_music_video (mm_metadata_music_video_guid, mm_metadata_music_video_media_id, mm_media_music_video_band, mm_media_music_video_song, mm_metadata_music_video_json, mm_metadata_music_video_localimage_json, mm_metadata_music_video_user_json) FROM stdin;
\.


--
-- Data for Name: mm_metadata_musician; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY public.mm_metadata_musician (mm_metadata_musician_guid, mm_metadata_musician_name, mm_metadata_musician_id, mm_metadata_musician_json, mm_metadata_musician_localimage_json) FROM stdin;
\.


--
-- Data for Name: mm_metadata_person; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY public.mm_metadata_person (mmp_id, mmp_person_media_id, mmp_person_meta_json, mmp_person_image, mmp_person_name) FROM stdin;
\.


--
-- Data for Name: mm_metadata_sports; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY public.mm_metadata_sports (mm_metadata_sports_guid, mm_metadata_media_sports_id, mm_metadata_sports_name, mm_metadata_sports_json, mm_metadata_sports_user_json, mm_metadata_sports_image_json) FROM stdin;
\.


--
-- Data for Name: mm_metadata_tvshow; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY public.mm_metadata_tvshow (mm_metadata_tvshow_guid, mm_metadata_media_tvshow_id, mm_metadata_tvshow_name, mm_metadata_tvshow_json, mm_metadata_tvshow_localimage_json, mm_metadata_tvshow_user_json) FROM stdin;
\.


--
-- Data for Name: mm_notification; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY public.mm_notification (mm_notification_guid, mm_notification_text, mm_notification_time, mm_notification_dismissable) FROM stdin;
\.


--
-- Data for Name: mm_options_and_status; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY public.mm_options_and_status (mm_options_and_status_guid, mm_options_json, mm_status_json) FROM stdin;
62b7e775-8e3e-4eda-8eb4-60d991a03833	{"SD": {"User": null, "Password": null}, "API": {"anidb": null, "imvdb": null, "dirble": "184709fc95ff6c4dacf841eb14", "google": "AIzaSyCwMkNYp8E4H19BDzlM7-IDkNCQtw0R9lY", "isbndb": "25C8IT4I", "tvmaze": "mknotneeded", "thetvdb": "147CB43DCA8B61B7", "shoutcast": null, "thelogodb": null, "soundcloud": null, "themoviedb": "f72118d1e84b8a1438935972a9c37cac", "globalcache": null, "musicbrainz": null, "thesportsdb": "4352761817344", "opensubtitles": null, "openweathermap": "575b4ae4615e4e2a4c34fb9defa17ceb", "rottentomatoes": "f4tnu5dn9r7f28gjth3ftqaj"}, "User": {"Password Lock": null, "Activity Purge": null}, "AWSS3": {"Bucket": "mediakraken", "AccessKey": null, "BackupBucket": "mkbackup", "SecretAccessKey": null}, "Trakt": {"ClientID": null, "OAuth": null}, "Twitch": {"ApiKey": null, "ClientID": null, "SecretKey": null}, "Backup": {"Interval": 0, "BackupType": "local"}, "Docker": {"Nodes": 0, "SwarmID": null, "Instances": 0}, "LastFM": {"api_key": null, "password": null, "username": null, "api_secret": null}, "Metadata": {"MetadataImageLocal": false, "DL Subtitle": false, "Trailer": {"Clip": false, "Behind": false, "Carpool": false, "Trailer": false, "Featurette": false}, "MusicBrainz": {"Host": null, "Port": 5000, "User": null, "Password": null, "BrainzDBHost": null, "BrainzDBName": null, "BrainzDBPass": null, "BrainzDBPort": 5432, "BrainzDBUser": null}}, "MaxResumePct": 5, "Transmission": {"Host": null, "Port": 9091, "Password": "metaman", "Username": "spootdev"}, "Docker Instances": {"smtp": false, "mumble": false, "pgadmin": false, "portainer": false, "teamspeak": false, "wireshark": false, "musicbrainz": false, "transmission": false}, "MediaKrakenServer": {"MOTD": null, "BackupLocal": "/mediakraken/backups/", "Server Name": "MediaKraken"}}	{"thetvdb_Updated_Epoc": 0}
\.


--
-- Data for Name: mm_radio; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY public.mm_radio (mm_radio_guid, mm_radio_name, mm_radio_adress, mm_radio_active) FROM stdin;
\.


--
-- Data for Name: mm_review; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY public.mm_review (mm_review_guid, mm_review_metadata_id, mm_review_metadata_guid, mm_review_json) FROM stdin;
\.


--
-- Data for Name: mm_sync; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY public.mm_sync (mm_sync_guid, mm_sync_path, mm_sync_path_to, mm_sync_options_json) FROM stdin;
\.


--
-- Data for Name: mm_tv_schedule; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY public.mm_tv_schedule (mm_tv_schedule_id, mm_tv_schedule_station_id, mm_tv_schedule_date, mm_tv_schedule_json) FROM stdin;
\.


--
-- Data for Name: mm_tv_schedule_program; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY public.mm_tv_schedule_program (mm_tv_schedule_program_guid, mm_tv_schedule_program_id, mm_tv_schedule_program_json) FROM stdin;
\.


--
-- Data for Name: mm_tv_stations; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY public.mm_tv_stations (mm_tv_stations_id, mm_tv_station_name, mm_tv_station_id, mm_tv_station_channel, mm_tv_station_json, mm_tv_station_image) FROM stdin;
\.


--
-- Data for Name: mm_user; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY public.mm_user (id, username, email, password, created_at, active, is_admin, user_json, lang) FROM stdin;
\.


--
-- Data for Name: mm_user_activity; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY public.mm_user_activity (mm_activity_guid, mm_activity_name, mm_activity_overview, mm_activity_short_overview, mm_activity_type, mm_activity_itemid, mm_activity_userid, mm_activity_datecreated, mm_activity_log_severity) FROM stdin;
\.


--
-- Data for Name: mm_user_group; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY public.mm_user_group (mm_user_group_guid, mm_user_group_name, mm_user_group_description, mm_user_group_rights_json) FROM stdin;
43245db5-e3f2-4d2f-afaf-95d3847555b0	Administrator	Server administrator	{"Admin": true, "PreviewOnly": false}
34099a51-d3eb-4c5b-9257-68fe8b7c3b62	User	General user	{"Admin": false, "PreviewOnly": false}
4067a224-3c9a-42d8-8096-8ab6c950a8ff	Guest	Guest (Preview only)	{"Admin": false, "PreviewOnly": true}
\.


--
-- Data for Name: mm_user_profile; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY public.mm_user_profile (mm_user_profile_guid, mm_user_profile_name, mm_user_profile_json) FROM stdin;
34f122f3-2fa7-4b7a-a485-1f201ef02f8b	Adult	{"3D": true, "TV": true, "Home": true, "Lang": "en", "Sync": true, "Adult": true, "Books": true, "Games": true, "MaxBR": 100, "Movie": true, "Music": true, "IRadio": true, "Images": true, "LiveTV": true, "Sports": true, "Internet": true, "MaxRating": 5}
5ad879a3-4c57-411a-9983-eaecf1473c9c	Teen	{"3D": true, "TV": true, "Home": true, "Lang": "en", "Sync": false, "Adult": false, "Books": true, "Games": true, "MaxBR": 50, "Movie": true, "Music": true, "IRadio": true, "Images": true, "LiveTV": true, "Sports": true, "Internet": true, "MaxRating": 3}
ae303673-9a39-45ee-a761-e18c3a9d027e	Child	{"3D": false, "TV": true, "Home": true, "Lang": "en", "Sync": false, "Adult": false, "Books": true, "Games": true, "MaxBR": 20, "Movie": true, "Music": true, "IRadio": false, "Images": true, "LiveTV": false, "Sports": true, "Internet": false, "MaxRating": 0}
\.


--
-- Data for Name: mm_version; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY public.mm_version (mm_version_no) FROM stdin;
21
\.


--
-- Name: mm_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: metamanpg
--

SELECT pg_catalog.setval('public.mm_user_id_seq', 1, false);


--
-- Name: mm_game_category gc_id_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY public.mm_game_category
    ADD CONSTRAINT gc_id_pk PRIMARY KEY (gc_id);


--
-- Name: mm_metadata_game_software_info gi_id_mpk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY public.mm_metadata_game_software_info
    ADD CONSTRAINT gi_id_mpk PRIMARY KEY (gi_id);


--
-- Name: mm_metadata_game_systems_info gs_id_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY public.mm_metadata_game_systems_info
    ADD CONSTRAINT gs_id_pk PRIMARY KEY (gs_id);


--
-- Name: mm_download_que mdq_id_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY public.mm_download_que
    ADD CONSTRAINT mdq_id_pk PRIMARY KEY (mdq_id);


--
-- Name: mm_user_activity mm_activity_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY public.mm_user_activity
    ADD CONSTRAINT mm_activity_pk PRIMARY KEY (mm_activity_guid);


--
-- Name: mm_channel mm_channel_guid_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY public.mm_channel
    ADD CONSTRAINT mm_channel_guid_pk PRIMARY KEY (mm_channel_guid);


--
-- Name: mm_cron mm_cron_guid_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY public.mm_cron
    ADD CONSTRAINT mm_cron_guid_pk PRIMARY KEY (mm_cron_guid);


--
-- Name: mm_device mm_device_id_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY public.mm_device
    ADD CONSTRAINT mm_device_id_pk PRIMARY KEY (mm_device_id);


--
-- Name: mm_hardware mm_hardware_id; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY public.mm_hardware
    ADD CONSTRAINT mm_hardware_id PRIMARY KEY (mm_hardware_id);


--
-- Name: mm_link mm_link_guid_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY public.mm_link
    ADD CONSTRAINT mm_link_guid_pk PRIMARY KEY (mm_link_guid);


--
-- Name: mm_loan mm_loan_guid_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY public.mm_loan
    ADD CONSTRAINT mm_loan_guid_pk PRIMARY KEY (mm_loan_guid);


--
-- Name: mm_media_class mm_media_class_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY public.mm_media_class
    ADD CONSTRAINT mm_media_class_pk PRIMARY KEY (mm_media_class_guid);


--
-- Name: mm_media_dir mm_media_dir_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY public.mm_media_dir
    ADD CONSTRAINT mm_media_dir_pk PRIMARY KEY (mm_media_dir_guid);


--
-- Name: mm_media mm_media_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY public.mm_media
    ADD CONSTRAINT mm_media_pk PRIMARY KEY (mm_media_guid);


--
-- Name: mm_media_share mm_media_share_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY public.mm_media_share
    ADD CONSTRAINT mm_media_share_pk PRIMARY KEY (mm_media_share_guid);


--
-- Name: mm_metadata_album mm_metadata_album_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY public.mm_metadata_album
    ADD CONSTRAINT mm_metadata_album_pk PRIMARY KEY (mm_metadata_album_guid);


--
-- Name: mm_metadata_anime mm_metadata_anime_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY public.mm_metadata_anime
    ADD CONSTRAINT mm_metadata_anime_pk PRIMARY KEY (mm_metadata_anime_guid);


--
-- Name: mm_metadata_book mm_metadata_book_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY public.mm_metadata_book
    ADD CONSTRAINT mm_metadata_book_pk PRIMARY KEY (mm_metadata_book_guid);


--
-- Name: mm_metadata_collection mm_metadata_collection_guid_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY public.mm_metadata_collection
    ADD CONSTRAINT mm_metadata_collection_guid_pk PRIMARY KEY (mm_metadata_collection_guid);


--
-- Name: mm_metadata_logo mm_metadata_logo_guid_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY public.mm_metadata_logo
    ADD CONSTRAINT mm_metadata_logo_guid_pk PRIMARY KEY (mm_metadata_logo_guid);


--
-- Name: mm_metadata_music mm_metadata_music_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY public.mm_metadata_music
    ADD CONSTRAINT mm_metadata_music_pk PRIMARY KEY (mm_metadata_music_guid);


--
-- Name: mm_metadata_music_video mm_metadata_music_video_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY public.mm_metadata_music_video
    ADD CONSTRAINT mm_metadata_music_video_pk PRIMARY KEY (mm_metadata_music_video_guid);


--
-- Name: mm_metadata_musician mm_metadata_musician_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY public.mm_metadata_musician
    ADD CONSTRAINT mm_metadata_musician_pk PRIMARY KEY (mm_metadata_musician_guid);


--
-- Name: mm_metadata_movie mm_metadata_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY public.mm_metadata_movie
    ADD CONSTRAINT mm_metadata_pk PRIMARY KEY (mm_metadata_guid);


--
-- Name: mm_metadata_sports mm_metadata_sports_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY public.mm_metadata_sports
    ADD CONSTRAINT mm_metadata_sports_pk PRIMARY KEY (mm_metadata_sports_guid);


--
-- Name: mm_metadata_tvshow mm_metadata_tvshow_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY public.mm_metadata_tvshow
    ADD CONSTRAINT mm_metadata_tvshow_pk PRIMARY KEY (mm_metadata_tvshow_guid);


--
-- Name: mm_notification mm_notification_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY public.mm_notification
    ADD CONSTRAINT mm_notification_pk PRIMARY KEY (mm_notification_guid);


--
-- Name: mm_options_and_status mm_options_and_status_guid_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY public.mm_options_and_status
    ADD CONSTRAINT mm_options_and_status_guid_pk PRIMARY KEY (mm_options_and_status_guid);


--
-- Name: mm_radio mm_radio_guid_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY public.mm_radio
    ADD CONSTRAINT mm_radio_guid_pk PRIMARY KEY (mm_radio_guid);


--
-- Name: mm_review mm_review_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY public.mm_review
    ADD CONSTRAINT mm_review_pk PRIMARY KEY (mm_review_guid);


--
-- Name: mm_sync mm_sync_guid_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY public.mm_sync
    ADD CONSTRAINT mm_sync_guid_pk PRIMARY KEY (mm_sync_guid);


--
-- Name: mm_task mm_task_guid_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY public.mm_task
    ADD CONSTRAINT mm_task_guid_pk PRIMARY KEY (mm_task_guid);


--
-- Name: mm_tv_schedule mm_tv_schedule_id_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY public.mm_tv_schedule
    ADD CONSTRAINT mm_tv_schedule_id_pk PRIMARY KEY (mm_tv_schedule_id);


--
-- Name: mm_tv_schedule_program mm_tv_schedule_program_guid_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY public.mm_tv_schedule_program
    ADD CONSTRAINT mm_tv_schedule_program_guid_pk PRIMARY KEY (mm_tv_schedule_program_guid);


--
-- Name: mm_tv_stations mm_tv_stations_id_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY public.mm_tv_stations
    ADD CONSTRAINT mm_tv_stations_id_pk PRIMARY KEY (mm_tv_stations_id);


--
-- Name: mm_user_group mm_user_group_guid_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY public.mm_user_group
    ADD CONSTRAINT mm_user_group_guid_pk PRIMARY KEY (mm_user_group_guid);


--
-- Name: mm_user mm_user_pkey; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY public.mm_user
    ADD CONSTRAINT mm_user_pkey PRIMARY KEY (id);


--
-- Name: mm_user_profile mm_user_profile_guid_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY public.mm_user_profile
    ADD CONSTRAINT mm_user_profile_guid_pk PRIMARY KEY (mm_user_profile_guid);


--
-- Name: mm_metadata_person mmp_id_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY public.mm_metadata_person
    ADD CONSTRAINT mmp_id_pk PRIMARY KEY (mmp_id);


--
-- Name: mm_media_remote mmr_media_remote_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY public.mm_media_remote
    ADD CONSTRAINT mmr_media_remote_pk PRIMARY KEY (mmr_media_guid);


--
-- Name: gc_category_idx_name; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX gc_category_idx_name ON public.mm_game_category USING btree (gc_category);


--
-- Name: gi_game_idx_name; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX gi_game_idx_name ON public.mm_metadata_game_software_info USING btree (gi_game_info_name);


--
-- Name: gi_game_idx_name_trigram_idx; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX gi_game_idx_name_trigram_idx ON public.mm_metadata_game_software_info USING gist (gi_game_info_name public.gist_trgm_ops);


--
-- Name: gi_game_idx_short_name; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX gi_game_idx_short_name ON public.mm_metadata_game_software_info USING btree (gi_game_info_short_name);


--
-- Name: gi_system_id_ndx; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX gi_system_id_ndx ON public.mm_metadata_game_software_info USING btree (gi_system_id);


--
-- Name: mdq_que_type_idx_name; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mdq_que_type_idx_name ON public.mm_download_que USING btree (mdq_que_type);


--
-- Name: mm_channel_idx_country; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_channel_idx_country ON public.mm_channel USING btree (mm_channel_country_guid);


--
-- Name: mm_channel_idx_logo; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_channel_idx_logo ON public.mm_channel USING btree (mm_channel_logo_guid);


--
-- Name: mm_channel_idx_name; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_channel_idx_name ON public.mm_channel USING btree (mm_channel_name);


--
-- Name: mm_channel_idxgin_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_channel_idxgin_json ON public.mm_channel USING gin (mm_channel_media_id);


--
-- Name: mm_device_idx_type; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_device_idx_type ON public.mm_device USING btree (mm_device_type);


--
-- Name: mm_device_idxgin_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_device_idxgin_json ON public.mm_device USING gin (mm_device_json);


--
-- Name: mm_download_idx_provider; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_download_idx_provider ON public.mm_download_que USING btree (mdq_provider);


--
-- Name: mm_download_que_idxgin_meta_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_download_que_idxgin_meta_json ON public.mm_download_que USING gin (mdq_download_json);


--
-- Name: mm_game_info_idxgin_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_game_info_idxgin_json ON public.mm_metadata_game_software_info USING gin (gi_game_info_json);


--
-- Name: mm_game_info_idxgin_name; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_game_info_idxgin_name ON public.mm_metadata_game_software_info USING gin (((gi_game_info_json -> '@name'::text)));


--
-- Name: mm_game_systems_idxgin_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_game_systems_idxgin_json ON public.mm_metadata_game_systems_info USING gin (gs_game_system_json);


--
-- Name: mm_hardware_idx_manufacturer; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_hardware_idx_manufacturer ON public.mm_hardware USING btree (mm_hardware_manufacturer);


--
-- Name: mm_hardware_idx_model; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_hardware_idx_model ON public.mm_hardware USING btree (mm_hardware_model);


--
-- Name: mm_link_idx_name; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_link_idx_name ON public.mm_link USING btree (mm_link_name);


--
-- Name: mm_link_json_idxgin; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_link_json_idxgin ON public.mm_link USING gin (mm_link_json);


--
-- Name: mm_media_anime_name_trigram_idx; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_media_anime_name_trigram_idx ON public.mm_metadata_anime USING gist (mm_media_anime_name public.gist_trgm_ops);


--
-- Name: mm_media_class_idx_type; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_media_class_idx_type ON public.mm_media_class USING btree (mm_media_class_type);


--
-- Name: mm_media_dir_idx_share; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_media_dir_idx_share ON public.mm_media_dir USING btree (mm_media_dir_share_guid);


--
-- Name: mm_media_idx_metadata_uuid; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_media_idx_metadata_uuid ON public.mm_media USING btree (mm_media_metadata_guid);


--
-- Name: mm_media_idx_path; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_media_idx_path ON public.mm_media USING btree (mm_media_path);


--
-- Name: mm_media_idxgin_ffprobe; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_media_idxgin_ffprobe ON public.mm_media USING gin (mm_media_ffprobe_json);


--
-- Name: mm_media_music_video_band_trigram_idx; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_media_music_video_band_trigram_idx ON public.mm_metadata_music_video USING gist (mm_media_music_video_band public.gist_trgm_ops);


--
-- Name: mm_media_music_video_song_trigram_idx; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_media_music_video_song_trigram_idx ON public.mm_metadata_music_video USING gist (mm_media_music_video_song public.gist_trgm_ops);


--
-- Name: mm_media_name_trigram_idx; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_media_name_trigram_idx ON public.mm_metadata_movie USING gist (mm_media_name public.gist_trgm_ops);


--
-- Name: mm_metadata_album_idx_musician; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_album_idx_musician ON public.mm_metadata_album USING btree (mm_metadata_album_musician_guid);


--
-- Name: mm_metadata_album_idx_name; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_album_idx_name ON public.mm_metadata_album USING btree (mm_metadata_album_name);


--
-- Name: mm_metadata_album_idx_name_lower; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_album_idx_name_lower ON public.mm_metadata_album USING btree (lower(mm_metadata_album_name));


--
-- Name: mm_metadata_album_idxgin_id_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_album_idxgin_id_json ON public.mm_metadata_album USING gin (mm_metadata_album_id);


--
-- Name: mm_metadata_album_idxgin_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_album_idxgin_json ON public.mm_metadata_album USING gin (mm_metadata_album_json);


--
-- Name: mm_metadata_album_name_trigram_idx; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_album_name_trigram_idx ON public.mm_metadata_album USING gist (mm_metadata_album_name public.gist_trgm_ops);


--
-- Name: mm_metadata_aniem_idxgin_media_id; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_aniem_idxgin_media_id ON public.mm_metadata_anime USING gin (mm_metadata_anime_media_id);


--
-- Name: mm_metadata_anime_idx_name; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_anime_idx_name ON public.mm_metadata_anime USING btree (mm_media_anime_name);


--
-- Name: mm_metadata_anime_idx_name_lower; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_anime_idx_name_lower ON public.mm_metadata_anime USING btree (lower(mm_media_anime_name));


--
-- Name: mm_metadata_anime_idxgin_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_anime_idxgin_json ON public.mm_metadata_anime USING gin (mm_metadata_anime_json);


--
-- Name: mm_metadata_anime_idxgin_media_id_anidb; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_anime_idxgin_media_id_anidb ON public.mm_metadata_anime USING gin (((mm_metadata_anime_media_id -> 'anidb'::text)));


--
-- Name: mm_metadata_anime_idxgin_media_id_imdb; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_anime_idxgin_media_id_imdb ON public.mm_metadata_anime USING gin (((mm_metadata_anime_media_id -> 'imdb'::text)));


--
-- Name: mm_metadata_anime_idxgin_media_id_thetvdb; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_anime_idxgin_media_id_thetvdb ON public.mm_metadata_anime USING gin (((mm_metadata_anime_media_id -> 'thetvdb'::text)));


--
-- Name: mm_metadata_anime_idxgin_media_id_tmdb; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_anime_idxgin_media_id_tmdb ON public.mm_metadata_anime USING gin (((mm_metadata_anime_media_id -> 'tmdb'::text)));


--
-- Name: mm_metadata_anime_idxgin_user_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_anime_idxgin_user_json ON public.mm_metadata_anime USING gin (mm_metadata_anime_user_json);


--
-- Name: mm_metadata_book_name_trigram_idx; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_book_name_trigram_idx ON public.mm_metadata_book USING gist (mm_metadata_book_name public.gist_trgm_ops);


--
-- Name: mm_metadata_collection_idxgin_media_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_collection_idxgin_media_json ON public.mm_metadata_collection USING gin (mm_metadata_collection_media_ids);


--
-- Name: mm_metadata_collection_idxgin_meta_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_collection_idxgin_meta_json ON public.mm_metadata_collection USING gin (mm_metadata_collection_json);


--
-- Name: mm_metadata_collection_idxgin_name_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_collection_idxgin_name_json ON public.mm_metadata_collection USING gin (mm_metadata_collection_name);


--
-- Name: mm_metadata_idx_band_name; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_idx_band_name ON public.mm_metadata_music_video USING btree (mm_media_music_video_band);


--
-- Name: mm_metadata_idx_band_name_lower; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_idx_band_name_lower ON public.mm_metadata_music_video USING btree (lower(mm_media_music_video_band));


--
-- Name: mm_metadata_idx_book_name; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_idx_book_name ON public.mm_metadata_book USING btree (mm_metadata_book_name);


--
-- Name: mm_metadata_idx_book_name_lower; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_idx_book_name_lower ON public.mm_metadata_book USING btree (lower(mm_metadata_book_name));


--
-- Name: mm_metadata_idx_name; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_idx_name ON public.mm_metadata_movie USING btree (mm_media_name);


--
-- Name: mm_metadata_idx_name_lower; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_idx_name_lower ON public.mm_metadata_movie USING btree (lower(mm_media_name));


--
-- Name: mm_metadata_idx_song_name; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_idx_song_name ON public.mm_metadata_music_video USING btree (mm_media_music_video_song);


--
-- Name: mm_metadata_idx_song_name_lower; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_idx_song_name_lower ON public.mm_metadata_music_video USING btree (lower(mm_media_music_video_song));


--
-- Name: mm_metadata_idxgin_isbn; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_idxgin_isbn ON public.mm_metadata_book USING btree (mm_metadata_book_isbn);


--
-- Name: mm_metadata_idxgin_isbn13; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_idxgin_isbn13 ON public.mm_metadata_book USING btree (mm_metadata_book_isbn13);


--
-- Name: mm_metadata_idxgin_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_idxgin_json ON public.mm_metadata_movie USING gin (mm_metadata_json);


--
-- Name: mm_metadata_idxgin_media_id; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_idxgin_media_id ON public.mm_metadata_movie USING gin (mm_metadata_media_id);


--
-- Name: mm_metadata_idxgin_media_id_imdb; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_idxgin_media_id_imdb ON public.mm_metadata_movie USING gin (((mm_metadata_media_id -> 'imdb'::text)));


--
-- Name: mm_metadata_idxgin_media_id_thetvdb; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_idxgin_media_id_thetvdb ON public.mm_metadata_movie USING gin (((mm_metadata_media_id -> 'thetvdb'::text)));


--
-- Name: mm_metadata_idxgin_media_id_tmdb; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_idxgin_media_id_tmdb ON public.mm_metadata_movie USING gin (((mm_metadata_media_id -> 'tmdb'::text)));


--
-- Name: mm_metadata_idxgin_music_video_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_idxgin_music_video_json ON public.mm_metadata_music_video USING gin (mm_metadata_music_video_json);


--
-- Name: mm_metadata_idxgin_music_video_media_id; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_idxgin_music_video_media_id ON public.mm_metadata_music_video USING gin (mm_metadata_music_video_media_id);


--
-- Name: mm_metadata_idxgin_music_video_media_id_imvdb; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_idxgin_music_video_media_id_imvdb ON public.mm_metadata_music_video USING gin (((mm_metadata_music_video_media_id -> 'imvdb'::text)));


--
-- Name: mm_metadata_idxgin_user_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_idxgin_user_json ON public.mm_metadata_movie USING gin (mm_metadata_user_json);


--
-- Name: mm_metadata_logo_idxgin_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_logo_idxgin_json ON public.mm_metadata_logo USING gin (mm_metadata_logo_media_guid);


--
-- Name: mm_metadata_music_idx_album; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_music_idx_album ON public.mm_metadata_music USING btree (mm_metadata_music_album_guid);


--
-- Name: mm_metadata_music_idx_name; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_music_idx_name ON public.mm_metadata_music USING btree (mm_metadata_music_name);


--
-- Name: mm_metadata_music_idx_name_lower; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_music_idx_name_lower ON public.mm_metadata_music USING btree (lower(mm_metadata_music_name));


--
-- Name: mm_metadata_music_idxgin_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_music_idxgin_json ON public.mm_metadata_music USING gin (mm_metadata_music_json);


--
-- Name: mm_metadata_music_idxgin_media_id; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_music_idxgin_media_id ON public.mm_metadata_music USING gin (mm_metadata_media_music_id);


--
-- Name: mm_metadata_music_idxgin_user_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_music_idxgin_user_json ON public.mm_metadata_music USING gin (mm_metadata_music_user_json);


--
-- Name: mm_metadata_music_name_trigram_idx; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_music_name_trigram_idx ON public.mm_metadata_music USING gist (mm_metadata_music_name public.gist_trgm_ops);


--
-- Name: mm_metadata_music_video_idxgin_user_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_music_video_idxgin_user_json ON public.mm_metadata_music_video USING gin (mm_metadata_music_video_user_json);


--
-- Name: mm_metadata_musician_idx_name; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_musician_idx_name ON public.mm_metadata_musician USING btree (mm_metadata_musician_name);


--
-- Name: mm_metadata_musician_idx_name_lower; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_musician_idx_name_lower ON public.mm_metadata_musician USING btree (lower(mm_metadata_musician_name));


--
-- Name: mm_metadata_musician_idxgin_id_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_musician_idxgin_id_json ON public.mm_metadata_musician USING gin (mm_metadata_musician_id);


--
-- Name: mm_metadata_musician_idxgin_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_musician_idxgin_json ON public.mm_metadata_musician USING gin (mm_metadata_musician_json);


--
-- Name: mm_metadata_musician_name_trigram_idx; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_musician_name_trigram_idx ON public.mm_metadata_musician USING gist (mm_metadata_musician_name public.gist_trgm_ops);


--
-- Name: mm_metadata_person_idx_name; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_person_idx_name ON public.mm_metadata_person USING btree (mmp_person_name);


--
-- Name: mm_metadata_person_idxgin_id_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_person_idxgin_id_json ON public.mm_metadata_person USING gin (mmp_person_media_id);


--
-- Name: mm_metadata_person_idxgin_meta_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_person_idxgin_meta_json ON public.mm_metadata_person USING gin (mmp_person_meta_json);


--
-- Name: mm_metadata_review_idx_metadata_uuid; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_review_idx_metadata_uuid ON public.mm_review USING btree (mm_review_metadata_guid);


--
-- Name: mm_metadata_review_idxgin_media_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_review_idxgin_media_json ON public.mm_review USING gin (mm_review_metadata_id);


--
-- Name: mm_metadata_sports_idx_name; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_sports_idx_name ON public.mm_metadata_sports USING btree (mm_metadata_sports_name);


--
-- Name: mm_metadata_sports_idx_name_lower; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_sports_idx_name_lower ON public.mm_metadata_sports USING btree (lower(mm_metadata_sports_name));


--
-- Name: mm_metadata_sports_idxgin_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_sports_idxgin_json ON public.mm_metadata_sports USING gin (mm_metadata_sports_json);


--
-- Name: mm_metadata_sports_idxgin_media_id; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_sports_idxgin_media_id ON public.mm_metadata_sports USING gin (mm_metadata_media_sports_id);


--
-- Name: mm_metadata_sports_idxgin_media_id_imdb; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_sports_idxgin_media_id_imdb ON public.mm_metadata_sports USING gin (((mm_metadata_media_sports_id -> 'imdb'::text)));


--
-- Name: mm_metadata_sports_idxgin_media_id_thesportsdb; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_sports_idxgin_media_id_thesportsdb ON public.mm_metadata_sports USING gin (((mm_metadata_media_sports_id -> 'thesportsdb'::text)));


--
-- Name: mm_metadata_sports_idxgin_media_id_thetvdb; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_sports_idxgin_media_id_thetvdb ON public.mm_metadata_sports USING gin (((mm_metadata_media_sports_id -> 'thetvdb'::text)));


--
-- Name: mm_metadata_sports_idxgin_media_id_thetvdbseries; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_sports_idxgin_media_id_thetvdbseries ON public.mm_metadata_sports USING gin (((mm_metadata_media_sports_id -> 'thetvdbSeries'::text)));


--
-- Name: mm_metadata_sports_idxgin_media_id_tmdb; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_sports_idxgin_media_id_tmdb ON public.mm_metadata_sports USING gin (((mm_metadata_media_sports_id -> 'tmdb'::text)));


--
-- Name: mm_metadata_sports_idxgin_media_id_tvmaze; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_sports_idxgin_media_id_tvmaze ON public.mm_metadata_sports USING gin (((mm_metadata_media_sports_id -> 'tvmaze'::text)));


--
-- Name: mm_metadata_sports_name_trigram_idx; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_sports_name_trigram_idx ON public.mm_metadata_sports USING gist (mm_metadata_sports_name public.gist_trgm_ops);


--
-- Name: mm_metadata_tvshow_idx_name; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_tvshow_idx_name ON public.mm_metadata_tvshow USING btree (mm_metadata_tvshow_name);


--
-- Name: mm_metadata_tvshow_idx_name_lower; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_tvshow_idx_name_lower ON public.mm_metadata_tvshow USING btree (lower(mm_metadata_tvshow_name));


--
-- Name: mm_metadata_tvshow_idxgin_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_tvshow_idxgin_json ON public.mm_metadata_tvshow USING gin (mm_metadata_tvshow_json);


--
-- Name: mm_metadata_tvshow_idxgin_localimage_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_tvshow_idxgin_localimage_json ON public.mm_metadata_tvshow USING gin (mm_metadata_tvshow_json);


--
-- Name: mm_metadata_tvshow_idxgin_media_id; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_tvshow_idxgin_media_id ON public.mm_metadata_tvshow USING gin (mm_metadata_media_tvshow_id);


--
-- Name: mm_metadata_tvshow_idxgin_media_id_imdb; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_tvshow_idxgin_media_id_imdb ON public.mm_metadata_tvshow USING gin (((mm_metadata_media_tvshow_id -> 'imdb'::text)));


--
-- Name: mm_metadata_tvshow_idxgin_media_id_thetvdb; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_tvshow_idxgin_media_id_thetvdb ON public.mm_metadata_tvshow USING gin (((mm_metadata_media_tvshow_id -> 'thetvdb'::text)));


--
-- Name: mm_metadata_tvshow_idxgin_media_id_thetvdbseries; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_tvshow_idxgin_media_id_thetvdbseries ON public.mm_metadata_tvshow USING gin (((mm_metadata_media_tvshow_id -> 'thetvdbSeries'::text)));


--
-- Name: mm_metadata_tvshow_idxgin_media_id_tmdb; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_tvshow_idxgin_media_id_tmdb ON public.mm_metadata_tvshow USING gin (((mm_metadata_media_tvshow_id -> 'tmdb'::text)));


--
-- Name: mm_metadata_tvshow_idxgin_media_id_tvmaze; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_tvshow_idxgin_media_id_tvmaze ON public.mm_metadata_tvshow USING gin (((mm_metadata_media_tvshow_id -> 'tvmaze'::text)));


--
-- Name: mm_metadata_tvshow_idxgin_user_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_tvshow_idxgin_user_json ON public.mm_metadata_tvshow USING gin (mm_metadata_tvshow_user_json);


--
-- Name: mm_metadata_tvshow_name_trigram_idx; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_tvshow_name_trigram_idx ON public.mm_metadata_tvshow USING gist (mm_metadata_tvshow_name public.gist_trgm_ops);


--
-- Name: mm_notification_idx_dismissable; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_notification_idx_dismissable ON public.mm_notification USING btree (mm_notification_dismissable);


--
-- Name: mm_notification_idx_time; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_notification_idx_time ON public.mm_notification USING btree (mm_notification_time);


--
-- Name: mm_sync_idxgin_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_sync_idxgin_json ON public.mm_sync USING gin (mm_sync_options_json);


--
-- Name: mm_tv_schedule_idx_date; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_tv_schedule_idx_date ON public.mm_tv_schedule USING btree (mm_tv_schedule_date);


--
-- Name: mm_tv_schedule_idx_program; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_tv_schedule_idx_program ON public.mm_tv_schedule_program USING btree (mm_tv_schedule_program_id);


--
-- Name: mm_tv_schedule_idx_station; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_tv_schedule_idx_station ON public.mm_tv_schedule USING btree (mm_tv_schedule_station_id);


--
-- Name: mm_tv_stations_idx_name; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_tv_stations_idx_name ON public.mm_tv_stations USING btree (mm_tv_station_name);


--
-- Name: mm_tv_stations_idx_station; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_tv_stations_idx_station ON public.mm_tv_stations USING btree (mm_tv_station_id);


--
-- Name: mm_user_activity_idx_date; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_user_activity_idx_date ON public.mm_user_activity USING btree (mm_activity_datecreated);


--
-- Name: mm_user_activity_idx_user_guid; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_user_activity_idx_user_guid ON public.mm_user_activity USING btree (mm_activity_userid);


--
-- Name: mm_user_group_idx_name; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_user_group_idx_name ON public.mm_user_group USING btree (mm_user_group_name);


--
-- Name: mm_user_idx_username; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_user_idx_username ON public.mm_user USING btree (username);


--
-- Name: mm_user_profile_idx_name; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_user_profile_idx_name ON public.mm_user_profile USING btree (mm_user_profile_name);


--
-- Name: mmp_person_name_trigram_idx; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mmp_person_name_trigram_idx ON public.mm_metadata_person USING gist (mmp_person_name public.gist_trgm_ops);


--
-- Name: mmr_media_idx_link_uuid; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mmr_media_idx_link_uuid ON public.mm_media_remote USING btree (mmr_media_link_id);


--
-- Name: mmr_media_idx_metadata_uuid; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mmr_media_idx_metadata_uuid ON public.mm_media_remote USING btree (mmr_media_metadata_guid);


--
-- Name: mmr_media_idxgin_ffprobe; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mmr_media_idxgin_ffprobe ON public.mm_media_remote USING gin (mmr_media_ffprobe_json);


--
-- PostgreSQL database dump complete
--

