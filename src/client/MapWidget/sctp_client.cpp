//
//  main.cpp
//  walker_sctp_client
//
//  Created by 牛天睿 on 16/5/23.
//  Copyright (c) 2016 Anzalized. All rights reserved.
//

#include <iostream>


#include "sctp_client.h"
using namespace sctp;

void sctp::sctp_client::splitf(pyl s, std::string delim,vpyl & sv) {
    std::string delimiter=delim;
    size_t pos = 0;
    std::string token;
    while ((pos = s.find(delimiter)) != std::string::npos) {
        token = s.substr(0, pos);
        sv.push_back(token);
        s.erase(0, pos + delimiter.length());
    }
    sv.push_back(s);
}

pyl sctp_client::parenthesis_smasher(pyt python_tuple, bool replace_by_bracketsp) {
    pyl res=python_tuple;
    if(*(res.begin())=='(' and *(res.end()-1)==')')
        if(not replace_by_bracketsp)
            return res.substr(1, res.length()-2); //cowsay : test it.
        else return "["+res.substr(1, res.length()-2)+"]";
    else return res;
}

pyl sctp_client::square_remover(pyt python_list) {
    pyl res=python_list;

    if(*(res.begin())=='[' and *(res.end()-1)==']') {
        return res.substr(1, res.length() - 2);
    }
    else return res;
}
pyl sctp_client::filter_space(pyl origin) {
    for (auto it=origin.begin();it!=origin.end();){
        if(*it==' ')
            origin.erase(it); //no it++;

        else
        if(it!=origin.end())
            it++;
    }
    return origin;
}

void sctp_client::extract_sublists(pyl python_list, vpyl &pyv) {
    bool in_bracket=false;
    bool packed=false;
    pyl current="";
    for(auto symb : python_list){
        if(symb=='['){
            in_bracket=true;
            continue;
        }
        else if(symb==']'){
            if(in_bracket) {
                in_bracket = false;
                packed = true;
            }
            else {;} //this should alert error.
        }

        if(in_bracket){
            current+=symb;
        }
        if(packed){
            pyv.emplace_back(current);
            current.clear();
            packed=false;
        }
    }
}


void sctp_client::extract_element_from_plain_list(pyl python_list, vpyl& elemv) {
    python_list=square_remover(filter_space(python_list));
    this->split_by_comma(python_list, elemv);
}







/*
void sctp_client::path_parser(pyl origin, imatrix & path_list, int &time, int & cost){
   origin=parenthesis_smasher(filter_space(origin), false);
    long index;
    for(index=origin.length()-1;index>0;index--){
        if(origin[index]==']'){
            ++index;
            break;
        }
    }
    auto the_path=origin.substr(0, index);
    auto tac="["+origin.substr(index+1, origin.length()-1)+"]";
    matrix_pylist_extractor(the_path, path_list);
    ivector v;
    plain_pylist_extractor(tac, v);
    time=v[0];
    cost=v[1];
}

*/

/*int main(int argc, const char * argv[]) {

    sctp_client sc;
    pyl s="[[1,2,3,4,5], [2,4,5,6,7], [5,6,7,8,9],[9,1,2,3,4]]";//query_all
    pyl u="(1,2,3,4,5,6,7)";//query
    pyl t="([[1,2],[2,2],[3,2], 4,-1]], 711,310)"; //path

    vector<QString> vq;
    sc.plain_pylist_extractor(u, vq, [](std::string x){return QString::fromStdString(x);});

    vector<vector<QString>> matrix;
    sc.matrix_pylist_extractor(s, matrix, [](std::string x){return QString::fromStdString(x);});




    return 0;
}

*/
