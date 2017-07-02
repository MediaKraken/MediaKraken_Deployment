--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.6
-- Dumped by pg_dump version 9.5.6

-- Started on 2017-07-01 22:30:30 CDT

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
-- TOC entry 2546 (class 0 OID 0)
-- Dependencies: 1
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- TOC entry 209 (class 1259 OID 22800)
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
-- TOC entry 203 (class 1259 OID 22753)
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
-- TOC entry 219 (class 1259 OID 22896)
-- Name: mm_device; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE mm_device (
    mm_device_id uuid NOT NULL,
    mm_device_type text,
    mm_device_json jsonb
);


ALTER TABLE mm_device OWNER TO metamanpg;

--
-- TOC entry 223 (class 1259 OID 23013)
-- Name: mm_download_image_que; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE mm_download_image_que (
    mdq_image_id uuid NOT NULL,
    mdq_image_provider text,
    mdq_image_download_json jsonb
);


ALTER TABLE mm_download_image_que OWNER TO metamanpg;

--
-- TOC entry 216 (class 1259 OID 22869)
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
-- TOC entry 186 (class 1259 OID 22546)
-- Name: mm_link; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE mm_link (
    mm_link_guid uuid NOT NULL,
    mm_link_name text,
    mm_link_json jsonb
);


ALTER TABLE mm_link OWNER TO metamanpg;

--
-- TOC entry 206 (class 1259 OID 22778)
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
-- TOC entry 184 (class 1259 OID 22524)
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
-- TOC entry 192 (class 1259 OID 22631)
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
-- TOC entry 183 (class 1259 OID 22515)
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
-- TOC entry 185 (class 1259 OID 22535)
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
-- TOC entry 182 (class 1259 OID 22507)
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
-- TOC entry 190 (class 1259 OID 22605)
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
-- TOC entry 193 (class 1259 OID 22640)
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
-- TOC entry 196 (class 1259 OID 22688)
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
-- TOC entry 202 (class 1259 OID 22742)
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
-- TOC entry 213 (class 1259 OID 22838)
-- Name: mm_metadata_game_software_info; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE mm_metadata_game_software_info (
    gi_id uuid NOT NULL,
    gi_system_id uuid,
    gi_game_info_json jsonb
);


ALTER TABLE mm_metadata_game_software_info OWNER TO metamanpg;

--
-- TOC entry 214 (class 1259 OID 22849)
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
-- TOC entry 208 (class 1259 OID 22791)
-- Name: mm_metadata_logo; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE mm_metadata_logo (
    mm_metadata_logo_guid uuid NOT NULL,
    mm_metadata_logo_media_guid jsonb,
    mm_metadata_logo_image_path text
);


ALTER TABLE mm_metadata_logo OWNER TO metamanpg;

--
-- TOC entry 194 (class 1259 OID 22657)
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
-- TOC entry 191 (class 1259 OID 22618)
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
-- TOC entry 195 (class 1259 OID 22673)
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
-- TOC entry 189 (class 1259 OID 22593)
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
-- TOC entry 215 (class 1259 OID 22858)
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
-- TOC entry 188 (class 1259 OID 22575)
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
-- TOC entry 187 (class 1259 OID 22556)
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
-- TOC entry 218 (class 1259 OID 22888)
-- Name: mm_nas; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE mm_nas (
    mm_nas_id uuid NOT NULL,
    mm_nas_json jsonb
);


ALTER TABLE mm_nas OWNER TO metamanpg;

--
-- TOC entry 198 (class 1259 OID 22710)
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
-- TOC entry 212 (class 1259 OID 22830)
-- Name: mm_options_and_status; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE mm_options_and_status (
    mm_options_and_status_guid uuid NOT NULL,
    mm_options_json jsonb,
    mm_status_json jsonb
);


ALTER TABLE mm_options_and_status OWNER TO metamanpg;

--
-- TOC entry 204 (class 1259 OID 22761)
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
-- TOC entry 201 (class 1259 OID 22732)
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
-- TOC entry 205 (class 1259 OID 22769)
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
-- TOC entry 207 (class 1259 OID 22783)
-- Name: mm_trigger; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE mm_trigger (
    mm_trigger_guid uuid NOT NULL,
    mm_trigger_command bytea,
    mm_trigger_background boolean
);


ALTER TABLE mm_trigger OWNER TO metamanpg;

--
-- TOC entry 217 (class 1259 OID 22880)
-- Name: mm_tuner; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE mm_tuner (
    mm_tuner_id uuid NOT NULL,
    mm_tuner_json jsonb
);


ALTER TABLE mm_tuner OWNER TO metamanpg;

--
-- TOC entry 221 (class 1259 OID 22916)
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
-- TOC entry 222 (class 1259 OID 22926)
-- Name: mm_tv_schedule_program; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE mm_tv_schedule_program (
    mm_tv_schedule_program_guid uuid NOT NULL,
    mm_tv_schedule_program_id text,
    mm_tv_schedule_program_json jsonb
);


ALTER TABLE mm_tv_schedule_program OWNER TO metamanpg;

--
-- TOC entry 220 (class 1259 OID 22906)
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
-- TOC entry 200 (class 1259 OID 22722)
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
-- TOC entry 197 (class 1259 OID 22700)
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
-- TOC entry 210 (class 1259 OID 22812)
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
-- TOC entry 199 (class 1259 OID 22720)
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
-- TOC entry 2547 (class 0 OID 0)
-- Dependencies: 199
-- Name: mm_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: metamanpg
--

ALTER SEQUENCE mm_user_id_seq OWNED BY mm_user.id;


--
-- TOC entry 211 (class 1259 OID 22821)
-- Name: mm_user_profile; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE mm_user_profile (
    mm_user_profile_guid uuid NOT NULL,
    mm_user_profile_name text,
    mm_user_profile_json jsonb
);


ALTER TABLE mm_user_profile OWNER TO metamanpg;

--
-- TOC entry 181 (class 1259 OID 22501)
-- Name: mm_version; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE mm_version (
    mm_version_no integer
);


ALTER TABLE mm_version OWNER TO metamanpg;

--
-- TOC entry 2187 (class 2604 OID 22725)
-- Name: id; Type: DEFAULT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_user ALTER COLUMN id SET DEFAULT nextval('mm_user_id_seq'::regclass);


--
-- TOC entry 2524 (class 0 OID 22800)
-- Dependencies: 209
-- Data for Name: mm_channel; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_channel (mm_channel_guid, mm_channel_name, mm_channel_media_id, mm_channel_country_guid, mm_channel_logo_guid) FROM stdin;
\.


