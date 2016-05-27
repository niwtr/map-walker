#include "mainwindow.h"
#include "ui_mainwindow.h"
#include "header.h"
#include"mapwidget.h"
#include"sctp_client.h"
#include<QBitmap>
#include <QColor>
#include <QPalette>
#include<QGraphicsEffect>
//extern sctp::sctp_client sc;
MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{   start_and_stop=0;
    pause=1;
    speed=1000;
    faster=0;
    //timer->start(1000);
    ui->setupUi(this);

    this->setAttribute(Qt::WA_TranslucentBackground, true);
    connect(timer,SIGNAL(timeout()),this,SLOT(time_count()));
    connect(ui->slider,SIGNAL(valueChanged(int)),this,SLOT(slotzoom(int)));
    connect(this,SIGNAL(sendslotzoom(int)),ui->mapw,SLOT(setslotzoom(int)));//将此界面上的滚动条值发送给地图显示界面
    connect(ui->mapw,SIGNAL(sendmouseevent(QPoint)),this,SLOT(setmouse(QPoint)));
    connect(ui->mapw,SIGNAL(sendmousepress(QPointF)),this,SLOT(setplace(QPointF)));
    ui->strategy->setId(ui->one,1);//三种策略选择
    ui->strategy->setId(ui->two,2);
    ui->strategy->setId(ui->three,3);
    ui->one->setChecked(true);
    ui->traveltimeh->hide();
    connect(ui->three,SIGNAL(toggled(bool)),ui->traveltimeh,SLOT(setVisible(bool)));
    button_pic();



    ui->tracer->setParent(this);
    ui->pushButton_2->setParent(this);
    QPropertyAnimation *ani = new QPropertyAnimation(ui->widget, "windowOpacity");
    ani->setDuration(100);
    ani->setStartValue(1);
    ani->setEndValue(0.5);

    auto *effect = new QGraphicsOpacityEffect(this);
    effect->setOpacity(0.9);
    ui->widget->setGraphicsEffect(effect);

    auto *effect2 = new QGraphicsOpacityEffect(this);
    effect2->setOpacity(0.8);
    ui->widget_2->setGraphicsEffect(effect2);


    auto *effect3 = new QGraphicsOpacityEffect(this);
    effect3->setOpacity(0.7);
    ui->widget_3->setGraphicsEffect(effect3);


    auto *effect4 = new QGraphicsOpacityEffect(this);
    effect4->setOpacity(0.6);
    ui->widget_4->setGraphicsEffect(effect4);


    auto *effect5 = new QGraphicsOpacityEffect(this);
    effect5->setOpacity(0.9);
    ui->traveltimeh->setGraphicsEffect(effect5);




    auto *effect6 = new QGraphicsOpacityEffect(this);
    effect6->setOpacity(0.8);
    ui->mapw->setGraphicsEffect(effect6);

    ui->slider->hide();

    QPalette pal;
    pal.setColor(QPalette::WindowText, QColor(255,255,255));
    ui->label_3->setPalette(pal);
    ui->label_4->setPalette(pal);
    //ui->label_5->setPalette(pal);
}

MainWindow::~MainWindow()
{
    delete ui;
}



void MainWindow::slotzoom(int value){
    emit sendslotzoom(value);


}
void MainWindow::time_count(){
    travel_time++;

}

