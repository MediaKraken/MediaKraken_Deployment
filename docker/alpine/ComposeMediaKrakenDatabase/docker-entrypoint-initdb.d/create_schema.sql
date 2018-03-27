--
-- PostgreSQL database dump
--

-- Dumped from database version 10.2
-- Dumped by pg_dump version 10.2

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
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


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
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
-- Name: mm_device; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE mm_device (
    mm_device_id uuid NOT NULL,
    mm_device_type text,
    mm_device_json jsonb
);


ALTER TABLE mm_device OWNER TO metamanpg;

--
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
-- Name: mm_link; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE mm_link (
    mm_link_guid uuid NOT NULL,
    mm_link_name text,
    mm_link_json jsonb
);


ALTER TABLE mm_link OWNER TO metamanpg;

--
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
-- Name: mm_metadata_game_software_info; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE mm_metadata_game_software_info (
    gi_id uuid NOT NULL,
    gi_system_id uuid,
    gi_game_info_name text,
    gi_game_info_json jsonb
);


ALTER TABLE mm_metadata_game_software_info OWNER TO metamanpg;

--
-- Name: mm_metadata_game_systems_info; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE mm_metadata_game_systems_info (
    gs_id uuid NOT NULL,
    gs_game_system_name text,
    gs_game_system_alias text,
    gs_game_system_json jsonb
);


ALTER TABLE mm_metadata_game_systems_info OWNER TO metamanpg;

--
-- Name: mm_metadata_logo; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE mm_metadata_logo (
    mm_metadata_logo_guid uuid NOT NULL,
    mm_metadata_logo_media_guid jsonb,
    mm_metadata_logo_image_path text
);


ALTER TABLE mm_metadata_logo OWNER TO metamanpg;

--
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
-- Name: mm_options_and_status; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE mm_options_and_status (
    mm_options_and_status_guid uuid NOT NULL,
    mm_options_json jsonb,
    mm_status_json jsonb
);


ALTER TABLE mm_options_and_status OWNER TO metamanpg;

--
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
-- Name: mm_tv_schedule_program; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE mm_tv_schedule_program (
    mm_tv_schedule_program_guid uuid NOT NULL,
    mm_tv_schedule_program_id text,
    mm_tv_schedule_program_json jsonb
);


ALTER TABLE mm_tv_schedule_program OWNER TO metamanpg;

--
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
-- Name: mm_user_id_seq; Type: SEQUENCE; Schema: public; Owner: metamanpg
--

CREATE SEQUENCE mm_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE mm_user_id_seq OWNER TO metamanpg;

--
-- Name: mm_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: metamanpg
--

ALTER SEQUENCE mm_user_id_seq OWNED BY mm_user.id;


--
-- Name: mm_user_profile; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE mm_user_profile (
    mm_user_profile_guid uuid NOT NULL,
    mm_user_profile_name text,
    mm_user_profile_json jsonb
);


ALTER TABLE mm_user_profile OWNER TO metamanpg;

--
-- Name: mm_version; Type: TABLE; Schema: public; Owner: metamanpg
--

CREATE TABLE mm_version (
    mm_version_no integer
);


ALTER TABLE mm_version OWNER TO metamanpg;

--
-- Name: mm_user id; Type: DEFAULT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_user ALTER COLUMN id SET DEFAULT nextval('mm_user_id_seq'::regclass);


--
-- Data for Name: mm_channel; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_channel (mm_channel_guid, mm_channel_name, mm_channel_media_id, mm_channel_country_guid, mm_channel_logo_guid) FROM stdin;
\.


--
-- Data for Name: mm_cron; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_cron (mm_cron_guid, mm_cron_name, mm_cron_description, mm_cron_enabled, mm_cron_schedule, mm_cron_last_run, mm_cron_file_path) FROM stdin;
\.


--
-- Data for Name: mm_device; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_device (mm_device_id, mm_device_type, mm_device_json) FROM stdin;
\.


--
-- Data for Name: mm_download_image_que; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_download_image_que (mdq_image_id, mdq_image_provider, mdq_image_download_json) FROM stdin;
\.


--
-- Data for Name: mm_download_que; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_download_que (mdq_id, mdq_provider, mdq_que_type, mdq_download_json) FROM stdin;
\.


--
-- Data for Name: mm_link; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_link (mm_link_guid, mm_link_name, mm_link_json) FROM stdin;
\.


--
-- Data for Name: mm_loan; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_loan (mm_loan_guid, mm_loan_media_id, mm_loan_user_id, mm_load_user_loan_id, mm_loan_time, mm_loan_return_time) FROM stdin;
\.


--
-- Data for Name: mm_media; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_media (mm_media_guid, mm_media_class_guid, mm_media_metadata_guid, mm_media_path, mm_media_ffprobe_json, mm_media_json) FROM stdin;
\.


--
-- Data for Name: mm_media_class; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_media_class (mm_media_class_guid, mm_media_class_type, mm_media_class_parent_type, mm_media_class_display) FROM stdin;
d2a584a0-f255-40ca-8cbc-ef30c9b73b1b	Adult	Video	t
33a24789-c9b9-488d-b132-008f01dc08d2	Anime	Video	t
4adf0bbc-efab-4105-a8e1-a6bf28e45884	Book	Publication	t
ba655afa-6c07-4953-b375-aed8250146b5	Boxset	\N	f
aaeef69f-791b-4657-9018-85cd79e57b45	Game CHD	\N	f
11e5ef43-b55a-4d64-a98e-0a48875eebff	Game ISO	\N	f
592f2a92-ac09-442c-a2a4-941fb82d6fa6	Game ROM	\N	f
636ae273-615e-43ff-bc46-70e2ceb445c6	Home Movie	Video	t
f05854e1-36bd-4b83-b5e6-385d0355877e	Magazine	Publication	t
a85e39a4-a441-4153-9865-604a6b8682c8	Movie	Video	t
d47f4e00-de59-48cc-8f65-812f43142575	Movie Extras	Video	f
11ca1a7e-37fe-4267-bc15-4847270c24a8	Movie Collection	\N	f
1935401c-2e61-432c-b47f-858e6ed68ffb	Movie Theme	Audio	f
4d3b49d9-8eb7-4221-ade6-31fefee50fd5	Movie Trailer	Video	f
0c290d3d-8b04-41f7-9ea7-18f375857fea	Music	Audio	t
4b4fa85d-426a-4e04-813c-4ae87bc546ed	Music Album	\N	f
e7e95ddb-a4da-49b6-9686-219378a558b8	Music Collection	\N	f
3fb4eb83-991c-49c4-a074-aed12c3667f0	Music Lyric	\N	f
c80adee7-88be-4e76-b2a7-bd84b7387a93	Music Video	Video	t
b1ca2251-0bca-494e-84ea-2000caa54ddc	Person	\N	f
145aa1d6-a00f-4556-8bb6-c4e4835ee7e0	Picture	Image	t
cc8ac688-3105-486f-959c-e908bc542200	Soundtrack	Audio	f
981da86a-e726-4570-8eb1-68e38bb90337	Sports	Video	t
da7d560d-31d7-4597-8620-0e8e5ad5e3d6	Subtitle	\N	f
3d0b2f73-62ed-4b90-9afc-dffc65fc73ad	TV Episode	Video	f
ad53f94c-a1d0-4a7c-9aa0-0f033a4169d7	TV Extras	Video	f
ac101fb7-7d8f-4023-b05e-e378fb5a25ba	TV Season	\N	f
9d67c9bc-a35e-4af9-a2a8-fb91084bf588	TV Show	Video	t
a1215d38-116f-42d6-8347-485aa173766e	TV Theme	Audio	f
35870354-9e87-421a-a8de-7dd13589e9f4	TV Trailer	Video	f
db995617-7584-4218-becc-b0443216f0a6	Video Game	Game	t
c9c65ede-c763-4547-9b65-ea46746e537c	Video Game Intro	Video	t
e1c66a43-e582-4768-b076-880152738b7d	Video Game Speedrun	Video	t
0c31d95c-00c5-4fe1-8247-070ab2ef9197	Video Game Superplay	Video	t
\.


