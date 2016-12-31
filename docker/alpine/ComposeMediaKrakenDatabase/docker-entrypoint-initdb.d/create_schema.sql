--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.4
-- Dumped by pg_dump version 9.5.4

-- Started on 2016-12-31 01:44:52 CST

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 2540 (class 1262 OID 17274)
-- Name: metamandb; Type: DATABASE; Schema: -; Owner: postgres
--

CREATE DATABASE metamandb WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'C' LC_CTYPE = 'C.UTF-8';


ALTER DATABASE metamandb OWNER TO postgres;

\connect metamandb

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- TOC entry 1 (class 3079 OID 12358)
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- TOC entry 2543 (class 0 OID 0)
-- Dependencies: 1
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- TOC entry 209 (class 1259 OID 17574)
-- Name: mm_channel; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE mm_channel (
    mm_channel_guid uuid NOT NULL,
    mm_channel_name text,
    mm_channel_media_id jsonb,
    mm_channel_country_guid uuid,
    mm_channel_logo_guid uuid
);


ALTER TABLE mm_channel OWNER TO postgres;

--
-- TOC entry 203 (class 1259 OID 17527)
-- Name: mm_cron; Type: TABLE; Schema: public; Owner: postgres
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


ALTER TABLE mm_cron OWNER TO postgres;

--
-- TOC entry 220 (class 1259 OID 17679)
-- Name: mm_device; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE mm_device (
    mm_device_id uuid NOT NULL,
    mm_device_type text,
    mm_device_json jsonb
);


ALTER TABLE mm_device OWNER TO postgres;

--
-- TOC entry 217 (class 1259 OID 17654)
-- Name: mm_download_image_que; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE mm_download_image_que (
    mdq_image_id uuid NOT NULL,
    mdq_image_provider text,
    mdq_image_download_json jsonb
);


ALTER TABLE mm_download_image_que OWNER TO postgres;

--
-- TOC entry 216 (class 1259 OID 17643)
-- Name: mm_download_que; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE mm_download_que (
    mdq_id uuid NOT NULL,
    mdq_provider text,
    mqd_que_type smallint,
    mdq_download_json jsonb
);


ALTER TABLE mm_download_que OWNER TO postgres;

--
-- TOC entry 186 (class 1259 OID 17320)
-- Name: mm_link; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE mm_link (
    mm_link_guid uuid NOT NULL,
    mm_link_name text,
    mm_link_json jsonb
);


ALTER TABLE mm_link OWNER TO postgres;

--
-- TOC entry 206 (class 1259 OID 17552)
-- Name: mm_loan; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE mm_loan (
    mm_loan_guid uuid NOT NULL,
    mm_loan_media_id uuid,
    mm_loan_user_id uuid,
    mm_load_user_loan_id uuid,
    mm_loan_time timestamp without time zone,
    mm_loan_return_time timestamp without time zone
);


ALTER TABLE mm_loan OWNER TO postgres;

--
-- TOC entry 184 (class 1259 OID 17298)
-- Name: mm_media; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE mm_media (
    mm_media_guid uuid NOT NULL,
    mm_media_class_guid uuid,
    mm_media_metadata_guid uuid,
    mm_media_path text,
    mm_media_ffprobe_json jsonb,
    mm_media_json jsonb
);


ALTER TABLE mm_media OWNER TO postgres;

--
-- TOC entry 192 (class 1259 OID 17405)
-- Name: mm_media_class; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE mm_media_class (
    mm_media_class_guid uuid NOT NULL,
    mm_media_class_type text,
    mm_media_class_parent_type text,
    mm_media_class_display boolean
);


ALTER TABLE mm_media_class OWNER TO postgres;

--
-- TOC entry 183 (class 1259 OID 17289)
-- Name: mm_media_dir; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE mm_media_dir (
    mm_media_dir_guid uuid NOT NULL,
    mm_media_dir_path text,
    mm_media_dir_class_type uuid,
    mm_media_dir_last_scanned timestamp without time zone,
    mm_media_dir_share_guid uuid,
    mm_media_dir_status jsonb
);


ALTER TABLE mm_media_dir OWNER TO postgres;

--
-- TOC entry 185 (class 1259 OID 17309)
-- Name: mm_media_remote; Type: TABLE; Schema: public; Owner: postgres
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


ALTER TABLE mm_media_remote OWNER TO postgres;

--
-- TOC entry 182 (class 1259 OID 17281)
-- Name: mm_media_share; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE mm_media_share (
    mm_media_share_guid uuid NOT NULL,
    mm_media_share_type text,
    mm_media_share_user text,
    mm_media_share_password text,
    mm_media_share_server text,
    mm_media_share_path text
);


ALTER TABLE mm_media_share OWNER TO postgres;

--
-- TOC entry 190 (class 1259 OID 17379)
-- Name: mm_metadata_album; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE mm_metadata_album (
    mm_metadata_album_guid uuid NOT NULL,
    mm_metadata_album_name text,
    mm_metadata_album_id jsonb,
    mm_metadata_album_json jsonb,
    mm_metadata_album_musician_guid uuid
);


ALTER TABLE mm_metadata_album OWNER TO postgres;

--
-- TOC entry 193 (class 1259 OID 17414)
-- Name: mm_metadata_anime; Type: TABLE; Schema: public; Owner: postgres
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


ALTER TABLE mm_metadata_anime OWNER TO postgres;

--
-- TOC entry 196 (class 1259 OID 17462)
-- Name: mm_metadata_book; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE mm_metadata_book (
    mm_metadata_book_guid uuid NOT NULL,
    mm_metadata_book_isbn text,
    mm_metadata_book_isbn13 text,
    mm_metadata_book_name text,
    mm_metadata_book_json jsonb
);


ALTER TABLE mm_metadata_book OWNER TO postgres;

--
-- TOC entry 202 (class 1259 OID 17516)
-- Name: mm_metadata_collection; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE mm_metadata_collection (
    mm_metadata_collection_guid uuid NOT NULL,
    mm_metadata_collection_name jsonb,
    mm_metadata_collection_media_ids jsonb,
    mm_metadata_collection_json jsonb,
    mm_metadata_collection_imagelocal_json jsonb
);


ALTER TABLE mm_metadata_collection OWNER TO postgres;

--
-- TOC entry 213 (class 1259 OID 17612)
-- Name: mm_metadata_game_software_info; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE mm_metadata_game_software_info (
    gi_id uuid NOT NULL,
    gi_system_id uuid,
    gi_game_info_json jsonb
);


ALTER TABLE mm_metadata_game_software_info OWNER TO postgres;

--
-- TOC entry 214 (class 1259 OID 17623)
-- Name: mm_metadata_game_systems_info; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE mm_metadata_game_systems_info (
    gs_id uuid NOT NULL,
    gs_game_system_id integer,
    gs_game_system_name text,
    gs_game_system_alias text,
    gs_game_system_json jsonb
);


ALTER TABLE mm_metadata_game_systems_info OWNER TO postgres;

--
-- TOC entry 208 (class 1259 OID 17565)
-- Name: mm_metadata_logo; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE mm_metadata_logo (
    mm_metadata_logo_guid uuid NOT NULL,
    mm_metadata_logo_media_guid jsonb,
    mm_metadata_logo_image_path text
);


ALTER TABLE mm_metadata_logo OWNER TO postgres;

--
-- TOC entry 194 (class 1259 OID 17431)
-- Name: mm_metadata_movie; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE mm_metadata_movie (
    mm_metadata_guid uuid NOT NULL,
    mm_metadata_media_id jsonb,
    mm_media_name text,
    mm_metadata_json jsonb,
    mm_metadata_localimage_json jsonb,
    mm_metadata_user_json jsonb
);


ALTER TABLE mm_metadata_movie OWNER TO postgres;

--
-- TOC entry 191 (class 1259 OID 17392)
-- Name: mm_metadata_music; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE mm_metadata_music (
    mm_metadata_music_guid uuid NOT NULL,
    mm_metadata_media_music_id jsonb,
    mm_metadata_music_name text,
    mm_metadata_music_json jsonb,
    mm_metadata_music_album_guid uuid
);


ALTER TABLE mm_metadata_music OWNER TO postgres;

--
-- TOC entry 195 (class 1259 OID 17447)
-- Name: mm_metadata_music_video; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE mm_metadata_music_video (
    mm_metadata_music_video_guid uuid NOT NULL,
    mm_metadata_music_video_media_id jsonb,
    mm_media_music_video_band text,
    mm_media_music_video_song text,
    mm_metadata_music_video_json jsonb,
    mm_metadata_music_video_localimage_json jsonb
);


ALTER TABLE mm_metadata_music_video OWNER TO postgres;

--
-- TOC entry 189 (class 1259 OID 17367)
-- Name: mm_metadata_musician; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE mm_metadata_musician (
    mm_metadata_musician_guid uuid NOT NULL,
    mm_metadata_musician_name text,
    mm_metadata_musician_id jsonb,
    mm_metadata_musician_json jsonb
);


ALTER TABLE mm_metadata_musician OWNER TO postgres;