--
-- TOC entry 2518 (class 0 OID 22753)
-- Dependencies: 203
-- Data for Name: mm_cron; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_cron (mm_cron_guid, mm_cron_name, mm_cron_description, mm_cron_enabled, mm_cron_schedule, mm_cron_last_run, mm_cron_file_path) FROM stdin;
dc767e06-210b-43de-86ae-652d290aa3b2	Game Audit	Scan for new game media	f	Days 1	1970-01-01 00:00:01	./subprogram_game_audit.py
044dede1-4136-4cbc-9b13-6ca452f006a7	Create Chapter Image	Create chapter images for all media	f	Days 1	1970-01-01 00:00:01	./subprogram_create_chapter_images.py
3173d3c4-8a2d-49c2-9f92-805a0344b71e	Anime	Match anime via Scudlee data	f	Days 1	1970-01-01 00:00:01	./subprogram_match_anime_id_scudlee.py
d00db78f-a55a-4faf-8eb5-e866d574d216	Roku Thumb	Generate Roku thumbnail images	f	Days 1	1970-01-01 00:00:01	./subprogram_roku_thumbnail_generate.py
22aa27e4-9783-4625-b477-c2809691acac	Schedules Direct	Fetch TV schedules from Schedules Direct	f	Days 1	1970-01-01 00:00:01	./subprogram_schedules_direct_updates.py
1b7e4151-569d-4c16-a26c-65094360e4ab	Subtitle	Download missing subtitles for media	f	Days 1	1970-01-01 00:00:01	./subprogram_subtitle_downloader.py
741cb966-d201-4b44-845b-0adfbc4fb32b	TheTVDB Update	Grab updated TheTVDB metadata	f	Days 1	1970-01-01 00:00:01	./subprogram_thetvdb_updates.py
14fa324f-5937-491f-807b-2decbcdcb520	The Movie Database	Grab updated movie metadata	f	Days 1	1970-01-01 00:00:01	./subprogram_tmdb_updates.py
ed4126d7-2156-4f0f-9a0c-8bad4e695f90	TVmaze Update	Grab updated TVmaze metadata	f	Days 1	1970-01-01 00:00:01	./subprogram_tvmze_updates.py
3842da28-436c-439d-881c-737063af325f	Collections	Create and update collection(s)	f	Days 1	1970-01-01 00:00:01	./subprogram_update_create_collections.py
fdeb4df4-a909-4479-845e-f61087b004c5	Media Scan	Scan for new media	f	Days 1	1970-01-01 00:00:01	./subprogram_file_scan.py
610355b4-ff45-410a-ae91-c9e04793cd0d	iRadio Scan	Scan for iRadio stations	f	Days 1	1970-01-01 00:00:01	./subprogram_iradio_channels.py
630ddfb8-01e7-4e56-93be-bc8124f568b6	Backup	Backup Postgresql DB	f	Days 1	1970-01-01 00:00:01	./subprogram_postgresql_backup.py
7fa07ec9-c0f6-4d4c-9221-f11dc86808e1	DB Vacuum	Postgresql Vacuum Analyze all tables	f	Days 1	1970-01-01 00:00:01	./subprogram_postgresql_vacuum.py
775b2282-1d18-46f7-ab78-f8b45b5687ad	Sync	Sync/Transcode media	f	Days 1	1970-01-01 00:00:01	./subprogram_sync.py
\.


--
-- TOC entry 2534 (class 0 OID 22896)
-- Dependencies: 219
-- Data for Name: mm_device; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_device (mm_device_id, mm_device_type, mm_device_json) FROM stdin;
\.


--
-- TOC entry 2538 (class 0 OID 23013)
-- Dependencies: 223
-- Data for Name: mm_download_image_que; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_download_image_que (mdq_image_id, mdq_image_provider, mdq_image_download_json) FROM stdin;
\.


--
-- TOC entry 2531 (class 0 OID 22869)
-- Dependencies: 216
-- Data for Name: mm_download_que; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_download_que (mdq_id, mdq_provider, mdq_que_type, mdq_download_json) FROM stdin;
\.


--
-- TOC entry 2501 (class 0 OID 22546)
-- Dependencies: 186
-- Data for Name: mm_link; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_link (mm_link_guid, mm_link_name, mm_link_json) FROM stdin;
\.


--
-- TOC entry 2521 (class 0 OID 22778)
-- Dependencies: 206
-- Data for Name: mm_loan; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_loan (mm_loan_guid, mm_loan_media_id, mm_loan_user_id, mm_load_user_loan_id, mm_loan_time, mm_loan_return_time) FROM stdin;
\.


--
-- TOC entry 2499 (class 0 OID 22524)
-- Dependencies: 184
-- Data for Name: mm_media; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_media (mm_media_guid, mm_media_class_guid, mm_media_metadata_guid, mm_media_path, mm_media_ffprobe_json, mm_media_json) FROM stdin;
\.


--
-- TOC entry 2507 (class 0 OID 22631)
-- Dependencies: 192
-- Data for Name: mm_media_class; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_media_class (mm_media_class_guid, mm_media_class_type, mm_media_class_parent_type, mm_media_class_display) FROM stdin;
776949d2-3d24-4d1f-a32d-c55ada1d5af2	Adult	Video	t
2e077854-3c01-4fbb-aebd-0672a96a9fde	Anime	Video	t
5c77d564-f1ca-4b32-a171-6011e347bf13	Book	Publication	t
f60f312a-1c86-4a62-9cd8-b4e55d9fd067	Boxset	\N	f
42b493e8-e087-42ee-8ec2-44e5a80c96ad	Game CHD	\N	f
8973e482-d69b-423a-ac16-a0ba203c5ea6	Game ISO	\N	f
a9928cb6-e9e6-45eb-990c-a7a64566077f	Game ROM	\N	f
abd6f903-2b1d-4ca4-9b64-598e29cd1a09	Home Movie	Video	t
e924ace2-c4c8-4563-88a5-b49c7023f7a7	Magazine	Publication	t
815ee3b8-d56f-441b-a3ca-6bcdb8a345d3	Movie	Video	t
e9365ded-f322-4062-87b2-434fc3f3eaa5	Movie Extras	Video	f
c59c86ec-e300-4c9b-9a3b-0cd4bb5b6c61	Movie Collection	\N	f
4a33119a-2521-4664-a966-10347536e311	Movie Theme	Audio	f
d7323374-9b73-4505-88c2-e9ed015e2bd8	Movie Trailer	Video	f
2afe1c27-08bd-4bf4-b6ec-78b5a0114773	Music	Audio	t
23c52d48-f7be-4901-937f-e6f4058645d7	Music Album	\N	f
c4185e11-b788-4a96-9b58-cef548d6e888	Music Collection	\N	f
7f8e83b1-c1de-4067-81b8-42a6d796899d	Music Lyric	\N	f
c3b3514f-af4f-4ef9-b523-069a478acad6	Music Video	Video	t
bfd2d309-4e61-4153-b38e-600ae7516036	Person	\N	f
1d029e28-4001-4679-94ae-7b6a559f5709	Picture	Image	t
1f3eb606-81fe-408c-8ef2-c5db9f839740	Soundtrack	Audio	f
beea1a0e-fe79-4806-a572-d6a94d79b26b	Sports	Video	t
ebb67431-04b5-4a8e-8f65-7ad95381c125	Subtitle	\N	f
1e6760cc-15b4-40cd-b666-4f0ab9e4f7b7	TV Episode	Video	f
901e800f-5202-4b7c-b3b3-e942c3b0e422	TV Extras	Video	f
646af372-d1f1-4165-9589-9cb220e663fc	TV Season	\N	f
7b387783-d106-447b-b20f-e8edd7f826eb	TV Show	Video	t
a18a5377-d43c-4956-bbed-6af03ff2eaf8	TV Theme	Audio	f
1dbfc709-b96a-4962-9960-1c94e58688fb	TV Trailer	Video	f
0968a4d9-ac66-41ab-b1f4-046d260b4a18	Video Game	Game	t
60c0d46a-48fe-4cf0-a2c4-a0d0f4b042f4	Video Game Intro	Video	t
7b0137ec-d8f2-49c5-a389-c88cf92ca0c5	Video Game Speedrun	Video	t
9a0c956a-4e80-472e-bbf9-64ffce339675	Video Game Superplay	Video	t
\.


--
-- TOC entry 2498 (class 0 OID 22515)
-- Dependencies: 183
-- Data for Name: mm_media_dir; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_media_dir (mm_media_dir_guid, mm_media_dir_path, mm_media_dir_class_type, mm_media_dir_last_scanned, mm_media_dir_share_guid, mm_media_dir_status) FROM stdin;
\.


--
-- TOC entry 2500 (class 0 OID 22535)
-- Dependencies: 185
-- Data for Name: mm_media_remote; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_media_remote (mmr_media_guid, mmr_media_link_id, mmr_media_uuid, mmr_media_class_guid, mmr_media_metadata_guid, mmr_media_ffprobe_json, mmr_media_json) FROM stdin;
\.


--
-- TOC entry 2497 (class 0 OID 22507)
-- Dependencies: 182
-- Data for Name: mm_media_share; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_media_share (mm_media_share_guid, mm_media_share_type, mm_media_share_user, mm_media_share_password, mm_media_share_server, mm_media_share_path) FROM stdin;
\.


