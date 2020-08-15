--
-- PostgreSQL database dump
--

-- Dumped from database version 11.3
-- Dumped by pg_dump version 11.3

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
-- Name: pg_trgm; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS pg_trgm WITH SCHEMA public;
CREATE EXTENSION IF NOT EXISTS pgcrypto WITH SCHEMA public;

--
-- Name: EXTENSION pg_trgm; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION pg_trgm IS 'text similarity measurement and index searching based on trigrams';


SET default_tablespace = '';

SET default_with_oids = false;

--
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
-- Name: mm_device; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mm_device (
    mm_device_id uuid NOT NULL,
    mm_device_type text,
    mm_device_json jsonb
);


ALTER TABLE public.mm_device OWNER TO postgres;

--
-- Name: mm_download_que; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mm_download_que (
    mdq_id uuid NOT NULL,
    mdq_provider text,
    mdq_que_type smallint,
    mdq_download_json jsonb
);


ALTER TABLE public.mm_download_que OWNER TO postgres;

--
-- Name: mm_game_category; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mm_game_category (
    gc_id uuid NOT NULL,
    gc_category text
);


ALTER TABLE public.mm_game_category OWNER TO postgres;

--
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
-- Name: mm_link; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mm_link (
    mm_link_guid uuid NOT NULL,
    mm_link_name text,
    mm_link_json jsonb
);


ALTER TABLE public.mm_link OWNER TO postgres;

--
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
-- Name: mm_media; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mm_media (
    mm_media_guid uuid NOT NULL,
    mm_media_class_guid uuid,
    mm_media_metadata_guid uuid,
    mm_media_path text,
    mm_media_ffprobe_json jsonb,
    mm_media_json jsonb
);


ALTER TABLE public.mm_media OWNER TO postgres;

--
-- Name: mm_media_class; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mm_media_class (
    mm_media_class_guid uuid NOT NULL,
    mm_media_class_type text,
    mm_media_class_parent_type text,
    mm_media_class_display boolean
);


ALTER TABLE public.mm_media_class OWNER TO postgres;

--
-- Name: mm_media_dir; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mm_media_dir (
    mm_media_dir_guid uuid NOT NULL,
    mm_media_dir_path text,
    mm_media_dir_class_type uuid,
    mm_media_dir_last_scanned timestamp without time zone,
    mm_media_dir_share_guid uuid,
    mm_media_dir_status jsonb
);


ALTER TABLE public.mm_media_dir OWNER TO postgres;

--
-- Name: mm_media_remote; Type: TABLE; Schema: public; Owner: postgres
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


ALTER TABLE public.mm_media_remote OWNER TO postgres;

--
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
-- Name: mm_metadata_game_software_info; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mm_metadata_game_software_info (
    gi_id uuid NOT NULL,
    gi_system_id uuid,
    gi_game_info_short_name text,
    gi_game_info_name text,
    gi_game_info_json jsonb
);


ALTER TABLE public.mm_metadata_game_software_info OWNER TO postgres;

--
-- Name: mm_metadata_game_systems_info; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mm_metadata_game_systems_info (
    gs_id uuid NOT NULL,
    gs_game_system_name text,
    gs_game_system_alias text,
    gs_game_system_json jsonb,
    mm_metadata_localimage_json jsonb
);


ALTER TABLE public.mm_metadata_game_systems_info OWNER TO postgres;

--
-- Name: mm_metadata_logo; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mm_metadata_logo (
    mm_metadata_logo_guid uuid NOT NULL,
    mm_metadata_logo_media_guid jsonb,
    mm_metadata_logo_image_path text
);


ALTER TABLE public.mm_metadata_logo OWNER TO postgres;

--
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
-- Name: mm_metadata_person; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mm_metadata_person (
    mmp_id uuid NOT NULL,
    mmp_person_media_id jsonb,
    mmp_person_meta_json jsonb,
    mmp_person_image text,
    mmp_person_name text
);


ALTER TABLE public.mm_metadata_person OWNER TO postgres;

--
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
-- Name: mm_metadata_tvshow; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mm_metadata_tvshow (
    mm_metadata_tvshow_guid uuid NOT NULL,
    mm_metadata_media_tvshow_id jsonb,
    mm_metadata_tvshow_name text,
    mm_metadata_tvshow_json jsonb,
    mm_metadata_tvshow_localimage_json jsonb,
    mm_metadata_tvshow_user_json jsonb
);


ALTER TABLE public.mm_metadata_tvshow OWNER TO postgres;

--
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
-- Name: mm_options_and_status; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mm_options_and_status (
    mm_options_and_status_guid uuid NOT NULL,
    mm_options_json jsonb,
    mm_status_json jsonb
);


ALTER TABLE public.mm_options_and_status OWNER TO postgres;

--
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
-- Name: mm_tv_schedule_program; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mm_tv_schedule_program (
    mm_tv_schedule_program_guid uuid NOT NULL,
    mm_tv_schedule_program_id text,
    mm_tv_schedule_program_json jsonb
);


ALTER TABLE public.mm_tv_schedule_program OWNER TO postgres;

--
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
-- Name: mm_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.mm_user_id_seq OWNED BY public.mm_user.id;


--
-- Name: mm_user_profile; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mm_user_profile (
    mm_user_profile_guid uuid NOT NULL,
    mm_user_profile_name text,
    mm_user_profile_json jsonb
);


ALTER TABLE public.mm_user_profile OWNER TO postgres;

--
-- Name: mm_version; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mm_version (
    mm_version_no integer
);


ALTER TABLE public.mm_version OWNER TO postgres;

--
-- Name: mm_user id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mm_user ALTER COLUMN id SET DEFAULT nextval('public.mm_user_id_seq'::regclass);


--
-- Data for Name: mm_channel; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mm_channel (mm_channel_guid, mm_channel_name, mm_channel_media_id, mm_channel_country_guid, mm_channel_logo_guid) FROM stdin;
\.


--
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
\.


--
-- Data for Name: mm_device; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mm_device (mm_device_id, mm_device_type, mm_device_json) FROM stdin;
\.


--
-- Data for Name: mm_download_que; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mm_download_que (mdq_id, mdq_provider, mdq_que_type, mdq_download_json) FROM stdin;
\.


--
-- Data for Name: mm_game_category; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mm_game_category (gc_id, gc_category) FROM stdin;
\.