--
-- TOC entry 215 (class 1259 OID 17632)
-- Name: mm_metadata_person; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE mm_metadata_person (
    mmp_id uuid NOT NULL,
    mmp_person_media_id jsonb,
    mmp_person_meta_json jsonb,
    mmp_person_image jsonb,
    mmp_person_name text
);


ALTER TABLE mm_metadata_person OWNER TO postgres;

--
-- TOC entry 188 (class 1259 OID 17349)
-- Name: mm_metadata_sports; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE mm_metadata_sports (
    mm_metadata_sports_guid uuid NOT NULL,
    mm_metadata_media_sports_id jsonb,
    mm_metadata_sports_name text,
    mm_metadata_sports_json jsonb,
    mm_metadata_sports_image_json jsonb
);


ALTER TABLE mm_metadata_sports OWNER TO postgres;

--
-- TOC entry 187 (class 1259 OID 17330)
-- Name: mm_metadata_tvshow; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE mm_metadata_tvshow (
    mm_metadata_tvshow_guid uuid NOT NULL,
    mm_metadata_media_tvshow_id jsonb,
    mm_metadata_tvshow_name text,
    mm_metadata_tvshow_json jsonb,
    mm_metadata_tvshow_localimage_json jsonb,
    mm_metadata_tvshow_user_json jsonb
);


ALTER TABLE mm_metadata_tvshow OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 17671)
-- Name: mm_nas; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE mm_nas (
    mm_nas_id uuid NOT NULL,
    mm_nas_json jsonb
);


ALTER TABLE mm_nas OWNER TO postgres;

--
-- TOC entry 198 (class 1259 OID 17484)
-- Name: mm_notification; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE mm_notification (
    mm_notification_guid uuid NOT NULL,
    mm_notification_text text,
    mm_notification_time timestamp without time zone,
    mm_notification_dismissable boolean
);


ALTER TABLE mm_notification OWNER TO postgres;

--
-- TOC entry 212 (class 1259 OID 17604)
-- Name: mm_options_and_status; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE mm_options_and_status (
    mm_options_and_status_guid uuid NOT NULL,
    mm_options_json jsonb,
    mm_status_json jsonb
);


ALTER TABLE mm_options_and_status OWNER TO postgres;

--
-- TOC entry 204 (class 1259 OID 17535)
-- Name: mm_radio; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE mm_radio (
    mm_radio_guid uuid NOT NULL,
    mm_radio_name text,
    mm_radio_adress text,
    mm_radio_active boolean
);


ALTER TABLE mm_radio OWNER TO postgres;

--
-- TOC entry 201 (class 1259 OID 17506)
-- Name: mm_review; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE mm_review (
    mm_review_guid uuid NOT NULL,
    mm_review_metadata_id jsonb,
    mm_review_metadata_guid uuid,
    mm_review_json jsonb
);


ALTER TABLE mm_review OWNER TO postgres;

--
-- TOC entry 205 (class 1259 OID 17543)
-- Name: mm_sync; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE mm_sync (
    mm_sync_guid uuid NOT NULL,
    mm_sync_path text,
    mm_sync_path_to text,
    mm_sync_options_json jsonb
);


ALTER TABLE mm_sync OWNER TO postgres;

--
-- TOC entry 207 (class 1259 OID 17557)
-- Name: mm_trigger; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE mm_trigger (
    mm_trigger_guid uuid NOT NULL,
    mm_trigger_command bytea,
    mm_trigger_background boolean
);


ALTER TABLE mm_trigger OWNER TO postgres;

--
-- TOC entry 218 (class 1259 OID 17663)
-- Name: mm_tuner; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE mm_tuner (
    mm_tuner_id uuid NOT NULL,
    mm_tuner_json jsonb
);


ALTER TABLE mm_tuner OWNER TO postgres;

--
-- TOC entry 222 (class 1259 OID 17699)
-- Name: mm_tv_schedule; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE mm_tv_schedule (
    mm_tv_schedule_id uuid NOT NULL,
    mm_tv_schedule_station_id text,
    mm_tv_schedule_date date,
    mm_tv_schedule_json jsonb
);


ALTER TABLE mm_tv_schedule OWNER TO postgres;

--
-- TOC entry 223 (class 1259 OID 17709)
-- Name: mm_tv_schedule_program; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE mm_tv_schedule_program (
    mm_tv_schedule_program_guid uuid NOT NULL,
    mm_tv_schedule_program_id text,
    mm_tv_schedule_program_json jsonb
);


ALTER TABLE mm_tv_schedule_program OWNER TO postgres;

--
-- TOC entry 221 (class 1259 OID 17689)
-- Name: mm_tv_stations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE mm_tv_stations (
    mm_tv_stations_id uuid NOT NULL,
    mm_tv_station_name text,
    mm_tv_station_id text,
    mm_tv_station_channel text,
    mm_tv_station_json jsonb,
    mm_tv_station_image text
);


ALTER TABLE mm_tv_stations OWNER TO postgres;

--
-- TOC entry 200 (class 1259 OID 17496)
-- Name: mm_user; Type: TABLE; Schema: public; Owner: postgres
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


ALTER TABLE mm_user OWNER TO postgres;

--
-- TOC entry 197 (class 1259 OID 17474)
-- Name: mm_user_activity; Type: TABLE; Schema: public; Owner: postgres
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


ALTER TABLE mm_user_activity OWNER TO postgres;

--
-- TOC entry 210 (class 1259 OID 17586)
-- Name: mm_user_group; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE mm_user_group (
    mm_user_group_guid uuid NOT NULL,
    mm_user_group_name text,
    mm_user_group_description text,
    mm_user_group_rights_json jsonb
);


ALTER TABLE mm_user_group OWNER TO postgres;

--
-- TOC entry 199 (class 1259 OID 17494)
-- Name: mm_user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE mm_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE mm_user_id_seq OWNER TO postgres;

--
-- TOC entry 2544 (class 0 OID 0)
-- Dependencies: 199
-- Name: mm_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE mm_user_id_seq OWNED BY mm_user.id;


--
-- TOC entry 211 (class 1259 OID 17595)
-- Name: mm_user_profile; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE mm_user_profile (
    mm_user_profile_guid uuid NOT NULL,
    mm_user_profile_name text,
    mm_user_profile_json jsonb
);


ALTER TABLE mm_user_profile OWNER TO postgres;

--
-- TOC entry 181 (class 1259 OID 17275)
-- Name: mm_version; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE mm_version (
    mm_version_no text
);


ALTER TABLE mm_version OWNER TO postgres;

--
-- TOC entry 2187 (class 2604 OID 17499)
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY mm_user ALTER COLUMN id SET DEFAULT nextval('mm_user_id_seq'::regclass);


--
-- TOC entry 2521 (class 0 OID 17574)
-- Dependencies: 209
-- Data for Name: mm_channel; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY mm_channel (mm_channel_guid, mm_channel_name, mm_channel_media_id, mm_channel_country_guid, mm_channel_logo_guid) FROM stdin;
\.


--
-- TOC entry 2515 (class 0 OID 17527)
-- Dependencies: 203
-- Data for Name: mm_cron; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY mm_cron (mm_cron_guid, mm_cron_name, mm_cron_description, mm_cron_enabled, mm_cron_schedule, mm_cron_last_run, mm_cron_file_path) FROM stdin;
d81e8480-642f-4d1d-8d53-54373f2f8165	Game Audit	Scan for new game media	f	Days 1	1970-01-01 00:00:01	./subprogram_game_audit.py
27bff79f-f7be-440c-9500-30a47e5fbe20	Create Chapter Image	Create chapter images for all media	f	Days 1	1970-01-01 00:00:01	./subprogram_create_chapter_images.py
d2bb3309-853b-47e6-a38d-057c19e25ce2	Anime	Match anime via Scudlee data	f	Days 1	1970-01-01 00:00:01	./subprogram_match_anime_id_scudlee.py
26297cb7-a93e-4077-b414-d8d17da8417e	Roku Thumb	Generate Roku thumbnail images	f	Days 1	1970-01-01 00:00:01	./subprogram_roku_thumbnail_generate.py
b1744302-6cc5-4f26-ab31-c557bf306de8	Schedules Direct	Fetch TV schedules from Schedules Direct	f	Days 1	1970-01-01 00:00:01	./subprogram_schedules_direct_updates.py
98876537-ea55-4d2f-9d01-e66f2e29a94a	Subtitle	Download missing subtitles for media	f	Days 1	1970-01-01 00:00:01	./subprogram_subtitle_downloader.py
812d690c-1c95-4e67-9fd8-68351baab66e	TheTVDB Update	Grab updated TheTVDB metadata	f	Days 1	1970-01-01 00:00:01	./subprogram_thetvdb_updates.py
d1c21eb9-9023-4003-88d6-edc644f205a3	The Movie Database	Grab updated movie metadata	f	Days 1	1970-01-01 00:00:01	./subprogram_tmdb_updates.py
35814227-abf2-45c5-b9bd-91011e155ded	TVmaze Update	Grab updated TVmaze metadata	f	Days 1	1970-01-01 00:00:01	./subprogram_tvmaze_updates.py
a3cf3d7e-ad07-4a1e-b4ff-3d24ecf1a037	Collections	Create and update collection(s)	f	Days 1	1970-01-01 00:00:01	./subprogram_update_create_collections.py
98c88283-84fd-4a66-8e75-0ce5a2c57c4f	Media Scan	Scan for new media	f	Days 1	1970-01-01 00:00:01	./subprogram_file_scan.py
a8b817ae-74ed-49f6-8ab7-fce9fd868ea0	iRadio Scan	Scan for iRadio stations	f	Days 1	1970-01-01 00:00:01	./subprogram_iradio_channels.py
eb0678ba-8094-4fa1-8614-de1bd1b7fd12	Backup	Backup Postgresql DB	f	Days 1	1970-01-01 00:00:01	./subprogram_postgresql_backup.py
f7bd220f-9b65-4c5c-8d27-068fcf6e7eb3	DB Vacuum	Postgresql Vacuum Analyze all tables	f	Days 1	1970-01-01 00:00:01	./subprogram_postgresql_vacuum.py
7aee3a4f-f2d1-4755-b9ca-4dbe2b763ecd	Sync	Sync/Transcode media	f	Days 1	1970-01-01 00:00:01	./subprogram_sync.py
\.


