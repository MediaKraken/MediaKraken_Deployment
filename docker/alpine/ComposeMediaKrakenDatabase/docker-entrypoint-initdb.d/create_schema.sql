--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.3
-- Dumped by pg_dump version 9.6.4

-- Started on 2017-08-19 20:19:14 CDT

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
-- TOC entry 2606 (class 0 OID 0)
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
-- TOC entry 2607 (class 0 OID 0)
-- Dependencies: 2
-- Name: EXTENSION pg_trgm; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION pg_trgm IS 'text similarity measurement and index searching based on trigrams';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- TOC entry 215 (class 1259 OID 26174)
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
-- TOC entry 209 (class 1259 OID 26127)
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
-- TOC entry 224 (class 1259 OID 26263)
-- Name: mm_device; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE mm_device (
    mm_device_id uuid NOT NULL,
    mm_device_type text,
    mm_device_json jsonb
);


ALTER TABLE mm_device OWNER TO metamanpg;

--
-- TOC entry 223 (class 1259 OID 26254)
-- Name: mm_download_image_que; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE mm_download_image_que (
    mdq_image_id uuid NOT NULL,
    mdq_image_provider text,
    mdq_image_download_json jsonb
);


ALTER TABLE mm_download_image_que OWNER TO metamanpg;

--
-- TOC entry 222 (class 1259 OID 26243)
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
-- TOC entry 191 (class 1259 OID 25912)
-- Name: mm_link; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE mm_link (
    mm_link_guid uuid NOT NULL,
    mm_link_name text,
    mm_link_json jsonb
);


ALTER TABLE mm_link OWNER TO metamanpg;

--
-- TOC entry 212 (class 1259 OID 26152)
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
-- TOC entry 189 (class 1259 OID 25890)
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
-- TOC entry 197 (class 1259 OID 25997)
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
-- TOC entry 188 (class 1259 OID 25881)
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
-- TOC entry 190 (class 1259 OID 25901)
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
-- TOC entry 187 (class 1259 OID 25873)
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
-- TOC entry 195 (class 1259 OID 25971)
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
-- TOC entry 198 (class 1259 OID 26006)
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
-- TOC entry 201 (class 1259 OID 26054)
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
-- TOC entry 207 (class 1259 OID 26108)
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
-- TOC entry 219 (class 1259 OID 26212)
-- Name: mm_metadata_game_software_info; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE mm_metadata_game_software_info (
    gi_id uuid NOT NULL,
    gi_system_id uuid,
    gi_game_info_json jsonb
);


ALTER TABLE mm_metadata_game_software_info OWNER TO metamanpg;

--
-- TOC entry 220 (class 1259 OID 26223)
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
-- TOC entry 214 (class 1259 OID 26165)
-- Name: mm_metadata_logo; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE mm_metadata_logo (
    mm_metadata_logo_guid uuid NOT NULL,
    mm_metadata_logo_media_guid jsonb,
    mm_metadata_logo_image_path text
);


ALTER TABLE mm_metadata_logo OWNER TO metamanpg;

--
-- TOC entry 199 (class 1259 OID 26023)
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
-- TOC entry 196 (class 1259 OID 25984)
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
-- TOC entry 200 (class 1259 OID 26039)
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
-- TOC entry 194 (class 1259 OID 25959)
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
-- TOC entry 221 (class 1259 OID 26232)
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
-- TOC entry 193 (class 1259 OID 25941)
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
-- TOC entry 192 (class 1259 OID 25922)
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
-- TOC entry 203 (class 1259 OID 26076)
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
-- TOC entry 218 (class 1259 OID 26204)
-- Name: mm_options_and_status; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE mm_options_and_status (
    mm_options_and_status_guid uuid NOT NULL,
    mm_options_json jsonb,
    mm_status_json jsonb
);


ALTER TABLE mm_options_and_status OWNER TO metamanpg;

--
-- TOC entry 210 (class 1259 OID 26135)
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
-- TOC entry 206 (class 1259 OID 26098)
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
-- TOC entry 211 (class 1259 OID 26143)
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
-- TOC entry 208 (class 1259 OID 26119)
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
-- TOC entry 213 (class 1259 OID 26157)
-- Name: mm_trigger; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE mm_trigger (
    mm_trigger_guid uuid NOT NULL,
    mm_trigger_command bytea,
    mm_trigger_background boolean
);


ALTER TABLE mm_trigger OWNER TO metamanpg;

--
-- TOC entry 226 (class 1259 OID 26283)
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
-- TOC entry 227 (class 1259 OID 26293)
-- Name: mm_tv_schedule_program; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE mm_tv_schedule_program (
    mm_tv_schedule_program_guid uuid NOT NULL,
    mm_tv_schedule_program_id text,
    mm_tv_schedule_program_json jsonb
);


ALTER TABLE mm_tv_schedule_program OWNER TO metamanpg;

--
-- TOC entry 225 (class 1259 OID 26273)
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
-- TOC entry 205 (class 1259 OID 26088)
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
-- TOC entry 202 (class 1259 OID 26066)
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
-- TOC entry 216 (class 1259 OID 26186)
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
-- TOC entry 204 (class 1259 OID 26086)
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
-- TOC entry 2608 (class 0 OID 0)
-- Dependencies: 204
-- Name: mm_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: metamanpg
--

ALTER SEQUENCE mm_user_id_seq OWNED BY mm_user.id;


--
-- TOC entry 217 (class 1259 OID 26195)
-- Name: mm_user_profile; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE mm_user_profile (
    mm_user_profile_guid uuid NOT NULL,
    mm_user_profile_name text,
    mm_user_profile_json jsonb
);


ALTER TABLE mm_user_profile OWNER TO metamanpg;

--
-- TOC entry 186 (class 1259 OID 25870)
-- Name: mm_version; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE mm_version (
    mm_version_no integer
);


ALTER TABLE mm_version OWNER TO metamanpg;

--
-- TOC entry 2240 (class 2604 OID 26091)
-- Name: mm_user id; Type: DEFAULT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_user ALTER COLUMN id SET DEFAULT nextval('mm_user_id_seq'::regclass);


--
-- TOC entry 2587 (class 0 OID 26174)
-- Dependencies: 215
-- Data for Name: mm_channel; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_channel (mm_channel_guid, mm_channel_name, mm_channel_media_id, mm_channel_country_guid, mm_channel_logo_guid) FROM stdin;
\.


--
-- TOC entry 2581 (class 0 OID 26127)
-- Dependencies: 209
-- Data for Name: mm_cron; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_cron (mm_cron_guid, mm_cron_name, mm_cron_description, mm_cron_enabled, mm_cron_schedule, mm_cron_last_run, mm_cron_file_path) FROM stdin;
\.


--
-- TOC entry 2596 (class 0 OID 26263)
-- Dependencies: 224
-- Data for Name: mm_device; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_device (mm_device_id, mm_device_type, mm_device_json) FROM stdin;
\.


--
-- TOC entry 2595 (class 0 OID 26254)
-- Dependencies: 223
-- Data for Name: mm_download_image_que; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_download_image_que (mdq_image_id, mdq_image_provider, mdq_image_download_json) FROM stdin;
\.


--
-- TOC entry 2594 (class 0 OID 26243)
-- Dependencies: 222
-- Data for Name: mm_download_que; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_download_que (mdq_id, mdq_provider, mdq_que_type, mdq_download_json) FROM stdin;
\.


--
-- TOC entry 2563 (class 0 OID 25912)
-- Dependencies: 191
-- Data for Name: mm_link; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_link (mm_link_guid, mm_link_name, mm_link_json) FROM stdin;
\.


--
-- TOC entry 2584 (class 0 OID 26152)
-- Dependencies: 212
-- Data for Name: mm_loan; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_loan (mm_loan_guid, mm_loan_media_id, mm_loan_user_id, mm_load_user_loan_id, mm_loan_time, mm_loan_return_time) FROM stdin;
\.


--
-- TOC entry 2561 (class 0 OID 25890)
-- Dependencies: 189
-- Data for Name: mm_media; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_media (mm_media_guid, mm_media_class_guid, mm_media_metadata_guid, mm_media_path, mm_media_ffprobe_json, mm_media_json) FROM stdin;
\.