--
-- Data for Name: mm_hardware; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mm_hardware (mm_hardware_id, mm_hardware_manufacturer, mm_hardware_model, mm_hardware_json) FROM stdin;
\.


--
-- Data for Name: mm_link; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mm_link (mm_link_guid, mm_link_name, mm_link_json) FROM stdin;
\.


--
-- Data for Name: mm_loan; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mm_loan (mm_loan_guid, mm_loan_media_id, mm_loan_user_id, mm_load_user_loan_id, mm_loan_time, mm_loan_return_time) FROM stdin;
\.


--
-- Data for Name: mm_media; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mm_media (mm_media_guid, mm_media_class_guid, mm_media_metadata_guid, mm_media_path, mm_media_ffprobe_json, mm_media_json) FROM stdin;
\.


--
-- Data for Name: mm_media_class; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mm_media_class (mm_media_class_guid, mm_media_class_type, mm_media_class_parent_type, mm_media_class_display) FROM stdin;
bfd269c6-3105-4694-b02d-da76e1431165	Adult	Video	t
323af63c-0641-4c87-9aa9-f6b6d09fc33b	Anime	Video	t
ff7bb1dd-d54d-4935-9dca-9e3ff737ab19	Book	Publication	t
64e41d00-dac3-4de9-87ef-0905eb1ac56b	Boxset	\N	f
abd9e32e-da96-482e-9e77-b5efde45a931	Comic	Publication	t
568fb520-ecbb-4ca0-b7d4-a057f3162881	Comic Strip	Publication	t
52c4032d-bbf0-43aa-b893-f9a336046fe4	Game CHD	\N	f
c01818e8-4592-409a-bbc1-528eedce0502	Game ISO	\N	f
cf7c80c3-0a7c-4136-97ab-ef0eb4b5264a	Game ROM	\N	f
a050c950-2eff-4c69-9b38-37349b3260ca	Home Movie	Video	t
323568eb-5984-4685-b436-66909fa2bb78	Magazine	Publication	t
e636fdde-8de1-43b3-9c36-66c76b88e693	Movie	Video	t
872059dc-00bb-44f9-b422-3a1218740962	Movie Extras	Video	f
02bfd775-aa0e-4d6a-9d52-5eee9398efbf	Movie Collection	\N	f
e6e96f4f-cc6b-462a-9f33-e396b775d47e	Movie Theme	Audio	f
d2513915-3d94-442f-93cb-78e72396b3d2	Movie Subtitle	\N	f
5bf4e542-e234-4e61-a80b-93dc24b793a8	Movie Trailer	Video	f
179586d2-8352-4195-868d-5c834034231b	Music	Audio	t
3d4f9436-ebd5-4816-b962-58123a93ba34	Music Album	\N	f
c09e2f26-553a-4c36-8915-51776ac1e9a1	Music Collection	\N	f
2e8f085c-2ba2-4088-9a31-923b35c962e3	Music Lyric	\N	f
98f64f59-eea9-4397-945b-4758e512f15a	Music Video	Video	t
56fd8dce-8fea-4671-a776-f2e6bf1ec307	Person	\N	f
db400fa4-b0ad-45b3-b679-a998fcfe0e6d	Picture	Image	t
80629edf-3157-4c90-9b37-06c70afd5d61	Soundtrack	Audio	f
251b593d-e89a-4aa0-8347-08ac832711b3	Sports	Video	t
ad0fed4c-cf23-4482-85cb-3b5a89509848	Subtitle	\N	f
2e12c3d0-6bff-48a2-8af6-f903e2d18caa	TV Episode	Video	f
29b747c2-1256-4f8b-b939-82d99ab211fc	TV Extras	Video	f
2188520b-acbc-47e0-85c7-ef457e0e1415	TV Season	\N	f
e58e2a2e-3bc0-464f-9b07-2651336615e3	TV Show	Video	t
5380c3bf-22c6-49ac-a375-170c01078987	TV Subtitle	\N	f
b0718413-5e07-453d-afc0-9e1aa477dad7	TV Theme	Audio	f
680e9904-8b03-4ee0-a037-3bf94e6dc57b	TV Trailer	Video	f
28c0573c-acc9-4d34-8e72-604474814acb	Video Game	Game	t
f1371e1b-b79b-4d76-9e47-95ba727840d1	Video Game Intro	Video	t
2829ab8f-5839-458d-9f5a-2e06488ee52b	Video Game Speedrun	Video	t
5136162e-846b-4027-981a-163d61d2d86a	Video Game Superplay	Video	t
\.


--
-- Data for Name: mm_media_dir; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mm_media_dir (mm_media_dir_guid, mm_media_dir_path, mm_media_dir_class_type, mm_media_dir_last_scanned, mm_media_dir_share_guid, mm_media_dir_status) FROM stdin;
\.


--
-- Data for Name: mm_media_remote; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mm_media_remote (mmr_media_guid, mmr_media_link_id, mmr_media_uuid, mmr_media_class_guid, mmr_media_metadata_guid, mmr_media_ffprobe_json, mmr_media_json) FROM stdin;
\.


--
-- Data for Name: mm_media_share; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mm_media_share (mm_media_share_guid, mm_media_share_type, mm_media_share_user, mm_media_share_password, mm_media_share_server, mm_media_share_path) FROM stdin;
\.


--
-- Data for Name: mm_metadata_album; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mm_metadata_album (mm_metadata_album_guid, mm_metadata_album_name, mm_metadata_album_id, mm_metadata_album_json, mm_metadata_album_musician_guid, mm_metadata_album_user_json, mm_metadata_album_localimage) FROM stdin;
\.


--
-- Data for Name: mm_metadata_anime; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mm_metadata_anime (mm_metadata_anime_guid, mm_metadata_anime_media_id, mm_media_anime_name, mm_metadata_anime_json, mm_metadata_anime_mapping, mm_metadata_anime_mapping_before, mm_metadata_anime_localimage_json, mm_metadata_anime_user_json) FROM stdin;
\.


--
-- Data for Name: mm_metadata_book; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mm_metadata_book (mm_metadata_book_guid, mm_metadata_book_isbn, mm_metadata_book_isbn13, mm_metadata_book_name, mm_metadata_book_json, mm_metadata_book_user_json, mm_metadata_book_localimage_json) FROM stdin;
\.


--
-- Data for Name: mm_metadata_collection; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mm_metadata_collection (mm_metadata_collection_guid, mm_metadata_collection_name, mm_metadata_collection_media_ids, mm_metadata_collection_json, mm_metadata_collection_imagelocal_json) FROM stdin;
\.