--
-- TOC entry 2532 (class 0 OID 17679)
-- Dependencies: 220
-- Data for Name: mm_device; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY mm_device (mm_device_id, mm_device_type, mm_device_json) FROM stdin;
\.


--
-- TOC entry 2529 (class 0 OID 17654)
-- Dependencies: 217
-- Data for Name: mm_download_image_que; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY mm_download_image_que (mdq_image_id, mdq_image_provider, mdq_image_download_json) FROM stdin;
\.


--
-- TOC entry 2528 (class 0 OID 17643)
-- Dependencies: 216
-- Data for Name: mm_download_que; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY mm_download_que (mdq_id, mdq_provider, mqd_que_type, mdq_download_json) FROM stdin;
\.


--
-- TOC entry 2498 (class 0 OID 17320)
-- Dependencies: 186
-- Data for Name: mm_link; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY mm_link (mm_link_guid, mm_link_name, mm_link_json) FROM stdin;
\.


--
-- TOC entry 2518 (class 0 OID 17552)
-- Dependencies: 206
-- Data for Name: mm_loan; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY mm_loan (mm_loan_guid, mm_loan_media_id, mm_loan_user_id, mm_load_user_loan_id, mm_loan_time, mm_loan_return_time) FROM stdin;
\.


--
-- TOC entry 2496 (class 0 OID 17298)
-- Dependencies: 184
-- Data for Name: mm_media; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY mm_media (mm_media_guid, mm_media_class_guid, mm_media_metadata_guid, mm_media_path, mm_media_ffprobe_json, mm_media_json) FROM stdin;
\.


--
-- TOC entry 2504 (class 0 OID 17405)
-- Dependencies: 192
-- Data for Name: mm_media_class; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY mm_media_class (mm_media_class_guid, mm_media_class_type, mm_media_class_parent_type, mm_media_class_display) FROM stdin;
faca08b4-da07-40c3-a4e1-e9bd9cb877af	Adult	Video	t
2f93025f-d572-4cf1-8969-6d1243237b25	Anime	Video	t
d4ec6b23-5d42-4bd9-bb55-f767274209b4	Book	Publication	t
4b2e84c8-02d8-4695-8b84-ceb92c852d18	Boxset	\N	f
3880b47d-4a85-4779-b239-934139b369c1	Game CHD	\N	f
99d97c75-0f0e-4251-8f23-9a3b45e244e6	Game ISO	\N	f
65e7f0f8-64ba-4d35-9500-84566dd51776	Game ROM	\N	f
691b5261-9b38-498f-a33d-0da8bf10a797	Home Movie	Video	t
7f12c18c-49c3-45a3-a3c1-65bb868e7271	Magazine	Publication	t
7ea31126-0040-4ccf-be24-462e2aeb3399	Movie	Video	t
cdcc136d-0129-4471-8655-e523500bc21a	Movie Extras	Video	f
1f4161d6-e70a-4acb-9b3f-59aefe0b8dce	Movie Collection	\N	f
75b741cc-be02-4e63-8069-e5a70df0f8d4	Movie Theme	Audio	f
6c6557e0-cad2-41b8-a3e9-be1a96656066	Movie Trailer	Video	f
ef5563c7-91f3-4b55-8b65-b009fc1d16b3	Music	Audio	t
f6489c2d-3aae-48a3-a8ea-daeabc20167e	Music Album	\N	f
b82a3c2f-be2e-4c65-bac6-010ac684e340	Music Collection	\N	f
977b9c9b-dd91-4c82-a3c0-e0161db71482	Music Lyric	\N	f
91cfad08-f7e9-4a2c-a596-364c0d45b522	Music Video	Video	t
c2bcb890-7cbd-4437-b4f7-db31026da2b0	Person	\N	f
ef8afd2a-0400-4071-baf5-17878d758a46	Picture	Image	t
3e85027d-97a0-409a-a9bf-e01bb744e85c	Soundtrack	Audio	f
22051608-1e9a-48d4-8ed3-0e6fe996cde7	Sports	Video	t
2a6971fc-484f-4dab-8473-93151577f6b8	Subtitle	\N	f
852dbd1e-fc55-48a8-a964-55a1f1ecfc04	TV Episode	Video	f
c0e417dc-786e-4ecb-a0c3-b71b97f7fca7	TV Extras	Video	f
9b5de5b5-a62f-4d37-9014-10b8d6c96d0a	TV Season	\N	f
84737613-b836-46d1-8f39-42d312b3e084	TV Show	Video	t
fc2e0207-bb9c-4efc-9491-b62dc0ed887f	TV Theme	Audio	f
96837b7e-fc64-474c-b1ac-ba974f3caefe	TV Trailer	Video	f
d24a1ef2-c752-4c39-a823-cfc6378fc25b	Video Game	Game	t
1fc31e1e-5797-47c7-a696-0ab367fbe14f	Video Game Intro	Video	t
1f616828-e5a0-493e-b5e3-f4c26cae2f6c	Video Game Speedrun	Video	t
61073759-4be8-4d81-9b11-912ca3371454	Video Game Superplay	Video	t
\.


--
-- TOC entry 2495 (class 0 OID 17289)
-- Dependencies: 183
-- Data for Name: mm_media_dir; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY mm_media_dir (mm_media_dir_guid, mm_media_dir_path, mm_media_dir_class_type, mm_media_dir_last_scanned, mm_media_dir_share_guid, mm_media_dir_status) FROM stdin;
\.


--
-- TOC entry 2497 (class 0 OID 17309)
-- Dependencies: 185
-- Data for Name: mm_media_remote; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY mm_media_remote (mmr_media_guid, mmr_media_link_id, mmr_media_uuid, mmr_media_class_guid, mmr_media_metadata_guid, mmr_media_ffprobe_json, mmr_media_json) FROM stdin;
\.


--
-- TOC entry 2494 (class 0 OID 17281)
-- Dependencies: 182
-- Data for Name: mm_media_share; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY mm_media_share (mm_media_share_guid, mm_media_share_type, mm_media_share_user, mm_media_share_password, mm_media_share_server, mm_media_share_path) FROM stdin;
\.


--
-- TOC entry 2502 (class 0 OID 17379)
-- Dependencies: 190
-- Data for Name: mm_metadata_album; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY mm_metadata_album (mm_metadata_album_guid, mm_metadata_album_name, mm_metadata_album_id, mm_metadata_album_json, mm_metadata_album_musician_guid) FROM stdin;
\.


--
-- TOC entry 2505 (class 0 OID 17414)
-- Dependencies: 193
-- Data for Name: mm_metadata_anime; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY mm_metadata_anime (mm_metadata_anime_guid, mm_metadata_anime_media_id, mm_media_anime_name, mm_metadata_anime_json, mm_metadata_anime_mapping, mm_metadata_anime_mapping_before, mm_metadata_anime_localimage_json, mm_metadata_anime_user_json) FROM stdin;
\.


--
-- TOC entry 2508 (class 0 OID 17462)
-- Dependencies: 196
-- Data for Name: mm_metadata_book; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY mm_metadata_book (mm_metadata_book_guid, mm_metadata_book_isbn, mm_metadata_book_isbn13, mm_metadata_book_name, mm_metadata_book_json) FROM stdin;
\.


--
-- TOC entry 2514 (class 0 OID 17516)
-- Dependencies: 202
-- Data for Name: mm_metadata_collection; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY mm_metadata_collection (mm_metadata_collection_guid, mm_metadata_collection_name, mm_metadata_collection_media_ids, mm_metadata_collection_json, mm_metadata_collection_imagelocal_json) FROM stdin;
\.


--
-- TOC entry 2525 (class 0 OID 17612)
-- Dependencies: 213
-- Data for Name: mm_metadata_game_software_info; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY mm_metadata_game_software_info (gi_id, gi_system_id, gi_game_info_json) FROM stdin;
\.


