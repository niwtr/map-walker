#ifndef CLIENTWIDGET_H
#define CLIENTWIDGET_H

#include <QDialog>
#include "mainwindow.h"
namespace Ui {
class clientconnect;
}

class clientconnect : public QDialog
{
    Q_OBJECT

public:
    explicit clientconnect(QWidget *parent = 0);
    ~clientconnect();
    MainWindow* w=new MainWindow;
    QString convert_time(QString);
private slots:
    void on_pushButton_clicked();
    void serverdisconnect();
    void showtime();
    void closeEvent(QCloseEvent *);
    void recv_route(vector<vector<QString>>);
private:
    Ui::clientconnect *ui;
        int count=0;
        int all_price;
        int all_time;
        int all_distance;
};

#endif // CLIENTCONNECT_H