--
-- TOC entry 2569 (class 0 OID 25997)
-- Dependencies: 197
-- Data for Name: mm_media_class; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_media_class (mm_media_class_guid, mm_media_class_type, mm_media_class_parent_type, mm_media_class_display) FROM stdin;
c23fca10-2e01-4e9e-936f-3b426dd3f467	Adult	Video	t
7de26d86-bbdd-4d35-990e-cdb16932a4b3	Anime	Video	t
0fa910fa-d8f0-4f89-92ec-427cfaa701da	Book	Publication	t
4d87384a-7b0b-4db9-b4f5-71b2b3c0d267	Boxset	\N	f
d9115cf4-4610-451d-997e-2ddc615050d5	Game CHD	\N	f
eab7e940-dbf4-4555-91e5-9768d93da0b6	Game ISO	\N	f
dd70784d-0a53-4e4b-891a-17b7d57520ca	Game ROM	\N	f
98787d09-ea5f-40c5-b5d8-a28c3a685c26	Home Movie	Video	t
7b892f44-a251-487f-881b-528c36746336	Magazine	Publication	t
0189aff4-2522-48a0-a8aa-912f2a4873b6	Movie	Video	t
84ad8013-a50e-41ef-96cb-cc8334dbefe1	Movie Extras	Video	f
ce8d10ac-b69d-44ed-943f-3d030320833d	Movie Collection	\N	f
cbb65baf-15fe-4c15-9dfa-1e4e64a2242d	Movie Theme	Audio	f
23fce6b0-0323-4041-8b32-9a50c807ff0b	Movie Trailer	Video	f
69b40a5b-0226-49c2-aed5-115b4a3da2ac	Music	Audio	t
96807d03-49a9-4ccf-a9f7-d8aef3f05c5e	Music Album	\N	f
a94663ba-a86b-4e48-aac1-c8c2c6734d33	Music Collection	\N	f
eabb9498-bba7-4a55-9557-c2702f2bae4d	Music Lyric	\N	f
95716b34-04eb-4242-abce-ced0b9048387	Music Video	Video	t
62f91b57-87db-4ecb-bdc3-58798afc5bda	Person	\N	f
d1e71402-c3c3-4a61-b566-edcb5bbe5a43	Picture	Image	t
517bc2d1-edae-477c-a9fa-2502d1f46e56	Soundtrack	Audio	f
a4564f64-c3db-4933-9105-f76561f3f2e7	Sports	Video	t
8fc7339c-a96c-43e3-9dd0-759a681ef8fa	Subtitle	\N	f
e77ac035-7291-4cea-b1cf-1204d948cfc9	TV Episode	Video	f
11f36cf9-d884-4e55-8f47-e54797c82a58	TV Extras	Video	f
a6b4c8a0-62df-48a1-bcdc-64508e9d77fe	TV Season	\N	f
8204b60a-cc0b-4a60-99d0-129309a31af4	TV Show	Video	t
7a7656eb-39e7-4967-b9b3-62d50cbd13c7	TV Theme	Audio	f
f068a5ab-3eb4-4430-85e9-d3017033eadd	TV Trailer	Video	f
45c33b73-fc9e-4282-bd9c-fb572f22a8d8	Video Game	Game	t
b3711d1c-bfce-49ad-bf9f-4adf1504c55f	Video Game Intro	Video	t
0825e0f9-cc77-48c1-ade1-aa8bcd6009f9	Video Game Speedrun	Video	t
70f8f4ef-95c2-4363-8555-ce1803d4fbfa	Video Game Superplay	Video	t
\.


--
-- TOC entry 2560 (class 0 OID 25881)
-- Dependencies: 188
-- Data for Name: mm_media_dir; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_media_dir (mm_media_dir_guid, mm_media_dir_path, mm_media_dir_class_type, mm_media_dir_last_scanned, mm_media_dir_share_guid, mm_media_dir_status) FROM stdin;
\.


--
-- TOC entry 2562 (class 0 OID 25901)
-- Dependencies: 190
-- Data for Name: mm_media_remote; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_media_remote (mmr_media_guid, mmr_media_link_id, mmr_media_uuid, mmr_media_class_guid, mmr_media_metadata_guid, mmr_media_ffprobe_json, mmr_media_json) FROM stdin;
\.


--
-- TOC entry 2559 (class 0 OID 25873)
-- Dependencies: 187
-- Data for Name: mm_media_share; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_media_share (mm_media_share_guid, mm_media_share_type, mm_media_share_user, mm_media_share_password, mm_media_share_server, mm_media_share_path) FROM stdin;
\.


--
-- TOC entry 2567 (class 0 OID 25971)
-- Dependencies: 195
-- Data for Name: mm_metadata_album; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_metadata_album (mm_metadata_album_guid, mm_metadata_album_name, mm_metadata_album_id, mm_metadata_album_json, mm_metadata_album_musician_guid) FROM stdin;
\.


--
-- TOC entry 2570 (class 0 OID 26006)
-- Dependencies: 198
-- Data for Name: mm_metadata_anime; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_metadata_anime (mm_metadata_anime_guid, mm_metadata_anime_media_id, mm_media_anime_name, mm_metadata_anime_json, mm_metadata_anime_mapping, mm_metadata_anime_mapping_before, mm_metadata_anime_localimage_json, mm_metadata_anime_user_json) FROM stdin;
\.


--
-- TOC entry 2573 (class 0 OID 26054)
-- Dependencies: 201
-- Data for Name: mm_metadata_book; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_metadata_book (mm_metadata_book_guid, mm_metadata_book_isbn, mm_metadata_book_isbn13, mm_metadata_book_name, mm_metadata_book_json, mm_metadata_book_image_json) FROM stdin;
\.


--
-- TOC entry 2579 (class 0 OID 26108)
-- Dependencies: 207
-- Data for Name: mm_metadata_collection; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_metadata_collection (mm_metadata_collection_guid, mm_metadata_collection_name, mm_metadata_collection_media_ids, mm_metadata_collection_json, mm_metadata_collection_imagelocal_json) FROM stdin;
\.


--
-- TOC entry 2591 (class 0 OID 26212)
-- Dependencies: 219
-- Data for Name: mm_metadata_game_software_info; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_metadata_game_software_info (gi_id, gi_system_id, gi_game_info_json) FROM stdin;
\.


--
-- TOC entry 2592 (class 0 OID 26223)
-- Dependencies: 220
-- Data for Name: mm_metadata_game_systems_info; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_metadata_game_systems_info (gs_id, gs_game_system_id, gs_game_system_name, gs_game_system_alias, gs_game_system_json) FROM stdin;
\.


--
-- TOC entry 2586 (class 0 OID 26165)
-- Dependencies: 214
-- Data for Name: mm_metadata_logo; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_metadata_logo (mm_metadata_logo_guid, mm_metadata_logo_media_guid, mm_metadata_logo_image_path) FROM stdin;
\.


--
-- TOC entry 2571 (class 0 OID 26023)
-- Dependencies: 199
-- Data for Name: mm_metadata_movie; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_metadata_movie (mm_metadata_guid, mm_metadata_media_id, mm_media_name, mm_metadata_json, mm_metadata_localimage_json, mm_metadata_user_json) FROM stdin;
\.


--
-- TOC entry 2568 (class 0 OID 25984)
-- Dependencies: 196
-- Data for Name: mm_metadata_music; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_metadata_music (mm_metadata_music_guid, mm_metadata_media_music_id, mm_metadata_music_name, mm_metadata_music_json, mm_metadata_music_album_guid) FROM stdin;
\.


--
-- TOC entry 2572 (class 0 OID 26039)
-- Dependencies: 200
-- Data for Name: mm_metadata_music_video; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_metadata_music_video (mm_metadata_music_video_guid, mm_metadata_music_video_media_id, mm_media_music_video_band, mm_media_music_video_song, mm_metadata_music_video_json, mm_metadata_music_video_localimage_json) FROM stdin;
\.


--
-- TOC entry 2566 (class 0 OID 25959)
-- Dependencies: 194
-- Data for Name: mm_metadata_musician; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_metadata_musician (mm_metadata_musician_guid, mm_metadata_musician_name, mm_metadata_musician_id, mm_metadata_musician_json) FROM stdin;
\.


--
-- TOC entry 2593 (class 0 OID 26232)
-- Dependencies: 221
-- Data for Name: mm_metadata_person; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_metadata_person (mmp_id, mmp_person_media_id, mmp_person_meta_json, mmp_person_image, mmp_person_name) FROM stdin;
\.


