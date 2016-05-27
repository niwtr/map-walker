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
        /* parse plain python list into native C++ vector<int>.
         * example:
         * "[0, 1, 2, 3]" -->  vector<int>, its element being 0, 1 2 and 3.
         */
        template <typename vecto, typename transformer>
        void plain_pylist_extractor(pyl originl, vecto &container, transformer tr){
            vpyl v;
            originl=parenthesis_smasher(originl, true);
            this->extract_element_from_plain_list(originl, v);
            for(auto x : v){
                container.emplace_back(tr(x));
            }
        }
        /* parse matrix list into native C++ vector<vector<int>>.
         * example:
         * [[0,1,2],[1,2,3],[2,3,4]]  --> vector<vector<int>>, you know.
         */
        template <typename vecto, typename transformer>
        void matrix_pylist_extractor(pyl origin, std::vector<vecto> & matrix, transformer tr){
            origin=parenthesis_smasher(filter_space(origin), false);
            vpyl lypv;
            origin=this->square_remover(origin);
            extract_sublists(origin, lypv);
            for (auto ppyl : lypv){
                vecto vi;
                plain_pylist_extractor(ppyl, vi, tr);
                matrix.emplace_back(vi);
            }
        }

        //old implementations:
        //void trace_parser();
        //void path_parser(pyl origin, imatrix &path_list, int &time, int & cost);
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