/*void MainWindow::wheelEvent(QWheelEvent *event){
    int a=event->delta();
    int m=ui->slider->maximumHeight();
    int b=ui->slider->value();

    ui->slider->valueChanged(a/10);
    ui->slider->setValue(b+a/10);
}
*/
void MainWindow::setmouse(QPoint viewPoint){



    //ui->view->setText(QString::number(viewPoint.x())+","+QString::number(viewPoint.y()));
    QPointF scenePoint=ui->mapw->mapToScene(viewPoint);
    ui->scene->setText("x:"+QString::number(scenePoint.x(),'f',0)+","+"y:"+QString::number(scenePoint.y(),'f',0));
    /*if(event->buttons() & Qt::LeftButton){
    QPoint p=event->pos();
    QPointF pt =ui->mapwidget->mapToScene (p);

QPointF offset = pt;//-mPos;
int x = contentsRect().x() - offset.x();
int y = contentsRect().y() - offset.y();


//竖直位置调整

int nYValue =ui->mapwidget->verticalScrollBar()->value ();
ui->mapwidget->verticalScrollBar()->setValue(nYValue+y);



//水平位置调整

int nXValue =ui->mapwidget->horizontalScrollBar()->value ();
ui->mapwidget->horizontalScrollBar()->setValue(nXValue+x);

}*/
}
void MainWindow::setplace(QPointF place){
    QString city;
    if(place.x()>544&&place.x()<572&&place.y()>390&&place.y()<425){
        //南昌
        city="3";
        if(ui->mapw->nanchang->isVisible()==true){
            ui->mapw->nanchang->hide();
            cn->deletecity(city);
        }
        else {
            ui->mapw->nanchang->show();
            cn->sendbuff1.push_back(city);
        }

    }
    else if(place.x()>760&&place.x()<789&&place.y()>548&&place.y()<578){
        //福州
        city="8";
        if(ui->mapw->fuzhou->isVisible()==true){
            ui->mapw->fuzhou->hide();
            cn->deletecity(city);
        }
        else {
            ui->mapw->fuzhou->show();
            cn->sendbuff1.push_back(city);
        }
    }
    else if(place.x()>414&&place.x()<446&&place.y()>774&&place.y()<811){
        //广州
        city="9";
        if(ui->mapw->guangzhou->isVisible()==true){
            ui->mapw->guangzhou->hide();
            cn->deletecity(city);
        }
        else {
            ui->mapw->guangzhou->show();
            cn->sendbuff1.push_back(city);
        }
    }
    else if(place.x()>353&&place.x()<383&&place.y()>432&&place.y()<464){
        //长沙
        city="1";
        if(ui->mapw->changsha->isVisible()==true){
            ui->mapw->changsha->hide();
            cn->deletecity(city);
        }
        else {
            ui->mapw->changsha->show();
            cn->sendbuff1.push_back(city);
        }
    }
    else if(place.x()>700&&place.x()<730&&place.y()>250&&place.y()<280){
        //杭州
        city="6";
        if(ui->mapw->hangzhou->isVisible()==true){
            ui->mapw->hangzhou->hide();
            cn->deletecity(city);
        }
        else {
            ui->mapw->hangzhou->show();
            cn->sendbuff1.push_back(city);
        }
    }
    else if(place.x()>706&&place.x()<736&&place.y()>147&&place.y()<180){
        //南京
        city="5";
        if(ui->mapw->nanjing->isVisible()==true){
            ui->mapw->nanjing->hide();
            cn->deletecity(city);
        }
        else {
            ui->mapw->nanjing->show();
            cn->sendbuff1.push_back(city);
        }
    }
    else if(place.x()>841&&place.x()<886&&place.y()>166&&place.y()<206){
        //上海
        city="7";
        if(ui->mapw->shanghai->isVisible()==true){
            ui->mapw->shanghai->hide();
            cn->deletecity(city);
        }
        else {
            ui->mapw->shanghai->show();
            cn->sendbuff1.push_back(city);
        }
    }
    else if(place.x()>599&&place.x()<629&&place.y()>150&&place.y()<189){
        //合肥
        city="4";
        if(ui->mapw->hefei->isVisible()==true){
            ui->mapw->hefei->hide();
            cn->deletecity(city);
        }
        else {
            ui->mapw->hefei->show();
            cn->sendbuff1.push_back(city);
        }
    }
    else if(place.x()>436&&place.x()<466&&place.y()>268&&place.y()<298){
        //武汉
        city="2";
        if(ui->mapw->wuhan->isVisible()==true){
            ui->mapw->wuhan->hide();
            cn->deletecity(city);
        }
        else {
            ui->mapw->wuhan->show();
            cn->sendbuff1.push_back(city);
        }
    }
    else if(place.x()>87&&place.x()<119&&place.y()>824&&place.y()<855){
        //南宁
        city="10";
        if(ui->mapw->nanning->isVisible()==true){
            ui->mapw->nanning->hide();
            cn->deletecity(city);
        }
        else {
            ui->mapw->nanning->show();
            cn->sendbuff1.push_back(city);
        }
    }
    if(cn->sendbuff1.size()>=1)
        ui->sourse->setText(city_name[cn->sendbuff1[0].toInt()-1]);
    //if(cn->sendbuff1.size()>=2)
    // ui->destination->setText(city_name[cn->sendbuff1[1].toInt()-1]);
    //ui->sourse->text().isEmpty()
    \
}