--
-- TOC entry 2505 (class 0 OID 22605)
-- Dependencies: 190
-- Data for Name: mm_metadata_album; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_metadata_album (mm_metadata_album_guid, mm_metadata_album_name, mm_metadata_album_id, mm_metadata_album_json, mm_metadata_album_musician_guid) FROM stdin;
\.


--
-- TOC entry 2508 (class 0 OID 22640)
-- Dependencies: 193
-- Data for Name: mm_metadata_anime; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_metadata_anime (mm_metadata_anime_guid, mm_metadata_anime_media_id, mm_media_anime_name, mm_metadata_anime_json, mm_metadata_anime_mapping, mm_metadata_anime_mapping_before, mm_metadata_anime_localimage_json, mm_metadata_anime_user_json) FROM stdin;
\.


--
-- TOC entry 2511 (class 0 OID 22688)
-- Dependencies: 196
-- Data for Name: mm_metadata_book; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_metadata_book (mm_metadata_book_guid, mm_metadata_book_isbn, mm_metadata_book_isbn13, mm_metadata_book_name, mm_metadata_book_json, mm_metadata_book_image_json) FROM stdin;
\.


--
-- TOC entry 2517 (class 0 OID 22742)
-- Dependencies: 202
-- Data for Name: mm_metadata_collection; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_metadata_collection (mm_metadata_collection_guid, mm_metadata_collection_name, mm_metadata_collection_media_ids, mm_metadata_collection_json, mm_metadata_collection_imagelocal_json) FROM stdin;
\.


--
-- TOC entry 2528 (class 0 OID 22838)
-- Dependencies: 213
-- Data for Name: mm_metadata_game_software_info; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_metadata_game_software_info (gi_id, gi_system_id, gi_game_info_json) FROM stdin;
\.


--
-- TOC entry 2529 (class 0 OID 22849)
-- Dependencies: 214
-- Data for Name: mm_metadata_game_systems_info; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_metadata_game_systems_info (gs_id, gs_game_system_id, gs_game_system_name, gs_game_system_alias, gs_game_system_json) FROM stdin;
\.


--
-- TOC entry 2523 (class 0 OID 22791)
-- Dependencies: 208
-- Data for Name: mm_metadata_logo; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_metadata_logo (mm_metadata_logo_guid, mm_metadata_logo_media_guid, mm_metadata_logo_image_path) FROM stdin;
\.


--
-- TOC entry 2509 (class 0 OID 22657)
-- Dependencies: 194
-- Data for Name: mm_metadata_movie; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_metadata_movie (mm_metadata_guid, mm_metadata_media_id, mm_media_name, mm_metadata_json, mm_metadata_localimage_json, mm_metadata_user_json) FROM stdin;
\.


--
-- TOC entry 2506 (class 0 OID 22618)
-- Dependencies: 191
-- Data for Name: mm_metadata_music; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_metadata_music (mm_metadata_music_guid, mm_metadata_media_music_id, mm_metadata_music_name, mm_metadata_music_json, mm_metadata_music_album_guid) FROM stdin;
\.


--
-- TOC entry 2510 (class 0 OID 22673)
-- Dependencies: 195
-- Data for Name: mm_metadata_music_video; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_metadata_music_video (mm_metadata_music_video_guid, mm_metadata_music_video_media_id, mm_media_music_video_band, mm_media_music_video_song, mm_metadata_music_video_json, mm_metadata_music_video_localimage_json) FROM stdin;
\.


--
-- TOC entry 2504 (class 0 OID 22593)
-- Dependencies: 189
-- Data for Name: mm_metadata_musician; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_metadata_musician (mm_metadata_musician_guid, mm_metadata_musician_name, mm_metadata_musician_id, mm_metadata_musician_json) FROM stdin;
\.


--
-- TOC entry 2530 (class 0 OID 22858)
-- Dependencies: 215
-- Data for Name: mm_metadata_person; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_metadata_person (mmp_id, mmp_person_media_id, mmp_person_meta_json, mmp_person_image, mmp_person_name) FROM stdin;
\.


--
-- TOC entry 2503 (class 0 OID 22575)
-- Dependencies: 188
-- Data for Name: mm_metadata_sports; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_metadata_sports (mm_metadata_sports_guid, mm_metadata_media_sports_id, mm_metadata_sports_name, mm_metadata_sports_json, mm_metadata_sports_image_json) FROM stdin;
\.


--
-- TOC entry 2502 (class 0 OID 22556)
-- Dependencies: 187
-- Data for Name: mm_metadata_tvshow; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_metadata_tvshow (mm_metadata_tvshow_guid, mm_metadata_media_tvshow_id, mm_metadata_tvshow_name, mm_metadata_tvshow_json, mm_metadata_tvshow_localimage_json, mm_metadata_tvshow_user_json) FROM stdin;
\.


--
-- TOC entry 2533 (class 0 OID 22888)
-- Dependencies: 218
-- Data for Name: mm_nas; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_nas (mm_nas_id, mm_nas_json) FROM stdin;
\.


--
-- TOC entry 2513 (class 0 OID 22710)
-- Dependencies: 198
-- Data for Name: mm_notification; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_notification (mm_notification_guid, mm_notification_text, mm_notification_time, mm_notification_dismissable) FROM stdin;
\.


--
-- TOC entry 2527 (class 0 OID 22830)
-- Dependencies: 212
-- Data for Name: mm_options_and_status; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_options_and_status (mm_options_and_status_guid, mm_options_json, mm_status_json) FROM stdin;
e26857c1-8742-4947-93b8-2929ba7848b1	{"SD": {"User": null, "Password": null}, "API": {"anidb": null, "imvdb": null, "google": null, "isbndb": "25C8IT4I", "tvmaze": null, "thetvdb": "147CB43DCA8B61B7", "thelogodb": null, "themoviedb": "f72118d1e84b8a1438935972a9c37cac", "globalcache": null, "mediabrainz": null, "thesportsdb": "4352761817344", "opensubtitles": null, "rottentomatoes": "f4tnu5dn9r7f28gjth3ftqaj"}, "AWSS3": {"Bucket": "mediakraken", "AccessKey": null, "BackupBucket": "mkbackup", "SecretAccessKey": null}, "Trakt": {"ApiKey": null, "ClientID": null, "SecretKey": null}, "Backup": {"Interval": 0, "BackupType": "awss3"}, "Docker": {"Nodes": 0, "SwarmID": "Manager", "Instances": 0}, "Dropbox": {"APIKey": null, "APISecret": null}, "OneDrive": {"ClientID": null, "SecretKey": null}, "GoogleDrive": {"SecretFile": null}, "Maintenance": null, "MediaBrainz": {"Host": null, "Port": 5000, "User": null, "Password": null, "BrainzDBHost": null, "BrainzDBName": null, "BrainzDBPass": null, "BrainzDBPort": 5432, "BrainzDBUser": null}, "MaxResumePct": 5, "Transmission": {"Host": null, "Port": 9091}, "MediaKrakenServer": {"FFMPEG": 8900, "APIPort": 8097, "ImageWeb": 8099, "ListenPort": 8098, "BackupLocal": "/mediakraken/backups/"}}	{"thetvdb_Updated_Epoc": 0}
\.


--
-- TOC entry 2519 (class 0 OID 22761)
-- Dependencies: 204
-- Data for Name: mm_radio; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_radio (mm_radio_guid, mm_radio_name, mm_radio_adress, mm_radio_active) FROM stdin;
\.


--
-- TOC entry 2516 (class 0 OID 22732)
-- Dependencies: 201
-- Data for Name: mm_review; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_review (mm_review_guid, mm_review_metadata_id, mm_review_metadata_guid, mm_review_json) FROM stdin;
\.


--
-- TOC entry 2520 (class 0 OID 22769)
-- Dependencies: 205
-- Data for Name: mm_sync; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_sync (mm_sync_guid, mm_sync_path, mm_sync_path_to, mm_sync_options_json) FROM stdin;
\.


