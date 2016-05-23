//
// Created by 牛天睿 on 16/5/23.
// Copyright (c) 2016 Anzalized. All rights reserved.
//

#ifndef WALKER_SCTP_CLIENT_SCTP_CLIENT_H
#define WALKER_SCTP_CLIENT_SCTP_CLIENT_H

#include <iostream>
#include <vector>
namespace  sctp {
    using pyt=std::string; //python tuple.
    using pyl=std::string; //python list.
    using vpyl=std::vector<pyl>; //python list vector.
    using std::vector;
    using imatrix=vector<vector<int>>;
    using ivector=vector<int>;
    class sctp_client {



    public:

        void path_parser(pyl origin, imatrix &path_list, int &time, int & cost);

        void query_parser(pyl originl, ivector &container);

        void query_all_parser(pyl origin, imatrix &matrix);


        void trace_parser();

    private:
        void splitf(pyl s, std::string delim, vpyl &sv);

        inline void split_by_comma(pyl lst, vpyl &v){
            splitf(lst, ",", v);
        }
        pyl filter_space(pyl origin);
        //template <typename elemtype>
        void extract_sublists(pyl python_list, vpyl & pyv);

        pyl parenthesis_smasher(pyt python_tuple, bool replace_by_bracketsp);

        pyl square_remover(pyt python_list);
        void extract_element_from_plain_list(pyl python_list, vpyl& elemv);

    };
}

#endif //WALKER_SCTP_CLIENT_SCTP_CLIENT_H