--
-- Data for Name: mm_media_dir; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_media_dir (mm_media_dir_guid, mm_media_dir_path, mm_media_dir_class_type, mm_media_dir_last_scanned, mm_media_dir_share_guid, mm_media_dir_status) FROM stdin;
\.


--
-- Data for Name: mm_media_remote; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_media_remote (mmr_media_guid, mmr_media_link_id, mmr_media_uuid, mmr_media_class_guid, mmr_media_metadata_guid, mmr_media_ffprobe_json, mmr_media_json) FROM stdin;
\.


--
-- Data for Name: mm_media_share; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_media_share (mm_media_share_guid, mm_media_share_type, mm_media_share_user, mm_media_share_password, mm_media_share_server, mm_media_share_path) FROM stdin;
\.


--
-- Data for Name: mm_metadata_album; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_metadata_album (mm_metadata_album_guid, mm_metadata_album_name, mm_metadata_album_id, mm_metadata_album_json, mm_metadata_album_musician_guid) FROM stdin;
\.


--
-- Data for Name: mm_metadata_anime; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_metadata_anime (mm_metadata_anime_guid, mm_metadata_anime_media_id, mm_media_anime_name, mm_metadata_anime_json, mm_metadata_anime_mapping, mm_metadata_anime_mapping_before, mm_metadata_anime_localimage_json, mm_metadata_anime_user_json) FROM stdin;
\.


--
-- Data for Name: mm_metadata_book; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_metadata_book (mm_metadata_book_guid, mm_metadata_book_isbn, mm_metadata_book_isbn13, mm_metadata_book_name, mm_metadata_book_json, mm_metadata_book_image_json) FROM stdin;
\.


--
-- Data for Name: mm_metadata_collection; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_metadata_collection (mm_metadata_collection_guid, mm_metadata_collection_name, mm_metadata_collection_media_ids, mm_metadata_collection_json, mm_metadata_collection_imagelocal_json) FROM stdin;
\.


--
-- Data for Name: mm_metadata_game_software_info; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_metadata_game_software_info (gi_id, gi_system_id, gi_game_info_name, gi_game_info_json) FROM stdin;
\.


--
-- Data for Name: mm_metadata_game_systems_info; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_metadata_game_systems_info (gs_id, gs_game_system_name, gs_game_system_alias, gs_game_system_json) FROM stdin;
\.


--
-- Data for Name: mm_metadata_logo; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_metadata_logo (mm_metadata_logo_guid, mm_metadata_logo_media_guid, mm_metadata_logo_image_path) FROM stdin;
\.


--
-- Data for Name: mm_metadata_movie; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_metadata_movie (mm_metadata_guid, mm_metadata_media_id, mm_media_name, mm_metadata_json, mm_metadata_localimage_json, mm_metadata_user_json) FROM stdin;
\.


--
-- Data for Name: mm_metadata_music; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_metadata_music (mm_metadata_music_guid, mm_metadata_media_music_id, mm_metadata_music_name, mm_metadata_music_json, mm_metadata_music_album_guid) FROM stdin;
\.


--
-- Data for Name: mm_metadata_music_video; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_metadata_music_video (mm_metadata_music_video_guid, mm_metadata_music_video_media_id, mm_media_music_video_band, mm_media_music_video_song, mm_metadata_music_video_json, mm_metadata_music_video_localimage_json) FROM stdin;
\.


--
-- Data for Name: mm_metadata_musician; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_metadata_musician (mm_metadata_musician_guid, mm_metadata_musician_name, mm_metadata_musician_id, mm_metadata_musician_json) FROM stdin;
\.


--
-- Data for Name: mm_metadata_person; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_metadata_person (mmp_id, mmp_person_media_id, mmp_person_meta_json, mmp_person_image, mmp_person_name) FROM stdin;
\.


--
-- Data for Name: mm_metadata_sports; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_metadata_sports (mm_metadata_sports_guid, mm_metadata_media_sports_id, mm_metadata_sports_name, mm_metadata_sports_json, mm_metadata_sports_image_json) FROM stdin;
\.


--
-- Data for Name: mm_metadata_tvshow; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_metadata_tvshow (mm_metadata_tvshow_guid, mm_metadata_media_tvshow_id, mm_metadata_tvshow_name, mm_metadata_tvshow_json, mm_metadata_tvshow_localimage_json, mm_metadata_tvshow_user_json) FROM stdin;
\.


--
-- Data for Name: mm_notification; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_notification (mm_notification_guid, mm_notification_text, mm_notification_time, mm_notification_dismissable) FROM stdin;
\.