--
-- TOC entry 2522 (class 0 OID 22783)
-- Dependencies: 207
-- Data for Name: mm_trigger; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_trigger (mm_trigger_guid, mm_trigger_command, mm_trigger_background) FROM stdin;
\.


--
-- TOC entry 2532 (class 0 OID 22880)
-- Dependencies: 217
-- Data for Name: mm_tuner; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_tuner (mm_tuner_id, mm_tuner_json) FROM stdin;
\.


--
-- TOC entry 2536 (class 0 OID 22916)
-- Dependencies: 221
-- Data for Name: mm_tv_schedule; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_tv_schedule (mm_tv_schedule_id, mm_tv_schedule_station_id, mm_tv_schedule_date, mm_tv_schedule_json) FROM stdin;
\.


--
-- TOC entry 2537 (class 0 OID 22926)
-- Dependencies: 222
-- Data for Name: mm_tv_schedule_program; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_tv_schedule_program (mm_tv_schedule_program_guid, mm_tv_schedule_program_id, mm_tv_schedule_program_json) FROM stdin;
\.


--
-- TOC entry 2535 (class 0 OID 22906)
-- Dependencies: 220
-- Data for Name: mm_tv_stations; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_tv_stations (mm_tv_stations_id, mm_tv_station_name, mm_tv_station_id, mm_tv_station_channel, mm_tv_station_json, mm_tv_station_image) FROM stdin;
\.


--
-- TOC entry 2515 (class 0 OID 22722)
-- Dependencies: 200
-- Data for Name: mm_user; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_user (id, username, email, password, created_at, active, is_admin, user_json, lang) FROM stdin;
\.


--
-- TOC entry 2512 (class 0 OID 22700)
-- Dependencies: 197
-- Data for Name: mm_user_activity; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_user_activity (mm_activity_guid, mm_activity_name, mm_activity_overview, mm_activity_short_overview, mm_activity_type, mm_activity_itemid, mm_activity_userid, mm_activity_datecreated, mm_activity_log_severity) FROM stdin;
\.


--
-- TOC entry 2525 (class 0 OID 22812)
-- Dependencies: 210
-- Data for Name: mm_user_group; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_user_group (mm_user_group_guid, mm_user_group_name, mm_user_group_description, mm_user_group_rights_json) FROM stdin;
a5d83c3e-edcc-4e9e-869f-e5eafd39dada	Administrator	Server administrator	{"Admin": true, "PreviewOnly": false}
d0eaba7f-ac88-4db5-87dc-20e2a41ce15c	User	General user	{"Admin": false, "PreviewOnly": false}
1165406d-ac12-4703-9e9b-f1b7df17cfa5	Guest	Guest (Preview only)	{"Admin": false, "PreviewOnly": true}
\.


--
-- TOC entry 2548 (class 0 OID 0)
-- Dependencies: 199
-- Name: mm_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: metamanpg
--

SELECT pg_catalog.setval('mm_user_id_seq', 1, true);


--
-- TOC entry 2526 (class 0 OID 22821)
-- Dependencies: 211
-- Data for Name: mm_user_profile; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_user_profile (mm_user_profile_guid, mm_user_profile_name, mm_user_profile_json) FROM stdin;
5ae47994-0d67-4bf9-989d-8d2f4815a4f1	Adult	{"3D": true, "TV": true, "Home": true, "Lang": "en", "Sync": true, "Adult": true, "Books": true, "Games": true, "MaxBR": 100, "Movie": true, "Music": true, "IRadio": true, "Images": true, "LiveTV": true, "Sports": true, "Internet": true, "MaxRating": 5}
8b988721-ba74-411a-a3d5-c6b98b78b301	Teen	{"3D": true, "TV": true, "Home": true, "Lang": "en", "Sync": false, "Adult": false, "Books": true, "Games": true, "MaxBR": 50, "Movie": true, "Music": true, "IRadio": true, "Images": true, "LiveTV": true, "Sports": true, "Internet": true, "MaxRating": 3}
34a01e89-223a-4cb5-a855-8b4dee225d8f	Child	{"3D": false, "TV": true, "Home": true, "Lang": "en", "Sync": false, "Adult": false, "Books": true, "Games": true, "MaxBR": 20, "Movie": true, "Music": true, "IRadio": false, "Images": true, "LiveTV": false, "Sports": true, "Internet": false, "MaxRating": 0}
\.


--
-- TOC entry 2496 (class 0 OID 22501)
-- Dependencies: 181
-- Data for Name: mm_version; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_version (mm_version_no) FROM stdin;
4
\.


--
-- TOC entry 2343 (class 2606 OID 22845)
-- Name: gi_id_mpk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_metadata_game_software_info
    ADD CONSTRAINT gi_id_mpk PRIMARY KEY (gi_id);


--
-- TOC entry 2348 (class 2606 OID 22856)
-- Name: gs_id_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_metadata_game_systems_info
    ADD CONSTRAINT gs_id_pk PRIMARY KEY (gs_id);


--
-- TOC entry 2356 (class 2606 OID 22876)
-- Name: mdq_id_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_download_que
    ADD CONSTRAINT mdq_id_pk PRIMARY KEY (mdq_id);


--
-- TOC entry 2380 (class 2606 OID 23020)
-- Name: mdq_image_id_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_download_image_que
    ADD CONSTRAINT mdq_image_id_pk PRIMARY KEY (mdq_image_id);


--
-- TOC entry 2295 (class 2606 OID 22707)
-- Name: mm_activity_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_user_activity
    ADD CONSTRAINT mm_activity_pk PRIMARY KEY (mm_activity_guid);


--
-- TOC entry 2329 (class 2606 OID 22807)
-- Name: mm_channel_guid_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_channel
    ADD CONSTRAINT mm_channel_guid_pk PRIMARY KEY (mm_channel_guid);


--
-- TOC entry 2315 (class 2606 OID 22760)
-- Name: mm_cron_guid_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_cron
    ADD CONSTRAINT mm_cron_guid_pk PRIMARY KEY (mm_cron_guid);


--
-- TOC entry 2365 (class 2606 OID 22903)
-- Name: mm_device_id_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_device
    ADD CONSTRAINT mm_device_id_pk PRIMARY KEY (mm_device_id);


--
-- TOC entry 2204 (class 2606 OID 22553)
-- Name: mm_link_guid_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_link
    ADD CONSTRAINT mm_link_guid_pk PRIMARY KEY (mm_link_guid);


--
-- TOC entry 2322 (class 2606 OID 22782)
-- Name: mm_loan_guid_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_loan
    ADD CONSTRAINT mm_loan_guid_pk PRIMARY KEY (mm_loan_guid);


--
-- TOC entry 2257 (class 2606 OID 22638)
-- Name: mm_media_class_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_media_class
    ADD CONSTRAINT mm_media_class_pk PRIMARY KEY (mm_media_class_guid);


--
-- TOC entry 2192 (class 2606 OID 22522)
-- Name: mm_media_dir_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_media_dir
    ADD CONSTRAINT mm_media_dir_pk PRIMARY KEY (mm_media_dir_guid);


--
-- TOC entry 2197 (class 2606 OID 22531)
-- Name: mm_media_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_media
    ADD CONSTRAINT mm_media_pk PRIMARY KEY (mm_media_guid);


--
-- TOC entry 2189 (class 2606 OID 22514)
-- Name: mm_media_share_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_media_share
    ADD CONSTRAINT mm_media_share_pk PRIMARY KEY (mm_media_share_guid);


--
-- TOC entry 2247 (class 2606 OID 22612)
-- Name: mm_metadata_album_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_metadata_album
    ADD CONSTRAINT mm_metadata_album_pk PRIMARY KEY (mm_metadata_album_guid);


--
-- TOC entry 2268 (class 2606 OID 22647)
-- Name: mm_metadata_anime_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_metadata_anime
    ADD CONSTRAINT mm_metadata_anime_pk PRIMARY KEY (mm_metadata_anime_guid);


