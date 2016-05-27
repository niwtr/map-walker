#ifndef MAINWINDOW_H
#define MAINWINDOW_H
#include<QMessageBox>
#include <QMainWindow>
#include<QGraphicsPixmapItem>
#include<QGraphicsView>
#include<math.h>
#include<QScrollBar>
#include<QMouseEvent>
#include<QPen>
#include<QGraphicsScene>
#include<QGraphicsItemAnimation>//模拟旅行用
#include<QTimeLine>//时间
#include<QTimer>
#include<QDateTime>
#include<QElapsedTimer>
//网络用
#include<vector>
#include <QHostAddress>
#include<QTcpSocket>
#include<QDebug>
#include<QObject>
#include"sctp_client.h"
namespace Ui {
class MainWindow;

}
//***********************************************************地图主界面
class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = 0);
    ~MainWindow();
    //void wheelEvent(QWheelEvent *event);
    void button_pic();//按钮加图片


private:
 Ui::MainWindow *ui;
 int count;//用于地图缩放
 int pause;//旅行暂停
 int travel_time=0;  //旅行计时器
 QTimer*timer=new QTimer(this);
 int start_and_stop;//判断是暂停还是开始
 int speed;//速度
 int faster;//判断快进倍数
signals:
 void sendslotzoom(int);
 void send_route(vector<vector<QString>>);
public slots:
void slotzoom(int);//与滚动条相连
void setmouse(QPoint);
void setplace(QPointF);
private slots:
void on_pushButton_3_clicked();
void on_pushButton_2_clicked();
void on_fangda_clicked();
void on_suoxiao_clicked();
void on_tracer_clicked();
void time_count();
void coordinate_recv();
void on_kuaijin_clicked();
};

//***********************************************************显示地图的界面
class mapwidget : public QGraphicsView
{
    Q_OBJECT
public:
    explicit mapwidget(QWidget *parent = 0);
    ~mapwidget();
     QPen p;
   void simtour();
   // mapwidget();
    void mouseMoveEvent(QMouseEvent*event);
    void mousePressEvent(QMouseEvent *event);
    void clearmap();
    void initmap();
    void show_cursor(qreal,qreal);//显示旅行位置
    void create_cursor();//晚点创建游标 让其在路线上方
    QGraphicsScene *scene = new QGraphicsScene;
    QGraphicsPixmapItem*wuhan=new QGraphicsPixmapItem;
    QGraphicsPixmapItem*changsha=new QGraphicsPixmapItem;
    QGraphicsPixmapItem*nanchang=new QGraphicsPixmapItem;
    QGraphicsPixmapItem*nanning=new QGraphicsPixmapItem;
    QGraphicsPixmapItem*guangzhou=new QGraphicsPixmapItem;
    QGraphicsPixmapItem*fuzhou=new QGraphicsPixmapItem;
    QGraphicsPixmapItem*nanjing=new QGraphicsPixmapItem;
    QGraphicsPixmapItem*shanghai=new QGraphicsPixmapItem;
    QGraphicsPixmapItem*hefei=new QGraphicsPixmapItem;
    QGraphicsPixmapItem*hangzhou=new QGraphicsPixmapItem;

    QGraphicsPixmapItem*cursor=new QGraphicsPixmapItem;
signals:
    void sendmouseevent(QPoint);//发送鼠标信号给MAINWINDOW中的显示函数 显示坐标
    void sendmousepress(QPointF);
private:
    qreal zoom;
    //int x,y=0;//地图显示界面滚动条的位置  。。用创建一张新地图来清空地图，为了让用户感觉不到，需要清空前滚动条的位置 并在创建后移动到那个位置
    QPixmap map;
    QPixmap citybutton;
    QPixmap cursor_pic;
public slots:
//void paintEvent(QPaintEvent *event);
//void mouseMoveEvent(QMouseEvent*event);

void setslotzoom(int);
};
//***********************************************************通信socket
using namespace std;

class connectserver: public QObject
{
 Q_OBJECT
public:
    bool able_to_send;
    connectserver();
    ~connectserver();
    void con();//连接
   bool status;//连接状态
   QHostAddress*serverIP;//主机地址
   int port;//端口
   //void conser();
   vector<QString>sendbuff1;//原始数据旅客
   QString sendtoserver;//转化为服务端认识的符号
   void deletecity(QString);
   void inforchange(int,int);//转化成服务端可接受的字符  int为策略 第二个是策略三的时间
   void sendserver();
   void tracer_send(QString,int);//旅行信息发送
   int strategy;//旅行策略
   QString msg;//接收服务器消息
   QString route_table="empty";//保存初始的路径表
   int start_time;
   int end_time;
private:

    vector<QString>information;//端口分配器的信息
    QTcpSocket*tcpSocket;//与端口分配器连接
    QTcpSocket*tcpSocket2;//与服务端连接
public slots:
    void sth();//接收端口分配器的消息
    void send_dis();
    void recv_route();//接受路线
    //void XYrecv();//接收坐标
   // void slotConnected();
signals:
    void send_disconnected();
};
extern connectserver *cn;
#endif // MAINWINDOW_H