--
-- Data for Name: mm_options_and_status; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_options_and_status (mm_options_and_status_guid, mm_options_json, mm_status_json) FROM stdin;
df9a110f-b916-4b78-9d11-35f6ad9b1998	{"SD": {"User": null, "Password": null}, "API": {"anidb": null, "imvdb": null, "google": "AIzaSyCwMkNYp8E4H19BDzlM7-IDkNCQtw0R9lY", "isbndb": "25C8IT4I", "tvmaze": null, "thetvdb": "147CB43DCA8B61B7", "thelogodb": null, "soundcloud": null, "themoviedb": "f72118d1e84b8a1438935972a9c37cac", "globalcache": null, "mediabrainz": null, "thesportsdb": "4352761817344", "opensubtitles": null, "openweathermap": "575b4ae4615e4e2a4c34fb9defa17ceb", "rottentomatoes": "f4tnu5dn9r7f28gjth3ftqaj"}, "AWSS3": {"Bucket": "mediakraken", "AccessKey": null, "BackupBucket": "mkbackup", "SecretAccessKey": null}, "Trakt": {"ApiKey": null, "ClientID": null, "SecretKey": null}, "Backup": {"Interval": 0, "BackupType": "local"}, "Docker": {"Nodes": 0, "SwarmID": null, "Instances": 0}, "Dropbox": {"APIKey": null, "APISecret": null}, "Trailer": {"Clip": false, "Behind": false, "Carpool": false, "Trailer": false, "Featurette": false}, "OneDrive": {"ClientID": null, "SecretKey": null}, "GoogleDrive": {"SecretFile": null}, "Maintenance": null, "MediaBrainz": {"Host": null, "Port": 5000, "User": null, "Password": null, "BrainzDBHost": null, "BrainzDBName": null, "BrainzDBPass": null, "BrainzDBPort": 5432, "BrainzDBUser": null}, "MaxResumePct": 5, "Transmission": {"Host": null, "Port": 9091}, "MediaKrakenServer": {"APIPort": 8097, "ListenPort": 8098, "BackupLocal": "/mediakraken/backups/"}}	{"thetvdb_Updated_Epoc": 0}
\.


--
-- Data for Name: mm_radio; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_radio (mm_radio_guid, mm_radio_name, mm_radio_adress, mm_radio_active) FROM stdin;
\.


--
-- Data for Name: mm_review; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_review (mm_review_guid, mm_review_metadata_id, mm_review_metadata_guid, mm_review_json) FROM stdin;
\.


--
-- Data for Name: mm_sync; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_sync (mm_sync_guid, mm_sync_path, mm_sync_path_to, mm_sync_options_json) FROM stdin;
\.


--
-- Data for Name: mm_task; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_task (mm_task_guid, mm_task_name, mm_task_description, mm_task_enabled, mm_task_schedule, mm_task_last_run, mm_task_file_path, mm_task_json) FROM stdin;
318e7481-aa7c-4d79-a08f-a75d3cebec6f	Anime	Match anime via Scudlee data	f	Days 1	1970-01-01 00:00:01	/mediakraken/subprogram_match_anime_id_scudlee.py	{"task": "anime", "route_key": "Z", "exchange_key": "mkque_metadata_ex"}
64549cdf-0f18-4710-834a-8d5022463b3b	Collections	Create and update collection(s)	f	Days 1	1970-01-01 00:00:01	/mediakraken/subprogram_metadata_update_create_collections.py	{"task": "collection", "route_key": "themoviedb", "exchange_key": "mkque_metadata_ex"}
f0c02554-dd72-455f-a3a4-d373cea686ea	Create Chapter Image	Create chapter images for all media	f	Days 1	1970-01-01 00:00:01	/mediakraken/subprogram_create_chapter_images.py	{"task": "chapter", "route_key": "mkque", "exchange_key": "mkque_ex"}
10c814ea-6e9b-4ee4-b048-59e25b175b32	Roku Thumb	Generate Roku thumbnail images	f	Days 1	1970-01-01 00:00:01	/mediakraken/subprogram_roku_thumbnail_generate.py	{"task": "rokuthumbnail", "route_key": "mkque", "exchange_key": "mkque_ex"}
38f8b2d2-8bdf-48eb-8dd5-37a9a80e94fb	Schedules Direct	Fetch TV schedules from Schedules Direct	f	Days 1	1970-01-01 00:00:01	/mediakraken/subprogram_schedules_direct_updates.py	{"task": "update", "route_key": "schedulesdirect", "exchange_key": "mkque_metadata_ex"}
a51ddbbd-f729-4e34-b90a-beedad54e4fc	Subtitle	Download missing subtitles for media	f	Days 1	1970-01-01 00:00:01	/mediakraken/subprogram_subtitle_downloader.py	{"task": "subtitle", "route_key": "Z", "exchange_key": "mkque_metadata_ex"}
31fd27cd-60ab-4e01-b1a8-0c4da72e1525	The Movie Database	Grab updated movie metadata	f	Days 1	1970-01-01 00:00:01	/mediakraken/subprogram_metadata_tmdb_updates.py	{"task": "update", "route_key": "themoviedb", "exchange_key": "mkque_metadata_ex"}
595c01cd-7d12-4f8c-9a28-3a2e2863f539	TheTVDB Update	Grab updated TheTVDB metadata	f	Days 1	1970-01-01 00:00:01	/mediakraken/subprogram_metadata_thetvdb_updates.py	{"task": "update", "route_key": "thetvdb", "exchange_key": "mkque_metadata_ex"}
2ab40aff-c8dd-4c44-9593-91c7f5cc709c	TVmaze Update	Grab updated TVmaze metadata	f	Days 1	1970-01-01 00:00:01	/mediakraken/subprogram_metadata_tvmaze_updates.py	{"task": "update", "route_key": "tvmaze", "exchange_key": "mkque_metadata_ex"}
979b362c-8fd3-4c53-954e-9743038c2865	Trailer	Download new trailers	f	Days 1	1970-01-01 00:00:01	/mediakraken/subprogram_metadata_trailer_download.py	{"task": "trailer", "route_key": "Z", "exchange_key": "mkque_metadata_ex"}
e9883c84-5022-4a2b-801a-1e8380ddd86a	Backup	Backup Postgresql DB	f	Days 1	1970-01-01 00:00:01	/mediakraken/subprogram_postgresql_backup.py	{"task": "dbbackup", "route_key": "mkque", "exchange_key": "mkque_ex"}
1493a727-3f89-41ac-857a-baf6b19e501d	DB Vacuum	Postgresql Vacuum Analyze all tables	f	Days 1	1970-01-01 00:00:01	/mediakraken/subprogram_postgresql_vacuum.py	{"task": "dbvacuum", "route_key": "mkque", "exchange_key": "mkque_ex"}
a8754d6e-0d08-4c4a-9596-719ab58e3794	iRadio Scan	Scan for iRadio stations	f	Days 1	1970-01-01 00:00:01	/mediakraken/subprogram_iradio_channels.py	{"task": "iradio", "route_key": "mkque", "exchange_key": "mkque_ex"}
1204080b-c376-4e80-a602-8f57e41b8e43	Media Scan	Scan for new media	f	Days 1	1970-01-01 00:00:01	/mediakraken/subprogram_file_scan.py	{"task": "scan", "route_key": "mkque", "exchange_key": "mkque_ex"}
e77f80cd-f2c9-4cfb-aa72-438181a40217	Sync	Sync/Transcode media	f	Days 1	1970-01-01 00:00:01	/mediakraken/subprogram_sync.py	{"task": "sync", "route_key": "mkque", "exchange_key": "mkque_ex"}
\.


