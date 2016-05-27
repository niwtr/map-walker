#include"serverconnect.h"
#include"mainwindow.h"
#include<QHostInfo>
#include"clientwidget.h"
connectserver:: connectserver(){
    status=false;
    port=9999;
    serverIP=new QHostAddress();
    tcpSocket=new QTcpSocket;
    tcpSocket2=new QTcpSocket;
    able_to_send=false;
}
connectserver::    ~connectserver(){

}

void connectserver::con(){
        serverIP->setAddress("127.0.0.1");

        tcpSocket->connectToHost(*serverIP,port);
       //bool t=tcpSocket->waitForConnected();//判断连接成功
       //qDebug()<<t;
         connect(tcpSocket,SIGNAL(readyRead()),this,SLOT(sth()));
}

void connectserver::sth(){
    while(tcpSocket->bytesAvailable()) //接收端口分配器的数据
     {
         QByteArray datagram;
         datagram.resize(tcpSocket->bytesAvailable());
         tcpSocket->read(datagram.data(),datagram.size());
         QString msg=datagram.data();
         information.push_back(msg);
         //qDebug()<<msg;
     }


     if(information.size()>1){
     port=information[1].toInt();

     tcpSocket2->connectToHost("127.0.0.1",port);
     status=tcpSocket2->waitForConnected();//判断连接成功
     connect(tcpSocket2,SIGNAL(disconnected()),this,SLOT(send_dis()));
     connect(tcpSocket2,SIGNAL(readyRead()),this,SLOT(recv_route()));
     //qDebug()<<status;
     }
}
void connectserver::send_dis(){//发送断开连接信号
    emit send_disconnected();
}
void connectserver::deletecity(QString name){ //用户可删除想去的城市
    int i;
    for(i=0;i<sendbuff1.size();i++){
         if(sendbuff1[i]==name)sendbuff1.erase(sendbuff1.begin()+i);
    }
}
void connectserver::inforchange(int i,int time){
    int p;
    if(i==1){
        sendtoserver="mcp::["+sendbuff1[0]+",[";
        for(p=2;p<sendbuff1.size();p++){
            if(p==sendbuff1.size()-1)
            sendtoserver=sendtoserver+sendbuff1[p];
            else
             sendtoserver=sendtoserver+sendbuff1[p]+",";
        }
        if(sendbuff1.size()>2)
        sendtoserver=sendtoserver+","+sendbuff1[1]+"]]";
        else sendtoserver=sendtoserver+sendbuff1[1]+"]]";

    }
    else if(i==2){
        sendtoserver="mtp::["+sendbuff1[0]+",[";
        for(p=2;p<sendbuff1.size();p++){
            if(p==sendbuff1.size()-1)
            sendtoserver=sendtoserver+sendbuff1[p];
            else
            sendtoserver=sendtoserver+sendbuff1[p]+",";
        }
        if(sendbuff1.size()>2)
        sendtoserver=sendtoserver+","+sendbuff1[1]+"]]";
        else sendtoserver=sendtoserver+sendbuff1[1]+"]]";
    }
    else if(i==3){
        sendtoserver="rmcp::["+sendbuff1[0]+",[";
        for(p=2;p<sendbuff1.size();p++){
            if(p==sendbuff1.size()-1)
            sendtoserver=sendtoserver+sendbuff1[p]; //最后一个不需要逗号
            else
            sendtoserver=sendtoserver+sendbuff1[p]+",";
        }
        if(sendbuff1.size()>2)//这是历史遗留问题。。当时认为最后一个目的地是固定的  只能最后到达 所以放最后了
        sendtoserver=sendtoserver+","+sendbuff1[1]+"],"+QString::number(time*60,10)+"]";
        else sendtoserver=sendtoserver+sendbuff1[1]+"],"+QString::number(time*60,10)+"]";
    }
}
void connectserver::recv_route(){
    while(tcpSocket2->bytesAvailable()) //接收端口分配器的数据
     {
         QByteArray datagram;
         datagram.resize(tcpSocket2->bytesAvailable());
         tcpSocket2->read(datagram.data(),datagram.size());
         msg=datagram.data();
         if(msg!="established"){
         able_to_send=true;}
         //qDebug()<<able_to_send;}
    }
     }

void connectserver::sendserver(){//获取路径表
    tcpSocket2->write(sendtoserver.toLatin1(),sendtoserver.length());
    qDebug()<<sendtoserver.toLatin1();
}
void connectserver::tracer_send(QString mode,int i){//旅行指令发送给服务端
    if(i==0){//0为获取出发与到达时间 1为获得坐标
    mode=mode+route_table;
    qDebug()<<mode;
    tcpSocket2->write(mode.toLatin1(),mode.length());
    able_to_send=false;}
    else{
        mode=mode+route_table+"]";
        qDebug()<<mode;
        tcpSocket2->write(mode.toLatin1(),mode.length());
        able_to_send=false;
    }
}