--
-- TOC entry 2289 (class 2606 OID 22695)
-- Name: mm_metadata_book_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_metadata_book
    ADD CONSTRAINT mm_metadata_book_pk PRIMARY KEY (mm_metadata_book_guid);


--
-- TOC entry 2310 (class 2606 OID 22749)
-- Name: mm_metadata_collection_guid_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_metadata_collection
    ADD CONSTRAINT mm_metadata_collection_guid_pk PRIMARY KEY (mm_metadata_collection_guid);


--
-- TOC entry 2326 (class 2606 OID 22798)
-- Name: mm_metadata_logo_guid_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_metadata_logo
    ADD CONSTRAINT mm_metadata_logo_guid_pk PRIMARY KEY (mm_metadata_logo_guid);


--
-- TOC entry 2254 (class 2606 OID 22625)
-- Name: mm_metadata_music_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_metadata_music
    ADD CONSTRAINT mm_metadata_music_pk PRIMARY KEY (mm_metadata_music_guid);


--
-- TOC entry 2287 (class 2606 OID 22680)
-- Name: mm_metadata_music_video_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_metadata_music_video
    ADD CONSTRAINT mm_metadata_music_video_pk PRIMARY KEY (mm_metadata_music_video_guid);


--
-- TOC entry 2240 (class 2606 OID 22600)
-- Name: mm_metadata_musician_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_metadata_musician
    ADD CONSTRAINT mm_metadata_musician_pk PRIMARY KEY (mm_metadata_musician_guid);


--
-- TOC entry 2278 (class 2606 OID 22664)
-- Name: mm_metadata_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_metadata_movie
    ADD CONSTRAINT mm_metadata_pk PRIMARY KEY (mm_metadata_guid);


--
-- TOC entry 2234 (class 2606 OID 22582)
-- Name: mm_metadata_sports_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_metadata_sports
    ADD CONSTRAINT mm_metadata_sports_pk PRIMARY KEY (mm_metadata_sports_guid);


--
-- TOC entry 2222 (class 2606 OID 22563)
-- Name: mm_metadata_tvshow_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_metadata_tvshow
    ADD CONSTRAINT mm_metadata_tvshow_pk PRIMARY KEY (mm_metadata_tvshow_guid);


--
-- TOC entry 2363 (class 2606 OID 22895)
-- Name: mm_nas_id_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_nas
    ADD CONSTRAINT mm_nas_id_pk PRIMARY KEY (mm_nas_id);


--
-- TOC entry 2301 (class 2606 OID 22717)
-- Name: mm_notification_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_notification
    ADD CONSTRAINT mm_notification_pk PRIMARY KEY (mm_notification_guid);


--
-- TOC entry 2341 (class 2606 OID 22837)
-- Name: mm_options_and_status_guid_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_options_and_status
    ADD CONSTRAINT mm_options_and_status_guid_pk PRIMARY KEY (mm_options_and_status_guid);


--
-- TOC entry 2317 (class 2606 OID 22768)
-- Name: mm_radio_guid_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_radio
    ADD CONSTRAINT mm_radio_guid_pk PRIMARY KEY (mm_radio_guid);


--
-- TOC entry 2308 (class 2606 OID 22739)
-- Name: mm_review_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_review
    ADD CONSTRAINT mm_review_pk PRIMARY KEY (mm_review_guid);


--
-- TOC entry 2319 (class 2606 OID 22776)
-- Name: mm_sync_guid_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_sync
    ADD CONSTRAINT mm_sync_guid_pk PRIMARY KEY (mm_sync_guid);


--
-- TOC entry 2324 (class 2606 OID 22790)
-- Name: mm_trigger_guid_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_trigger
    ADD CONSTRAINT mm_trigger_guid_pk PRIMARY KEY (mm_trigger_guid);


--
-- TOC entry 2361 (class 2606 OID 22887)
-- Name: mm_tuner_id_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_tuner
    ADD CONSTRAINT mm_tuner_id_pk PRIMARY KEY (mm_tuner_id);


--
-- TOC entry 2373 (class 2606 OID 22923)
-- Name: mm_tv_schedule_id_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_tv_schedule
    ADD CONSTRAINT mm_tv_schedule_id_pk PRIMARY KEY (mm_tv_schedule_id);


--
-- TOC entry 2378 (class 2606 OID 22933)
-- Name: mm_tv_schedule_program_guid_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_tv_schedule_program
    ADD CONSTRAINT mm_tv_schedule_program_guid_pk PRIMARY KEY (mm_tv_schedule_program_guid);


--
-- TOC entry 2369 (class 2606 OID 22913)
-- Name: mm_tv_stations_id_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_tv_stations
    ADD CONSTRAINT mm_tv_stations_id_pk PRIMARY KEY (mm_tv_stations_id);


--
-- TOC entry 2335 (class 2606 OID 22819)
-- Name: mm_user_group_guid_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_user_group
    ADD CONSTRAINT mm_user_group_guid_pk PRIMARY KEY (mm_user_group_guid);


--
-- TOC entry 2304 (class 2606 OID 22730)
-- Name: mm_user_pkey; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_user
    ADD CONSTRAINT mm_user_pkey PRIMARY KEY (id);


--
-- TOC entry 2338 (class 2606 OID 22828)
-- Name: mm_user_profile_guid_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_user_profile
    ADD CONSTRAINT mm_user_profile_guid_pk PRIMARY KEY (mm_user_profile_guid);


--
-- TOC entry 2354 (class 2606 OID 22865)
-- Name: mmp_id_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_metadata_person
    ADD CONSTRAINT mmp_id_pk PRIMARY KEY (mmp_id);


--
-- TOC entry 2202 (class 2606 OID 22542)
-- Name: mmr_media_remote_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_media_remote
    ADD CONSTRAINT mmr_media_remote_pk PRIMARY KEY (mmr_media_guid);


--
-- TOC entry 2344 (class 1259 OID 22846)
-- Name: gi_system_id_ndx; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX gi_system_id_ndx ON mm_metadata_game_software_info USING btree (gi_system_id);


--
-- TOC entry 2330 (class 1259 OID 22810)
-- Name: mm_channel_idx_country; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_channel_idx_country ON mm_channel USING btree (mm_channel_country_guid);


--
-- TOC entry 2331 (class 1259 OID 22811)
-- Name: mm_channel_idx_logo; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_channel_idx_logo ON mm_channel USING btree (mm_channel_logo_guid);


--
-- TOC entry 2332 (class 1259 OID 22808)
-- Name: mm_channel_idx_name; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_channel_idx_name ON mm_channel USING btree (mm_channel_name);


--
-- TOC entry 2333 (class 1259 OID 22809)
-- Name: mm_channel_idxgin_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_channel_idxgin_json ON mm_channel USING gin (mm_channel_media_id);


--
-- TOC entry 2366 (class 1259 OID 22904)
-- Name: mm_device_idx_type; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_device_idx_type ON mm_device USING btree (mm_device_type);


--
-- TOC entry 2367 (class 1259 OID 22905)
-- Name: mm_device_idxgin_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_device_idxgin_json ON mm_device USING gin (mm_device_json);


--
-- TOC entry 2357 (class 1259 OID 22877)
-- Name: mm_download_idx_provider; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_download_idx_provider ON mm_download_que USING btree (mdq_provider);


--
-- TOC entry 2358 (class 1259 OID 22878)
-- Name: mm_download_que_idxgin_meta_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_download_que_idxgin_meta_json ON mm_download_que USING gin (mdq_download_json);


--
-- TOC entry 2345 (class 1259 OID 22847)
-- Name: mm_game_info_idxgin_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_game_info_idxgin_json ON mm_metadata_game_software_info USING gin (gi_game_info_json);


--
-- TOC entry 2346 (class 1259 OID 22848)
-- Name: mm_game_info_idxgin_name; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_game_info_idxgin_name ON mm_metadata_game_software_info USING gin (((gi_game_info_json -> '@name'::text)));