--
-- Data for Name: mm_tv_schedule; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_tv_schedule (mm_tv_schedule_id, mm_tv_schedule_station_id, mm_tv_schedule_date, mm_tv_schedule_json) FROM stdin;
\.


--
-- Data for Name: mm_tv_schedule_program; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_tv_schedule_program (mm_tv_schedule_program_guid, mm_tv_schedule_program_id, mm_tv_schedule_program_json) FROM stdin;
\.


--
-- Data for Name: mm_tv_stations; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_tv_stations (mm_tv_stations_id, mm_tv_station_name, mm_tv_station_id, mm_tv_station_channel, mm_tv_station_json, mm_tv_station_image) FROM stdin;
\.


--
-- Data for Name: mm_user; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_user (id, username, email, password, created_at, active, is_admin, user_json, lang) FROM stdin;
\.


--
-- Data for Name: mm_user_activity; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_user_activity (mm_activity_guid, mm_activity_name, mm_activity_overview, mm_activity_short_overview, mm_activity_type, mm_activity_itemid, mm_activity_userid, mm_activity_datecreated, mm_activity_log_severity) FROM stdin;
\.


--
-- Data for Name: mm_user_group; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_user_group (mm_user_group_guid, mm_user_group_name, mm_user_group_description, mm_user_group_rights_json) FROM stdin;
26fb94ac-7331-40a0-8fee-9c06ec16b295	Administrator	Server administrator	{"Admin": true, "PreviewOnly": false}
4860c10e-a413-4e78-8535-a93bd364e5d5	User	General user	{"Admin": false, "PreviewOnly": false}
db4cb5f8-6bad-4186-a7e7-38f6cd2e9289	Guest	Guest (Preview only)	{"Admin": false, "PreviewOnly": true}
\.


--
-- Data for Name: mm_user_profile; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_user_profile (mm_user_profile_guid, mm_user_profile_name, mm_user_profile_json) FROM stdin;
59c2511c-65a9-4680-b29f-88f3eb913be2	Adult	{"3D": true, "TV": true, "Home": true, "Lang": "en", "Sync": true, "Adult": true, "Books": true, "Games": true, "MaxBR": 100, "Movie": true, "Music": true, "IRadio": true, "Images": true, "LiveTV": true, "Sports": true, "Internet": true, "MaxRating": 5}
785b908a-575c-467e-9135-9258966ac4e3	Teen	{"3D": true, "TV": true, "Home": true, "Lang": "en", "Sync": false, "Adult": false, "Books": true, "Games": true, "MaxBR": 50, "Movie": true, "Music": true, "IRadio": true, "Images": true, "LiveTV": true, "Sports": true, "Internet": true, "MaxRating": 3}
e6b26b0e-0a6e-4eb6-9d9b-ea5094d1efe7	Child	{"3D": false, "TV": true, "Home": true, "Lang": "en", "Sync": false, "Adult": false, "Books": true, "Games": true, "MaxBR": 20, "Movie": true, "Music": true, "IRadio": false, "Images": true, "LiveTV": false, "Sports": true, "Internet": false, "MaxRating": 0}
\.


--
-- Data for Name: mm_version; Type: TABLE DATA; Schema: public; Owner: metamanpg
--

COPY mm_version (mm_version_no) FROM stdin;
15
\.


--
-- Name: mm_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: metamanpg
--

SELECT pg_catalog.setval('mm_user_id_seq', 1, false);


--
-- Name: mm_metadata_game_software_info gi_id_mpk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_metadata_game_software_info
    ADD CONSTRAINT gi_id_mpk PRIMARY KEY (gi_id);


--
-- Name: mm_metadata_game_systems_info gs_id_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_metadata_game_systems_info
    ADD CONSTRAINT gs_id_pk PRIMARY KEY (gs_id);


--
-- Name: mm_download_que mdq_id_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_download_que
    ADD CONSTRAINT mdq_id_pk PRIMARY KEY (mdq_id);


--
-- Name: mm_download_image_que mdq_image_id_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_download_image_que
    ADD CONSTRAINT mdq_image_id_pk PRIMARY KEY (mdq_image_id);


--
-- Name: mm_user_activity mm_activity_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_user_activity
    ADD CONSTRAINT mm_activity_pk PRIMARY KEY (mm_activity_guid);


--
-- Name: mm_channel mm_channel_guid_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_channel
    ADD CONSTRAINT mm_channel_guid_pk PRIMARY KEY (mm_channel_guid);


--
-- Name: mm_cron mm_cron_guid_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_cron
    ADD CONSTRAINT mm_cron_guid_pk PRIMARY KEY (mm_cron_guid);


--
-- Name: mm_device mm_device_id_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_device
    ADD CONSTRAINT mm_device_id_pk PRIMARY KEY (mm_device_id);


--
-- Name: mm_link mm_link_guid_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_link
    ADD CONSTRAINT mm_link_guid_pk PRIMARY KEY (mm_link_guid);


--
-- Name: mm_loan mm_loan_guid_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_loan
    ADD CONSTRAINT mm_loan_guid_pk PRIMARY KEY (mm_loan_guid);


--
-- Name: mm_media_class mm_media_class_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_media_class
    ADD CONSTRAINT mm_media_class_pk PRIMARY KEY (mm_media_class_guid);


--
-- Name: mm_media_dir mm_media_dir_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_media_dir
    ADD CONSTRAINT mm_media_dir_pk PRIMARY KEY (mm_media_dir_guid);


--
-- Name: mm_media mm_media_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_media
    ADD CONSTRAINT mm_media_pk PRIMARY KEY (mm_media_guid);