--
-- TOC entry 2565 (class 0 OID 25941)
-- Dependencies: 193
-- Data for Name: mm_metadata_sports; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_metadata_sports (mm_metadata_sports_guid, mm_metadata_media_sports_id, mm_metadata_sports_name, mm_metadata_sports_json, mm_metadata_sports_image_json) FROM stdin;
\.


--
-- TOC entry 2564 (class 0 OID 25922)
-- Dependencies: 192
-- Data for Name: mm_metadata_tvshow; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_metadata_tvshow (mm_metadata_tvshow_guid, mm_metadata_media_tvshow_id, mm_metadata_tvshow_name, mm_metadata_tvshow_json, mm_metadata_tvshow_localimage_json, mm_metadata_tvshow_user_json) FROM stdin;
\.


--
-- TOC entry 2575 (class 0 OID 26076)
-- Dependencies: 203
-- Data for Name: mm_notification; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_notification (mm_notification_guid, mm_notification_text, mm_notification_time, mm_notification_dismissable) FROM stdin;
\.


--
-- TOC entry 2590 (class 0 OID 26204)
-- Dependencies: 218
-- Data for Name: mm_options_and_status; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_options_and_status (mm_options_and_status_guid, mm_options_json, mm_status_json) FROM stdin;
f1f8983d-56f9-438d-bd48-48cf596c6964	{"SD": {"User": null, "Password": null}, "API": {"anidb": null, "imvdb": null, "google": null, "isbndb": "25C8IT4I", "tvmaze": null, "thetvdb": "147CB43DCA8B61B7", "thelogodb": null, "themoviedb": "f72118d1e84b8a1438935972a9c37cac", "globalcache": null, "mediabrainz": null, "thesportsdb": "4352761817344", "opensubtitles": null, "rottentomatoes": "f4tnu5dn9r7f28gjth3ftqaj"}, "AWSS3": {"Bucket": "mediakraken", "AccessKey": null, "BackupBucket": "mkbackup", "SecretAccessKey": null}, "Trakt": {"ApiKey": null, "ClientID": null, "SecretKey": null}, "Backup": {"Interval": 0, "BackupType": "local"}, "Docker": {"Nodes": 0, "SwarmID": null, "Instances": 0}, "Dropbox": {"APIKey": null, "APISecret": null}, "Trailer": {"Clip": false, "Behind": false, "Carpool": false, "Trailer": false, "Featurette": false}, "OneDrive": {"ClientID": null, "SecretKey": null}, "GoogleDrive": {"SecretFile": null}, "Maintenance": null, "MediaBrainz": {"Host": null, "Port": 5000, "User": null, "Password": null, "BrainzDBHost": null, "BrainzDBName": null, "BrainzDBPass": null, "BrainzDBPort": 5432, "BrainzDBUser": null}, "MaxResumePct": 5, "Transmission": {"Host": null, "Port": 9091}, "MediaKrakenServer": {"APIPort": 8097, "ListenPort": 8098, "BackupLocal": "/mediakraken/backups/"}}	{"thetvdb_Updated_Epoc": 0}
\.


--
-- TOC entry 2582 (class 0 OID 26135)
-- Dependencies: 210
-- Data for Name: mm_radio; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_radio (mm_radio_guid, mm_radio_name, mm_radio_adress, mm_radio_active) FROM stdin;
\.


--
-- TOC entry 2578 (class 0 OID 26098)
-- Dependencies: 206
-- Data for Name: mm_review; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_review (mm_review_guid, mm_review_metadata_id, mm_review_metadata_guid, mm_review_json) FROM stdin;
\.


--
-- TOC entry 2583 (class 0 OID 26143)
-- Dependencies: 211
-- Data for Name: mm_sync; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_sync (mm_sync_guid, mm_sync_path, mm_sync_path_to, mm_sync_options_json) FROM stdin;
\.


--
-- TOC entry 2580 (class 0 OID 26119)
-- Dependencies: 208
-- Data for Name: mm_task; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_task (mm_task_guid, mm_task_name, mm_task_description, mm_task_enabled, mm_task_schedule, mm_task_last_run, mm_task_file_path, mm_task_json) FROM stdin;
2934ffbc-331c-494b-ad84-5c8f29e67466	Anime	Match anime via Scudlee data	f	Days 1	1970-01-01 00:00:01	/mediakraken/subprogram_match_anime_id_scudlee.py	{"task": "anime", "route_key": "Z", "exchange_key": "mkque_metadata_ex"}
02dbc7c7-c706-489a-a298-6194c4d75671	Collections	Create and update collection(s)	f	Days 1	1970-01-01 00:00:01	/mediakraken/subprogram_metadata_update_create_collections.py	{"task": "collection", "route_key": "themoviedb", "exchange_key": "mkque_metadata_ex"}
a6011bbb-bbb5-4bb1-857f-503fd71b86f8	Create Chapter Image	Create chapter images for all media	f	Days 1	1970-01-01 00:00:01	/mediakraken/subprogram_create_chapter_images.py	{"task": "chapter", "route_key": "mkque", "exchange_key": "mkque_ex"}
ac798730-5588-4ab8-bf92-da18aee55a31	Roku Thumb	Generate Roku thumbnail images	f	Days 1	1970-01-01 00:00:01	/mediakraken/subprogram_roku_thumbnail_generate.py	{"task": "rokuthumbnail", "route_key": "mkque", "exchange_key": "mkque_ex"}
99c7bd0f-872d-45dd-a04e-88f5b3a2edc7	Schedules Direct	Fetch TV schedules from Schedules Direct	f	Days 1	1970-01-01 00:00:01	/mediakraken/subprogram_schedules_direct_updates.py	{"task": "update", "route_key": "schedulesdirect", "exchange_key": "mkque_metadata_ex"}
7447f71f-5ac1-40eb-b335-795ca7449452	Subtitle	Download missing subtitles for media	f	Days 1	1970-01-01 00:00:01	/mediakraken/subprogram_subtitle_downloader.py	{"task": "subtitle", "route_key": "Z", "exchange_key": "mkque_metadata_ex"}
9197bd7c-3d9c-4b94-b7da-bf2217202ba7	The Movie Database	Grab updated movie metadata	f	Days 1	1970-01-01 00:00:01	/mediakraken/subprogram_metadata_tmdb_updates.py	{"task": "update", "route_key": "themoviedb", "exchange_key": "mkque_metadata_ex"}
f32bda5f-e531-4af6-b8f7-d6e90a507ae6	TheTVDB Update	Grab updated TheTVDB metadata	f	Days 1	1970-01-01 00:00:01	/mediakraken/subprogram_metadata_thetvdb_updates.py	{"task": "update", "route_key": "thetvdb", "exchange_key": "mkque_metadata_ex"}
4113828f-79ce-4c0a-9c77-04f18d33a162	TVmaze Update	Grab updated TVmaze metadata	f	Days 1	1970-01-01 00:00:01	/mediakraken/subprogram_metadata_tvmaze_updates.py	{"task": "update", "route_key": "tvmaze", "exchange_key": "mkque_metadata_ex"}
c7af96a6-6b1d-4fec-a483-8e6ea9fa0acc	Trailer	Download new trailers	f	Days 1	1970-01-01 00:00:01	/mediakraken/subprogram_metadata_trailer_download.py	{"task": "trailer", "route_key": "Z", "exchange_key": "mkque_metadata_ex"}
73eda2e2-425c-4186-99a5-161bdf36d418	Backup	Backup Postgresql DB	f	Days 1	1970-01-01 00:00:01	/mediakraken/subprogram_postgresql_backup.py	{"task": "dbbackup", "route_key": "mkque", "exchange_key": "mkque_ex"}
570d6d32-9e75-4069-9ec6-1af9f91d739e	DB Vacuum	Postgresql Vacuum Analyze all tables	f	Days 1	1970-01-01 00:00:01	/mediakraken/subprogram_postgresql_vacuum.py	{"task": "dbvacuum", "route_key": "mkque", "exchange_key": "mkque_ex"}
56e432b9-b1e4-4224-b6eb-72ca8b5abe49	iRadio Scan	Scan for iRadio stations	f	Days 1	1970-01-01 00:00:01	/mediakraken/subprogram_iradio_channels.py	{"task": "iradio", "route_key": "mkque", "exchange_key": "mkque_ex"}
a4b0456c-3fc0-45fe-9dd8-5748907b7d04	Media Scan	Scan for new media	f	Days 1	1970-01-01 00:00:01	/mediakraken/subprogram_file_scan.py	{"task": "scan", "route_key": "mkque", "exchange_key": "mkque_ex"}
efb59575-0ece-4d0b-96cc-5156fd838e96	Sync	Sync/Transcode media	f	Days 1	1970-01-01 00:00:01	/mediakraken/subprogram_sync.py	{"task": "sync", "route_key": "mkque", "exchange_key": "mkque_ex"}
\.