--
-- TOC entry 2526 (class 0 OID 17623)
-- Dependencies: 214
-- Data for Name: mm_metadata_game_systems_info; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY mm_metadata_game_systems_info (gs_id, gs_game_system_id, gs_game_system_name, gs_game_system_alias, gs_game_system_json) FROM stdin;
\.


--
-- TOC entry 2520 (class 0 OID 17565)
-- Dependencies: 208
-- Data for Name: mm_metadata_logo; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY mm_metadata_logo (mm_metadata_logo_guid, mm_metadata_logo_media_guid, mm_metadata_logo_image_path) FROM stdin;
\.


--
-- TOC entry 2506 (class 0 OID 17431)
-- Dependencies: 194
-- Data for Name: mm_metadata_movie; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY mm_metadata_movie (mm_metadata_guid, mm_metadata_media_id, mm_media_name, mm_metadata_json, mm_metadata_localimage_json, mm_metadata_user_json) FROM stdin;
\.


--
-- TOC entry 2503 (class 0 OID 17392)
-- Dependencies: 191
-- Data for Name: mm_metadata_music; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY mm_metadata_music (mm_metadata_music_guid, mm_metadata_media_music_id, mm_metadata_music_name, mm_metadata_music_json, mm_metadata_music_album_guid) FROM stdin;
\.


--
-- TOC entry 2507 (class 0 OID 17447)
-- Dependencies: 195
-- Data for Name: mm_metadata_music_video; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY mm_metadata_music_video (mm_metadata_music_video_guid, mm_metadata_music_video_media_id, mm_media_music_video_band, mm_media_music_video_song, mm_metadata_music_video_json, mm_metadata_music_video_localimage_json) FROM stdin;
\.


--
-- TOC entry 2501 (class 0 OID 17367)
-- Dependencies: 189
-- Data for Name: mm_metadata_musician; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY mm_metadata_musician (mm_metadata_musician_guid, mm_metadata_musician_name, mm_metadata_musician_id, mm_metadata_musician_json) FROM stdin;
\.


--
-- TOC entry 2527 (class 0 OID 17632)
-- Dependencies: 215
-- Data for Name: mm_metadata_person; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY mm_metadata_person (mmp_id, mmp_person_media_id, mmp_person_meta_json, mmp_person_image, mmp_person_name) FROM stdin;
\.


--
-- TOC entry 2500 (class 0 OID 17349)
-- Dependencies: 188
-- Data for Name: mm_metadata_sports; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY mm_metadata_sports (mm_metadata_sports_guid, mm_metadata_media_sports_id, mm_metadata_sports_name, mm_metadata_sports_json, mm_metadata_sports_image_json) FROM stdin;
\.


--
-- TOC entry 2499 (class 0 OID 17330)
-- Dependencies: 187
-- Data for Name: mm_metadata_tvshow; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY mm_metadata_tvshow (mm_metadata_tvshow_guid, mm_metadata_media_tvshow_id, mm_metadata_tvshow_name, mm_metadata_tvshow_json, mm_metadata_tvshow_localimage_json, mm_metadata_tvshow_user_json) FROM stdin;
\.


--
-- TOC entry 2531 (class 0 OID 17671)
-- Dependencies: 219
-- Data for Name: mm_nas; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY mm_nas (mm_nas_id, mm_nas_json) FROM stdin;
\.


--
-- TOC entry 2510 (class 0 OID 17484)
-- Dependencies: 198
-- Data for Name: mm_notification; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY mm_notification (mm_notification_guid, mm_notification_text, mm_notification_time, mm_notification_dismissable) FROM stdin;
\.


--
-- TOC entry 2524 (class 0 OID 17604)
-- Dependencies: 212
-- Data for Name: mm_options_and_status; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY mm_options_and_status (mm_options_and_status_guid, mm_options_json, mm_status_json) FROM stdin;
226a2619-890b-4fb8-9b17-85750474c3e1	{"SD": {"User": null, "Password": null}, "API": {"anidb": null, "imvdb": null, "google": null, "isbndb": "25C8IT4I", "tvmaze": null, "thetvdb": "147CB43DCA8B61B7", "thelogodb": null, "themoviedb": "f72118d1e84b8a1438935972a9c37cac", "globalcache": null, "mediabrainz": null, "thesportsdb": "4352761817344", "opensubtitles": null, "rottentomatoes": "f4tnu5dn9r7f28gjth3ftqaj"}, "AWSS3": {"Bucket": "mediakraken", "AccessKey": null, "BackupBucket": "mkbackup", "SecretAccessKey": null}, "Trakt": {"ApiKey": null, "ClientID": null, "SecretKey": null}, "Backup": {"Interval": 0, "BackupType": "awss3"}, "Dropbox": {"APIKey": null, "APISecret": null}, "OneDrive": {"ClientID": null, "SecretKey": null}, "GoogleDrive": {"SecretFile": null}, "Maintenance": null, "MediaBrainz": {"Host": null, "Port": 5000, "User": null, "Password": null, "BrainzDBHost": null, "BrainzDBName": null, "BrainzDBPass": null, "BrainzDBPort": 5432, "BrainzDBUser": null}, "MaxResumePct": 5, "Transmission": {"Host": null, "Port": 9091}, "MediaKrakenServer": {"FFMPEG": 8900, "APIPort": 8097, "ImageWeb": 8099, "ListenPort": 8098, "BackupLocal": "/mediakraken/backups/", "MetadataImageLocal": ""}}	{"thetvdb_Updated_Epoc": 0}
\.


--
-- TOC entry 2516 (class 0 OID 17535)
-- Dependencies: 204
-- Data for Name: mm_radio; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY mm_radio (mm_radio_guid, mm_radio_name, mm_radio_adress, mm_radio_active) FROM stdin;
\.


--
-- TOC entry 2513 (class 0 OID 17506)
-- Dependencies: 201
-- Data for Name: mm_review; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY mm_review (mm_review_guid, mm_review_metadata_id, mm_review_metadata_guid, mm_review_json) FROM stdin;
\.


--
-- TOC entry 2517 (class 0 OID 17543)
-- Dependencies: 205
-- Data for Name: mm_sync; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY mm_sync (mm_sync_guid, mm_sync_path, mm_sync_path_to, mm_sync_options_json) FROM stdin;
\.


--
-- TOC entry 2519 (class 0 OID 17557)
-- Dependencies: 207
-- Data for Name: mm_trigger; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY mm_trigger (mm_trigger_guid, mm_trigger_command, mm_trigger_background) FROM stdin;
\.


--
-- TOC entry 2530 (class 0 OID 17663)
-- Dependencies: 218
-- Data for Name: mm_tuner; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY mm_tuner (mm_tuner_id, mm_tuner_json) FROM stdin;
\.


--
-- TOC entry 2534 (class 0 OID 17699)
-- Dependencies: 222
-- Data for Name: mm_tv_schedule; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY mm_tv_schedule (mm_tv_schedule_id, mm_tv_schedule_station_id, mm_tv_schedule_date, mm_tv_schedule_json) FROM stdin;
\.


--
-- TOC entry 2535 (class 0 OID 17709)
-- Dependencies: 223
-- Data for Name: mm_tv_schedule_program; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY mm_tv_schedule_program (mm_tv_schedule_program_guid, mm_tv_schedule_program_id, mm_tv_schedule_program_json) FROM stdin;
\.


--
-- TOC entry 2533 (class 0 OID 17689)
-- Dependencies: 221
-- Data for Name: mm_tv_stations; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY mm_tv_stations (mm_tv_stations_id, mm_tv_station_name, mm_tv_station_id, mm_tv_station_channel, mm_tv_station_json, mm_tv_station_image) FROM stdin;
\.


--
-- TOC entry 2512 (class 0 OID 17496)
-- Dependencies: 200
-- Data for Name: mm_user; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY mm_user (id, username, email, password, created_at, active, is_admin, user_json, lang) FROM stdin;
\.


--
-- TOC entry 2509 (class 0 OID 17474)
-- Dependencies: 197
-- Data for Name: mm_user_activity; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY mm_user_activity (mm_activity_guid, mm_activity_name, mm_activity_overview, mm_activity_short_overview, mm_activity_type, mm_activity_itemid, mm_activity_userid, mm_activity_datecreated, mm_activity_log_severity) FROM stdin;
\.


--
-- TOC entry 2522 (class 0 OID 17586)
-- Dependencies: 210
-- Data for Name: mm_user_group; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY mm_user_group (mm_user_group_guid, mm_user_group_name, mm_user_group_description, mm_user_group_rights_json) FROM stdin;
e70b1953-b64c-4e52-a8f3-688baa79452a	Administrator	Server administrator	{"Admin": true, "PreviewOnly": false}
aadf4e22-c89d-49ed-992a-cde99d219f2a	User	General user	{"Admin": false, "PreviewOnly": false}
3c8b147f-05ee-4e71-b36e-481105501379	Guest	Guest (Preview only)	{"Admin": false, "PreviewOnly": true}
\.


