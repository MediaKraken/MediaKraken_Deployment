/********************************************************************************
** Form generated from reading UI file 'mainwindow.ui'
**
** Created by: Qt User Interface Compiler version 5.9.1
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_MAINWINDOW_H
#define UI_MAINWINDOW_H

#include <QtCore/QVariant>
#include <QtWidgets/QAction>
#include <QtWidgets/QApplication>
#include <QtWidgets/QButtonGroup>
#include <QtWidgets/QFormLayout>
#include <QtWidgets/QFrame>
#include <QtWidgets/QGridLayout>
#include <QtWidgets/QHBoxLayout>
#include <QtWidgets/QHeaderView>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QOpenGLWidget>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QVBoxLayout>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_MainWindow
{
public:
    QWidget *centralWidget;
    QGridLayout *gridLayout;
    QFrame *frame_3;
    QHBoxLayout *horizontalLayout;
    QPushButton *main_button_music;
    QPushButton *main_button_movie;
    QPushButton *main_button_tv;
    QPushButton *main_button_tv_live;
    QPushButton *main_button_home_movie;
    QFrame *frame_2;
    QVBoxLayout *verticalLayout_2;
    QPushButton *main_button_images;
    QPushButton *main_button_radio;
    QPushButton *main_button_books;
    QPushButton *main_button_settings;
    QFrame *frame;
    QVBoxLayout *verticalLayout;
    QPushButton *main_button_inprogress;
    QPushButton *main_button_new;
    QPushButton *main_button_games;
    QPushButton *main_button_music_video;
    QFrame *frame_4;
    QFormLayout *formLayout;
    QOpenGLWidget *openGLWidget;

    void setupUi(QMainWindow *MainWindow)
    {
        if (MainWindow->objectName().isEmpty())
            MainWindow->setObjectName(QStringLiteral("MainWindow"));
        MainWindow->resize(765, 612);
        centralWidget = new QWidget(MainWindow);
        centralWidget->setObjectName(QStringLiteral("centralWidget"));
        gridLayout = new QGridLayout(centralWidget);
        gridLayout->setSpacing(6);
        gridLayout->setContentsMargins(11, 11, 11, 11);
        gridLayout->setObjectName(QStringLiteral("gridLayout"));
        frame_3 = new QFrame(centralWidget);
        frame_3->setObjectName(QStringLiteral("frame_3"));
        QSizePolicy sizePolicy(QSizePolicy::Preferred, QSizePolicy::Preferred);
        sizePolicy.setHorizontalStretch(1);
        sizePolicy.setVerticalStretch(1);
        sizePolicy.setHeightForWidth(frame_3->sizePolicy().hasHeightForWidth());
        frame_3->setSizePolicy(sizePolicy);
        frame_3->setFrameShape(QFrame::StyledPanel);
        frame_3->setFrameShadow(QFrame::Raised);
        horizontalLayout = new QHBoxLayout(frame_3);
        horizontalLayout->setSpacing(6);
        horizontalLayout->setContentsMargins(11, 11, 11, 11);
        horizontalLayout->setObjectName(QStringLiteral("horizontalLayout"));
        main_button_music = new QPushButton(frame_3);
        main_button_music->setObjectName(QStringLiteral("main_button_music"));
        QSizePolicy sizePolicy1(QSizePolicy::Preferred, QSizePolicy::Preferred);
        sizePolicy1.setHorizontalStretch(0);
        sizePolicy1.setVerticalStretch(0);
        sizePolicy1.setHeightForWidth(main_button_music->sizePolicy().hasHeightForWidth());
        main_button_music->setSizePolicy(sizePolicy1);
        QIcon icon;
        icon.addFile(QStringLiteral("../images/headphone.png"), QSize(), QIcon::Normal, QIcon::Off);
        main_button_music->setIcon(icon);

        horizontalLayout->addWidget(main_button_music);

        main_button_movie = new QPushButton(frame_3);
        main_button_movie->setObjectName(QStringLiteral("main_button_movie"));
        sizePolicy1.setHeightForWidth(main_button_movie->sizePolicy().hasHeightForWidth());
        main_button_movie->setSizePolicy(sizePolicy1);
        QIcon icon1;
        icon1.addFile(QStringLiteral("../images/movie_ticket.png"), QSize(), QIcon::Normal, QIcon::Off);
        main_button_movie->setIcon(icon1);

        horizontalLayout->addWidget(main_button_movie);

        main_button_tv = new QPushButton(frame_3);
        main_button_tv->setObjectName(QStringLiteral("main_button_tv"));
        sizePolicy1.setHeightForWidth(main_button_tv->sizePolicy().hasHeightForWidth());
        main_button_tv->setSizePolicy(sizePolicy1);
        QIcon icon2;
        icon2.addFile(QStringLiteral("../images/television.png"), QSize(), QIcon::Normal, QIcon::Off);
        main_button_tv->setIcon(icon2);

        horizontalLayout->addWidget(main_button_tv);

        main_button_tv_live = new QPushButton(frame_3);
        main_button_tv_live->setObjectName(QStringLiteral("main_button_tv_live"));
        sizePolicy1.setHeightForWidth(main_button_tv_live->sizePolicy().hasHeightForWidth());
        main_button_tv_live->setSizePolicy(sizePolicy1);
        QIcon icon3;
        icon3.addFile(QStringLiteral("../images/television_live.png"), QSize(), QIcon::Normal, QIcon::Off);
        main_button_tv_live->setIcon(icon3);

        horizontalLayout->addWidget(main_button_tv_live);

        main_button_home_movie = new QPushButton(frame_3);
        main_button_home_movie->setObjectName(QStringLiteral("main_button_home_movie"));
        sizePolicy1.setHeightForWidth(main_button_home_movie->sizePolicy().hasHeightForWidth());
        main_button_home_movie->setSizePolicy(sizePolicy1);
        QIcon icon4;
        icon4.addFile(QStringLiteral("../images/vid_camera.png"), QSize(), QIcon::Normal, QIcon::Off);
        main_button_home_movie->setIcon(icon4);

        horizontalLayout->addWidget(main_button_home_movie);


        gridLayout->addWidget(frame_3, 1, 1, 1, 3);

        frame_2 = new QFrame(centralWidget);
        frame_2->setObjectName(QStringLiteral("frame_2"));
        QSizePolicy sizePolicy2(QSizePolicy::Preferred, QSizePolicy::Preferred);
        sizePolicy2.setHorizontalStretch(0);
        sizePolicy2.setVerticalStretch(4);
        sizePolicy2.setHeightForWidth(frame_2->sizePolicy().hasHeightForWidth());
        frame_2->setSizePolicy(sizePolicy2);
        frame_2->setFrameShape(QFrame::StyledPanel);
        frame_2->setFrameShadow(QFrame::Raised);
        verticalLayout_2 = new QVBoxLayout(frame_2);
        verticalLayout_2->setSpacing(6);
        verticalLayout_2->setContentsMargins(11, 11, 11, 11);
        verticalLayout_2->setObjectName(QStringLiteral("verticalLayout_2"));
        main_button_images = new QPushButton(frame_2);
        main_button_images->setObjectName(QStringLiteral("main_button_images"));
        sizePolicy1.setHeightForWidth(main_button_images->sizePolicy().hasHeightForWidth());
        main_button_images->setSizePolicy(sizePolicy1);
        QIcon icon5;
        icon5.addFile(QStringLiteral("../images/photo.png"), QSize(), QIcon::Normal, QIcon::Off);
        main_button_images->setIcon(icon5);

        verticalLayout_2->addWidget(main_button_images);

        main_button_radio = new QPushButton(frame_2);
        main_button_radio->setObjectName(QStringLiteral("main_button_radio"));
        sizePolicy1.setHeightForWidth(main_button_radio->sizePolicy().hasHeightForWidth());
        main_button_radio->setSizePolicy(sizePolicy1);
        QIcon icon6;
        icon6.addFile(QStringLiteral("../images/radio.png"), QSize(), QIcon::Normal, QIcon::Off);
        main_button_radio->setIcon(icon6);

        verticalLayout_2->addWidget(main_button_radio);

        main_button_books = new QPushButton(frame_2);
        main_button_books->setObjectName(QStringLiteral("main_button_books"));
        sizePolicy1.setHeightForWidth(main_button_books->sizePolicy().hasHeightForWidth());
        main_button_books->setSizePolicy(sizePolicy1);
        QIcon icon7;
        icon7.addFile(QStringLiteral("../images/books.png"), QSize(), QIcon::Normal, QIcon::Off);
        main_button_books->setIcon(icon7);

        verticalLayout_2->addWidget(main_button_books);

        main_button_settings = new QPushButton(frame_2);
        main_button_settings->setObjectName(QStringLiteral("main_button_settings"));
        sizePolicy1.setHeightForWidth(main_button_settings->sizePolicy().hasHeightForWidth());
        main_button_settings->setSizePolicy(sizePolicy1);
        QIcon icon8;
        icon8.addFile(QStringLiteral("../images/settings.png"), QSize(), QIcon::Normal, QIcon::Off);
        main_button_settings->setIcon(icon8);

        verticalLayout_2->addWidget(main_button_settings);


        gridLayout->addWidget(frame_2, 0, 3, 1, 1);

        frame = new QFrame(centralWidget);
        frame->setObjectName(QStringLiteral("frame"));
        QSizePolicy sizePolicy3(QSizePolicy::Preferred, QSizePolicy::Preferred);
        sizePolicy3.setHorizontalStretch(1);
        sizePolicy3.setVerticalStretch(4);
        sizePolicy3.setHeightForWidth(frame->sizePolicy().hasHeightForWidth());
        frame->setSizePolicy(sizePolicy3);
        frame->setFrameShape(QFrame::StyledPanel);
        frame->setFrameShadow(QFrame::Raised);
        verticalLayout = new QVBoxLayout(frame);
        verticalLayout->setSpacing(6);
        verticalLayout->setContentsMargins(11, 11, 11, 11);
        verticalLayout->setObjectName(QStringLiteral("verticalLayout"));
        main_button_inprogress = new QPushButton(frame);
        main_button_inprogress->setObjectName(QStringLiteral("main_button_inprogress"));
        sizePolicy1.setHeightForWidth(main_button_inprogress->sizePolicy().hasHeightForWidth());
        main_button_inprogress->setSizePolicy(sizePolicy1);
        QIcon icon9;
        icon9.addFile(QStringLiteral("../images/progress.png"), QSize(), QIcon::Normal, QIcon::Off);
        main_button_inprogress->setIcon(icon9);

        verticalLayout->addWidget(main_button_inprogress);

        main_button_new = new QPushButton(frame);
        main_button_new->setObjectName(QStringLiteral("main_button_new"));
        sizePolicy1.setHeightForWidth(main_button_new->sizePolicy().hasHeightForWidth());
        main_button_new->setSizePolicy(sizePolicy1);
        QIcon icon10;
        icon10.addFile(QStringLiteral("../images/new.png"), QSize(), QIcon::Normal, QIcon::Off);
        main_button_new->setIcon(icon10);

        verticalLayout->addWidget(main_button_new);

        main_button_games = new QPushButton(frame);
        main_button_games->setObjectName(QStringLiteral("main_button_games"));
        sizePolicy1.setHeightForWidth(main_button_games->sizePolicy().hasHeightForWidth());
        main_button_games->setSizePolicy(sizePolicy1);
        QIcon icon11;
        icon11.addFile(QStringLiteral("../images/vid_game.png"), QSize(), QIcon::Normal, QIcon::Off);
        main_button_games->setIcon(icon11);

        verticalLayout->addWidget(main_button_games);

        main_button_music_video = new QPushButton(frame);
        main_button_music_video->setObjectName(QStringLiteral("main_button_music_video"));
        sizePolicy1.setHeightForWidth(main_button_music_video->sizePolicy().hasHeightForWidth());
        main_button_music_video->setSizePolicy(sizePolicy1);
        QIcon icon12;
        icon12.addFile(QStringLiteral("../images/music_vid.png"), QSize(), QIcon::Normal, QIcon::Off);
        main_button_music_video->setIcon(icon12);

        verticalLayout->addWidget(main_button_music_video);


        gridLayout->addWidget(frame, 0, 1, 1, 1);

        frame_4 = new QFrame(centralWidget);
        frame_4->setObjectName(QStringLiteral("frame_4"));
        QSizePolicy sizePolicy4(QSizePolicy::Preferred, QSizePolicy::Preferred);
        sizePolicy4.setHorizontalStretch(4);
        sizePolicy4.setVerticalStretch(4);
        sizePolicy4.setHeightForWidth(frame_4->sizePolicy().hasHeightForWidth());
        frame_4->setSizePolicy(sizePolicy4);
        frame_4->setFrameShape(QFrame::StyledPanel);
        frame_4->setFrameShadow(QFrame::Raised);
        formLayout = new QFormLayout(frame_4);
        formLayout->setSpacing(6);
        formLayout->setContentsMargins(11, 11, 11, 11);
        formLayout->setObjectName(QStringLiteral("formLayout"));
        openGLWidget = new QOpenGLWidget(frame_4);
        openGLWidget->setObjectName(QStringLiteral("openGLWidget"));

        formLayout->setWidget(0, QFormLayout::LabelRole, openGLWidget);


        gridLayout->addWidget(frame_4, 0, 2, 1, 1);

        MainWindow->setCentralWidget(centralWidget);

        retranslateUi(MainWindow);

        QMetaObject::connectSlotsByName(MainWindow);
    } // setupUi

    void retranslateUi(QMainWindow *MainWindow)
    {
        MainWindow->setWindowTitle(QApplication::translate("MainWindow", "MediaKraken", Q_NULLPTR));
        main_button_music->setText(QString());
        main_button_movie->setText(QString());
        main_button_tv->setText(QString());
        main_button_tv_live->setText(QString());
        main_button_home_movie->setText(QString());
        main_button_images->setText(QString());
        main_button_radio->setText(QString());
        main_button_books->setText(QString());
        main_button_settings->setText(QString());
        main_button_inprogress->setText(QString());
        main_button_new->setText(QString());
        main_button_games->setText(QString());
        main_button_music_video->setText(QString());
    } // retranslateUi

};

namespace Ui {
    class MainWindow: public Ui_MainWindow {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_MAINWINDOW_H
