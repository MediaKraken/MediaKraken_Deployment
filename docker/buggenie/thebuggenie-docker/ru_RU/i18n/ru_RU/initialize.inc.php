<?php

    \thebuggenie\core\framework\Context::getI18n()->setCharset('utf-8');
    setlocale(LC_ALL, array('ru_RU', 'ru'));
    // see \thebuggenie\core\entities\i18n::getDateTimeFormat for the list of all available formats
    \thebuggenie\core\framework\Context::getI18n()->setDateTimeFormats( array( 1 => '%d.%m.%Y (%H:%M)'
                                                                                                    , 2 => '%d.%m.%Y (%H:%M)'
                                                                                                    , 3 => '%d.%m (%H:%M)'
                                                                                                    , 4 => '%d.%m (%H:%M)'
                                                                                                    , 5 => '%d.%m.%Y'
                                                                                                    , 6 => '%d.%m.%Y (%H:%M)'
                                                                                                    , 7 => '%d.%m.%Y (%H:%M)'
                                                                                                    , 8 => '%d.%m.%Y (%H:%M)'
                                                                                                    , 9 => '%d.%m.%Y (%H:%M)'
                                                                                                    , 10 => '%d.%m.%Y (%H:%M)'
                                                                                                    , 11 => '%m'
                                                                                                    , 12 => '%d.%m'
                                                                                                    , 13 => '%w'
                                                                                                    , 14 => '%H:%M'
                                                                                                    , 15 => '%d.%m.%Y (%H:%M)'
                                                                                                    , 16 => '%m.%Y'
                                                                                                    , 17 => '%d.%m.%Y %H:%M:%S GMT' ));