--
-- Name: mm_media_share mm_media_share_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_media_share
    ADD CONSTRAINT mm_media_share_pk PRIMARY KEY (mm_media_share_guid);


--
-- Name: mm_metadata_album mm_metadata_album_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_metadata_album
    ADD CONSTRAINT mm_metadata_album_pk PRIMARY KEY (mm_metadata_album_guid);


--
-- Name: mm_metadata_anime mm_metadata_anime_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_metadata_anime
    ADD CONSTRAINT mm_metadata_anime_pk PRIMARY KEY (mm_metadata_anime_guid);


--
-- Name: mm_metadata_book mm_metadata_book_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_metadata_book
    ADD CONSTRAINT mm_metadata_book_pk PRIMARY KEY (mm_metadata_book_guid);


--
-- Name: mm_metadata_collection mm_metadata_collection_guid_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_metadata_collection
    ADD CONSTRAINT mm_metadata_collection_guid_pk PRIMARY KEY (mm_metadata_collection_guid);


--
-- Name: mm_metadata_logo mm_metadata_logo_guid_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_metadata_logo
    ADD CONSTRAINT mm_metadata_logo_guid_pk PRIMARY KEY (mm_metadata_logo_guid);


--
-- Name: mm_metadata_music mm_metadata_music_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_metadata_music
    ADD CONSTRAINT mm_metadata_music_pk PRIMARY KEY (mm_metadata_music_guid);


--
-- Name: mm_metadata_music_video mm_metadata_music_video_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_metadata_music_video
    ADD CONSTRAINT mm_metadata_music_video_pk PRIMARY KEY (mm_metadata_music_video_guid);


--
-- Name: mm_metadata_musician mm_metadata_musician_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_metadata_musician
    ADD CONSTRAINT mm_metadata_musician_pk PRIMARY KEY (mm_metadata_musician_guid);


--
-- Name: mm_metadata_movie mm_metadata_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_metadata_movie
    ADD CONSTRAINT mm_metadata_pk PRIMARY KEY (mm_metadata_guid);


--
-- Name: mm_metadata_sports mm_metadata_sports_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_metadata_sports
    ADD CONSTRAINT mm_metadata_sports_pk PRIMARY KEY (mm_metadata_sports_guid);


--
-- Name: mm_metadata_tvshow mm_metadata_tvshow_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_metadata_tvshow
    ADD CONSTRAINT mm_metadata_tvshow_pk PRIMARY KEY (mm_metadata_tvshow_guid);


--
-- Name: mm_notification mm_notification_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_notification
    ADD CONSTRAINT mm_notification_pk PRIMARY KEY (mm_notification_guid);


--
-- Name: mm_options_and_status mm_options_and_status_guid_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_options_and_status
    ADD CONSTRAINT mm_options_and_status_guid_pk PRIMARY KEY (mm_options_and_status_guid);


--
-- Name: mm_radio mm_radio_guid_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_radio
    ADD CONSTRAINT mm_radio_guid_pk PRIMARY KEY (mm_radio_guid);


--
-- Name: mm_review mm_review_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_review
    ADD CONSTRAINT mm_review_pk PRIMARY KEY (mm_review_guid);


--
-- Name: mm_sync mm_sync_guid_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_sync
    ADD CONSTRAINT mm_sync_guid_pk PRIMARY KEY (mm_sync_guid);


--
-- Name: mm_task mm_task_guid_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_task
    ADD CONSTRAINT mm_task_guid_pk PRIMARY KEY (mm_task_guid);


--
-- Name: mm_tv_schedule mm_tv_schedule_id_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_tv_schedule
    ADD CONSTRAINT mm_tv_schedule_id_pk PRIMARY KEY (mm_tv_schedule_id);


--
-- Name: mm_tv_schedule_program mm_tv_schedule_program_guid_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_tv_schedule_program
    ADD CONSTRAINT mm_tv_schedule_program_guid_pk PRIMARY KEY (mm_tv_schedule_program_guid);


--
-- Name: mm_tv_stations mm_tv_stations_id_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_tv_stations
    ADD CONSTRAINT mm_tv_stations_id_pk PRIMARY KEY (mm_tv_stations_id);


--
-- Name: mm_user_group mm_user_group_guid_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_user_group
    ADD CONSTRAINT mm_user_group_guid_pk PRIMARY KEY (mm_user_group_guid);


--
-- Name: mm_user mm_user_pkey; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_user
    ADD CONSTRAINT mm_user_pkey PRIMARY KEY (id);


--
-- Name: mm_user_profile mm_user_profile_guid_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_user_profile
    ADD CONSTRAINT mm_user_profile_guid_pk PRIMARY KEY (mm_user_profile_guid);


--
-- Name: mm_metadata_person mmp_id_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_metadata_person
    ADD CONSTRAINT mmp_id_pk PRIMARY KEY (mmp_id);


--
-- Name: mm_media_remote mmr_media_remote_pk; Type: CONSTRAINT; Schema: public; Owner: metamanpg
--

ALTER TABLE ONLY mm_media_remote
    ADD CONSTRAINT mmr_media_remote_pk PRIMARY KEY (mmr_media_guid);


--
-- Name: gi_game_idx_name; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX gi_game_idx_name ON mm_metadata_game_software_info USING btree (gi_game_info_name);


--
-- Name: gi_game_idx_name_trigram_idx; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX gi_game_idx_name_trigram_idx ON mm_metadata_game_software_info USING gist (gi_game_info_name gist_trgm_ops);


--
-- Name: gi_system_id_ndx; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX gi_system_id_ndx ON mm_metadata_game_software_info USING btree (gi_system_id);


--
-- Name: mdq_que_type_idx_name; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mdq_que_type_idx_name ON mm_download_que USING btree (mdq_que_type);


--
-- Name: mm_channel_idx_country; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_channel_idx_country ON mm_channel USING btree (mm_channel_country_guid);


--
-- Name: mm_channel_idx_logo; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_channel_idx_logo ON mm_channel USING btree (mm_channel_logo_guid);


--
-- Name: mm_channel_idx_name; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_channel_idx_name ON mm_channel USING btree (mm_channel_name);


--
-- Name: mm_channel_idxgin_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_channel_idxgin_json ON mm_channel USING gin (mm_channel_media_id);


--
-- Name: mm_device_idx_type; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_device_idx_type ON mm_device USING btree (mm_device_type);


