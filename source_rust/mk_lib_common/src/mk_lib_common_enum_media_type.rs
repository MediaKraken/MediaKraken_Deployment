#[non_exhaustive]
pub struct DLMediaType;

impl DLMediaType {
    pub const MOVIE: i16 = 1;
    pub const TV: i16 = 2;
    pub const PERSON: i16 = 3;

    pub const SPORTS: i16 = 4;
    pub const GAME: i16 = 5;
    pub const PUBLICATION: i16 = 6;
    pub const PICTURE: i16 = 7;
    pub const ANIME: i16 = 8;
    pub const MUSIC: i16 = 9;
    pub const ADULT: i16 = 10;

    pub const ADULT_IMAGE: i16 = 1000;
    pub const ADULT_MOVIE: i16 = 1001;
    pub const ADULT_SCENE: i16 = 1002;

    pub const GAME_CHD: i16 = 501;
    pub const GAME_CINEMATICS: i16 = 502;
    pub const GAME_INTRO: i16 = 503;
    pub const GAME_ISO: i16 = 504;
    pub const GAME_ROM: i16 = 505;
    pub const GAME_SPEEDRUN: i16 = 506;
    pub const GAME_SUPERPLAY: i16 = 507;

    pub const MOVIE_HOME: i16 = 111;
    pub const MOVIE_EXTRAS: i16 = 112;
    pub const MOVIE_SOUNDTRACK: i16 = 113;
    pub const MOVIE_SUBTITLE: i16 = 114;
    pub const MOVIE_THEME: i16 = 115;
    pub const MOVIE_TRAILER: i16 = 116;

    pub const MUSIC_ALBUM: i16 = 901;
    pub const MUSIC_LYRICS: i16 = 902;
    pub const MUSIC_SONG: i16 = 903;
    pub const MUSIC_VIDEO: i16 = 904;

    pub const PUBLICATION_BOOK: i16 = 601;
    pub const PUBLICATION_COMIC: i16 = 602;
    pub const PUBLICATION_COMIC_STRIP: i16 = 603;
    pub const PUBLICATION_MAGAZINE: i16 = 604;
    pub const PUBLICATION_GRAPHIC_NOVEL: i16 = 605;

    pub const TV_EPISODE: i16 = 201;
    pub const TV_EXTRAS: i16 = 202;
    pub const TV_SEASON: i16 = 203;
    pub const TV_SUBTITLE: i16 = 204;
    pub const TV_THEME: i16 = 205;
    pub const TV_TRAILER: i16 = 206;
}