--
-- Data for Name: mm_metadata_game_software_info; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mm_metadata_game_software_info (gi_id, gi_system_id, gi_game_info_short_name, gi_game_info_name, gi_game_info_json) FROM stdin;
\.


--
-- Data for Name: mm_metadata_game_systems_info; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mm_metadata_game_systems_info (gs_id, gs_game_system_name, gs_game_system_alias, gs_game_system_json, mm_metadata_localimage_json) FROM stdin;
\.


--
-- Data for Name: mm_metadata_logo; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mm_metadata_logo (mm_metadata_logo_guid, mm_metadata_logo_media_guid, mm_metadata_logo_image_path) FROM stdin;
\.


--
-- Data for Name: mm_metadata_movie; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mm_metadata_movie (mm_metadata_guid, mm_metadata_media_id, mm_media_name, mm_metadata_json, mm_metadata_localimage_json, mm_metadata_user_json) FROM stdin;
\.


--
-- Data for Name: mm_metadata_music; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mm_metadata_music (mm_metadata_music_guid, mm_metadata_media_music_id, mm_metadata_music_name, mm_metadata_music_json, mm_metadata_music_album_guid, mm_metadata_music_user_json) FROM stdin;
\.


--
-- Data for Name: mm_metadata_music_video; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mm_metadata_music_video (mm_metadata_music_video_guid, mm_metadata_music_video_media_id, mm_media_music_video_band, mm_media_music_video_song, mm_metadata_music_video_json, mm_metadata_music_video_localimage_json, mm_metadata_music_video_user_json) FROM stdin;
\.


--
-- Data for Name: mm_metadata_musician; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mm_metadata_musician (mm_metadata_musician_guid, mm_metadata_musician_name, mm_metadata_musician_id, mm_metadata_musician_json, mm_metadata_musician_localimage_json) FROM stdin;
\.


--
-- Data for Name: mm_metadata_person; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mm_metadata_person (mmp_id, mmp_person_media_id, mmp_person_meta_json, mmp_person_image, mmp_person_name) FROM stdin;
\.


--
-- Data for Name: mm_metadata_sports; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mm_metadata_sports (mm_metadata_sports_guid, mm_metadata_media_sports_id, mm_metadata_sports_name, mm_metadata_sports_json, mm_metadata_sports_user_json, mm_metadata_sports_image_json) FROM stdin;
\.


--
-- Data for Name: mm_metadata_tvshow; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mm_metadata_tvshow (mm_metadata_tvshow_guid, mm_metadata_media_tvshow_id, mm_metadata_tvshow_name, mm_metadata_tvshow_json, mm_metadata_tvshow_localimage_json, mm_metadata_tvshow_user_json) FROM stdin;
\.


--
-- Data for Name: mm_notification; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mm_notification (mm_notification_guid, mm_notification_text, mm_notification_time, mm_notification_dismissable) FROM stdin;
\.


--
-- Data for Name: mm_options_and_status; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mm_options_and_status (mm_options_and_status_guid, mm_options_json, mm_status_json) FROM stdin;
df641592-2c6a-4ffa-816d-5f24dcea1ddd	{"API": {"anidb": null, "imvdb": null, "dirble": "184709fc95ff6c4dacf841eb14", "google": "AIzaSyCwMkNYp8E4H19BDzlM7-IDkNCQtw0R9lY", "isbndb": "25C8IT4I", "tvmaze": "mknotneeded", "thetvdb": "147CB43DCA8B61B7", "shoutcast": null, "thelogodb": null, "soundcloud": null, "themoviedb": "f72118d1e84b8a1438935972a9c37cac", "globalcache": null, "musicbrainz": null, "thesportsdb": "4352761817344", "opensubtitles": null, "openweathermap": "575b4ae4615e4e2a4c34fb9defa17ceb", "rottentomatoes": "f4tnu5dn9r7f28gjth3ftqaj"}, "User": {"Password Lock": null, "Activity Purge": null}, "Cloud": {}, "Trakt": {"ApiKey": null, "ClientID": null, "SecretKey": null}, "Backup": {"Interval": 0, "BackupType": "local"}, "Docker": {"Nodes": 0, "SwarmID": null, "Instances": 0}, "LastFM": {"api_key": null, "password": null, "username": null, "api_secret": null}, "Twitch": {"OAuth": null, "ClientID": null}, "Account": {"ScheduleDirect": {"User": null, "Password": null}}, "Metadata": {"Trailer": {"Clip": false, "Behind": false, "Carpool": false, "Trailer": false, "Featurette": false}, "DL Subtitle": false, "MusicBrainz": {"Host": null, "Port": 5000, "User": null, "Password": null}, "MetadataImageLocal": false}, "Transmission": {"Host": null, "Port": 9091, "Password": "metaman", "Username": "spootdev"}, "Docker Instances": {"elk": false, "smtp": false, "mumble": false, "pgadmin": false, "portainer": false, "teamspeak": false, "wireshark": false, "musicbrainz": false, "transmission": false}, "MediaKrakenServer": {"MOTD": null, "Maintenance": null, "Server Name": "MediaKraken", "MaxResumePct": 5}}	{"thetvdb_Updated_Epoc": 0}
\.


--
-- Data for Name: mm_radio; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mm_radio (mm_radio_guid, mm_radio_name, mm_radio_description, mm_radio_address, mm_radio_active) FROM stdin;
\.


--
-- Data for Name: mm_review; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mm_review (mm_review_guid, mm_review_metadata_id, mm_review_metadata_guid, mm_review_json) FROM stdin;
\.


--
-- Data for Name: mm_sync; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mm_sync (mm_sync_guid, mm_sync_path, mm_sync_path_to, mm_sync_options_json) FROM stdin;
\.


--
-- Data for Name: mm_tv_schedule; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mm_tv_schedule (mm_tv_schedule_id, mm_tv_schedule_station_id, mm_tv_schedule_date, mm_tv_schedule_json) FROM stdin;
\.


--
-- Data for Name: mm_tv_schedule_program; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mm_tv_schedule_program (mm_tv_schedule_program_guid, mm_tv_schedule_program_id, mm_tv_schedule_program_json) FROM stdin;
\.


--
-- Data for Name: mm_tv_stations; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mm_tv_stations (mm_tv_stations_id, mm_tv_station_name, mm_tv_station_id, mm_tv_station_channel, mm_tv_station_json, mm_tv_station_image) FROM stdin;
\.