--
-- TOC entry 2585 (class 0 OID 26157)
-- Dependencies: 213
-- Data for Name: mm_trigger; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_trigger (mm_trigger_guid, mm_trigger_command, mm_trigger_background) FROM stdin;
\.


--
-- TOC entry 2598 (class 0 OID 26283)
-- Dependencies: 226
-- Data for Name: mm_tv_schedule; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_tv_schedule (mm_tv_schedule_id, mm_tv_schedule_station_id, mm_tv_schedule_date, mm_tv_schedule_json) FROM stdin;
\.


--
-- TOC entry 2599 (class 0 OID 26293)
-- Dependencies: 227
-- Data for Name: mm_tv_schedule_program; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_tv_schedule_program (mm_tv_schedule_program_guid, mm_tv_schedule_program_id, mm_tv_schedule_program_json) FROM stdin;
\.


--
-- TOC entry 2597 (class 0 OID 26273)
-- Dependencies: 225
-- Data for Name: mm_tv_stations; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_tv_stations (mm_tv_stations_id, mm_tv_station_name, mm_tv_station_id, mm_tv_station_channel, mm_tv_station_json, mm_tv_station_image) FROM stdin;
\.


--
-- TOC entry 2577 (class 0 OID 26088)
-- Dependencies: 205
-- Data for Name: mm_user; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_user (id, username, email, password, created_at, active, is_admin, user_json, lang) FROM stdin;
\.


--
-- TOC entry 2574 (class 0 OID 26066)
-- Dependencies: 202
-- Data for Name: mm_user_activity; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_user_activity (mm_activity_guid, mm_activity_name, mm_activity_overview, mm_activity_short_overview, mm_activity_type, mm_activity_itemid, mm_activity_userid, mm_activity_datecreated, mm_activity_log_severity) FROM stdin;
\.


--
-- TOC entry 2588 (class 0 OID 26186)
-- Dependencies: 216
-- Data for Name: mm_user_group; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_user_group (mm_user_group_guid, mm_user_group_name, mm_user_group_description, mm_user_group_rights_json) FROM stdin;
84040aa8-933f-42bb-b2f9-c24a408c8dfa	Administrator	Server administrator	{"Admin": true, "PreviewOnly": false}
5e22a2de-1597-40b6-b47d-57fe2381bb15	User	General user	{"Admin": false, "PreviewOnly": false}
5dc3e09b-b3b3-4eb8-9071-967486551fb4	Guest	Guest (Preview only)	{"Admin": false, "PreviewOnly": true}
\.


--
-- TOC entry 2609 (class 0 OID 0)
-- Dependencies: 204
-- Name: mm_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: metamanpg
--

SELECT pg_catalog.setval('mm_user_id_seq', 1, false);


--
-- TOC entry 2589 (class 0 OID 26195)
-- Dependencies: 217
-- Data for Name: mm_user_profile; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_user_profile (mm_user_profile_guid, mm_user_profile_name, mm_user_profile_json) FROM stdin;
835d11bd-0ddb-4c4c-bb72-2e990bf8e7c4	Adult	{"3D": true, "TV": true, "Home": true, "Lang": "en", "Sync": true, "Adult": true, "Books": true, "Games": true, "MaxBR": 100, "Movie": true, "Music": true, "IRadio": true, "Images": true, "LiveTV": true, "Sports": true, "Internet": true, "MaxRating": 5}
8bfb9734-62ac-4df9-9fc1-485a0ad79a18	Teen	{"3D": true, "TV": true, "Home": true, "Lang": "en", "Sync": false, "Adult": false, "Books": true, "Games": true, "MaxBR": 50, "Movie": true, "Music": true, "IRadio": true, "Images": true, "LiveTV": true, "Sports": true, "Internet": true, "MaxRating": 3}
8a6c2588-5046-4bab-ba30-ba34c2629e9f	Child	{"3D": false, "TV": true, "Home": true, "Lang": "en", "Sync": false, "Adult": false, "Books": true, "Games": true, "MaxBR": 20, "Movie": true, "Music": true, "IRadio": false, "Images": true, "LiveTV": false, "Sports": true, "Internet": false, "MaxRating": 0}
\.


--
-- TOC entry 2558 (class 0 OID 25870)
-- Dependencies: 186
-- Data for Name: mm_version; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_version (mm_version_no) FROM stdin;
8
\.


--
-- TOC entry 2405 (class 2606 OID 26219)
-- Name: mm_metadata_game_software_info gi_id_mpk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_metadata_game_software_info
    ADD CONSTRAINT gi_id_mpk PRIMARY KEY (gi_id);


--
-- TOC entry 2410 (class 2606 OID 26230)
-- Name: mm_metadata_game_systems_info gs_id_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_metadata_game_systems_info
    ADD CONSTRAINT gs_id_pk PRIMARY KEY (gs_id);


--
-- TOC entry 2419 (class 2606 OID 26250)
-- Name: mm_download_que mdq_id_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_download_que
    ADD CONSTRAINT mdq_id_pk PRIMARY KEY (mdq_id);


--
-- TOC entry 2424 (class 2606 OID 26261)
-- Name: mm_download_image_que mdq_image_id_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_download_image_que
    ADD CONSTRAINT mdq_image_id_pk PRIMARY KEY (mdq_image_id);


--
-- TOC entry 2355 (class 2606 OID 26073)
-- Name: mm_user_activity mm_activity_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_user_activity
    ADD CONSTRAINT mm_activity_pk PRIMARY KEY (mm_activity_guid);


--
-- TOC entry 2391 (class 2606 OID 26181)
-- Name: mm_channel mm_channel_guid_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_channel
    ADD CONSTRAINT mm_channel_guid_pk PRIMARY KEY (mm_channel_guid);


--
-- TOC entry 2377 (class 2606 OID 26134)
-- Name: mm_cron mm_cron_guid_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_cron
    ADD CONSTRAINT mm_cron_guid_pk PRIMARY KEY (mm_cron_guid);


--
-- TOC entry 2427 (class 2606 OID 26270)
-- Name: mm_device mm_device_id_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_device
    ADD CONSTRAINT mm_device_id_pk PRIMARY KEY (mm_device_id);


--
-- TOC entry 2257 (class 2606 OID 25919)
-- Name: mm_link mm_link_guid_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_link
    ADD CONSTRAINT mm_link_guid_pk PRIMARY KEY (mm_link_guid);


--
-- TOC entry 2384 (class 2606 OID 26156)
-- Name: mm_loan mm_loan_guid_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_loan
    ADD CONSTRAINT mm_loan_guid_pk PRIMARY KEY (mm_loan_guid);


--
-- TOC entry 2312 (class 2606 OID 26004)
-- Name: mm_media_class mm_media_class_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_media_class
    ADD CONSTRAINT mm_media_class_pk PRIMARY KEY (mm_media_class_guid);


--
-- TOC entry 2245 (class 2606 OID 25888)
-- Name: mm_media_dir mm_media_dir_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_media_dir
    ADD CONSTRAINT mm_media_dir_pk PRIMARY KEY (mm_media_dir_guid);


--
-- TOC entry 2250 (class 2606 OID 25897)
-- Name: mm_media mm_media_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_media
    ADD CONSTRAINT mm_media_pk PRIMARY KEY (mm_media_guid);


--
-- TOC entry 2242 (class 2606 OID 25880)
-- Name: mm_media_share mm_media_share_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_media_share
    ADD CONSTRAINT mm_media_share_pk PRIMARY KEY (mm_media_share_guid);


--
-- TOC entry 2301 (class 2606 OID 25978)
-- Name: mm_metadata_album mm_metadata_album_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_metadata_album
    ADD CONSTRAINT mm_metadata_album_pk PRIMARY KEY (mm_metadata_album_guid);


--
-- TOC entry 2324 (class 2606 OID 26013)
-- Name: mm_metadata_anime mm_metadata_anime_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_metadata_anime
    ADD CONSTRAINT mm_metadata_anime_pk PRIMARY KEY (mm_metadata_anime_guid);