--
-- Name: mm_device_idxgin_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_device_idxgin_json ON mm_device USING gin (mm_device_json);


--
-- Name: mm_download_idx_provider; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_download_idx_provider ON mm_download_que USING btree (mdq_provider);


--
-- Name: mm_download_que_idxgin_meta_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_download_que_idxgin_meta_json ON mm_download_que USING gin (mdq_download_json);


--
-- Name: mm_game_info_idxgin_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_game_info_idxgin_json ON mm_metadata_game_software_info USING gin (gi_game_info_json);


--
-- Name: mm_game_info_idxgin_name; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_game_info_idxgin_name ON mm_metadata_game_software_info USING gin (((gi_game_info_json -> '@name'::text)));


--
-- Name: mm_game_systems_idxgin_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_game_systems_idxgin_json ON mm_metadata_game_systems_info USING gin (gs_game_system_json);


--
-- Name: mm_image_download_idx_provider; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_image_download_idx_provider ON mm_download_image_que USING btree (mdq_image_provider);


--
-- Name: mm_link_idx_name; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_link_idx_name ON mm_link USING btree (mm_link_name);


--
-- Name: mm_link_json_idxgin; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_link_json_idxgin ON mm_link USING gin (mm_link_json);


--
-- Name: mm_media_anime_name_trigram_idx; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_media_anime_name_trigram_idx ON mm_metadata_anime USING gist (mm_media_anime_name gist_trgm_ops);


--
-- Name: mm_media_class_idx_type; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_media_class_idx_type ON mm_media_class USING btree (mm_media_class_type);


--
-- Name: mm_media_dir_idx_share; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_media_dir_idx_share ON mm_media_dir USING btree (mm_media_dir_share_guid);


--
-- Name: mm_media_idx_metadata_uuid; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_media_idx_metadata_uuid ON mm_media USING btree (mm_media_metadata_guid);


--
-- Name: mm_media_idx_path; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_media_idx_path ON mm_media USING btree (mm_media_path);


--
-- Name: mm_media_idxgin_ffprobe; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_media_idxgin_ffprobe ON mm_media USING gin (mm_media_ffprobe_json);


--
-- Name: mm_media_music_video_band_trigram_idx; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_media_music_video_band_trigram_idx ON mm_metadata_music_video USING gist (mm_media_music_video_band gist_trgm_ops);


--
-- Name: mm_media_music_video_song_trigram_idx; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_media_music_video_song_trigram_idx ON mm_metadata_music_video USING gist (mm_media_music_video_song gist_trgm_ops);


--
-- Name: mm_media_name_trigram_idx; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_media_name_trigram_idx ON mm_metadata_movie USING gist (mm_media_name gist_trgm_ops);


--
-- Name: mm_metadata_album_idx_musician; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_album_idx_musician ON mm_metadata_album USING btree (mm_metadata_album_musician_guid);


--
-- Name: mm_metadata_album_idx_name; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_album_idx_name ON mm_metadata_album USING btree (mm_metadata_album_name);


--
-- Name: mm_metadata_album_idx_name_lower; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_album_idx_name_lower ON mm_metadata_album USING btree (lower(mm_metadata_album_name));


--
-- Name: mm_metadata_album_idxgin_id_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_album_idxgin_id_json ON mm_metadata_album USING gin (mm_metadata_album_id);


--
-- Name: mm_metadata_album_idxgin_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_album_idxgin_json ON mm_metadata_album USING gin (mm_metadata_album_json);


--
-- Name: mm_metadata_album_name_trigram_idx; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_album_name_trigram_idx ON mm_metadata_album USING gist (mm_metadata_album_name gist_trgm_ops);


--
-- Name: mm_metadata_aniem_idxgin_media_id; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_aniem_idxgin_media_id ON mm_metadata_anime USING gin (mm_metadata_anime_media_id);


--
-- Name: mm_metadata_anime_idx_name; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_anime_idx_name ON mm_metadata_anime USING btree (mm_media_anime_name);


--
-- Name: mm_metadata_anime_idx_name_lower; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_anime_idx_name_lower ON mm_metadata_anime USING btree (lower(mm_media_anime_name));


--
-- Name: mm_metadata_anime_idxgin_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_anime_idxgin_json ON mm_metadata_anime USING gin (mm_metadata_anime_json);


--
-- Name: mm_metadata_anime_idxgin_media_id_anidb; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_anime_idxgin_media_id_anidb ON mm_metadata_anime USING gin (((mm_metadata_anime_media_id -> 'anidb'::text)));


--
-- Name: mm_metadata_anime_idxgin_media_id_imdb; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_anime_idxgin_media_id_imdb ON mm_metadata_anime USING gin (((mm_metadata_anime_media_id -> 'imdb'::text)));


--
-- Name: mm_metadata_anime_idxgin_media_id_thetvdb; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_anime_idxgin_media_id_thetvdb ON mm_metadata_anime USING gin (((mm_metadata_anime_media_id -> 'thetvdb'::text)));


--
-- Name: mm_metadata_anime_idxgin_media_id_tmdb; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_anime_idxgin_media_id_tmdb ON mm_metadata_anime USING gin (((mm_metadata_anime_media_id -> 'tmdb'::text)));


--
-- Name: mm_metadata_anime_idxgin_user_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_anime_idxgin_user_json ON mm_metadata_anime USING gin (mm_metadata_anime_user_json);


--
-- Name: mm_metadata_book_name_trigram_idx; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_book_name_trigram_idx ON mm_metadata_book USING gist (mm_metadata_book_name gist_trgm_ops);


--
-- Name: mm_metadata_collection_idxgin_media_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_collection_idxgin_media_json ON mm_metadata_collection USING gin (mm_metadata_collection_media_ids);


--
-- Name: mm_metadata_collection_idxgin_meta_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_collection_idxgin_meta_json ON mm_metadata_collection USING gin (mm_metadata_collection_json);


--
-- Name: mm_metadata_collection_idxgin_name_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_collection_idxgin_name_json ON mm_metadata_collection USING gin (mm_metadata_collection_name);


--
-- Name: mm_metadata_idx_band_name; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_idx_band_name ON mm_metadata_music_video USING btree (mm_media_music_video_band);


--
-- Name: mm_metadata_idx_band_name_lower; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_idx_band_name_lower ON mm_metadata_music_video USING btree (lower(mm_media_music_video_band));


--
-- Name: mm_metadata_idx_book_name; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_idx_book_name ON mm_metadata_book USING btree (mm_metadata_book_name);