--
-- Data for Name: mm_user; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mm_user (id, username, email, password, created_at, active, is_admin, user_json, lang) FROM stdin;
\.


--
-- Data for Name: mm_user_activity; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mm_user_activity (mm_activity_guid, mm_activity_name, mm_activity_overview, mm_activity_short_overview, mm_activity_type, mm_activity_itemid, mm_activity_userid, mm_activity_datecreated, mm_activity_log_severity) FROM stdin;
\.


--
-- Data for Name: mm_user_group; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mm_user_group (mm_user_group_guid, mm_user_group_name, mm_user_group_description, mm_user_group_rights_json) FROM stdin;
38117775-93b4-47d6-9a42-fc886ab6580c	Administrator	Server administrator	{"Admin": true, "PreviewOnly": false}
6666956c-a4d8-45bc-9c56-deaa1c2b68d3	User	General user	{"Admin": false, "PreviewOnly": false}
bea39ac2-505e-4cdd-9a3b-9c7da2cb28b2	Guest	Guest (Preview only)	{"Admin": false, "PreviewOnly": true}
\.


--
-- Data for Name: mm_user_profile; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mm_user_profile (mm_user_profile_guid, mm_user_profile_name, mm_user_profile_json) FROM stdin;
0863c596-3d62-4409-83c2-0515d3465adc	Adult	{"3D": true, "TV": true, "Home": true, "Lang": "en", "Sync": true, "Adult": true, "Books": true, "Games": true, "MaxBR": 100, "Movie": true, "Music": true, "IRadio": true, "Images": true, "LiveTV": true, "Sports": true, "Internet": true, "MaxRating": 5}
2bf39eb6-8192-4c2d-88cf-6341bbec1cd8	Teen	{"3D": true, "TV": true, "Home": true, "Lang": "en", "Sync": false, "Adult": false, "Books": true, "Games": true, "MaxBR": 50, "Movie": true, "Music": true, "IRadio": true, "Images": true, "LiveTV": true, "Sports": true, "Internet": true, "MaxRating": 3}
2bcbbd3e-8e2e-4fdc-92a9-471e5d018539	Child	{"3D": false, "TV": true, "Home": true, "Lang": "en", "Sync": false, "Adult": false, "Books": true, "Games": true, "MaxBR": 20, "Movie": true, "Music": true, "IRadio": false, "Images": true, "LiveTV": false, "Sports": true, "Internet": false, "MaxRating": 0}
\.


--
-- Data for Name: mm_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.mm_version (mm_version_no) FROM stdin;
22
\.


--
-- Name: mm_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.mm_user_id_seq', 1, false);


--
-- Name: mm_game_category gc_id_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mm_game_category
    ADD CONSTRAINT gc_id_pk PRIMARY KEY (gc_id);


--
-- Name: mm_metadata_game_software_info gi_id_mpk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mm_metadata_game_software_info
    ADD CONSTRAINT gi_id_mpk PRIMARY KEY (gi_id);


--
-- Name: mm_metadata_game_systems_info gs_id_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mm_metadata_game_systems_info
    ADD CONSTRAINT gs_id_pk PRIMARY KEY (gs_id);


--
-- Name: mm_download_que mdq_id_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mm_download_que
    ADD CONSTRAINT mdq_id_pk PRIMARY KEY (mdq_id);


--
-- Name: mm_user_activity mm_activity_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mm_user_activity
    ADD CONSTRAINT mm_activity_pk PRIMARY KEY (mm_activity_guid);


--
-- Name: mm_channel mm_channel_guid_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mm_channel
    ADD CONSTRAINT mm_channel_guid_pk PRIMARY KEY (mm_channel_guid);


--
-- Name: mm_cron mm_cron_guid_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mm_cron
    ADD CONSTRAINT mm_cron_guid_pk PRIMARY KEY (mm_cron_guid);


--
-- Name: mm_device mm_device_id_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mm_device
    ADD CONSTRAINT mm_device_id_pk PRIMARY KEY (mm_device_id);


--
-- Name: mm_hardware mm_hardware_id; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mm_hardware
    ADD CONSTRAINT mm_hardware_id PRIMARY KEY (mm_hardware_id);


--
-- Name: mm_link mm_link_guid_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mm_link
    ADD CONSTRAINT mm_link_guid_pk PRIMARY KEY (mm_link_guid);


--
-- Name: mm_loan mm_loan_guid_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mm_loan
    ADD CONSTRAINT mm_loan_guid_pk PRIMARY KEY (mm_loan_guid);


--
-- Name: mm_media_class mm_media_class_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mm_media_class
    ADD CONSTRAINT mm_media_class_pk PRIMARY KEY (mm_media_class_guid);


--
-- Name: mm_media_dir mm_media_dir_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mm_media_dir
    ADD CONSTRAINT mm_media_dir_pk PRIMARY KEY (mm_media_dir_guid);


--
-- Name: mm_media mm_media_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mm_media
    ADD CONSTRAINT mm_media_pk PRIMARY KEY (mm_media_guid);


--
-- Name: mm_media_share mm_media_share_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mm_media_share
    ADD CONSTRAINT mm_media_share_pk PRIMARY KEY (mm_media_share_guid);


--
-- Name: mm_metadata_album mm_metadata_album_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mm_metadata_album
    ADD CONSTRAINT mm_metadata_album_pk PRIMARY KEY (mm_metadata_album_guid);


--
-- Name: mm_metadata_anime mm_metadata_anime_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mm_metadata_anime
    ADD CONSTRAINT mm_metadata_anime_pk PRIMARY KEY (mm_metadata_anime_guid);


--
-- Name: mm_metadata_book mm_metadata_book_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mm_metadata_book
    ADD CONSTRAINT mm_metadata_book_pk PRIMARY KEY (mm_metadata_book_guid);


--
-- Name: mm_metadata_collection mm_metadata_collection_guid_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mm_metadata_collection
    ADD CONSTRAINT mm_metadata_collection_guid_pk PRIMARY KEY (mm_metadata_collection_guid);


--
-- Name: mm_metadata_logo mm_metadata_logo_guid_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mm_metadata_logo
    ADD CONSTRAINT mm_metadata_logo_guid_pk PRIMARY KEY (mm_metadata_logo_guid);