--
-- TOC entry 2349 (class 2606 OID 26061)
-- Name: mm_metadata_book mm_metadata_book_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_metadata_book
    ADD CONSTRAINT mm_metadata_book_pk PRIMARY KEY (mm_metadata_book_guid);


--
-- TOC entry 2370 (class 2606 OID 26115)
-- Name: mm_metadata_collection mm_metadata_collection_guid_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_metadata_collection
    ADD CONSTRAINT mm_metadata_collection_guid_pk PRIMARY KEY (mm_metadata_collection_guid);


--
-- TOC entry 2388 (class 2606 OID 26172)
-- Name: mm_metadata_logo mm_metadata_logo_guid_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_metadata_logo
    ADD CONSTRAINT mm_metadata_logo_guid_pk PRIMARY KEY (mm_metadata_logo_guid);


--
-- TOC entry 2309 (class 2606 OID 25991)
-- Name: mm_metadata_music mm_metadata_music_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_metadata_music
    ADD CONSTRAINT mm_metadata_music_pk PRIMARY KEY (mm_metadata_music_guid);


--
-- TOC entry 2346 (class 2606 OID 26046)
-- Name: mm_metadata_music_video mm_metadata_music_video_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_metadata_music_video
    ADD CONSTRAINT mm_metadata_music_video_pk PRIMARY KEY (mm_metadata_music_video_guid);


--
-- TOC entry 2293 (class 2606 OID 25966)
-- Name: mm_metadata_musician mm_metadata_musician_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_metadata_musician
    ADD CONSTRAINT mm_metadata_musician_pk PRIMARY KEY (mm_metadata_musician_guid);


--
-- TOC entry 2335 (class 2606 OID 26030)
-- Name: mm_metadata_movie mm_metadata_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_metadata_movie
    ADD CONSTRAINT mm_metadata_pk PRIMARY KEY (mm_metadata_guid);


--
-- TOC entry 2286 (class 2606 OID 25948)
-- Name: mm_metadata_sports mm_metadata_sports_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_metadata_sports
    ADD CONSTRAINT mm_metadata_sports_pk PRIMARY KEY (mm_metadata_sports_guid);


--
-- TOC entry 2273 (class 2606 OID 25929)
-- Name: mm_metadata_tvshow mm_metadata_tvshow_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_metadata_tvshow
    ADD CONSTRAINT mm_metadata_tvshow_pk PRIMARY KEY (mm_metadata_tvshow_guid);


--
-- TOC entry 2361 (class 2606 OID 26083)
-- Name: mm_notification mm_notification_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_notification
    ADD CONSTRAINT mm_notification_pk PRIMARY KEY (mm_notification_guid);


--
-- TOC entry 2403 (class 2606 OID 26211)
-- Name: mm_options_and_status mm_options_and_status_guid_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_options_and_status
    ADD CONSTRAINT mm_options_and_status_guid_pk PRIMARY KEY (mm_options_and_status_guid);


--
-- TOC entry 2379 (class 2606 OID 26142)
-- Name: mm_radio mm_radio_guid_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_radio
    ADD CONSTRAINT mm_radio_guid_pk PRIMARY KEY (mm_radio_guid);


--
-- TOC entry 2368 (class 2606 OID 26105)
-- Name: mm_review mm_review_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_review
    ADD CONSTRAINT mm_review_pk PRIMARY KEY (mm_review_guid);


--
-- TOC entry 2381 (class 2606 OID 26150)
-- Name: mm_sync mm_sync_guid_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_sync
    ADD CONSTRAINT mm_sync_guid_pk PRIMARY KEY (mm_sync_guid);


--
-- TOC entry 2375 (class 2606 OID 26126)
-- Name: mm_task mm_task_guid_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_task
    ADD CONSTRAINT mm_task_guid_pk PRIMARY KEY (mm_task_guid);


--
-- TOC entry 2386 (class 2606 OID 26164)
-- Name: mm_trigger mm_trigger_guid_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_trigger
    ADD CONSTRAINT mm_trigger_guid_pk PRIMARY KEY (mm_trigger_guid);


--
-- TOC entry 2435 (class 2606 OID 26290)
-- Name: mm_tv_schedule mm_tv_schedule_id_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_tv_schedule
    ADD CONSTRAINT mm_tv_schedule_id_pk PRIMARY KEY (mm_tv_schedule_id);


--
-- TOC entry 2440 (class 2606 OID 26300)
-- Name: mm_tv_schedule_program mm_tv_schedule_program_guid_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_tv_schedule_program
    ADD CONSTRAINT mm_tv_schedule_program_guid_pk PRIMARY KEY (mm_tv_schedule_program_guid);


--
-- TOC entry 2431 (class 2606 OID 26280)
-- Name: mm_tv_stations mm_tv_stations_id_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_tv_stations
    ADD CONSTRAINT mm_tv_stations_id_pk PRIMARY KEY (mm_tv_stations_id);


--
-- TOC entry 2397 (class 2606 OID 26193)
-- Name: mm_user_group mm_user_group_guid_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_user_group
    ADD CONSTRAINT mm_user_group_guid_pk PRIMARY KEY (mm_user_group_guid);


--
-- TOC entry 2364 (class 2606 OID 26096)
-- Name: mm_user mm_user_pkey; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_user
    ADD CONSTRAINT mm_user_pkey PRIMARY KEY (id);


--
-- TOC entry 2400 (class 2606 OID 26202)
-- Name: mm_user_profile mm_user_profile_guid_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_user_profile
    ADD CONSTRAINT mm_user_profile_guid_pk PRIMARY KEY (mm_user_profile_guid);


--
-- TOC entry 2416 (class 2606 OID 26239)
-- Name: mm_metadata_person mmp_id_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_metadata_person
    ADD CONSTRAINT mmp_id_pk PRIMARY KEY (mmp_id);


--
-- TOC entry 2255 (class 2606 OID 25908)
-- Name: mm_media_remote mmr_media_remote_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_media_remote
    ADD CONSTRAINT mmr_media_remote_pk PRIMARY KEY (mmr_media_guid);


--
-- TOC entry 2406 (class 1259 OID 26220)
-- Name: gi_system_id_ndx; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX gi_system_id_ndx ON mm_metadata_game_software_info USING btree (gi_system_id);


--
-- TOC entry 2420 (class 1259 OID 26253)
-- Name: mdq_que_type_idx_name; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mdq_que_type_idx_name ON mm_download_que USING btree (mdq_que_type);


--
-- TOC entry 2392 (class 1259 OID 26184)
-- Name: mm_channel_idx_country; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_channel_idx_country ON mm_channel USING btree (mm_channel_country_guid);


--
-- TOC entry 2393 (class 1259 OID 26185)
-- Name: mm_channel_idx_logo; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_channel_idx_logo ON mm_channel USING btree (mm_channel_logo_guid);


--
-- TOC entry 2394 (class 1259 OID 26182)
-- Name: mm_channel_idx_name; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_channel_idx_name ON mm_channel USING btree (mm_channel_name);


--
-- TOC entry 2395 (class 1259 OID 26183)
-- Name: mm_channel_idxgin_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_channel_idxgin_json ON mm_channel USING gin (mm_channel_media_id);


--
-- TOC entry 2428 (class 1259 OID 26271)
-- Name: mm_device_idx_type; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_device_idx_type ON mm_device USING btree (mm_device_type);


--
-- TOC entry 2429 (class 1259 OID 26272)
-- Name: mm_device_idxgin_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_device_idxgin_json ON mm_device USING gin (mm_device_json);


--
-- TOC entry 2421 (class 1259 OID 26251)
-- Name: mm_download_idx_provider; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_download_idx_provider ON mm_download_que USING btree (mdq_provider);


--
-- TOC entry 2422 (class 1259 OID 26252)
-- Name: mm_download_que_idxgin_meta_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_download_que_idxgin_meta_json ON mm_download_que USING gin (mdq_download_json);


--
-- TOC entry 2407 (class 1259 OID 26221)
-- Name: mm_game_info_idxgin_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_game_info_idxgin_json ON mm_metadata_game_software_info USING gin (gi_game_info_json);


--
-- TOC entry 2408 (class 1259 OID 26222)
-- Name: mm_game_info_idxgin_name; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_game_info_idxgin_name ON mm_metadata_game_software_info USING gin (((gi_game_info_json -> '@name'::text)));