--
-- TOC entry 2545 (class 0 OID 0)
-- Dependencies: 199
-- Name: mm_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('mm_user_id_seq', 1, false);


--
-- TOC entry 2523 (class 0 OID 17595)
-- Dependencies: 211
-- Data for Name: mm_user_profile; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY mm_user_profile (mm_user_profile_guid, mm_user_profile_name, mm_user_profile_json) FROM stdin;
0152cf38-2ebb-48c6-8064-b7c7810cdc42	Adult	{"3D": true, "TV": true, "Home": true, "Lang": "en", "Sync": true, "Adult": true, "Books": true, "Games": true, "MaxBR": 100, "Movie": true, "Music": true, "IRadio": true, "Images": true, "LiveTV": true, "Sports": true, "Internet": true, "MaxRating": 5}
a17c8898-6e8e-45c0-a5b6-c2a5a5327921	Teen	{"3D": true, "TV": true, "Home": true, "Lang": "en", "Sync": false, "Adult": false, "Books": true, "Games": true, "MaxBR": 50, "Movie": true, "Music": true, "IRadio": true, "Images": true, "LiveTV": true, "Sports": true, "Internet": true, "MaxRating": 3}
4fd08a79-ab81-438a-a185-0e9064b616b6	Child	{"3D": false, "TV": true, "Home": true, "Lang": "en", "Sync": false, "Adult": false, "Books": true, "Games": true, "MaxBR": 20, "Movie": true, "Music": true, "IRadio": false, "Images": true, "LiveTV": false, "Sports": true, "Internet": false, "MaxRating": 0}
\.


--
-- TOC entry 2493 (class 0 OID 17275)
-- Dependencies: 181
-- Data for Name: mm_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY mm_version (mm_version_no) FROM stdin;
2
\.


--
-- TOC entry 2340 (class 2606 OID 17619)
-- Name: gi_id_mpk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY mm_metadata_game_software_info
    ADD CONSTRAINT gi_id_mpk PRIMARY KEY (gi_id);


--
-- TOC entry 2345 (class 2606 OID 17630)
-- Name: gs_id_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY mm_metadata_game_systems_info
    ADD CONSTRAINT gs_id_pk PRIMARY KEY (gs_id);


--
-- TOC entry 2353 (class 2606 OID 17650)
-- Name: mdq_id_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY mm_download_que
    ADD CONSTRAINT mdq_id_pk PRIMARY KEY (mdq_id);


--
-- TOC entry 2358 (class 2606 OID 17661)
-- Name: mdq_image_id_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY mm_download_image_que
    ADD CONSTRAINT mdq_image_id_pk PRIMARY KEY (mdq_image_id);


--
-- TOC entry 2292 (class 2606 OID 17481)
-- Name: mm_activity_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY mm_user_activity
    ADD CONSTRAINT mm_activity_pk PRIMARY KEY (mm_activity_guid);


--
-- TOC entry 2326 (class 2606 OID 17581)
-- Name: mm_channel_guid_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY mm_channel
    ADD CONSTRAINT mm_channel_guid_pk PRIMARY KEY (mm_channel_guid);


--
-- TOC entry 2312 (class 2606 OID 17534)
-- Name: mm_cron_guid_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY mm_cron
    ADD CONSTRAINT mm_cron_guid_pk PRIMARY KEY (mm_cron_guid);


--
-- TOC entry 2365 (class 2606 OID 17686)
-- Name: mm_device_id_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY mm_device
    ADD CONSTRAINT mm_device_id_pk PRIMARY KEY (mm_device_id);


--
-- TOC entry 2204 (class 2606 OID 17327)
-- Name: mm_link_guid_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY mm_link
    ADD CONSTRAINT mm_link_guid_pk PRIMARY KEY (mm_link_guid);


--
-- TOC entry 2319 (class 2606 OID 17556)
-- Name: mm_loan_guid_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY mm_loan
    ADD CONSTRAINT mm_loan_guid_pk PRIMARY KEY (mm_loan_guid);


--
-- TOC entry 2254 (class 2606 OID 17412)
-- Name: mm_media_class_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY mm_media_class
    ADD CONSTRAINT mm_media_class_pk PRIMARY KEY (mm_media_class_guid);


--
-- TOC entry 2192 (class 2606 OID 17296)
-- Name: mm_media_dir_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY mm_media_dir
    ADD CONSTRAINT mm_media_dir_pk PRIMARY KEY (mm_media_dir_guid);


--
-- TOC entry 2197 (class 2606 OID 17305)
-- Name: mm_media_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY mm_media
    ADD CONSTRAINT mm_media_pk PRIMARY KEY (mm_media_guid);


--
-- TOC entry 2189 (class 2606 OID 17288)
-- Name: mm_media_share_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY mm_media_share
    ADD CONSTRAINT mm_media_share_pk PRIMARY KEY (mm_media_share_guid);


--
-- TOC entry 2244 (class 2606 OID 17386)
-- Name: mm_metadata_album_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY mm_metadata_album
    ADD CONSTRAINT mm_metadata_album_pk PRIMARY KEY (mm_metadata_album_guid);


--
-- TOC entry 2265 (class 2606 OID 17421)
-- Name: mm_metadata_anime_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY mm_metadata_anime
    ADD CONSTRAINT mm_metadata_anime_pk PRIMARY KEY (mm_metadata_anime_guid);


--
-- TOC entry 2286 (class 2606 OID 17469)
-- Name: mm_metadata_book_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY mm_metadata_book
    ADD CONSTRAINT mm_metadata_book_pk PRIMARY KEY (mm_metadata_book_guid);


--
-- TOC entry 2307 (class 2606 OID 17523)
-- Name: mm_metadata_collection_guid_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY mm_metadata_collection
    ADD CONSTRAINT mm_metadata_collection_guid_pk PRIMARY KEY (mm_metadata_collection_guid);


--
-- TOC entry 2323 (class 2606 OID 17572)
-- Name: mm_metadata_logo_guid_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY mm_metadata_logo
    ADD CONSTRAINT mm_metadata_logo_guid_pk PRIMARY KEY (mm_metadata_logo_guid);


--
-- TOC entry 2251 (class 2606 OID 17399)
-- Name: mm_metadata_music_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY mm_metadata_music
    ADD CONSTRAINT mm_metadata_music_pk PRIMARY KEY (mm_metadata_music_guid);


--
-- TOC entry 2284 (class 2606 OID 17454)
-- Name: mm_metadata_music_video_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY mm_metadata_music_video
    ADD CONSTRAINT mm_metadata_music_video_pk PRIMARY KEY (mm_metadata_music_video_guid);


--
-- TOC entry 2237 (class 2606 OID 17374)
-- Name: mm_metadata_musician_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY mm_metadata_musician
    ADD CONSTRAINT mm_metadata_musician_pk PRIMARY KEY (mm_metadata_musician_guid);


--
-- TOC entry 2275 (class 2606 OID 17438)
-- Name: mm_metadata_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY mm_metadata_movie
    ADD CONSTRAINT mm_metadata_pk PRIMARY KEY (mm_metadata_guid);


--
-- TOC entry 2231 (class 2606 OID 17356)
-- Name: mm_metadata_sports_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY mm_metadata_sports
    ADD CONSTRAINT mm_metadata_sports_pk PRIMARY KEY (mm_metadata_sports_guid);


--
-- TOC entry 2219 (class 2606 OID 17337)
-- Name: mm_metadata_tvshow_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY mm_metadata_tvshow
    ADD CONSTRAINT mm_metadata_tvshow_pk PRIMARY KEY (mm_metadata_tvshow_guid);


--
-- TOC entry 2363 (class 2606 OID 17678)
-- Name: mm_nas_id_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY mm_nas
    ADD CONSTRAINT mm_nas_id_pk PRIMARY KEY (mm_nas_id);


--
-- TOC entry 2298 (class 2606 OID 17491)
-- Name: mm_notification_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY mm_notification
    ADD CONSTRAINT mm_notification_pk PRIMARY KEY (mm_notification_guid);


--
-- TOC entry 2338 (class 2606 OID 17611)
-- Name: mm_options_and_status_guid_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY mm_options_and_status
    ADD CONSTRAINT mm_options_and_status_guid_pk PRIMARY KEY (mm_options_and_status_guid);


--
-- TOC entry 2314 (class 2606 OID 17542)
-- Name: mm_radio_guid_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY mm_radio
    ADD CONSTRAINT mm_radio_guid_pk PRIMARY KEY (mm_radio_guid);


--
-- TOC entry 2305 (class 2606 OID 17513)
-- Name: mm_review_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY mm_review
    ADD CONSTRAINT mm_review_pk PRIMARY KEY (mm_review_guid);


--
-- TOC entry 2316 (class 2606 OID 17550)
-- Name: mm_sync_guid_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY mm_sync
    ADD CONSTRAINT mm_sync_guid_pk PRIMARY KEY (mm_sync_guid);