--
-- Name: mm_metadata_music mm_metadata_music_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mm_metadata_music
    ADD CONSTRAINT mm_metadata_music_pk PRIMARY KEY (mm_metadata_music_guid);


--
-- Name: mm_metadata_music_video mm_metadata_music_video_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mm_metadata_music_video
    ADD CONSTRAINT mm_metadata_music_video_pk PRIMARY KEY (mm_metadata_music_video_guid);


--
-- Name: mm_metadata_musician mm_metadata_musician_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mm_metadata_musician
    ADD CONSTRAINT mm_metadata_musician_pk PRIMARY KEY (mm_metadata_musician_guid);


--
-- Name: mm_metadata_movie mm_metadata_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mm_metadata_movie
    ADD CONSTRAINT mm_metadata_pk PRIMARY KEY (mm_metadata_guid);


--
-- Name: mm_metadata_sports mm_metadata_sports_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mm_metadata_sports
    ADD CONSTRAINT mm_metadata_sports_pk PRIMARY KEY (mm_metadata_sports_guid);


--
-- Name: mm_metadata_tvshow mm_metadata_tvshow_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mm_metadata_tvshow
    ADD CONSTRAINT mm_metadata_tvshow_pk PRIMARY KEY (mm_metadata_tvshow_guid);


--
-- Name: mm_notification mm_notification_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mm_notification
    ADD CONSTRAINT mm_notification_pk PRIMARY KEY (mm_notification_guid);


--
-- Name: mm_options_and_status mm_options_and_status_guid_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mm_options_and_status
    ADD CONSTRAINT mm_options_and_status_guid_pk PRIMARY KEY (mm_options_and_status_guid);


--
-- Name: mm_radio mm_radio_guid_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mm_radio
    ADD CONSTRAINT mm_radio_guid_pk PRIMARY KEY (mm_radio_guid);


--
-- Name: mm_review mm_review_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mm_review
    ADD CONSTRAINT mm_review_pk PRIMARY KEY (mm_review_guid);


--
-- Name: mm_sync mm_sync_guid_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mm_sync
    ADD CONSTRAINT mm_sync_guid_pk PRIMARY KEY (mm_sync_guid);


--
-- Name: mm_tv_schedule mm_tv_schedule_id_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mm_tv_schedule
    ADD CONSTRAINT mm_tv_schedule_id_pk PRIMARY KEY (mm_tv_schedule_id);


--
-- Name: mm_tv_schedule_program mm_tv_schedule_program_guid_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mm_tv_schedule_program
    ADD CONSTRAINT mm_tv_schedule_program_guid_pk PRIMARY KEY (mm_tv_schedule_program_guid);


--
-- Name: mm_tv_stations mm_tv_stations_id_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mm_tv_stations
    ADD CONSTRAINT mm_tv_stations_id_pk PRIMARY KEY (mm_tv_stations_id);


--
-- Name: mm_user_group mm_user_group_guid_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mm_user_group
    ADD CONSTRAINT mm_user_group_guid_pk PRIMARY KEY (mm_user_group_guid);


--
-- Name: mm_user mm_user_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mm_user
    ADD CONSTRAINT mm_user_pkey PRIMARY KEY (id);


--
-- Name: mm_user_profile mm_user_profile_guid_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mm_user_profile
    ADD CONSTRAINT mm_user_profile_guid_pk PRIMARY KEY (mm_user_profile_guid);


--
-- Name: mm_metadata_person mmp_id_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mm_metadata_person
    ADD CONSTRAINT mmp_id_pk PRIMARY KEY (mmp_id);


--
-- Name: mm_media_remote mmr_media_remote_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mm_media_remote
    ADD CONSTRAINT mmr_media_remote_pk PRIMARY KEY (mmr_media_guid);


--
-- Name: gc_category_idx_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX gc_category_idx_name ON public.mm_game_category USING btree (gc_category);


--
-- Name: gi_game_idx_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX gi_game_idx_name ON public.mm_metadata_game_software_info USING btree (gi_game_info_name);


--
-- Name: gi_game_idx_name_trigram_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX gi_game_idx_name_trigram_idx ON public.mm_metadata_game_software_info USING gist (gi_game_info_name public.gist_trgm_ops);


--
-- Name: gi_game_idx_short_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX gi_game_idx_short_name ON public.mm_metadata_game_software_info USING btree (gi_game_info_short_name);


--
-- Name: gi_system_id_ndx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX gi_system_id_ndx ON public.mm_metadata_game_software_info USING btree (gi_system_id);


--
-- Name: mdq_que_type_idx_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mdq_que_type_idx_name ON public.mm_download_que USING btree (mdq_que_type);


--
-- Name: mm_channel_idx_country; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_channel_idx_country ON public.mm_channel USING btree (mm_channel_country_guid);


--
-- Name: mm_channel_idx_logo; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_channel_idx_logo ON public.mm_channel USING btree (mm_channel_logo_guid);


--
-- Name: mm_channel_idx_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_channel_idx_name ON public.mm_channel USING btree (mm_channel_name);


--
-- Name: mm_channel_idxgin_json; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_channel_idxgin_json ON public.mm_channel USING gin (mm_channel_media_id);


--
-- Name: mm_device_idx_type; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_device_idx_type ON public.mm_device USING btree (mm_device_type);


--
-- Name: mm_device_idxgin_json; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_device_idxgin_json ON public.mm_device USING gin (mm_device_json);


--
-- Name: mm_download_idx_provider; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_download_idx_provider ON public.mm_download_que USING btree (mdq_provider);


--
-- Name: mm_download_que_idxgin_meta_json; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_download_que_idxgin_meta_json ON public.mm_download_que USING gin (mdq_download_json);


--
-- Name: mm_game_info_idxgin_json; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_game_info_idxgin_json ON public.mm_metadata_game_software_info USING gin (gi_game_info_json);


--
-- Name: mm_game_info_idxgin_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_game_info_idxgin_name ON public.mm_metadata_game_software_info USING gin (((gi_game_info_json -> '@name'::text)));


--
-- Name: mm_game_systems_idxgin_json; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_game_systems_idxgin_json ON public.mm_metadata_game_systems_info USING gin (gs_game_system_json);


--
-- Name: mm_hardware_idx_manufacturer; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_hardware_idx_manufacturer ON public.mm_hardware USING btree (mm_hardware_manufacturer);


--
-- Name: mm_hardware_idx_model; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_hardware_idx_model ON public.mm_hardware USING btree (mm_hardware_model);