--
-- TOC entry 2411 (class 1259 OID 26231)
-- Name: mm_game_systems_idxgin_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_game_systems_idxgin_json ON mm_metadata_game_systems_info USING gin (gs_game_system_json);


--
-- TOC entry 2425 (class 1259 OID 26262)
-- Name: mm_image_download_idx_provider; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_image_download_idx_provider ON mm_download_image_que USING btree (mdq_image_provider);


--
-- TOC entry 2258 (class 1259 OID 25921)
-- Name: mm_link_idx_name; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_link_idx_name ON mm_link USING btree (mm_link_name);


--
-- TOC entry 2259 (class 1259 OID 25920)
-- Name: mm_link_json_idxgin; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_link_json_idxgin ON mm_link USING gin (mm_link_json);


--
-- TOC entry 2313 (class 1259 OID 26307)
-- Name: mm_media_anime_name_trigram_idx; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_media_anime_name_trigram_idx ON mm_metadata_anime USING gist (mm_media_anime_name gist_trgm_ops);


--
-- TOC entry 2310 (class 1259 OID 26005)
-- Name: mm_media_class_idx_type; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_media_class_idx_type ON mm_media_class USING btree (mm_media_class_type);


--
-- TOC entry 2243 (class 1259 OID 25889)
-- Name: mm_media_dir_idx_share; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_media_dir_idx_share ON mm_media_dir USING btree (mm_media_dir_share_guid);


--
-- TOC entry 2246 (class 1259 OID 25899)
-- Name: mm_media_idx_metadata_uuid; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_media_idx_metadata_uuid ON mm_media USING btree (mm_media_metadata_guid);


--
-- TOC entry 2247 (class 1259 OID 25900)
-- Name: mm_media_idx_path; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_media_idx_path ON mm_media USING btree (mm_media_path);


--
-- TOC entry 2248 (class 1259 OID 25898)
-- Name: mm_media_idxgin_ffprobe; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_media_idxgin_ffprobe ON mm_media USING gin (mm_media_ffprobe_json);


--
-- TOC entry 2336 (class 1259 OID 26309)
-- Name: mm_media_music_video_band_trigram_idx; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_media_music_video_band_trigram_idx ON mm_metadata_music_video USING gist (mm_media_music_video_band gist_trgm_ops);


--
-- TOC entry 2337 (class 1259 OID 26310)
-- Name: mm_media_music_video_song_trigram_idx; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_media_music_video_song_trigram_idx ON mm_metadata_music_video USING gist (mm_media_music_video_song gist_trgm_ops);


--
-- TOC entry 2325 (class 1259 OID 26308)
-- Name: mm_media_name_trigram_idx; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_media_name_trigram_idx ON mm_metadata_movie USING gist (mm_media_name gist_trgm_ops);


--
-- TOC entry 2294 (class 1259 OID 25983)
-- Name: mm_metadata_album_idx_musician; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_album_idx_musician ON mm_metadata_album USING btree (mm_metadata_album_musician_guid);


--
-- TOC entry 2295 (class 1259 OID 25979)
-- Name: mm_metadata_album_idx_name; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_album_idx_name ON mm_metadata_album USING btree (mm_metadata_album_name);


--
-- TOC entry 2296 (class 1259 OID 25980)
-- Name: mm_metadata_album_idx_name_lower; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_album_idx_name_lower ON mm_metadata_album USING btree (lower(mm_metadata_album_name));


--
-- TOC entry 2297 (class 1259 OID 25981)
-- Name: mm_metadata_album_idxgin_id_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_album_idxgin_id_json ON mm_metadata_album USING gin (mm_metadata_album_id);


--
-- TOC entry 2298 (class 1259 OID 25982)
-- Name: mm_metadata_album_idxgin_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_album_idxgin_json ON mm_metadata_album USING gin (mm_metadata_album_json);


--
-- TOC entry 2299 (class 1259 OID 26305)
-- Name: mm_metadata_album_name_trigram_idx; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_album_name_trigram_idx ON mm_metadata_album USING gist (mm_metadata_album_name gist_trgm_ops);


--
-- TOC entry 2314 (class 1259 OID 26017)
-- Name: mm_metadata_aniem_idxgin_media_id; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_aniem_idxgin_media_id ON mm_metadata_anime USING gin (mm_metadata_anime_media_id);


--
-- TOC entry 2315 (class 1259 OID 26014)
-- Name: mm_metadata_anime_idx_name; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_anime_idx_name ON mm_metadata_anime USING btree (mm_media_anime_name);


--
-- TOC entry 2316 (class 1259 OID 26015)
-- Name: mm_metadata_anime_idx_name_lower; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_anime_idx_name_lower ON mm_metadata_anime USING btree (lower(mm_media_anime_name));


--
-- TOC entry 2317 (class 1259 OID 26016)
-- Name: mm_metadata_anime_idxgin_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_anime_idxgin_json ON mm_metadata_anime USING gin (mm_metadata_anime_json);


--
-- TOC entry 2318 (class 1259 OID 26018)
-- Name: mm_metadata_anime_idxgin_media_id_anidb; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_anime_idxgin_media_id_anidb ON mm_metadata_anime USING gin (((mm_metadata_anime_media_id -> 'anidb'::text)));


--
-- TOC entry 2319 (class 1259 OID 26021)
-- Name: mm_metadata_anime_idxgin_media_id_imdb; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_anime_idxgin_media_id_imdb ON mm_metadata_anime USING gin (((mm_metadata_anime_media_id -> 'imdb'::text)));


--
-- TOC entry 2320 (class 1259 OID 26019)
-- Name: mm_metadata_anime_idxgin_media_id_thetvdb; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_anime_idxgin_media_id_thetvdb ON mm_metadata_anime USING gin (((mm_metadata_anime_media_id -> 'thetvdb'::text)));


--
-- TOC entry 2321 (class 1259 OID 26020)
-- Name: mm_metadata_anime_idxgin_media_id_tmdb; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_anime_idxgin_media_id_tmdb ON mm_metadata_anime USING gin (((mm_metadata_anime_media_id -> 'tmdb'::text)));


--
-- TOC entry 2322 (class 1259 OID 26022)
-- Name: mm_metadata_anime_idxgin_user_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_anime_idxgin_user_json ON mm_metadata_anime USING gin (mm_metadata_anime_user_json);


--
-- TOC entry 2347 (class 1259 OID 26311)
-- Name: mm_metadata_book_name_trigram_idx; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_book_name_trigram_idx ON mm_metadata_book USING gist (mm_metadata_book_name gist_trgm_ops);


--
-- TOC entry 2371 (class 1259 OID 26116)
-- Name: mm_metadata_collection_idxgin_media_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_collection_idxgin_media_json ON mm_metadata_collection USING gin (mm_metadata_collection_media_ids);


--
-- TOC entry 2372 (class 1259 OID 26118)
-- Name: mm_metadata_collection_idxgin_meta_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_collection_idxgin_meta_json ON mm_metadata_collection USING gin (mm_metadata_collection_json);


--
-- TOC entry 2373 (class 1259 OID 26117)
-- Name: mm_metadata_collection_idxgin_name_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_collection_idxgin_name_json ON mm_metadata_collection USING gin (mm_metadata_collection_name);


--
-- TOC entry 2338 (class 1259 OID 26047)
-- Name: mm_metadata_idx_band_name; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_idx_band_name ON mm_metadata_music_video USING btree (mm_media_music_video_band);


--
-- TOC entry 2339 (class 1259 OID 26048)
-- Name: mm_metadata_idx_band_name_lower; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_idx_band_name_lower ON mm_metadata_music_video USING btree (lower(mm_media_music_video_band));


--
-- TOC entry 2350 (class 1259 OID 26062)
-- Name: mm_metadata_idx_book_name; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_idx_book_name ON mm_metadata_book USING btree (mm_metadata_book_name);


--
-- TOC entry 2351 (class 1259 OID 26063)
-- Name: mm_metadata_idx_book_name_lower; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_idx_book_name_lower ON mm_metadata_book USING btree (lower(mm_metadata_book_name));


--
-- TOC entry 2326 (class 1259 OID 26031)
-- Name: mm_metadata_idx_name; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_idx_name ON mm_metadata_movie USING btree (mm_media_name);