--
-- TOC entry 2321 (class 2606 OID 17564)
-- Name: mm_trigger_guid_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY mm_trigger
    ADD CONSTRAINT mm_trigger_guid_pk PRIMARY KEY (mm_trigger_guid);


--
-- TOC entry 2361 (class 2606 OID 17670)
-- Name: mm_tuner_id_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY mm_tuner
    ADD CONSTRAINT mm_tuner_id_pk PRIMARY KEY (mm_tuner_id);


--
-- TOC entry 2373 (class 2606 OID 17706)
-- Name: mm_tv_schedule_id_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY mm_tv_schedule
    ADD CONSTRAINT mm_tv_schedule_id_pk PRIMARY KEY (mm_tv_schedule_id);


--
-- TOC entry 2378 (class 2606 OID 17716)
-- Name: mm_tv_schedule_program_guid_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY mm_tv_schedule_program
    ADD CONSTRAINT mm_tv_schedule_program_guid_pk PRIMARY KEY (mm_tv_schedule_program_guid);


--
-- TOC entry 2369 (class 2606 OID 17696)
-- Name: mm_tv_stations_id_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY mm_tv_stations
    ADD CONSTRAINT mm_tv_stations_id_pk PRIMARY KEY (mm_tv_stations_id);


--
-- TOC entry 2332 (class 2606 OID 17593)
-- Name: mm_user_group_guid_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY mm_user_group
    ADD CONSTRAINT mm_user_group_guid_pk PRIMARY KEY (mm_user_group_guid);


--
-- TOC entry 2301 (class 2606 OID 17504)
-- Name: mm_user_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY mm_user
    ADD CONSTRAINT mm_user_pkey PRIMARY KEY (id);


--
-- TOC entry 2335 (class 2606 OID 17602)
-- Name: mm_user_profile_guid_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY mm_user_profile
    ADD CONSTRAINT mm_user_profile_guid_pk PRIMARY KEY (mm_user_profile_guid);


--
-- TOC entry 2351 (class 2606 OID 17639)
-- Name: mmp_id_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY mm_metadata_person
    ADD CONSTRAINT mmp_id_pk PRIMARY KEY (mmp_id);


--
-- TOC entry 2202 (class 2606 OID 17316)
-- Name: mmr_media_remote_pk; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY mm_media_remote
    ADD CONSTRAINT mmr_media_remote_pk PRIMARY KEY (mmr_media_guid);


--
-- TOC entry 2341 (class 1259 OID 17620)
-- Name: gi_system_id_ndx; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX gi_system_id_ndx ON mm_metadata_game_software_info USING btree (gi_system_id);


--
-- TOC entry 2327 (class 1259 OID 17584)
-- Name: mm_channel_idx_country; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_channel_idx_country ON mm_channel USING btree (mm_channel_country_guid);


--
-- TOC entry 2328 (class 1259 OID 17585)
-- Name: mm_channel_idx_logo; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_channel_idx_logo ON mm_channel USING btree (mm_channel_logo_guid);


--
-- TOC entry 2329 (class 1259 OID 17582)
-- Name: mm_channel_idx_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_channel_idx_name ON mm_channel USING btree (mm_channel_name);


--
-- TOC entry 2330 (class 1259 OID 17583)
-- Name: mm_channel_idxgin_json; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_channel_idxgin_json ON mm_channel USING gin (mm_channel_media_id);


--
-- TOC entry 2366 (class 1259 OID 17687)
-- Name: mm_device_idx_type; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_device_idx_type ON mm_device USING btree (mm_device_type);


--
-- TOC entry 2367 (class 1259 OID 17688)
-- Name: mm_device_idxgin_json; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_device_idxgin_json ON mm_device USING gin (mm_device_json);


--
-- TOC entry 2354 (class 1259 OID 17651)
-- Name: mm_download_idx_provider; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_download_idx_provider ON mm_download_que USING btree (mdq_provider);


--
-- TOC entry 2355 (class 1259 OID 17652)
-- Name: mm_download_que_idxgin_meta_json; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_download_que_idxgin_meta_json ON mm_download_que USING gin (mdq_download_json);


--
-- TOC entry 2342 (class 1259 OID 17621)
-- Name: mm_game_info_idxgin_json; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_game_info_idxgin_json ON mm_metadata_game_software_info USING gin (gi_game_info_json);


--
-- TOC entry 2343 (class 1259 OID 17622)
-- Name: mm_game_info_idxgin_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_game_info_idxgin_name ON mm_metadata_game_software_info USING gin (((gi_game_info_json -> '@name'::text)));


--
-- TOC entry 2346 (class 1259 OID 17631)
-- Name: mm_game_systems_idxgin_json; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_game_systems_idxgin_json ON mm_metadata_game_systems_info USING gin (gs_game_system_json);


--
-- TOC entry 2359 (class 1259 OID 17662)
-- Name: mm_image_download_idx_provider; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_image_download_idx_provider ON mm_download_image_que USING btree (mdq_image_provider);


--
-- TOC entry 2205 (class 1259 OID 17329)
-- Name: mm_link_idx_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_link_idx_name ON mm_link USING btree (mm_link_name);


--
-- TOC entry 2206 (class 1259 OID 17328)
-- Name: mm_link_json_idxgin; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_link_json_idxgin ON mm_link USING gin (mm_link_json);


--
-- TOC entry 2252 (class 1259 OID 17413)
-- Name: mm_media_class_idx_type; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_media_class_idx_type ON mm_media_class USING btree (mm_media_class_type);


--
-- TOC entry 2190 (class 1259 OID 17297)
-- Name: mm_media_dir_idx_share; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_media_dir_idx_share ON mm_media_dir USING btree (mm_media_dir_share_guid);


--
-- TOC entry 2193 (class 1259 OID 17307)
-- Name: mm_media_idx_metadata_uuid; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_media_idx_metadata_uuid ON mm_media USING btree (mm_media_metadata_guid);


--
-- TOC entry 2194 (class 1259 OID 17308)
-- Name: mm_media_idx_path; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_media_idx_path ON mm_media USING btree (mm_media_path);


--
-- TOC entry 2195 (class 1259 OID 17306)
-- Name: mm_media_idxgin_ffprobe; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_media_idxgin_ffprobe ON mm_media USING gin (mm_media_ffprobe_json);


--
-- TOC entry 2238 (class 1259 OID 17391)
-- Name: mm_metadata_album_idx_musician; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_album_idx_musician ON mm_metadata_album USING btree (mm_metadata_album_musician_guid);


--
-- TOC entry 2239 (class 1259 OID 17387)
-- Name: mm_metadata_album_idx_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_album_idx_name ON mm_metadata_album USING btree (mm_metadata_album_name);


--
-- TOC entry 2240 (class 1259 OID 17388)
-- Name: mm_metadata_album_idx_name_lower; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_album_idx_name_lower ON mm_metadata_album USING btree (lower(mm_metadata_album_name));


--
-- TOC entry 2241 (class 1259 OID 17389)
-- Name: mm_metadata_album_idxgin_id_json; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_album_idxgin_id_json ON mm_metadata_album USING gin (mm_metadata_album_id);


--
-- TOC entry 2242 (class 1259 OID 17390)
-- Name: mm_metadata_album_idxgin_json; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_album_idxgin_json ON mm_metadata_album USING gin (mm_metadata_album_json);


--
-- TOC entry 2255 (class 1259 OID 17425)
-- Name: mm_metadata_aniem_idxgin_media_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_aniem_idxgin_media_id ON mm_metadata_anime USING gin (mm_metadata_anime_media_id);


--
-- TOC entry 2256 (class 1259 OID 17422)
-- Name: mm_metadata_anime_idx_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_anime_idx_name ON mm_metadata_anime USING btree (mm_media_anime_name);


--
-- TOC entry 2257 (class 1259 OID 17423)
-- Name: mm_metadata_anime_idx_name_lower; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_anime_idx_name_lower ON mm_metadata_anime USING btree (lower(mm_media_anime_name));


--
-- TOC entry 2258 (class 1259 OID 17424)
-- Name: mm_metadata_anime_idxgin_json; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_anime_idxgin_json ON mm_metadata_anime USING gin (mm_metadata_anime_json);


--
-- TOC entry 2259 (class 1259 OID 17426)
-- Name: mm_metadata_anime_idxgin_media_id_anidb; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_anime_idxgin_media_id_anidb ON mm_metadata_anime USING gin (((mm_metadata_anime_media_id -> 'anidb'::text)));


--
-- TOC entry 2260 (class 1259 OID 17429)
-- Name: mm_metadata_anime_idxgin_media_id_imdb; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_anime_idxgin_media_id_imdb ON mm_metadata_anime USING gin (((mm_metadata_anime_media_id -> 'imdb'::text)));


--
-- TOC entry 2261 (class 1259 OID 17427)
-- Name: mm_metadata_anime_idxgin_media_id_thetvdb; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_anime_idxgin_media_id_thetvdb ON mm_metadata_anime USING gin (((mm_metadata_anime_media_id -> 'thetvdb'::text)));