--
-- Name: mm_link_idx_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_link_idx_name ON public.mm_link USING btree (mm_link_name);


--
-- Name: mm_link_json_idxgin; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_link_json_idxgin ON public.mm_link USING gin (mm_link_json);


--
-- Name: mm_media_anime_name_trigram_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_media_anime_name_trigram_idx ON public.mm_metadata_anime USING gist (mm_media_anime_name public.gist_trgm_ops);


--
-- Name: mm_media_class_idx_type; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_media_class_idx_type ON public.mm_media_class USING btree (mm_media_class_type);


--
-- Name: mm_media_dir_idx_share; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_media_dir_idx_share ON public.mm_media_dir USING btree (mm_media_dir_share_guid);


--
-- Name: mm_media_idx_metadata_uuid; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_media_idx_metadata_uuid ON public.mm_media USING btree (mm_media_metadata_guid);


--
-- Name: mm_media_idx_path; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_media_idx_path ON public.mm_media USING btree (mm_media_path);


--
-- Name: mm_media_idxgin_ffprobe; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_media_idxgin_ffprobe ON public.mm_media USING gin (mm_media_ffprobe_json);


--
-- Name: mm_media_music_video_band_trigram_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_media_music_video_band_trigram_idx ON public.mm_metadata_music_video USING gist (mm_media_music_video_band public.gist_trgm_ops);


--
-- Name: mm_media_music_video_song_trigram_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_media_music_video_song_trigram_idx ON public.mm_metadata_music_video USING gist (mm_media_music_video_song public.gist_trgm_ops);


--
-- Name: mm_media_name_trigram_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_media_name_trigram_idx ON public.mm_metadata_movie USING gist (mm_media_name public.gist_trgm_ops);


--
-- Name: mm_metadata_album_idx_musician; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_album_idx_musician ON public.mm_metadata_album USING btree (mm_metadata_album_musician_guid);


--
-- Name: mm_metadata_album_idx_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_album_idx_name ON public.mm_metadata_album USING btree (mm_metadata_album_name);


--
-- Name: mm_metadata_album_idx_name_lower; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_album_idx_name_lower ON public.mm_metadata_album USING btree (lower(mm_metadata_album_name));


--
-- Name: mm_metadata_album_idxgin_id_json; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_album_idxgin_id_json ON public.mm_metadata_album USING gin (mm_metadata_album_id);


--
-- Name: mm_metadata_album_idxgin_json; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_album_idxgin_json ON public.mm_metadata_album USING gin (mm_metadata_album_json);


--
-- Name: mm_metadata_album_name_trigram_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_album_name_trigram_idx ON public.mm_metadata_album USING gist (mm_metadata_album_name public.gist_trgm_ops);


--
-- Name: mm_metadata_aniem_idxgin_media_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_aniem_idxgin_media_id ON public.mm_metadata_anime USING gin (mm_metadata_anime_media_id);


--
-- Name: mm_metadata_anime_idx_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_anime_idx_name ON public.mm_metadata_anime USING btree (mm_media_anime_name);


--
-- Name: mm_metadata_anime_idx_name_lower; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_anime_idx_name_lower ON public.mm_metadata_anime USING btree (lower(mm_media_anime_name));


--
-- Name: mm_metadata_anime_idxgin_json; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_anime_idxgin_json ON public.mm_metadata_anime USING gin (mm_metadata_anime_json);


--
-- Name: mm_metadata_anime_idxgin_media_id_anidb; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_anime_idxgin_media_id_anidb ON public.mm_metadata_anime USING gin (((mm_metadata_anime_media_id -> 'anidb'::text)));


--
-- Name: mm_metadata_anime_idxgin_media_id_imdb; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_anime_idxgin_media_id_imdb ON public.mm_metadata_anime USING gin (((mm_metadata_anime_media_id -> 'imdb'::text)));


--
-- Name: mm_metadata_anime_idxgin_media_id_thetvdb; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_anime_idxgin_media_id_thetvdb ON public.mm_metadata_anime USING gin (((mm_metadata_anime_media_id -> 'thetvdb'::text)));


--
-- Name: mm_metadata_anime_idxgin_media_id_tmdb; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_anime_idxgin_media_id_tmdb ON public.mm_metadata_anime USING gin (((mm_metadata_anime_media_id -> 'tmdb'::text)));


--
-- Name: mm_metadata_anime_idxgin_user_json; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_anime_idxgin_user_json ON public.mm_metadata_anime USING gin (mm_metadata_anime_user_json);


--
-- Name: mm_metadata_book_name_trigram_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_book_name_trigram_idx ON public.mm_metadata_book USING gist (mm_metadata_book_name public.gist_trgm_ops);


--
-- Name: mm_metadata_collection_idxgin_media_json; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_collection_idxgin_media_json ON public.mm_metadata_collection USING gin (mm_metadata_collection_media_ids);


--
-- Name: mm_metadata_collection_idxgin_meta_json; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_collection_idxgin_meta_json ON public.mm_metadata_collection USING gin (mm_metadata_collection_json);


--
-- Name: mm_metadata_collection_idxgin_name_json; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_collection_idxgin_name_json ON public.mm_metadata_collection USING gin (mm_metadata_collection_name);


--
-- Name: mm_metadata_idx_band_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_idx_band_name ON public.mm_metadata_music_video USING btree (mm_media_music_video_band);


--
-- Name: mm_metadata_idx_band_name_lower; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_idx_band_name_lower ON public.mm_metadata_music_video USING btree (lower(mm_media_music_video_band));


--
-- Name: mm_metadata_idx_book_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_idx_book_name ON public.mm_metadata_book USING btree (mm_metadata_book_name);


--
-- Name: mm_metadata_idx_book_name_lower; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_idx_book_name_lower ON public.mm_metadata_book USING btree (lower(mm_metadata_book_name));


--
-- Name: mm_metadata_idx_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_idx_name ON public.mm_metadata_movie USING btree (mm_media_name);


--
-- Name: mm_metadata_idx_name_lower; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_idx_name_lower ON public.mm_metadata_movie USING btree (lower(mm_media_name));


--
-- Name: mm_metadata_idx_song_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_idx_song_name ON public.mm_metadata_music_video USING btree (mm_media_music_video_song);


--
-- Name: mm_metadata_idx_song_name_lower; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_idx_song_name_lower ON public.mm_metadata_music_video USING btree (lower(mm_media_music_video_song));