--
-- TOC entry 2327 (class 1259 OID 26032)
-- Name: mm_metadata_idx_name_lower; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_idx_name_lower ON mm_metadata_movie USING btree (lower(mm_media_name));


--
-- TOC entry 2340 (class 1259 OID 26049)
-- Name: mm_metadata_idx_song_name; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_idx_song_name ON mm_metadata_music_video USING btree (mm_media_music_video_song);


--
-- TOC entry 2341 (class 1259 OID 26050)
-- Name: mm_metadata_idx_song_name_lower; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_idx_song_name_lower ON mm_metadata_music_video USING btree (lower(mm_media_music_video_song));


--
-- TOC entry 2352 (class 1259 OID 26064)
-- Name: mm_metadata_idxgin_isbn; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_idxgin_isbn ON mm_metadata_book USING btree (mm_metadata_book_isbn);


--
-- TOC entry 2353 (class 1259 OID 26065)
-- Name: mm_metadata_idxgin_isbn13; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_idxgin_isbn13 ON mm_metadata_book USING btree (mm_metadata_book_isbn13);


--
-- TOC entry 2328 (class 1259 OID 26033)
-- Name: mm_metadata_idxgin_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_idxgin_json ON mm_metadata_movie USING gin (mm_metadata_json);


--
-- TOC entry 2329 (class 1259 OID 26034)
-- Name: mm_metadata_idxgin_media_id; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_idxgin_media_id ON mm_metadata_movie USING gin (mm_metadata_media_id);


--
-- TOC entry 2330 (class 1259 OID 26037)
-- Name: mm_metadata_idxgin_media_id_imdb; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_idxgin_media_id_imdb ON mm_metadata_movie USING gin (((mm_metadata_media_id -> 'imdb'::text)));


--
-- TOC entry 2331 (class 1259 OID 26035)
-- Name: mm_metadata_idxgin_media_id_thetvdb; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_idxgin_media_id_thetvdb ON mm_metadata_movie USING gin (((mm_metadata_media_id -> 'thetvdb'::text)));


--
-- TOC entry 2332 (class 1259 OID 26036)
-- Name: mm_metadata_idxgin_media_id_tmdb; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_idxgin_media_id_tmdb ON mm_metadata_movie USING gin (((mm_metadata_media_id -> 'tmdb'::text)));


--
-- TOC entry 2342 (class 1259 OID 26051)
-- Name: mm_metadata_idxgin_music_video_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_idxgin_music_video_json ON mm_metadata_music_video USING gin (mm_metadata_music_video_json);


--
-- TOC entry 2343 (class 1259 OID 26052)
-- Name: mm_metadata_idxgin_music_video_media_id; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_idxgin_music_video_media_id ON mm_metadata_music_video USING gin (mm_metadata_music_video_media_id);


--
-- TOC entry 2344 (class 1259 OID 26053)
-- Name: mm_metadata_idxgin_music_video_media_id_imvdb; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_idxgin_music_video_media_id_imvdb ON mm_metadata_music_video USING gin (((mm_metadata_music_video_media_id -> 'imvdb'::text)));


--
-- TOC entry 2333 (class 1259 OID 26038)
-- Name: mm_metadata_idxgin_user_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_idxgin_user_json ON mm_metadata_movie USING gin (mm_metadata_user_json);


--
-- TOC entry 2389 (class 1259 OID 26173)
-- Name: mm_metadata_logo_idxgin_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_logo_idxgin_json ON mm_metadata_logo USING gin (mm_metadata_logo_media_guid);


--
-- TOC entry 2302 (class 1259 OID 25996)
-- Name: mm_metadata_music_idx_album; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_music_idx_album ON mm_metadata_music USING btree (mm_metadata_music_album_guid);


--
-- TOC entry 2303 (class 1259 OID 25992)
-- Name: mm_metadata_music_idx_name; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_music_idx_name ON mm_metadata_music USING btree (mm_metadata_music_name);


--
-- TOC entry 2304 (class 1259 OID 25993)
-- Name: mm_metadata_music_idx_name_lower; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_music_idx_name_lower ON mm_metadata_music USING btree (lower(mm_metadata_music_name));


--
-- TOC entry 2305 (class 1259 OID 25994)
-- Name: mm_metadata_music_idxgin_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_music_idxgin_json ON mm_metadata_music USING gin (mm_metadata_music_json);


--
-- TOC entry 2306 (class 1259 OID 25995)
-- Name: mm_metadata_music_idxgin_media_id; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_music_idxgin_media_id ON mm_metadata_music USING gin (mm_metadata_media_music_id);


--
-- TOC entry 2307 (class 1259 OID 26306)
-- Name: mm_metadata_music_name_trigram_idx; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_music_name_trigram_idx ON mm_metadata_music USING gist (mm_metadata_music_name gist_trgm_ops);


--
-- TOC entry 2287 (class 1259 OID 25967)
-- Name: mm_metadata_musician_idx_name; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_musician_idx_name ON mm_metadata_musician USING btree (mm_metadata_musician_name);


--
-- TOC entry 2288 (class 1259 OID 25968)
-- Name: mm_metadata_musician_idx_name_lower; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_musician_idx_name_lower ON mm_metadata_musician USING btree (lower(mm_metadata_musician_name));


--
-- TOC entry 2289 (class 1259 OID 25969)
-- Name: mm_metadata_musician_idxgin_id_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_musician_idxgin_id_json ON mm_metadata_musician USING gin (mm_metadata_musician_id);


--
-- TOC entry 2290 (class 1259 OID 25970)
-- Name: mm_metadata_musician_idxgin_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_musician_idxgin_json ON mm_metadata_musician USING gin (mm_metadata_musician_json);


--
-- TOC entry 2291 (class 1259 OID 26304)
-- Name: mm_metadata_musician_name_trigram_idx; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_musician_name_trigram_idx ON mm_metadata_musician USING gist (mm_metadata_musician_name gist_trgm_ops);


--
-- TOC entry 2412 (class 1259 OID 26240)
-- Name: mm_metadata_person_idx_name; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_person_idx_name ON mm_metadata_person USING btree (mmp_person_name);


--
-- TOC entry 2413 (class 1259 OID 26241)
-- Name: mm_metadata_person_idxgin_id_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_person_idxgin_id_json ON mm_metadata_person USING gin (mmp_person_media_id);


--
-- TOC entry 2414 (class 1259 OID 26242)
-- Name: mm_metadata_person_idxgin_meta_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_person_idxgin_meta_json ON mm_metadata_person USING gin (mmp_person_meta_json);


--
-- TOC entry 2365 (class 1259 OID 26107)
-- Name: mm_metadata_review_idx_metadata_uuid; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_review_idx_metadata_uuid ON mm_review USING btree (mm_review_metadata_guid);


--
-- TOC entry 2366 (class 1259 OID 26106)
-- Name: mm_metadata_review_idxgin_media_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_review_idxgin_media_json ON mm_review USING gin (mm_review_metadata_id);


--
-- TOC entry 2274 (class 1259 OID 25949)
-- Name: mm_metadata_sports_idx_name; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_sports_idx_name ON mm_metadata_sports USING btree (mm_metadata_sports_name);


--
-- TOC entry 2275 (class 1259 OID 25950)
-- Name: mm_metadata_sports_idx_name_lower; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_sports_idx_name_lower ON mm_metadata_sports USING btree (lower(mm_metadata_sports_name));


--
-- TOC entry 2276 (class 1259 OID 25951)
-- Name: mm_metadata_sports_idxgin_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_sports_idxgin_json ON mm_metadata_sports USING gin (mm_metadata_sports_json);


--
-- TOC entry 2277 (class 1259 OID 25952)
-- Name: mm_metadata_sports_idxgin_media_id; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_sports_idxgin_media_id ON mm_metadata_sports USING gin (mm_metadata_media_sports_id);


--
-- TOC entry 2278 (class 1259 OID 25953)
-- Name: mm_metadata_sports_idxgin_media_id_imdb; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_sports_idxgin_media_id_imdb ON mm_metadata_sports USING gin (((mm_metadata_media_sports_id -> 'imdb'::text)));


--
-- TOC entry 2279 (class 1259 OID 25958)
-- Name: mm_metadata_sports_idxgin_media_id_thesportsdb; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_sports_idxgin_media_id_thesportsdb ON mm_metadata_sports USING gin (((mm_metadata_media_sports_id -> 'thesportsdb'::text)));