--
-- Name: mm_metadata_idx_book_name_lower; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_idx_book_name_lower ON mm_metadata_book USING btree (lower(mm_metadata_book_name));


--
-- Name: mm_metadata_idx_name; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_idx_name ON mm_metadata_movie USING btree (mm_media_name);


--
-- Name: mm_metadata_idx_name_lower; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_idx_name_lower ON mm_metadata_movie USING btree (lower(mm_media_name));


--
-- Name: mm_metadata_idx_song_name; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_idx_song_name ON mm_metadata_music_video USING btree (mm_media_music_video_song);


--
-- Name: mm_metadata_idx_song_name_lower; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_idx_song_name_lower ON mm_metadata_music_video USING btree (lower(mm_media_music_video_song));


--
-- Name: mm_metadata_idxgin_isbn; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_idxgin_isbn ON mm_metadata_book USING btree (mm_metadata_book_isbn);


--
-- Name: mm_metadata_idxgin_isbn13; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_idxgin_isbn13 ON mm_metadata_book USING btree (mm_metadata_book_isbn13);


--
-- Name: mm_metadata_idxgin_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_idxgin_json ON mm_metadata_movie USING gin (mm_metadata_json);


--
-- Name: mm_metadata_idxgin_media_id; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_idxgin_media_id ON mm_metadata_movie USING gin (mm_metadata_media_id);


--
-- Name: mm_metadata_idxgin_media_id_imdb; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_idxgin_media_id_imdb ON mm_metadata_movie USING gin (((mm_metadata_media_id -> 'imdb'::text)));


--
-- Name: mm_metadata_idxgin_media_id_thetvdb; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_idxgin_media_id_thetvdb ON mm_metadata_movie USING gin (((mm_metadata_media_id -> 'thetvdb'::text)));


--
-- Name: mm_metadata_idxgin_media_id_tmdb; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_idxgin_media_id_tmdb ON mm_metadata_movie USING gin (((mm_metadata_media_id -> 'tmdb'::text)));


--
-- Name: mm_metadata_idxgin_music_video_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_idxgin_music_video_json ON mm_metadata_music_video USING gin (mm_metadata_music_video_json);


--
-- Name: mm_metadata_idxgin_music_video_media_id; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_idxgin_music_video_media_id ON mm_metadata_music_video USING gin (mm_metadata_music_video_media_id);


--
-- Name: mm_metadata_idxgin_music_video_media_id_imvdb; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_idxgin_music_video_media_id_imvdb ON mm_metadata_music_video USING gin (((mm_metadata_music_video_media_id -> 'imvdb'::text)));


--
-- Name: mm_metadata_idxgin_user_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_idxgin_user_json ON mm_metadata_movie USING gin (mm_metadata_user_json);


--
-- Name: mm_metadata_logo_idxgin_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_logo_idxgin_json ON mm_metadata_logo USING gin (mm_metadata_logo_media_guid);


--
-- Name: mm_metadata_music_idx_album; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_music_idx_album ON mm_metadata_music USING btree (mm_metadata_music_album_guid);


--
-- Name: mm_metadata_music_idx_name; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_music_idx_name ON mm_metadata_music USING btree (mm_metadata_music_name);


--
-- Name: mm_metadata_music_idx_name_lower; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_music_idx_name_lower ON mm_metadata_music USING btree (lower(mm_metadata_music_name));


--
-- Name: mm_metadata_music_idxgin_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_music_idxgin_json ON mm_metadata_music USING gin (mm_metadata_music_json);


--
-- Name: mm_metadata_music_idxgin_media_id; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_music_idxgin_media_id ON mm_metadata_music USING gin (mm_metadata_media_music_id);


--
-- Name: mm_metadata_music_name_trigram_idx; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_music_name_trigram_idx ON mm_metadata_music USING gist (mm_metadata_music_name gist_trgm_ops);


--
-- Name: mm_metadata_musician_idx_name; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_musician_idx_name ON mm_metadata_musician USING btree (mm_metadata_musician_name);


--
-- Name: mm_metadata_musician_idx_name_lower; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_musician_idx_name_lower ON mm_metadata_musician USING btree (lower(mm_metadata_musician_name));


--
-- Name: mm_metadata_musician_idxgin_id_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_musician_idxgin_id_json ON mm_metadata_musician USING gin (mm_metadata_musician_id);


--
-- Name: mm_metadata_musician_idxgin_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_musician_idxgin_json ON mm_metadata_musician USING gin (mm_metadata_musician_json);


--
-- Name: mm_metadata_musician_name_trigram_idx; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_musician_name_trigram_idx ON mm_metadata_musician USING gist (mm_metadata_musician_name gist_trgm_ops);


--
-- Name: mm_metadata_person_idx_name; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_person_idx_name ON mm_metadata_person USING btree (mmp_person_name);


--
-- Name: mm_metadata_person_idxgin_id_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_person_idxgin_id_json ON mm_metadata_person USING gin (mmp_person_media_id);


--
-- Name: mm_metadata_person_idxgin_meta_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_person_idxgin_meta_json ON mm_metadata_person USING gin (mmp_person_meta_json);


--
-- Name: mm_metadata_review_idx_metadata_uuid; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_review_idx_metadata_uuid ON mm_review USING btree (mm_review_metadata_guid);


--
-- Name: mm_metadata_review_idxgin_media_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_review_idxgin_media_json ON mm_review USING gin (mm_review_metadata_id);


--
-- Name: mm_metadata_sports_idx_name; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_sports_idx_name ON mm_metadata_sports USING btree (mm_metadata_sports_name);


--
-- Name: mm_metadata_sports_idx_name_lower; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_sports_idx_name_lower ON mm_metadata_sports USING btree (lower(mm_metadata_sports_name));


--
-- Name: mm_metadata_sports_idxgin_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_sports_idxgin_json ON mm_metadata_sports USING gin (mm_metadata_sports_json);


--
-- Name: mm_metadata_sports_idxgin_media_id; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_sports_idxgin_media_id ON mm_metadata_sports USING gin (mm_metadata_media_sports_id);


--
-- Name: mm_metadata_sports_idxgin_media_id_imdb; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_sports_idxgin_media_id_imdb ON mm_metadata_sports USING gin (((mm_metadata_media_sports_id -> 'imdb'::text)));


--
-- Name: mm_metadata_sports_idxgin_media_id_thesportsdb; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_sports_idxgin_media_id_thesportsdb ON mm_metadata_sports USING gin (((mm_metadata_media_sports_id -> 'thesportsdb'::text)));


