#include "clientwidget.h"
#include "ui_clientwidget.h"
#include "mainwindow.h"
#include"header.h"
#include<QColor>
#include <QGraphicsEffect>
clientconnect::clientconnect(QWidget *parent) :
    QDialog(parent),
    ui(new Ui::clientconnect)
{
    ui->setupUi(this);
    ui->ip->setText(cn->serverIP->toString());
    ui->port->setText(QString::number(cn->port,10));
    QTimer*timer=new QTimer(this);
    timer->start(1000);

    connect(timer,SIGNAL(timeout()),this,SLOT(showtime()));
    connect(cn,SIGNAL(send_disconnected()),this,SLOT(serverdisconnect()));//接收断开连接信号
    connect(w,SIGNAL(send_route(vector<vector<QString> >)),this,SLOT(recv_route(vector<vector<QString> >)));

}

clientconnect::~clientconnect()
{
    delete ui;
}

void clientconnect::on_pushButton_clicked()
{
    auto *effect = new QGraphicsOpacityEffect(this);
    QPropertyAnimation *anim = new QPropertyAnimation(effect, "opacity" );
    ui->pushButton->setGraphicsEffect(effect);
    anim->setDuration(1000);
    anim->setStartValue(1);
    anim->setKeyValueAt(0.5, 0.5);
    anim->setEndValue(1);
    anim->setEasingCurve( QEasingCurve::OutCurve);
    anim->start();

    QTime t;
    t.start();
    while(t.elapsed()<500)
        QCoreApplication::processEvents();


    w->show();

}
void clientconnect::serverdisconnect(){
    QMessageBox::about(NULL,"断开","与服务器断开连接");
    w->close();
    this->close();
}
void clientconnect::showtime(){

    count++;
    ui->time->setText(QDateTime::currentDateTime().toString("hh:mm:ss"));//QString::number(count,10));//
}
void clientconnect::closeEvent(QCloseEvent *){
    w->close();
}
void clientconnect::recv_route(vector<vector<QString>>matrix){
    QString time;
    all_price=0;
    all_time=0;
    all_distance=0;
    ui->show_information->setRowCount(0);
    ui->show_information->clearContents();
    ui->show_information->setEditTriggers(QAbstractItemView::NoEditTriggers);//将表格设为只读。
    for(int i=0;i<matrix.size();i++){
        all_price=all_price+matrix[i][6].toInt();
        all_time=all_time+matrix[i][4].toInt();
        all_distance=all_distance+matrix[i][5].toInt();
        ui->show_information->insertRow(i);
        for(int p=0;p<matrix[i].size();p++){
            if(p<2){
                ui->show_information->setItem(i,p,new QTableWidgetItem(city_name[matrix[i][p].toInt()-1]));//出发地目的地
            }
            else if(p==3)ui->show_information->setItem(i,p,new QTableWidgetItem(vehicle[matrix[i][p].toInt()]));//交通方式
            else if(p==7){//将时间转换成可以看得懂的
                time=convert_time(matrix[i][p]);
                ui->show_information->setItem(i,p,new QTableWidgetItem(time));

            }
            else ui->show_information->setItem(i,p,new QTableWidgetItem(matrix[i][p]));
            auto color=new QColor(100,100,100);
            ui->show_information->item(i, p)->setBackgroundColor(*color);
            auto fnt=new QFont("PT Mono");
            ui->show_information->item(i, p)->setTextAlignment(Qt::AlignCenter);
            ui->show_information->item(i, p)->setFont(*fnt);


        }
    }
    ui->alldistance->setText(QString::number(all_distance,10));
    ui->allprice->setText(QString::number(all_price,10));
    ui->alltime->setText(QString::number(all_time,10));
}
QString clientconnect::convert_time(QString time){
    QString std_time;
    int t=time.toInt();
    int d=t/1440;
    int h=(t%1440)/60;
    int m=(t%1440)%60;
    std_time=QString::number(h,10)+"h"+QString::number(m,10)+"m";
    return std_time;

}