--
-- TOC entry 2349 (class 1259 OID 22857)
-- Name: mm_game_systems_idxgin_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_game_systems_idxgin_json ON mm_metadata_game_systems_info USING gin (gs_game_system_json);


--
-- TOC entry 2381 (class 1259 OID 23021)
-- Name: mm_image_download_idx_provider; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_image_download_idx_provider ON mm_download_image_que USING btree (mdq_image_provider);


--
-- TOC entry 2205 (class 1259 OID 22555)
-- Name: mm_link_idx_name; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_link_idx_name ON mm_link USING btree (mm_link_name);


--
-- TOC entry 2206 (class 1259 OID 22554)
-- Name: mm_link_json_idxgin; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_link_json_idxgin ON mm_link USING gin (mm_link_json);


--
-- TOC entry 2255 (class 1259 OID 22639)
-- Name: mm_media_class_idx_type; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_media_class_idx_type ON mm_media_class USING btree (mm_media_class_type);


--
-- TOC entry 2190 (class 1259 OID 22523)
-- Name: mm_media_dir_idx_share; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_media_dir_idx_share ON mm_media_dir USING btree (mm_media_dir_share_guid);


--
-- TOC entry 2193 (class 1259 OID 22533)
-- Name: mm_media_idx_metadata_uuid; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_media_idx_metadata_uuid ON mm_media USING btree (mm_media_metadata_guid);


--
-- TOC entry 2194 (class 1259 OID 22534)
-- Name: mm_media_idx_path; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_media_idx_path ON mm_media USING btree (mm_media_path);


--
-- TOC entry 2195 (class 1259 OID 22532)
-- Name: mm_media_idxgin_ffprobe; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_media_idxgin_ffprobe ON mm_media USING gin (mm_media_ffprobe_json);


--
-- TOC entry 2241 (class 1259 OID 22617)
-- Name: mm_metadata_album_idx_musician; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_album_idx_musician ON mm_metadata_album USING btree (mm_metadata_album_musician_guid);


--
-- TOC entry 2242 (class 1259 OID 22613)
-- Name: mm_metadata_album_idx_name; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_album_idx_name ON mm_metadata_album USING btree (mm_metadata_album_name);


--
-- TOC entry 2243 (class 1259 OID 22614)
-- Name: mm_metadata_album_idx_name_lower; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_album_idx_name_lower ON mm_metadata_album USING btree (lower(mm_metadata_album_name));


--
-- TOC entry 2244 (class 1259 OID 22615)
-- Name: mm_metadata_album_idxgin_id_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_album_idxgin_id_json ON mm_metadata_album USING gin (mm_metadata_album_id);


--
-- TOC entry 2245 (class 1259 OID 22616)
-- Name: mm_metadata_album_idxgin_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_album_idxgin_json ON mm_metadata_album USING gin (mm_metadata_album_json);


--
-- TOC entry 2258 (class 1259 OID 22651)
-- Name: mm_metadata_aniem_idxgin_media_id; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_aniem_idxgin_media_id ON mm_metadata_anime USING gin (mm_metadata_anime_media_id);


--
-- TOC entry 2259 (class 1259 OID 22648)
-- Name: mm_metadata_anime_idx_name; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_anime_idx_name ON mm_metadata_anime USING btree (mm_media_anime_name);


--
-- TOC entry 2260 (class 1259 OID 22649)
-- Name: mm_metadata_anime_idx_name_lower; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_anime_idx_name_lower ON mm_metadata_anime USING btree (lower(mm_media_anime_name));


--
-- TOC entry 2261 (class 1259 OID 22650)
-- Name: mm_metadata_anime_idxgin_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_anime_idxgin_json ON mm_metadata_anime USING gin (mm_metadata_anime_json);


--
-- TOC entry 2262 (class 1259 OID 22652)
-- Name: mm_metadata_anime_idxgin_media_id_anidb; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_anime_idxgin_media_id_anidb ON mm_metadata_anime USING gin (((mm_metadata_anime_media_id -> 'anidb'::text)));


--
-- TOC entry 2263 (class 1259 OID 22655)
-- Name: mm_metadata_anime_idxgin_media_id_imdb; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_anime_idxgin_media_id_imdb ON mm_metadata_anime USING gin (((mm_metadata_anime_media_id -> 'imdb'::text)));


--
-- TOC entry 2264 (class 1259 OID 22653)
-- Name: mm_metadata_anime_idxgin_media_id_thetvdb; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_anime_idxgin_media_id_thetvdb ON mm_metadata_anime USING gin (((mm_metadata_anime_media_id -> 'thetvdb'::text)));


--
-- TOC entry 2265 (class 1259 OID 22654)
-- Name: mm_metadata_anime_idxgin_media_id_tmdb; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_anime_idxgin_media_id_tmdb ON mm_metadata_anime USING gin (((mm_metadata_anime_media_id -> 'tmdb'::text)));


--
-- TOC entry 2266 (class 1259 OID 22656)
-- Name: mm_metadata_anime_idxgin_user_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_anime_idxgin_user_json ON mm_metadata_anime USING gin (mm_metadata_anime_user_json);


--
-- TOC entry 2311 (class 1259 OID 22750)
-- Name: mm_metadata_collection_idxgin_media_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_collection_idxgin_media_json ON mm_metadata_collection USING gin (mm_metadata_collection_media_ids);


--
-- TOC entry 2312 (class 1259 OID 22752)
-- Name: mm_metadata_collection_idxgin_meta_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_collection_idxgin_meta_json ON mm_metadata_collection USING gin (mm_metadata_collection_json);


--
-- TOC entry 2313 (class 1259 OID 22751)
-- Name: mm_metadata_collection_idxgin_name_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_collection_idxgin_name_json ON mm_metadata_collection USING gin (mm_metadata_collection_name);


--
-- TOC entry 2279 (class 1259 OID 22681)
-- Name: mm_metadata_idx_band_name; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_idx_band_name ON mm_metadata_music_video USING btree (mm_media_music_video_band);


--
-- TOC entry 2280 (class 1259 OID 22682)
-- Name: mm_metadata_idx_band_name_lower; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_idx_band_name_lower ON mm_metadata_music_video USING btree (lower(mm_media_music_video_band));


--
-- TOC entry 2290 (class 1259 OID 22696)
-- Name: mm_metadata_idx_book_name; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_idx_book_name ON mm_metadata_book USING btree (mm_metadata_book_name);


--
-- TOC entry 2291 (class 1259 OID 22697)
-- Name: mm_metadata_idx_book_name_lower; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_idx_book_name_lower ON mm_metadata_book USING btree (lower(mm_metadata_book_name));


--
-- TOC entry 2269 (class 1259 OID 22665)
-- Name: mm_metadata_idx_name; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_idx_name ON mm_metadata_movie USING btree (mm_media_name);


--
-- TOC entry 2270 (class 1259 OID 22666)
-- Name: mm_metadata_idx_name_lower; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_idx_name_lower ON mm_metadata_movie USING btree (lower(mm_media_name));


--
-- TOC entry 2281 (class 1259 OID 22683)
-- Name: mm_metadata_idx_song_name; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_idx_song_name ON mm_metadata_music_video USING btree (mm_media_music_video_song);


--
-- TOC entry 2282 (class 1259 OID 22684)
-- Name: mm_metadata_idx_song_name_lower; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_idx_song_name_lower ON mm_metadata_music_video USING btree (lower(mm_media_music_video_song));


--
-- TOC entry 2292 (class 1259 OID 22698)
-- Name: mm_metadata_idxgin_isbn; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_idxgin_isbn ON mm_metadata_book USING btree (mm_metadata_book_isbn);


--
-- TOC entry 2293 (class 1259 OID 22699)
-- Name: mm_metadata_idxgin_isbn13; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_idxgin_isbn13 ON mm_metadata_book USING btree (mm_metadata_book_isbn13);


--
-- TOC entry 2271 (class 1259 OID 22667)
-- Name: mm_metadata_idxgin_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_idxgin_json ON mm_metadata_movie USING gin (mm_metadata_json);