--
-- Name: mm_metadata_idxgin_isbn; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_idxgin_isbn ON public.mm_metadata_book USING btree (mm_metadata_book_isbn);


--
-- Name: mm_metadata_idxgin_isbn13; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_idxgin_isbn13 ON public.mm_metadata_book USING btree (mm_metadata_book_isbn13);


--
-- Name: mm_metadata_idxgin_json; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_idxgin_json ON public.mm_metadata_movie USING gin (mm_metadata_json);


--
-- Name: mm_metadata_idxgin_media_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_idxgin_media_id ON public.mm_metadata_movie USING gin (mm_metadata_media_id);


--
-- Name: mm_metadata_idxgin_media_id_imdb; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_idxgin_media_id_imdb ON public.mm_metadata_movie USING gin (((mm_metadata_media_id -> 'imdb'::text)));


--
-- Name: mm_metadata_idxgin_media_id_thetvdb; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_idxgin_media_id_thetvdb ON public.mm_metadata_movie USING gin (((mm_metadata_media_id -> 'thetvdb'::text)));


--
-- Name: mm_metadata_idxgin_media_id_tmdb; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_idxgin_media_id_tmdb ON public.mm_metadata_movie USING gin (((mm_metadata_media_id -> 'tmdb'::text)));


--
-- Name: mm_metadata_idxgin_music_video_json; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_idxgin_music_video_json ON public.mm_metadata_music_video USING gin (mm_metadata_music_video_json);


--
-- Name: mm_metadata_idxgin_music_video_media_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_idxgin_music_video_media_id ON public.mm_metadata_music_video USING gin (mm_metadata_music_video_media_id);


--
-- Name: mm_metadata_idxgin_music_video_media_id_imvdb; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_idxgin_music_video_media_id_imvdb ON public.mm_metadata_music_video USING gin (((mm_metadata_music_video_media_id -> 'imvdb'::text)));


--
-- Name: mm_metadata_idxgin_user_json; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_idxgin_user_json ON public.mm_metadata_movie USING gin (mm_metadata_user_json);


--
-- Name: mm_metadata_logo_idxgin_json; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_logo_idxgin_json ON public.mm_metadata_logo USING gin (mm_metadata_logo_media_guid);


--
-- Name: mm_metadata_music_idx_album; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_music_idx_album ON public.mm_metadata_music USING btree (mm_metadata_music_album_guid);


--
-- Name: mm_metadata_music_idx_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_music_idx_name ON public.mm_metadata_music USING btree (mm_metadata_music_name);


--
-- Name: mm_metadata_music_idx_name_lower; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_music_idx_name_lower ON public.mm_metadata_music USING btree (lower(mm_metadata_music_name));


--
-- Name: mm_metadata_music_idxgin_json; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_music_idxgin_json ON public.mm_metadata_music USING gin (mm_metadata_music_json);


--
-- Name: mm_metadata_music_idxgin_media_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_music_idxgin_media_id ON public.mm_metadata_music USING gin (mm_metadata_media_music_id);


--
-- Name: mm_metadata_music_idxgin_user_json; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_music_idxgin_user_json ON public.mm_metadata_music USING gin (mm_metadata_music_user_json);


--
-- Name: mm_metadata_music_name_trigram_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_music_name_trigram_idx ON public.mm_metadata_music USING gist (mm_metadata_music_name public.gist_trgm_ops);


--
-- Name: mm_metadata_music_video_idxgin_user_json; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_music_video_idxgin_user_json ON public.mm_metadata_music_video USING gin (mm_metadata_music_video_user_json);


--
-- Name: mm_metadata_musician_idx_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_musician_idx_name ON public.mm_metadata_musician USING btree (mm_metadata_musician_name);


--
-- Name: mm_metadata_musician_idx_name_lower; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_musician_idx_name_lower ON public.mm_metadata_musician USING btree (lower(mm_metadata_musician_name));


--
-- Name: mm_metadata_musician_idxgin_id_json; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_musician_idxgin_id_json ON public.mm_metadata_musician USING gin (mm_metadata_musician_id);


--
-- Name: mm_metadata_musician_idxgin_json; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_musician_idxgin_json ON public.mm_metadata_musician USING gin (mm_metadata_musician_json);


--
-- Name: mm_metadata_musician_name_trigram_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_musician_name_trigram_idx ON public.mm_metadata_musician USING gist (mm_metadata_musician_name public.gist_trgm_ops);


--
-- Name: mm_metadata_person_idx_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_person_idx_name ON public.mm_metadata_person USING btree (mmp_person_name);


--
-- Name: mm_metadata_person_idxgin_id_json; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_person_idxgin_id_json ON public.mm_metadata_person USING gin (mmp_person_media_id);


--
-- Name: mm_metadata_person_idxgin_meta_json; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_person_idxgin_meta_json ON public.mm_metadata_person USING gin (mmp_person_meta_json);


--
-- Name: mm_metadata_review_idx_metadata_uuid; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_review_idx_metadata_uuid ON public.mm_review USING btree (mm_review_metadata_guid);


--
-- Name: mm_metadata_review_idxgin_media_json; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_review_idxgin_media_json ON public.mm_review USING gin (mm_review_metadata_id);


--
-- Name: mm_metadata_sports_idx_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_sports_idx_name ON public.mm_metadata_sports USING btree (mm_metadata_sports_name);


--
-- Name: mm_metadata_sports_idx_name_lower; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_sports_idx_name_lower ON public.mm_metadata_sports USING btree (lower(mm_metadata_sports_name));


--
-- Name: mm_metadata_sports_idxgin_json; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_sports_idxgin_json ON public.mm_metadata_sports USING gin (mm_metadata_sports_json);


--
-- Name: mm_metadata_sports_idxgin_media_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_sports_idxgin_media_id ON public.mm_metadata_sports USING gin (mm_metadata_media_sports_id);


--
-- Name: mm_metadata_sports_idxgin_media_id_imdb; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_sports_idxgin_media_id_imdb ON public.mm_metadata_sports USING gin (((mm_metadata_media_sports_id -> 'imdb'::text)));


--
-- Name: mm_metadata_sports_idxgin_media_id_thesportsdb; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_sports_idxgin_media_id_thesportsdb ON public.mm_metadata_sports USING gin (((mm_metadata_media_sports_id -> 'thesportsdb'::text)));