--
-- TOC entry 2280 (class 1259 OID 25954)
-- Name: mm_metadata_sports_idxgin_media_id_thetvdb; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_sports_idxgin_media_id_thetvdb ON mm_metadata_sports USING gin (((mm_metadata_media_sports_id -> 'thetvdb'::text)));


--
-- TOC entry 2281 (class 1259 OID 25956)
-- Name: mm_metadata_sports_idxgin_media_id_thetvdbseries; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_sports_idxgin_media_id_thetvdbseries ON mm_metadata_sports USING gin (((mm_metadata_media_sports_id -> 'thetvdbSeries'::text)));


--
-- TOC entry 2282 (class 1259 OID 25955)
-- Name: mm_metadata_sports_idxgin_media_id_tmdb; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_sports_idxgin_media_id_tmdb ON mm_metadata_sports USING gin (((mm_metadata_media_sports_id -> 'tmdb'::text)));


--
-- TOC entry 2283 (class 1259 OID 25957)
-- Name: mm_metadata_sports_idxgin_media_id_tvmaze; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_sports_idxgin_media_id_tvmaze ON mm_metadata_sports USING gin (((mm_metadata_media_sports_id -> 'tvmaze'::text)));


--
-- TOC entry 2284 (class 1259 OID 26303)
-- Name: mm_metadata_sports_name_trigram_idx; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_sports_name_trigram_idx ON mm_metadata_sports USING gist (mm_metadata_sports_name gist_trgm_ops);


--
-- TOC entry 2260 (class 1259 OID 25930)
-- Name: mm_metadata_tvshow_idx_name; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_tvshow_idx_name ON mm_metadata_tvshow USING btree (mm_metadata_tvshow_name);


--
-- TOC entry 2261 (class 1259 OID 25931)
-- Name: mm_metadata_tvshow_idx_name_lower; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_tvshow_idx_name_lower ON mm_metadata_tvshow USING btree (lower(mm_metadata_tvshow_name));


--
-- TOC entry 2262 (class 1259 OID 25933)
-- Name: mm_metadata_tvshow_idxgin_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_tvshow_idxgin_json ON mm_metadata_tvshow USING gin (mm_metadata_tvshow_json);


--
-- TOC entry 2263 (class 1259 OID 25934)
-- Name: mm_metadata_tvshow_idxgin_localimage_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_tvshow_idxgin_localimage_json ON mm_metadata_tvshow USING gin (mm_metadata_tvshow_json);


--
-- TOC entry 2264 (class 1259 OID 25932)
-- Name: mm_metadata_tvshow_idxgin_media_id; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_tvshow_idxgin_media_id ON mm_metadata_tvshow USING gin (mm_metadata_media_tvshow_id);


--
-- TOC entry 2265 (class 1259 OID 25935)
-- Name: mm_metadata_tvshow_idxgin_media_id_imdb; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_tvshow_idxgin_media_id_imdb ON mm_metadata_tvshow USING gin (((mm_metadata_media_tvshow_id -> 'imdb'::text)));


--
-- TOC entry 2266 (class 1259 OID 25936)
-- Name: mm_metadata_tvshow_idxgin_media_id_thetvdb; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_tvshow_idxgin_media_id_thetvdb ON mm_metadata_tvshow USING gin (((mm_metadata_media_tvshow_id -> 'thetvdb'::text)));


--
-- TOC entry 2267 (class 1259 OID 25938)
-- Name: mm_metadata_tvshow_idxgin_media_id_thetvdbseries; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_tvshow_idxgin_media_id_thetvdbseries ON mm_metadata_tvshow USING gin (((mm_metadata_media_tvshow_id -> 'thetvdbSeries'::text)));


--
-- TOC entry 2268 (class 1259 OID 25937)
-- Name: mm_metadata_tvshow_idxgin_media_id_tmdb; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_tvshow_idxgin_media_id_tmdb ON mm_metadata_tvshow USING gin (((mm_metadata_media_tvshow_id -> 'tmdb'::text)));


--
-- TOC entry 2269 (class 1259 OID 25939)
-- Name: mm_metadata_tvshow_idxgin_media_id_tvmaze; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_tvshow_idxgin_media_id_tvmaze ON mm_metadata_tvshow USING gin (((mm_metadata_media_tvshow_id -> 'tvmaze'::text)));


--
-- TOC entry 2270 (class 1259 OID 25940)
-- Name: mm_metadata_tvshow_idxgin_user_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_tvshow_idxgin_user_json ON mm_metadata_tvshow USING gin (mm_metadata_tvshow_user_json);


--
-- TOC entry 2271 (class 1259 OID 26302)
-- Name: mm_metadata_tvshow_name_trigram_idx; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_tvshow_name_trigram_idx ON mm_metadata_tvshow USING gist (mm_metadata_tvshow_name gist_trgm_ops);


--
-- TOC entry 2358 (class 1259 OID 26085)
-- Name: mm_notification_idx_dismissable; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_notification_idx_dismissable ON mm_notification USING btree (mm_notification_dismissable);


--
-- TOC entry 2359 (class 1259 OID 26084)
-- Name: mm_notification_idx_time; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_notification_idx_time ON mm_notification USING btree (mm_notification_time);


--
-- TOC entry 2382 (class 1259 OID 26151)
-- Name: mm_sync_idxgin_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_sync_idxgin_json ON mm_sync USING gin (mm_sync_options_json);


--
-- TOC entry 2436 (class 1259 OID 26291)
-- Name: mm_tv_schedule_idx_date; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_tv_schedule_idx_date ON mm_tv_schedule USING btree (mm_tv_schedule_date);


--
-- TOC entry 2438 (class 1259 OID 26301)
-- Name: mm_tv_schedule_idx_program; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_tv_schedule_idx_program ON mm_tv_schedule_program USING btree (mm_tv_schedule_program_id);


--
-- TOC entry 2437 (class 1259 OID 26292)
-- Name: mm_tv_schedule_idx_station; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_tv_schedule_idx_station ON mm_tv_schedule USING btree (mm_tv_schedule_station_id);


--
-- TOC entry 2432 (class 1259 OID 26282)
-- Name: mm_tv_stations_idx_name; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_tv_stations_idx_name ON mm_tv_stations USING btree (mm_tv_station_name);


--
-- TOC entry 2433 (class 1259 OID 26281)
-- Name: mm_tv_stations_idx_station; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_tv_stations_idx_station ON mm_tv_stations USING btree (mm_tv_station_id);


--
-- TOC entry 2356 (class 1259 OID 26075)
-- Name: mm_user_activity_idx_date; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_user_activity_idx_date ON mm_user_activity USING btree (mm_activity_datecreated);


--
-- TOC entry 2357 (class 1259 OID 26074)
-- Name: mm_user_activity_idx_user_guid; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_user_activity_idx_user_guid ON mm_user_activity USING btree (mm_activity_userid);


--
-- TOC entry 2398 (class 1259 OID 26194)
-- Name: mm_user_group_idx_name; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_user_group_idx_name ON mm_user_group USING btree (mm_user_group_name);


--
-- TOC entry 2362 (class 1259 OID 26097)
-- Name: mm_user_idx_username; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_user_idx_username ON mm_user USING btree (username);


--
-- TOC entry 2401 (class 1259 OID 26203)
-- Name: mm_user_profile_idx_name; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_user_profile_idx_name ON mm_user_profile USING btree (mm_user_profile_name);


--
-- TOC entry 2417 (class 1259 OID 26312)
-- Name: mmp_person_name_trigram_idx; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mmp_person_name_trigram_idx ON mm_metadata_person USING gist (mmp_person_name gist_trgm_ops);


--
-- TOC entry 2251 (class 1259 OID 25911)
-- Name: mmr_media_idx_link_uuid; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mmr_media_idx_link_uuid ON mm_media_remote USING btree (mmr_media_link_id);


--
-- TOC entry 2252 (class 1259 OID 25910)
-- Name: mmr_media_idx_metadata_uuid; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mmr_media_idx_metadata_uuid ON mm_media_remote USING btree (mmr_media_metadata_guid);


--
-- TOC entry 2253 (class 1259 OID 25909)
-- Name: mmr_media_idxgin_ffprobe; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mmr_media_idxgin_ffprobe ON mm_media_remote USING gin (mmr_media_ffprobe_json);


-- Completed on 2017-08-19 20:19:15 CDT

--
-- PostgreSQL database dump complete
--