--
-- Name: mm_metadata_sports_idxgin_media_id_thetvdb; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_sports_idxgin_media_id_thetvdb ON mm_metadata_sports USING gin (((mm_metadata_media_sports_id -> 'thetvdb'::text)));


--
-- Name: mm_metadata_sports_idxgin_media_id_thetvdbseries; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_sports_idxgin_media_id_thetvdbseries ON mm_metadata_sports USING gin (((mm_metadata_media_sports_id -> 'thetvdbSeries'::text)));


--
-- Name: mm_metadata_sports_idxgin_media_id_tmdb; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_sports_idxgin_media_id_tmdb ON mm_metadata_sports USING gin (((mm_metadata_media_sports_id -> 'tmdb'::text)));


--
-- Name: mm_metadata_sports_idxgin_media_id_tvmaze; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_sports_idxgin_media_id_tvmaze ON mm_metadata_sports USING gin (((mm_metadata_media_sports_id -> 'tvmaze'::text)));


--
-- Name: mm_metadata_sports_name_trigram_idx; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_sports_name_trigram_idx ON mm_metadata_sports USING gist (mm_metadata_sports_name gist_trgm_ops);


--
-- Name: mm_metadata_tvshow_idx_name; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_tvshow_idx_name ON mm_metadata_tvshow USING btree (mm_metadata_tvshow_name);


--
-- Name: mm_metadata_tvshow_idx_name_lower; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_tvshow_idx_name_lower ON mm_metadata_tvshow USING btree (lower(mm_metadata_tvshow_name));


--
-- Name: mm_metadata_tvshow_idxgin_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_tvshow_idxgin_json ON mm_metadata_tvshow USING gin (mm_metadata_tvshow_json);


--
-- Name: mm_metadata_tvshow_idxgin_localimage_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_tvshow_idxgin_localimage_json ON mm_metadata_tvshow USING gin (mm_metadata_tvshow_json);


--
-- Name: mm_metadata_tvshow_idxgin_media_id; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_tvshow_idxgin_media_id ON mm_metadata_tvshow USING gin (mm_metadata_media_tvshow_id);


--
-- Name: mm_metadata_tvshow_idxgin_media_id_imdb; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_tvshow_idxgin_media_id_imdb ON mm_metadata_tvshow USING gin (((mm_metadata_media_tvshow_id -> 'imdb'::text)));


--
-- Name: mm_metadata_tvshow_idxgin_media_id_thetvdb; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_tvshow_idxgin_media_id_thetvdb ON mm_metadata_tvshow USING gin (((mm_metadata_media_tvshow_id -> 'thetvdb'::text)));


--
-- Name: mm_metadata_tvshow_idxgin_media_id_thetvdbseries; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_tvshow_idxgin_media_id_thetvdbseries ON mm_metadata_tvshow USING gin (((mm_metadata_media_tvshow_id -> 'thetvdbSeries'::text)));


--
-- Name: mm_metadata_tvshow_idxgin_media_id_tmdb; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_tvshow_idxgin_media_id_tmdb ON mm_metadata_tvshow USING gin (((mm_metadata_media_tvshow_id -> 'tmdb'::text)));


--
-- Name: mm_metadata_tvshow_idxgin_media_id_tvmaze; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_tvshow_idxgin_media_id_tvmaze ON mm_metadata_tvshow USING gin (((mm_metadata_media_tvshow_id -> 'tvmaze'::text)));


--
-- Name: mm_metadata_tvshow_idxgin_user_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_tvshow_idxgin_user_json ON mm_metadata_tvshow USING gin (mm_metadata_tvshow_user_json);


--
-- Name: mm_metadata_tvshow_name_trigram_idx; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_metadata_tvshow_name_trigram_idx ON mm_metadata_tvshow USING gist (mm_metadata_tvshow_name gist_trgm_ops);


--
-- Name: mm_notification_idx_dismissable; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_notification_idx_dismissable ON mm_notification USING btree (mm_notification_dismissable);


--
-- Name: mm_notification_idx_time; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_notification_idx_time ON mm_notification USING btree (mm_notification_time);


--
-- Name: mm_sync_idxgin_json; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_sync_idxgin_json ON mm_sync USING gin (mm_sync_options_json);


--
-- Name: mm_tv_schedule_idx_date; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_tv_schedule_idx_date ON mm_tv_schedule USING btree (mm_tv_schedule_date);


--
-- Name: mm_tv_schedule_idx_program; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_tv_schedule_idx_program ON mm_tv_schedule_program USING btree (mm_tv_schedule_program_id);


--
-- Name: mm_tv_schedule_idx_station; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_tv_schedule_idx_station ON mm_tv_schedule USING btree (mm_tv_schedule_station_id);


--
-- Name: mm_tv_stations_idx_name; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_tv_stations_idx_name ON mm_tv_stations USING btree (mm_tv_station_name);


--
-- Name: mm_tv_stations_idx_station; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_tv_stations_idx_station ON mm_tv_stations USING btree (mm_tv_station_id);


--
-- Name: mm_user_activity_idx_date; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_user_activity_idx_date ON mm_user_activity USING btree (mm_activity_datecreated);


--
-- Name: mm_user_activity_idx_user_guid; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_user_activity_idx_user_guid ON mm_user_activity USING btree (mm_activity_userid);


--
-- Name: mm_user_group_idx_name; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_user_group_idx_name ON mm_user_group USING btree (mm_user_group_name);


--
-- Name: mm_user_idx_username; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_user_idx_username ON mm_user USING btree (username);


--
-- Name: mm_user_profile_idx_name; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mm_user_profile_idx_name ON mm_user_profile USING btree (mm_user_profile_name);


--
-- Name: mmp_person_name_trigram_idx; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mmp_person_name_trigram_idx ON mm_metadata_person USING gist (mmp_person_name gist_trgm_ops);


--
-- Name: mmr_media_idx_link_uuid; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mmr_media_idx_link_uuid ON mm_media_remote USING btree (mmr_media_link_id);


--
-- Name: mmr_media_idx_metadata_uuid; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mmr_media_idx_metadata_uuid ON mm_media_remote USING btree (mmr_media_metadata_guid);


--
-- Name: mmr_media_idxgin_ffprobe; Type: INDEX; Schema: public; Owner: metamanpg
--

CREATE INDEX mmr_media_idxgin_ffprobe ON mm_media_remote USING gin (mmr_media_ffprobe_json);


--
-- PostgreSQL database dump complete
--