--
-- TOC entry 2262 (class 1259 OID 17428)
-- Name: mm_metadata_anime_idxgin_media_id_tmdb; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_anime_idxgin_media_id_tmdb ON mm_metadata_anime USING gin (((mm_metadata_anime_media_id -> 'tmdb'::text)));


--
-- TOC entry 2263 (class 1259 OID 17430)
-- Name: mm_metadata_anime_idxgin_user_json; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_anime_idxgin_user_json ON mm_metadata_anime USING gin (mm_metadata_anime_user_json);


--
-- TOC entry 2308 (class 1259 OID 17524)
-- Name: mm_metadata_collection_idxgin_media_json; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_collection_idxgin_media_json ON mm_metadata_collection USING gin (mm_metadata_collection_media_ids);


--
-- TOC entry 2309 (class 1259 OID 17526)
-- Name: mm_metadata_collection_idxgin_meta_json; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_collection_idxgin_meta_json ON mm_metadata_collection USING gin (mm_metadata_collection_json);


--
-- TOC entry 2310 (class 1259 OID 17525)
-- Name: mm_metadata_collection_idxgin_name_json; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_collection_idxgin_name_json ON mm_metadata_collection USING gin (mm_metadata_collection_name);


--
-- TOC entry 2276 (class 1259 OID 17455)
-- Name: mm_metadata_idx_band_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_idx_band_name ON mm_metadata_music_video USING btree (mm_media_music_video_band);


--
-- TOC entry 2277 (class 1259 OID 17456)
-- Name: mm_metadata_idx_band_name_lower; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_idx_band_name_lower ON mm_metadata_music_video USING btree (lower(mm_media_music_video_band));


--
-- TOC entry 2287 (class 1259 OID 17470)
-- Name: mm_metadata_idx_book_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_idx_book_name ON mm_metadata_book USING btree (mm_metadata_book_name);


--
-- TOC entry 2288 (class 1259 OID 17471)
-- Name: mm_metadata_idx_book_name_lower; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_idx_book_name_lower ON mm_metadata_book USING btree (lower(mm_metadata_book_name));


--
-- TOC entry 2266 (class 1259 OID 17439)
-- Name: mm_metadata_idx_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_idx_name ON mm_metadata_movie USING btree (mm_media_name);


--
-- TOC entry 2267 (class 1259 OID 17440)
-- Name: mm_metadata_idx_name_lower; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_idx_name_lower ON mm_metadata_movie USING btree (lower(mm_media_name));


--
-- TOC entry 2278 (class 1259 OID 17457)
-- Name: mm_metadata_idx_song_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_idx_song_name ON mm_metadata_music_video USING btree (mm_media_music_video_song);


--
-- TOC entry 2279 (class 1259 OID 17458)
-- Name: mm_metadata_idx_song_name_lower; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_idx_song_name_lower ON mm_metadata_music_video USING btree (lower(mm_media_music_video_song));


--
-- TOC entry 2289 (class 1259 OID 17472)
-- Name: mm_metadata_idxgin_isbn; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_idxgin_isbn ON mm_metadata_book USING btree (mm_metadata_book_isbn);


--
-- TOC entry 2290 (class 1259 OID 17473)
-- Name: mm_metadata_idxgin_isbn13; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_idxgin_isbn13 ON mm_metadata_book USING btree (mm_metadata_book_isbn13);


--
-- TOC entry 2268 (class 1259 OID 17441)
-- Name: mm_metadata_idxgin_json; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_idxgin_json ON mm_metadata_movie USING gin (mm_metadata_json);


--
-- TOC entry 2269 (class 1259 OID 17442)
-- Name: mm_metadata_idxgin_media_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_idxgin_media_id ON mm_metadata_movie USING gin (mm_metadata_media_id);


--
-- TOC entry 2270 (class 1259 OID 17445)
-- Name: mm_metadata_idxgin_media_id_imdb; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_idxgin_media_id_imdb ON mm_metadata_movie USING gin (((mm_metadata_media_id -> 'imdb'::text)));


--
-- TOC entry 2271 (class 1259 OID 17443)
-- Name: mm_metadata_idxgin_media_id_thetvdb; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_idxgin_media_id_thetvdb ON mm_metadata_movie USING gin (((mm_metadata_media_id -> 'thetvdb'::text)));


--
-- TOC entry 2272 (class 1259 OID 17444)
-- Name: mm_metadata_idxgin_media_id_tmdb; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_idxgin_media_id_tmdb ON mm_metadata_movie USING gin (((mm_metadata_media_id -> 'tmdb'::text)));


--
-- TOC entry 2280 (class 1259 OID 17459)
-- Name: mm_metadata_idxgin_music_video_json; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_idxgin_music_video_json ON mm_metadata_music_video USING gin (mm_metadata_music_video_json);


--
-- TOC entry 2281 (class 1259 OID 17460)
-- Name: mm_metadata_idxgin_music_video_media_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_idxgin_music_video_media_id ON mm_metadata_music_video USING gin (mm_metadata_music_video_media_id);


--
-- TOC entry 2282 (class 1259 OID 17461)
-- Name: mm_metadata_idxgin_music_video_media_id_imvdb; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_idxgin_music_video_media_id_imvdb ON mm_metadata_music_video USING gin (((mm_metadata_music_video_media_id -> 'imvdb'::text)));


--
-- TOC entry 2273 (class 1259 OID 17446)
-- Name: mm_metadata_idxgin_user_json; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_idxgin_user_json ON mm_metadata_movie USING gin (mm_metadata_user_json);


--
-- TOC entry 2324 (class 1259 OID 17573)
-- Name: mm_metadata_logo_idxgin_json; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_logo_idxgin_json ON mm_metadata_logo USING gin (mm_metadata_logo_media_guid);


--
-- TOC entry 2245 (class 1259 OID 17404)
-- Name: mm_metadata_music_idx_album; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_music_idx_album ON mm_metadata_music USING btree (mm_metadata_music_album_guid);


--
-- TOC entry 2246 (class 1259 OID 17400)
-- Name: mm_metadata_music_idx_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_music_idx_name ON mm_metadata_music USING btree (mm_metadata_music_name);


--
-- TOC entry 2247 (class 1259 OID 17401)
-- Name: mm_metadata_music_idx_name_lower; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_music_idx_name_lower ON mm_metadata_music USING btree (lower(mm_metadata_music_name));


--
-- TOC entry 2248 (class 1259 OID 17402)
-- Name: mm_metadata_music_idxgin_json; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_music_idxgin_json ON mm_metadata_music USING gin (mm_metadata_music_json);


--
-- TOC entry 2249 (class 1259 OID 17403)
-- Name: mm_metadata_music_idxgin_media_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_music_idxgin_media_id ON mm_metadata_music USING gin (mm_metadata_media_music_id);


--
-- TOC entry 2232 (class 1259 OID 17375)
-- Name: mm_metadata_musician_idx_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_musician_idx_name ON mm_metadata_musician USING btree (mm_metadata_musician_name);


--
-- TOC entry 2233 (class 1259 OID 17376)
-- Name: mm_metadata_musician_idx_name_lower; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_musician_idx_name_lower ON mm_metadata_musician USING btree (lower(mm_metadata_musician_name));


--
-- TOC entry 2234 (class 1259 OID 17377)
-- Name: mm_metadata_musician_idxgin_id_json; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_musician_idxgin_id_json ON mm_metadata_musician USING gin (mm_metadata_musician_id);


--
-- TOC entry 2235 (class 1259 OID 17378)
-- Name: mm_metadata_musician_idxgin_json; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_musician_idxgin_json ON mm_metadata_musician USING gin (mm_metadata_musician_json);


--
-- TOC entry 2347 (class 1259 OID 17640)
-- Name: mm_metadata_person_idx_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_person_idx_name ON mm_metadata_person USING btree (mmp_person_name);


--
-- TOC entry 2348 (class 1259 OID 17641)
-- Name: mm_metadata_person_idxgin_id_json; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_person_idxgin_id_json ON mm_metadata_person USING gin (mmp_person_media_id);


--
-- TOC entry 2349 (class 1259 OID 17642)
-- Name: mm_metadata_person_idxgin_meta_json; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_person_idxgin_meta_json ON mm_metadata_person USING gin (mmp_person_meta_json);


--
-- TOC entry 2302 (class 1259 OID 17515)
-- Name: mm_metadata_review_idx_metadata_uuid; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_review_idx_metadata_uuid ON mm_review USING btree (mm_review_metadata_guid);


--
-- TOC entry 2303 (class 1259 OID 17514)
-- Name: mm_metadata_review_idxgin_media_json; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_review_idxgin_media_json ON mm_review USING gin (mm_review_metadata_id);


--
-- TOC entry 2220 (class 1259 OID 17357)
-- Name: mm_metadata_sports_idx_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_sports_idx_name ON mm_metadata_sports USING btree (mm_metadata_sports_name);


--
-- TOC entry 2221 (class 1259 OID 17358)
-- Name: mm_metadata_sports_idx_name_lower; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_sports_idx_name_lower ON mm_metadata_sports USING btree (lower(mm_metadata_sports_name));