/*void MainWindow:: paintEvent(QPaintEvent *event){
    QPainter as(this);
    as.drawLine(0,0,819,664);
}
*/

void MainWindow::on_pushButton_3_clicked()
{

    auto *effect = new QGraphicsOpacityEffect(this);
    QPropertyAnimation *anim = new QPropertyAnimation(effect, "opacity" );
    ui->pushButton_3->setGraphicsEffect(effect);
    anim->setDuration(1000);
    anim->setStartValue(1);
    anim->setKeyValueAt(0.5, 0);
    anim->setEndValue(1);
    anim->setEasingCurve( QEasingCurve::OutCurve);
    anim->start();
    QTime t;
    t.start();
    while(t.elapsed()<500)
        QCoreApplication::processEvents();

    //清空缓冲区  界面线路  以及所有显示等
    cn->sendbuff1.clear();
    ui->mapw->clearmap();
    ui->sourse->clear();
    pause=1;               //很关键！！！！！！！！！！！！！！！！！
    travel_time=0;
    ui->mapw->scene->removeItem(ui->mapw->cursor);
    start_and_stop=0;
    //ui->destination->clear();
}

void MainWindow::on_pushButton_2_clicked()
{   //[source, destination, num,mode,travel_time, distance, price, start_time]

    auto *effect = new QGraphicsOpacityEffect(this);
    QPropertyAnimation *anim = new QPropertyAnimation(effect, "opacity" );
    ui->pushButton_2->setGraphicsEffect(effect);
    anim->setDuration(1000);
    anim->setStartValue(1);
    anim->setKeyValueAt(0.5, 0);
    anim->setEndValue(1);
    anim->setEasingCurve( QEasingCurve::OutCurve);
    anim->start();

    QTime t;
    t.start();
    while(t.elapsed()<500)
        QCoreApplication::processEvents();


    //显示路线
    if(cn->sendbuff1.size()<2)
        QMessageBox::about(NULL,"错误","请选择起点与目的地");
    else{
        QElapsedTimer t;//延迟等待接收
        int i;
        int stra=ui->strategy->checkedId();
        cn->inforchange(stra,ui->traveltimeh->text().toInt());
        cn->sendserver();
        qDebug()<<cn->sendtoserver;
        vector<vector<QString>> matrix;
        t.start();
        while(t.elapsed()<5000 and (not cn->able_to_send))
        {
            QCoreApplication::processEvents();
        }
        //qDebug()<<cn->able_to_send;
        /* while(cn->able_to_send==false){
        qDebug()<<cn->able_to_send;
        }*/
        if(cn->msg=="[]"){
            QMessageBox::about(NULL,"错误","没有可用的路径");
        }
        else{
            sc.matrix_pylist_extractor(cn->msg.toStdString(), matrix, [](std::string x){return QString::fromStdString(x);});
            cn->route_table=cn->msg;//保存路径表
            qDebug()<<cn->msg;

            emit send_route(matrix);
            for(long p=0;p<matrix.size();p++){
                QPointF s;
                s=coordinate[matrix[p][0].toInt()-1];
                QPointF d;
                d=coordinate[matrix[p][1].toInt()-1];
                ui->mapw->scene->addLine(s.x(),s.y(),d.x(),d.y(),ui->mapw->p);
            }
        }
    }

}
//界面上点击放缩
void MainWindow::on_fangda_clicked()
{  count=ui->slider->value();
    if(count<ui->slider->maximumHeight()){
        count+=2;
        ui->slider->setValue(count);
    }

}

void MainWindow::on_suoxiao_clicked()




{   count=ui->slider->value();
    if(count>ui->slider->minimumHeight()){
        count-=2;
        ui->slider->setValue(count);
    }

}
void MainWindow::button_pic(){
    //    QPixmap big,small;
    //    QIcon big1,small1;
    //big.load("/Users/apple/Desktop/map/clientmap/build-MapWidget-Desktop_Qt_5_6_0_clang_64bit-Debug/zoomin.png");
    //small.load("/Users/apple/Desktop/map/clientmap/build-MapWidget-Desktop_Qt_5_6_0_clang_64bit-Debug/zoomout.png");
    //        big1.addPixmap(big);
    //        small1.addPixmap(small);
    //ui->fangda->setFixedSize(big.width(),big.height());
    //        ui->fangda->setIcon(big);
    //        ui->fangda->setIconSize(QSize(big.width(),big.height()));
    //        ui->fangda->setMask(big.mask());
    //ui->suoxiao->setFixedSize(small.width(),small.height());
    //        ui->suoxiao->setIcon(small);
    //      ui->suoxiao->setIconSize(QSize(small.width(),small.height()));
    //      ui->suoxiao->setMask(small.mask());
}

