/********************************************************************
 *            Math Library Maker (M^2L), a math framework
 *                      Copyright 2010 by
 *
 *       Felipe Saavedra C. (fsaavedr@dcc.uchile.cl)
 *
 *
 *  This file is part of Math Library Maker (M^2L).
 *
 *  M^2L is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  M^2L is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with M^2L.  If not, see <http://www.gnu.org/licenses/>.
 *
 ********************************************************************/

#ifndef MATRIXBACKEND_HPP_
#define MATRIXBACKEND_HPP_

// boost matrix backend
#ifndef BOOST_UBLAS_HDRS_
#define BOOST_UBLAS_HDRS_

#include <boost/numeric/ublas/storage.hpp>
#include <boost/numeric/ublas/vector_expression.hpp>
#include <boost/numeric/ublas/vector_sparse.hpp>
#include <boost/numeric/ublas/vector.hpp>
#include <boost/numeric/ublas/banded.hpp>
#include <boost/numeric/ublas/matrix_expression.hpp>
#include <boost/numeric/ublas/matrix_sparse.hpp>
#include <boost/numeric/ublas/matrix_proxy.hpp>
#include <boost/numeric/ublas/matrix.hpp>
#include <boost/numeric/ublas/triangular.hpp>
#include <boost/numeric/ublas/lu.hpp>
#include <boost/numeric/ublas/io.hpp>
namespace ublas = boost::numeric::ublas;

#endif /* BOOST_UBLAS_HDRS_ */

namespace m2l
{
namespace math
{
/// @todo add consistent storage definition to configurable header
typedef double storage_type;
//typedef std::size_t size_t;

/// @todo define customizable and modularized header
typedef ublas::vector<storage_type> vector;
typedef ublas::matrix<storage_type> matrix;
typedef ublas::matrix_column<matrix> matrix_column;
typedef ublas::matrix_row<matrix> matrix_row;
typedef ublas::zero_vector<storage_type> zero_vector;
typedef ublas::zero_matrix<storage_type> zero_matrix;
typedef ublas::identity_matrix<storage_type> identity_matrix;
typedef ublas::compressed_vector<storage_type> sparse_vector;
typedef ublas::compressed_matrix<storage_type> sparse_matrix;
typedef ublas::scalar_vector<storage_type> scalar_vector;
typedef ublas::scalar_matrix<storage_type> scalar_matrix;


//template <class MatrixType>
//struct my_matrix_ptr
//{
//  typedef boost::shared_ptr<MatrixType> type;  
//};

typedef boost::shared_ptr<matrix> matrix_ptr;
typedef boost::shared_ptr<vector> vector_ptr;

//typedef ublas::vector<sparse_matrix> vector_sparse_matrix; // deprecated

// generic vector redefinition
// template alias definition in c++0x (Not supported by compilers yet)
//template<class T>
//using vector = ublas::vector<T>;

/// Alias for template <class T> vector 
/// Implementation could be interchanged 
template<class STORAGE_TYPE>
struct m2l_vector
{
    typedef ublas::vector<STORAGE_TYPE> type;
    typedef typename type::iterator iterator;
    typedef typename type::size_type size_type;
    typedef typename type::reference reference;
    typedef typename type::const_reference const_reference;
 
    m2l_vector () {};
    m2l_vector ( size_type i )
    {
        self(i);
    }
    const_reference operator() ( size_type i ) const
    {
        return self ( i );
    }

    reference operator() ( size_type i )
    {
        return self ( i );
    }

    void resize ( size_type size, bool preserve = true )
    {
        self.resize ( size, preserve );
    }

private:
    type self;
};

template<class STORAGE_TYPE>
struct m2l_matrix
{
    typedef ublas::matrix<STORAGE_TYPE> type;
    typedef typename type::iterator1 itertor;

};


}//namespace math
}//namespace m2l
#endif /* MATRIXBACKEND_HPP_ */
