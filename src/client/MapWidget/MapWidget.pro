#-------------------------------------------------
#
# Project created by QtCreator 2016-05-19T22:32:16
#
#-------------------------------------------------

QT       += core gui
QT       += network
greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = MapWidget
TEMPLATE = app


SOURCES += main.cpp\
        mainwindow.cpp \
    mapwidget.cpp \
    clientwidget.cpp \
    serverconnect.cpp \
    sctp_client.cpp

HEADERS  += mainwindow.h \
    mapwidget.h \
    clientwidget.h \
    header.h \
    serverconnect.h \
    sctp_client.h

FORMS    += mainwindow.ui \
    clientwidget.ui

RESOURCES += \
    map.qrc