void MainWindow::on_tracer_clicked()
//旅行或暂停
{

    auto *effect = new QGraphicsOpacityEffect(this);
    QPropertyAnimation *anim = new QPropertyAnimation(effect, "opacity" );
    ui->tracer->setGraphicsEffect(effect);
    anim->setDuration(1000);
    anim->setStartValue(1);
    anim->setKeyValueAt(0.5, 0);
    anim->setEndValue(1);
    anim->setEasingCurve( QEasingCurve::OutCurve);
    anim->start();

    QTime t;
    t.start();
    while(t.elapsed()<500)
        QCoreApplication::processEvents();



    if(start_and_stop==0){

        if(cn->route_table=="empty")
            QMessageBox::about(NULL,"错误","无效路径");
        else{
            QElapsedTimer t;
            cn->tracer_send("start-time::",0);
            t.start();
            while(t.elapsed()<5000 and (not cn->able_to_send))
            {
                QCoreApplication::processEvents();
            }

            cn->start_time=cn->msg.toInt();
            cn->tracer_send("end-time::",0);
            t.start();
            while(t.elapsed()<5000 and (not cn->able_to_send))
            {
                QCoreApplication::processEvents();
            }
            cn->end_time=cn->msg.toInt();
            qDebug()<<cn->end_time<<cn->start_time;
            ui->mapw->create_cursor();
            start_and_stop++;
        }
    }
    if(start_and_stop>=1){
        if(start_and_stop%2==1){
            start_and_stop++;//顺序很重要！！！！！！！！！！！
            timer->start(speed) ;//100毫秒超时 触发时间+1，1秒等于10秒
            ui->tracer->setStyleSheet("border-image:url(:/mapr/pause-circle-o.png)");
            coordinate_recv();

        }
        else{   pause=1;
            timer->stop();
            ui->tracer->setStyleSheet("border-image:url(:/mapr/watch.png)");
            start_and_stop++;
        }
    }






}
void MainWindow::coordinate_recv(){
    QElapsedTimer t;
    pause=0;
    while(pause==0&&(travel_time+cn->start_time)<=cn->end_time){
        cn->tracer_send(("trace::["+QString::number(travel_time+cn->start_time,10) +","),1);
        t.start();
        while(t.elapsed()<5000 and (not cn->able_to_send))
        {
            QCoreApplication::processEvents();
        }
        qDebug()<<cn->msg;
        vector<QString> vq;

        sc.plain_pylist_extractor(cn->msg.toStdString(), vq, [](std::string x){return QString::fromStdString(x);});

        ui->mapw->show_cursor(vq[0].toFloat(),vq[1].toFloat());
    }
}

void MainWindow::on_kuaijin_clicked()
{//快进

    ui->kuaijin->raise();
    switch(faster){
    case 0:speed=500;
        ui->kuaijin->setStyleSheet("border-image:url(:/mapr/X2.png)");
        faster++;
        break;
    case 1:speed=250;
        ui->kuaijin->setStyleSheet("border-image:url(:/mapr/X4.png)");
        faster++;
        break;
    case 2:speed=125;
        ui->kuaijin->setStyleSheet("border-image:url(:/mapr/X8.png)");
        faster++;
        break;
    case 3:speed=100;
        ui->kuaijin->setStyleSheet("border-image:url(:/mapr/X10.png)");
        faster++;
        break;
    case 4:speed=50;
        ui->kuaijin->setStyleSheet("border-image:url(:/mapr/X20.png)");
        faster++;
        break;
    case 5:speed=20;
        ui->kuaijin->setStyleSheet("border-image:url(:/mapr/X50.png)");
        faster++;
        break;
    case 6:speed=10;
        ui->kuaijin->setStyleSheet("border-image:url(:/mapr/X100.png)");
        faster++;
        break;
    case 7:speed=1000;
        ui->kuaijin->setStyleSheet("border-image:url(:/mapr/X1.png)");
        faster=0;
    }
    timer->start(speed);
}