--
-- Name: mm_metadata_sports_idxgin_media_id_thetvdb; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_sports_idxgin_media_id_thetvdb ON public.mm_metadata_sports USING gin (((mm_metadata_media_sports_id -> 'thetvdb'::text)));


--
-- Name: mm_metadata_sports_idxgin_media_id_thetvdbseries; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_sports_idxgin_media_id_thetvdbseries ON public.mm_metadata_sports USING gin (((mm_metadata_media_sports_id -> 'thetvdbSeries'::text)));


--
-- Name: mm_metadata_sports_idxgin_media_id_tmdb; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_sports_idxgin_media_id_tmdb ON public.mm_metadata_sports USING gin (((mm_metadata_media_sports_id -> 'tmdb'::text)));


--
-- Name: mm_metadata_sports_idxgin_media_id_tvmaze; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_sports_idxgin_media_id_tvmaze ON public.mm_metadata_sports USING gin (((mm_metadata_media_sports_id -> 'tvmaze'::text)));


--
-- Name: mm_metadata_sports_name_trigram_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_sports_name_trigram_idx ON public.mm_metadata_sports USING gist (mm_metadata_sports_name public.gist_trgm_ops);


--
-- Name: mm_metadata_tvshow_idx_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_tvshow_idx_name ON public.mm_metadata_tvshow USING btree (mm_metadata_tvshow_name);


--
-- Name: mm_metadata_tvshow_idx_name_lower; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_tvshow_idx_name_lower ON public.mm_metadata_tvshow USING btree (lower(mm_metadata_tvshow_name));


--
-- Name: mm_metadata_tvshow_idxgin_json; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_tvshow_idxgin_json ON public.mm_metadata_tvshow USING gin (mm_metadata_tvshow_json);


--
-- Name: mm_metadata_tvshow_idxgin_localimage_json; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_tvshow_idxgin_localimage_json ON public.mm_metadata_tvshow USING gin (mm_metadata_tvshow_json);


--
-- Name: mm_metadata_tvshow_idxgin_media_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_tvshow_idxgin_media_id ON public.mm_metadata_tvshow USING gin (mm_metadata_media_tvshow_id);


--
-- Name: mm_metadata_tvshow_idxgin_media_id_imdb; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_tvshow_idxgin_media_id_imdb ON public.mm_metadata_tvshow USING gin (((mm_metadata_media_tvshow_id -> 'imdb'::text)));


--
-- Name: mm_metadata_tvshow_idxgin_media_id_thetvdb; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_tvshow_idxgin_media_id_thetvdb ON public.mm_metadata_tvshow USING gin (((mm_metadata_media_tvshow_id -> 'thetvdb'::text)));


--
-- Name: mm_metadata_tvshow_idxgin_media_id_thetvdbseries; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_tvshow_idxgin_media_id_thetvdbseries ON public.mm_metadata_tvshow USING gin (((mm_metadata_media_tvshow_id -> 'thetvdbSeries'::text)));


--
-- Name: mm_metadata_tvshow_idxgin_media_id_tmdb; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_tvshow_idxgin_media_id_tmdb ON public.mm_metadata_tvshow USING gin (((mm_metadata_media_tvshow_id -> 'tmdb'::text)));


--
-- Name: mm_metadata_tvshow_idxgin_media_id_tvmaze; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_tvshow_idxgin_media_id_tvmaze ON public.mm_metadata_tvshow USING gin (((mm_metadata_media_tvshow_id -> 'tvmaze'::text)));


--
-- Name: mm_metadata_tvshow_idxgin_user_json; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_tvshow_idxgin_user_json ON public.mm_metadata_tvshow USING gin (mm_metadata_tvshow_user_json);


--
-- Name: mm_metadata_tvshow_name_trigram_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_tvshow_name_trigram_idx ON public.mm_metadata_tvshow USING gist (mm_metadata_tvshow_name public.gist_trgm_ops);


--
-- Name: mm_notification_idx_dismissable; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_notification_idx_dismissable ON public.mm_notification USING btree (mm_notification_dismissable);


--
-- Name: mm_notification_idx_time; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_notification_idx_time ON public.mm_notification USING btree (mm_notification_time);


--
-- Name: mm_sync_idxgin_json; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_sync_idxgin_json ON public.mm_sync USING gin (mm_sync_options_json);


--
-- Name: mm_tv_schedule_idx_date; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_tv_schedule_idx_date ON public.mm_tv_schedule USING btree (mm_tv_schedule_date);


--
-- Name: mm_tv_schedule_idx_program; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_tv_schedule_idx_program ON public.mm_tv_schedule_program USING btree (mm_tv_schedule_program_id);


--
-- Name: mm_tv_schedule_idx_station; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_tv_schedule_idx_station ON public.mm_tv_schedule USING btree (mm_tv_schedule_station_id);


--
-- Name: mm_tv_stations_idx_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_tv_stations_idx_name ON public.mm_tv_stations USING btree (mm_tv_station_name);


--
-- Name: mm_tv_stations_idx_station; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_tv_stations_idx_station ON public.mm_tv_stations USING btree (mm_tv_station_id);


--
-- Name: mm_user_activity_idx_date; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_user_activity_idx_date ON public.mm_user_activity USING btree (mm_activity_datecreated);


--
-- Name: mm_user_activity_idx_user_guid; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_user_activity_idx_user_guid ON public.mm_user_activity USING btree (mm_activity_userid);


--
-- Name: mm_user_group_idx_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_user_group_idx_name ON public.mm_user_group USING btree (mm_user_group_name);


--
-- Name: mm_user_idx_username; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_user_idx_username ON public.mm_user USING btree (username);


--
-- Name: mm_user_profile_idx_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_user_profile_idx_name ON public.mm_user_profile USING btree (mm_user_profile_name);


--
-- Name: mmp_person_name_trigram_idx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mmp_person_name_trigram_idx ON public.mm_metadata_person USING gist (mmp_person_name public.gist_trgm_ops);


--
-- Name: mmr_media_idx_link_uuid; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mmr_media_idx_link_uuid ON public.mm_media_remote USING btree (mmr_media_link_id);


--
-- Name: mmr_media_idx_metadata_uuid; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mmr_media_idx_metadata_uuid ON public.mm_media_remote USING btree (mmr_media_metadata_guid);


--
-- Name: mmr_media_idxgin_ffprobe; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mmr_media_idxgin_ffprobe ON public.mm_media_remote USING gin (mmr_media_ffprobe_json);


--
-- PostgreSQL database dump complete
--


