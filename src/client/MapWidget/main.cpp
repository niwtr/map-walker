#include "mainwindow.h"
#include <QApplication>
#include<QSplashScreen>
#include<QElapsedTimer>
#include<QDebug>
#include"serverconnect.h"
#include"clientwidget.h"
#include"header.h"
#include"sctp_client.h"


connectserver *cn=new connectserver;//网络通信
QString city_name[10]={"长沙","武汉","南昌","合肥","南京","杭州","上海","福州","广州","南宁"};
vector<QPointF>coordinate={{364,444},{447,278},{555,405},{612,161},{719,160},{713,262},{862,181},{774,558},{428,788},{100,834}};
vector<QString>vehicle={"飞机","火车","汽车"};
//using sctp::sctp_client;
sctp_client sc; //服务器与客户端协议

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    QElapsedTimer t;
    QSplashScreen splash(QPixmap(":/mapr/yu.png"));
    splash.setDisabled(true); //禁用用户的输入事件响应
    splash.show();
    splash.showMessage(QObject::tr("内存数据库管理器.正在启动中...."),Qt::AlignLeft|Qt::AlignBottom,Qt::white);
    t.start();
    while(t.elapsed()<2000)
    {
        QCoreApplication::processEvents();
    }
    splash.showMessage(QObject::tr("连接服务器...."),Qt::AlignLeft|Qt::AlignBottom,Qt::white);
    t.start();
    cn->con();
    while(t.elapsed()<2000)
    {
        QCoreApplication::processEvents();
    }
    clientconnect c;
    qDebug()<<cn->status;
    if(cn->status==false){
        QMessageBox::about(NULL,"失败","连接服务器失败");
        splash.finish(&c);
        c.close();
    }
    else {
        c.setWindowTitle("地图");
        c.show();
        splash.finish(&c);
    }
    /* c.show();
       splash.finish(&c);*/

    return a.exec();
}