--
-- TOC entry 2222 (class 1259 OID 17359)
-- Name: mm_metadata_sports_idxgin_json; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_sports_idxgin_json ON mm_metadata_sports USING gin (mm_metadata_sports_json);


--
-- TOC entry 2223 (class 1259 OID 17360)
-- Name: mm_metadata_sports_idxgin_media_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_sports_idxgin_media_id ON mm_metadata_sports USING gin (mm_metadata_media_sports_id);


--
-- TOC entry 2224 (class 1259 OID 17361)
-- Name: mm_metadata_sports_idxgin_media_id_imdb; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_sports_idxgin_media_id_imdb ON mm_metadata_sports USING gin (((mm_metadata_media_sports_id -> 'imdb'::text)));


--
-- TOC entry 2225 (class 1259 OID 17366)
-- Name: mm_metadata_sports_idxgin_media_id_thesportsdb; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_sports_idxgin_media_id_thesportsdb ON mm_metadata_sports USING gin (((mm_metadata_media_sports_id -> 'thesportsdb'::text)));


--
-- TOC entry 2226 (class 1259 OID 17362)
-- Name: mm_metadata_sports_idxgin_media_id_thetvdb; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_sports_idxgin_media_id_thetvdb ON mm_metadata_sports USING gin (((mm_metadata_media_sports_id -> 'thetvdb'::text)));


--
-- TOC entry 2227 (class 1259 OID 17364)
-- Name: mm_metadata_sports_idxgin_media_id_thetvdbseries; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_sports_idxgin_media_id_thetvdbseries ON mm_metadata_sports USING gin (((mm_metadata_media_sports_id -> 'thetvdbSeries'::text)));


--
-- TOC entry 2228 (class 1259 OID 17363)
-- Name: mm_metadata_sports_idxgin_media_id_tmdb; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_sports_idxgin_media_id_tmdb ON mm_metadata_sports USING gin (((mm_metadata_media_sports_id -> 'tmdb'::text)));


--
-- TOC entry 2229 (class 1259 OID 17365)
-- Name: mm_metadata_sports_idxgin_media_id_tvmaze; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_sports_idxgin_media_id_tvmaze ON mm_metadata_sports USING gin (((mm_metadata_media_sports_id -> 'tvmaze'::text)));


--
-- TOC entry 2207 (class 1259 OID 17338)
-- Name: mm_metadata_tvshow_idx_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_tvshow_idx_name ON mm_metadata_tvshow USING btree (mm_metadata_tvshow_name);


--
-- TOC entry 2208 (class 1259 OID 17339)
-- Name: mm_metadata_tvshow_idx_name_lower; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_tvshow_idx_name_lower ON mm_metadata_tvshow USING btree (lower(mm_metadata_tvshow_name));


--
-- TOC entry 2209 (class 1259 OID 17341)
-- Name: mm_metadata_tvshow_idxgin_json; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_tvshow_idxgin_json ON mm_metadata_tvshow USING gin (mm_metadata_tvshow_json);


--
-- TOC entry 2210 (class 1259 OID 17342)
-- Name: mm_metadata_tvshow_idxgin_localimage_json; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_tvshow_idxgin_localimage_json ON mm_metadata_tvshow USING gin (mm_metadata_tvshow_json);


--
-- TOC entry 2211 (class 1259 OID 17340)
-- Name: mm_metadata_tvshow_idxgin_media_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_tvshow_idxgin_media_id ON mm_metadata_tvshow USING gin (mm_metadata_media_tvshow_id);


--
-- TOC entry 2212 (class 1259 OID 17343)
-- Name: mm_metadata_tvshow_idxgin_media_id_imdb; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_tvshow_idxgin_media_id_imdb ON mm_metadata_tvshow USING gin (((mm_metadata_media_tvshow_id -> 'imdb'::text)));


--
-- TOC entry 2213 (class 1259 OID 17344)
-- Name: mm_metadata_tvshow_idxgin_media_id_thetvdb; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_tvshow_idxgin_media_id_thetvdb ON mm_metadata_tvshow USING gin (((mm_metadata_media_tvshow_id -> 'thetvdb'::text)));


--
-- TOC entry 2214 (class 1259 OID 17346)
-- Name: mm_metadata_tvshow_idxgin_media_id_thetvdbseries; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_tvshow_idxgin_media_id_thetvdbseries ON mm_metadata_tvshow USING gin (((mm_metadata_media_tvshow_id -> 'thetvdbSeries'::text)));


--
-- TOC entry 2215 (class 1259 OID 17345)
-- Name: mm_metadata_tvshow_idxgin_media_id_tmdb; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_tvshow_idxgin_media_id_tmdb ON mm_metadata_tvshow USING gin (((mm_metadata_media_tvshow_id -> 'tmdb'::text)));


--
-- TOC entry 2216 (class 1259 OID 17347)
-- Name: mm_metadata_tvshow_idxgin_media_id_tvmaze; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_tvshow_idxgin_media_id_tvmaze ON mm_metadata_tvshow USING gin (((mm_metadata_media_tvshow_id -> 'tvmaze'::text)));


--
-- TOC entry 2217 (class 1259 OID 17348)
-- Name: mm_metadata_tvshow_idxgin_user_json; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_metadata_tvshow_idxgin_user_json ON mm_metadata_tvshow USING gin (mm_metadata_tvshow_user_json);


--
-- TOC entry 2295 (class 1259 OID 17493)
-- Name: mm_notification_idx_dismissable; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_notification_idx_dismissable ON mm_notification USING btree (mm_notification_dismissable);


--
-- TOC entry 2296 (class 1259 OID 17492)
-- Name: mm_notification_idx_time; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_notification_idx_time ON mm_notification USING btree (mm_notification_time);


--
-- TOC entry 2317 (class 1259 OID 17551)
-- Name: mm_sync_idxgin_json; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_sync_idxgin_json ON mm_sync USING gin (mm_sync_options_json);


--
-- TOC entry 2374 (class 1259 OID 17707)
-- Name: mm_tv_schedule_idx_date; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_tv_schedule_idx_date ON mm_tv_schedule USING btree (mm_tv_schedule_date);


--
-- TOC entry 2376 (class 1259 OID 17717)
-- Name: mm_tv_schedule_idx_program; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_tv_schedule_idx_program ON mm_tv_schedule_program USING btree (mm_tv_schedule_program_id);


--
-- TOC entry 2375 (class 1259 OID 17708)
-- Name: mm_tv_schedule_idx_station; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_tv_schedule_idx_station ON mm_tv_schedule USING btree (mm_tv_schedule_station_id);


--
-- TOC entry 2370 (class 1259 OID 17698)
-- Name: mm_tv_stations_idx_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_tv_stations_idx_name ON mm_tv_stations USING btree (mm_tv_station_name);


--
-- TOC entry 2371 (class 1259 OID 17697)
-- Name: mm_tv_stations_idx_station; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_tv_stations_idx_station ON mm_tv_stations USING btree (mm_tv_station_id);


--
-- TOC entry 2293 (class 1259 OID 17483)
-- Name: mm_user_activity_idx_date; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_user_activity_idx_date ON mm_user_activity USING btree (mm_activity_datecreated);


--
-- TOC entry 2294 (class 1259 OID 17482)
-- Name: mm_user_activity_idx_user_guid; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_user_activity_idx_user_guid ON mm_user_activity USING btree (mm_activity_userid);


--
-- TOC entry 2333 (class 1259 OID 17594)
-- Name: mm_user_group_idx_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_user_group_idx_name ON mm_user_group USING btree (mm_user_group_name);


--
-- TOC entry 2299 (class 1259 OID 17505)
-- Name: mm_user_idx_username; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_user_idx_username ON mm_user USING btree (username);


--
-- TOC entry 2336 (class 1259 OID 17603)
-- Name: mm_user_profile_idx_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mm_user_profile_idx_name ON mm_user_profile USING btree (mm_user_profile_name);


--
-- TOC entry 2198 (class 1259 OID 17319)
-- Name: mmr_media_idx_link_uuid; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mmr_media_idx_link_uuid ON mm_media_remote USING btree (mmr_media_link_id);


--
-- TOC entry 2199 (class 1259 OID 17318)
-- Name: mmr_media_idx_metadata_uuid; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mmr_media_idx_metadata_uuid ON mm_media_remote USING btree (mmr_media_metadata_guid);


--
-- TOC entry 2200 (class 1259 OID 17317)
-- Name: mmr_media_idxgin_ffprobe; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mmr_media_idxgin_ffprobe ON mm_media_remote USING gin (mmr_media_ffprobe_json);


--
-- TOC entry 2356 (class 1259 OID 17653)
-- Name: mqd_que_type_idx_name; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX mqd_que_type_idx_name ON mm_download_que USING btree (mqd_que_type);


--
-- TOC entry 2542 (class 0 OID 0)
-- Dependencies: 6
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


-- Completed on 2016-12-31 01:44:53 CST

--
-- PostgreSQL database dump complete
--