--
-- TOC entry 2272 (class 1259 OID 22668)
-- Name: mm_metadata_idxgin_media_id; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_idxgin_media_id ON mm_metadata_movie USING gin (mm_metadata_media_id);


--
-- TOC entry 2273 (class 1259 OID 22671)
-- Name: mm_metadata_idxgin_media_id_imdb; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_idxgin_media_id_imdb ON mm_metadata_movie USING gin (((mm_metadata_media_id -> 'imdb'::text)));


--
-- TOC entry 2274 (class 1259 OID 22669)
-- Name: mm_metadata_idxgin_media_id_thetvdb; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_idxgin_media_id_thetvdb ON mm_metadata_movie USING gin (((mm_metadata_media_id -> 'thetvdb'::text)));


--
-- TOC entry 2275 (class 1259 OID 22670)
-- Name: mm_metadata_idxgin_media_id_tmdb; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_idxgin_media_id_tmdb ON mm_metadata_movie USING gin (((mm_metadata_media_id -> 'tmdb'::text)));


--
-- TOC entry 2283 (class 1259 OID 22685)
-- Name: mm_metadata_idxgin_music_video_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_idxgin_music_video_json ON mm_metadata_music_video USING gin (mm_metadata_music_video_json);


--
-- TOC entry 2284 (class 1259 OID 22686)
-- Name: mm_metadata_idxgin_music_video_media_id; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_idxgin_music_video_media_id ON mm_metadata_music_video USING gin (mm_metadata_music_video_media_id);


--
-- TOC entry 2285 (class 1259 OID 22687)
-- Name: mm_metadata_idxgin_music_video_media_id_imvdb; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_idxgin_music_video_media_id_imvdb ON mm_metadata_music_video USING gin (((mm_metadata_music_video_media_id -> 'imvdb'::text)));


--
-- TOC entry 2276 (class 1259 OID 22672)
-- Name: mm_metadata_idxgin_user_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_idxgin_user_json ON mm_metadata_movie USING gin (mm_metadata_user_json);


--
-- TOC entry 2327 (class 1259 OID 22799)
-- Name: mm_metadata_logo_idxgin_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_logo_idxgin_json ON mm_metadata_logo USING gin (mm_metadata_logo_media_guid);


--
-- TOC entry 2248 (class 1259 OID 22630)
-- Name: mm_metadata_music_idx_album; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_music_idx_album ON mm_metadata_music USING btree (mm_metadata_music_album_guid);


--
-- TOC entry 2249 (class 1259 OID 22626)
-- Name: mm_metadata_music_idx_name; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_music_idx_name ON mm_metadata_music USING btree (mm_metadata_music_name);


--
-- TOC entry 2250 (class 1259 OID 22627)
-- Name: mm_metadata_music_idx_name_lower; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_music_idx_name_lower ON mm_metadata_music USING btree (lower(mm_metadata_music_name));


--
-- TOC entry 2251 (class 1259 OID 22628)
-- Name: mm_metadata_music_idxgin_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_music_idxgin_json ON mm_metadata_music USING gin (mm_metadata_music_json);


--
-- TOC entry 2252 (class 1259 OID 22629)
-- Name: mm_metadata_music_idxgin_media_id; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_music_idxgin_media_id ON mm_metadata_music USING gin (mm_metadata_media_music_id);


--
-- TOC entry 2235 (class 1259 OID 22601)
-- Name: mm_metadata_musician_idx_name; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_musician_idx_name ON mm_metadata_musician USING btree (mm_metadata_musician_name);


--
-- TOC entry 2236 (class 1259 OID 22602)
-- Name: mm_metadata_musician_idx_name_lower; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_musician_idx_name_lower ON mm_metadata_musician USING btree (lower(mm_metadata_musician_name));


--
-- TOC entry 2237 (class 1259 OID 22603)
-- Name: mm_metadata_musician_idxgin_id_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_musician_idxgin_id_json ON mm_metadata_musician USING gin (mm_metadata_musician_id);


--
-- TOC entry 2238 (class 1259 OID 22604)
-- Name: mm_metadata_musician_idxgin_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_musician_idxgin_json ON mm_metadata_musician USING gin (mm_metadata_musician_json);


--
-- TOC entry 2350 (class 1259 OID 22866)
-- Name: mm_metadata_person_idx_name; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_person_idx_name ON mm_metadata_person USING btree (mmp_person_name);


--
-- TOC entry 2351 (class 1259 OID 22867)
-- Name: mm_metadata_person_idxgin_id_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_person_idxgin_id_json ON mm_metadata_person USING gin (mmp_person_media_id);


--
-- TOC entry 2352 (class 1259 OID 22868)
-- Name: mm_metadata_person_idxgin_meta_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_person_idxgin_meta_json ON mm_metadata_person USING gin (mmp_person_meta_json);


--
-- TOC entry 2305 (class 1259 OID 22741)
-- Name: mm_metadata_review_idx_metadata_uuid; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_review_idx_metadata_uuid ON mm_review USING btree (mm_review_metadata_guid);


--
-- TOC entry 2306 (class 1259 OID 22740)
-- Name: mm_metadata_review_idxgin_media_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_review_idxgin_media_json ON mm_review USING gin (mm_review_metadata_id);


--
-- TOC entry 2223 (class 1259 OID 22583)
-- Name: mm_metadata_sports_idx_name; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_sports_idx_name ON mm_metadata_sports USING btree (mm_metadata_sports_name);


--
-- TOC entry 2224 (class 1259 OID 22584)
-- Name: mm_metadata_sports_idx_name_lower; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_sports_idx_name_lower ON mm_metadata_sports USING btree (lower(mm_metadata_sports_name));


--
-- TOC entry 2225 (class 1259 OID 22585)
-- Name: mm_metadata_sports_idxgin_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_sports_idxgin_json ON mm_metadata_sports USING gin (mm_metadata_sports_json);


--
-- TOC entry 2226 (class 1259 OID 22586)
-- Name: mm_metadata_sports_idxgin_media_id; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_sports_idxgin_media_id ON mm_metadata_sports USING gin (mm_metadata_media_sports_id);


--
-- TOC entry 2227 (class 1259 OID 22587)
-- Name: mm_metadata_sports_idxgin_media_id_imdb; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_sports_idxgin_media_id_imdb ON mm_metadata_sports USING gin (((mm_metadata_media_sports_id -> 'imdb'::text)));


--
-- TOC entry 2228 (class 1259 OID 22592)
-- Name: mm_metadata_sports_idxgin_media_id_thesportsdb; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_sports_idxgin_media_id_thesportsdb ON mm_metadata_sports USING gin (((mm_metadata_media_sports_id -> 'thesportsdb'::text)));


--
-- TOC entry 2229 (class 1259 OID 22588)
-- Name: mm_metadata_sports_idxgin_media_id_thetvdb; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_sports_idxgin_media_id_thetvdb ON mm_metadata_sports USING gin (((mm_metadata_media_sports_id -> 'thetvdb'::text)));


--
-- TOC entry 2230 (class 1259 OID 22590)
-- Name: mm_metadata_sports_idxgin_media_id_thetvdbseries; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_sports_idxgin_media_id_thetvdbseries ON mm_metadata_sports USING gin (((mm_metadata_media_sports_id -> 'thetvdbSeries'::text)));


--
-- TOC entry 2231 (class 1259 OID 22589)
-- Name: mm_metadata_sports_idxgin_media_id_tmdb; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_sports_idxgin_media_id_tmdb ON mm_metadata_sports USING gin (((mm_metadata_media_sports_id -> 'tmdb'::text)));


--
-- TOC entry 2232 (class 1259 OID 22591)
-- Name: mm_metadata_sports_idxgin_media_id_tvmaze; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_sports_idxgin_media_id_tvmaze ON mm_metadata_sports USING gin (((mm_metadata_media_sports_id -> 'tvmaze'::text)));


