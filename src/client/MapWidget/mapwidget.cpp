#include "mapwidget.h"
#include"mainwindow.h"
//在MAINWINDOW的UI界面中将手动添加的QGRAPHICSVIEW界面(ui->mapw)提升为这个类，可使用这些函数
mapwidget::mapwidget(QWidget *parent):
    QGraphicsView(parent)

{     setMouseTracking(true);
      zoom=0;
        map.load(":/mapr/ditu.png");
        citybutton.load(":/mapr/button1.png");
        cursor_pic.load(":/mapr/pin.png");

              p.setWidth(10);
                p.setColor(QColor("blue"));
                  //p.setStyle(Qt::PenStyle);
                  initmap();
                    //scene->addLine(434,265,351,431,p);

                    //simtour();
                    //scene->addPath()
                    //ui->mapwidget->resize(map.width()+10, map.height()+10);

                    //mapwidget->show();
}
mapwidget::~mapwidget(){

}
void mapwidget::initmap(){
    this->setScene(scene);
    scene->addPixmap(map);
    wuhan->setPixmap(citybutton);
    wuhan->setPos(434,240);
    scene->addItem(wuhan);
    wuhan->hide();

    changsha->setPixmap(citybutton);
    changsha->setPos(351,406);
    scene->addItem(changsha);
    changsha->hide();

    nanning->setPixmap(citybutton);
    nanning->setPos(85,795);
    scene->addItem(nanning);
    nanning->hide();

    nanjing->setPixmap(citybutton);
    nanjing->setPos(705,121);
    scene->addItem(nanjing);
    nanjing->hide();

    hefei->setPixmap(citybutton);
    hefei->setPos(597,120);
    scene->addItem(hefei);
    hefei->hide();

    shanghai->setPixmap(citybutton);
    shanghai->setPos(845,143);
    scene->addItem(shanghai);
    shanghai->hide();

    nanchang->setPixmap(citybutton);
    nanchang->setPos(540,366);
    scene->addItem(nanchang);
    nanchang->hide();

    hangzhou->setPixmap(citybutton);
    hangzhou->setPos(697,224);
    scene->addItem(hangzhou);
    hangzhou->hide();

    fuzhou->setPixmap(citybutton);
    fuzhou->setPos(758,520);
    scene->addItem(fuzhou);
    fuzhou->hide();

    guangzhou->setPixmap(citybutton);
    guangzhou->setPos(413,749);
    scene->addItem(guangzhou);
    guangzhou->hide();


}

//图片缩放
void mapwidget::setslotzoom(int value){
    qreal s;

    if(value>zoom){
        s=pow(1.01,(value-zoom));

    }
    else{
        s=pow(1/1.01,(zoom-value));
    }
    this->scale(s,s);

    zoom=value;
}
void mapwidget::mouseMoveEvent(QMouseEvent*event){
    QPoint viewPoint=event->pos();
    emit sendmouseevent(viewPoint); //发送鼠标坐标

}
void mapwidget::mousePressEvent(QMouseEvent *event){
    QPointF place=this->mapToScene(event->pos());
    emit sendmousepress(place);
}
void mapwidget::create_cursor(){//让游标在线的上面
    cursor->setPixmap(cursor_pic);
    scene->addItem(cursor);
    cursor->hide();
}

void mapwidget::show_cursor(qreal x,qreal y){
    cursor->setPos(x-20,y-30);
    cursor->show();
}

/*void mapwidget::simtour(){
     //scene->addLine(558,412,713,267,p);
      QGraphicsPixmapItem*tourist=scene->addPixmap(QPixmap("/Users/apple/Desktop/map/clientmap/build-MapWidget-Desktop_Qt_5_6_0_clang_64bit-Debug/yu.png"));
     QGraphicsItemAnimation*anim=new QGraphicsItemAnimation;
     anim->setItem(tourist);

     QTimeLine*timeline=new QTimeLine(4000);
     timeline->setCurveShape(QTimeLine::SineCurve);
    timeline->setLoopCount(0);
     anim->setTimeLine(timeline);
//anim->setPosAt(0,QPointF(558,412));
    for(int i=0;i<212;i++){

     anim->setPosAt(i/212.0,QPointF(558+i*0.8,412-i*0.7));    //这个.0很重要！！！！！
     }
     timeline->start();
     //scene->addItem(tourist);
}*/
void mapwidget::clearmap(){
    //scene->clear();
    // x=this->verticalScrollBar()->value();
    //y=this->horizontalScrollBar()->value();
    scene=new QGraphicsScene;

    initmap();

}

/*void mapwidget:: paintEvent(QPaintEvent *event){
    QPainter as(this);
    as.drawLine(558,412,713,267);
}
*/