--
-- TOC entry 2207 (class 1259 OID 22564)
-- Name: mm_metadata_tvshow_idx_name; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_tvshow_idx_name ON mm_metadata_tvshow USING btree (mm_metadata_tvshow_name);


--
-- TOC entry 2208 (class 1259 OID 22565)
-- Name: mm_metadata_tvshow_idx_name_lower; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_tvshow_idx_name_lower ON mm_metadata_tvshow USING btree (lower(mm_metadata_tvshow_name));


--
-- TOC entry 2209 (class 1259 OID 22567)
-- Name: mm_metadata_tvshow_idxgin_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_tvshow_idxgin_json ON mm_metadata_tvshow USING gin (mm_metadata_tvshow_json);


--
-- TOC entry 2210 (class 1259 OID 22568)
-- Name: mm_metadata_tvshow_idxgin_localimage_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_tvshow_idxgin_localimage_json ON mm_metadata_tvshow USING gin (mm_metadata_tvshow_json);


--
-- TOC entry 2211 (class 1259 OID 22566)
-- Name: mm_metadata_tvshow_idxgin_media_id; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_tvshow_idxgin_media_id ON mm_metadata_tvshow USING gin (mm_metadata_media_tvshow_id);


--
-- TOC entry 2212 (class 1259 OID 22569)
-- Name: mm_metadata_tvshow_idxgin_media_id_imdb; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_tvshow_idxgin_media_id_imdb ON mm_metadata_tvshow USING gin (((mm_metadata_media_tvshow_id -> 'imdb'::text)));


--
-- TOC entry 2213 (class 1259 OID 22570)
-- Name: mm_metadata_tvshow_idxgin_media_id_thetvdb; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_tvshow_idxgin_media_id_thetvdb ON mm_metadata_tvshow USING gin (((mm_metadata_media_tvshow_id -> 'thetvdb'::text)));


--
-- TOC entry 2214 (class 1259 OID 22572)
-- Name: mm_metadata_tvshow_idxgin_media_id_thetvdbseries; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_tvshow_idxgin_media_id_thetvdbseries ON mm_metadata_tvshow USING gin (((mm_metadata_media_tvshow_id -> 'thetvdbSeries'::text)));


--
-- TOC entry 2215 (class 1259 OID 22571)
-- Name: mm_metadata_tvshow_idxgin_media_id_tmdb; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_tvshow_idxgin_media_id_tmdb ON mm_metadata_tvshow USING gin (((mm_metadata_media_tvshow_id -> 'tmdb'::text)));


--
-- TOC entry 2216 (class 1259 OID 22573)
-- Name: mm_metadata_tvshow_idxgin_media_id_tvmaze; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_tvshow_idxgin_media_id_tvmaze ON mm_metadata_tvshow USING gin (((mm_metadata_media_tvshow_id -> 'tvmaze'::text)));


--
-- TOC entry 2217 (class 1259 OID 67497)
-- Name: mm_metadata_tvshow_idxgin_season_number_thetvdb; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_tvshow_idxgin_season_number_thetvdb ON mm_metadata_tvshow USING gin (((((((mm_metadata_tvshow_json -> 'Meta'::text) -> 'thetvdb'::text) -> 'Meta'::text) -> 'Episodes'::text) -> 'SeasonNumber'::text)));


--
-- TOC entry 2218 (class 1259 OID 67498)
-- Name: mm_metadata_tvshow_idxgin_season_number_thetvdb2; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_tvshow_idxgin_season_number_thetvdb2 ON mm_metadata_tvshow USING gin (((((((mm_metadata_tvshow_json -> 'Meta'::text) -> 'thetvdb'::text) -> 'Meta'::text) -> 'Episode'::text) -> 'SeasonNumber'::text)));


--
-- TOC entry 2219 (class 1259 OID 67499)
-- Name: mm_metadata_tvshow_idxgin_season_number_thetvdb23; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_tvshow_idxgin_season_number_thetvdb23 ON mm_metadata_tvshow USING gin ((((((mm_metadata_tvshow_json -> 'Meta'::text) -> 'thetvdb'::text) -> 'Meta'::text) -> 'Episode'::text)));


--
-- TOC entry 2220 (class 1259 OID 22574)
-- Name: mm_metadata_tvshow_idxgin_user_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_tvshow_idxgin_user_json ON mm_metadata_tvshow USING gin (mm_metadata_tvshow_user_json);


--
-- TOC entry 2298 (class 1259 OID 22719)
-- Name: mm_notification_idx_dismissable; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_notification_idx_dismissable ON mm_notification USING btree (mm_notification_dismissable);


--
-- TOC entry 2299 (class 1259 OID 22718)
-- Name: mm_notification_idx_time; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_notification_idx_time ON mm_notification USING btree (mm_notification_time);


--
-- TOC entry 2320 (class 1259 OID 22777)
-- Name: mm_sync_idxgin_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_sync_idxgin_json ON mm_sync USING gin (mm_sync_options_json);


--
-- TOC entry 2374 (class 1259 OID 22924)
-- Name: mm_tv_schedule_idx_date; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_tv_schedule_idx_date ON mm_tv_schedule USING btree (mm_tv_schedule_date);


--
-- TOC entry 2376 (class 1259 OID 22934)
-- Name: mm_tv_schedule_idx_program; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_tv_schedule_idx_program ON mm_tv_schedule_program USING btree (mm_tv_schedule_program_id);


--
-- TOC entry 2375 (class 1259 OID 22925)
-- Name: mm_tv_schedule_idx_station; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_tv_schedule_idx_station ON mm_tv_schedule USING btree (mm_tv_schedule_station_id);


--
-- TOC entry 2370 (class 1259 OID 22915)
-- Name: mm_tv_stations_idx_name; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_tv_stations_idx_name ON mm_tv_stations USING btree (mm_tv_station_name);


--
-- TOC entry 2371 (class 1259 OID 22914)
-- Name: mm_tv_stations_idx_station; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_tv_stations_idx_station ON mm_tv_stations USING btree (mm_tv_station_id);


--
-- TOC entry 2296 (class 1259 OID 22709)
-- Name: mm_user_activity_idx_date; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_user_activity_idx_date ON mm_user_activity USING btree (mm_activity_datecreated);


--
-- TOC entry 2297 (class 1259 OID 22708)
-- Name: mm_user_activity_idx_user_guid; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_user_activity_idx_user_guid ON mm_user_activity USING btree (mm_activity_userid);


--
-- TOC entry 2336 (class 1259 OID 22820)
-- Name: mm_user_group_idx_name; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_user_group_idx_name ON mm_user_group USING btree (mm_user_group_name);


--
-- TOC entry 2302 (class 1259 OID 22731)
-- Name: mm_user_idx_username; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_user_idx_username ON mm_user USING btree (username);


--
-- TOC entry 2339 (class 1259 OID 22829)
-- Name: mm_user_profile_idx_name; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_user_profile_idx_name ON mm_user_profile USING btree (mm_user_profile_name);


--
-- TOC entry 2198 (class 1259 OID 22545)
-- Name: mmr_media_idx_link_uuid; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mmr_media_idx_link_uuid ON mm_media_remote USING btree (mmr_media_link_id);


--
-- TOC entry 2199 (class 1259 OID 22544)
-- Name: mmr_media_idx_metadata_uuid; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mmr_media_idx_metadata_uuid ON mm_media_remote USING btree (mmr_media_metadata_guid);


--
-- TOC entry 2200 (class 1259 OID 22543)
-- Name: mmr_media_idxgin_ffprobe; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mmr_media_idxgin_ffprobe ON mm_media_remote USING gin (mmr_media_ffprobe_json);


--
-- TOC entry 2359 (class 1259 OID 22879)
-- Name: mqd_que_type_idx_name; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mqd_que_type_idx_name ON mm_download_que USING btree (mdq_que_type);


--
-- TOC entry 2545 (class 0 OID 0)
-- Dependencies: 6
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


-- Completed on 2017-07-01 22:30:31 CDT

--
-- PostgreSQL database dump complete
--

