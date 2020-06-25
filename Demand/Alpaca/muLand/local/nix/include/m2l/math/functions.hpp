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

#pragma once

#ifndef BOOST_FUNCTION_HDRS_
#define BOOST_FUNCTION_HDRS_

#include <boost/function.hpp>
#include <boost/concept_check.hpp>

#endif /* BOOST_FUNCTION_HDRS_ */

#include <numeric>
#include <m2l/matrix/matrix_backend.hpp>

namespace m2l
{
namespace math
{
/// @addtogroup functions
/// @{
/// generic functions libraries implementations
namespace functions
{


typedef ublas::vector<bool> idx_vector;

/// Function implemented from @todo add URL from author
template<class STORAGE_TYPE>
bool
InvertMatrix ( const ublas::compressed_matrix<STORAGE_TYPE>& input,
               ublas::compressed_matrix<STORAGE_TYPE>& inverse )
{
    using namespace boost::numeric::ublas;
    typedef permutation_matrix<std::size_t> pmatrix;
    // create a working copy of the input
    ublas::matrix<STORAGE_TYPE> A ( input );
    // create a permutation matrix for the LU-factorization
    pmatrix pm ( A.size1() );

    // perform LU-factorization
    int res = lu_factorize ( A, pm );
    if ( res != 0 )
        return false;

    // create identity matrix of "inverse"
    inverse.assign ( ublas::identity_matrix<STORAGE_TYPE> ( A.size1() ) );

    // backsubstitute to get the inverse
    lu_substitute ( A, pm, inverse );

    return true;
}

typedef boost::function<matrix ( matrix, storage_type ) > matrix_op;
typedef boost::function<sparse_matrix ( matrix, sparse_matrix& )> sparse_matrix_op; 
typedef boost::function<vector ( vector&, storage_type ) > vector_op;
typedef boost::function<vector ( vector&, storage_type, idx_vector ) > vector_op_mask;


// Functions definitions 
template<class VECTOR_TYPE, typename STORAGE_TYPE >
struct vector_element_pow_mask
{
    VECTOR_TYPE
    operator() ( VECTOR_TYPE& r_vector, STORAGE_TYPE linear_param, idx_vector& r_mask )
    {
        VECTOR_TYPE result = r_vector;
        for ( unsigned j = 0; j < r_vector.size(); j++ )
            if ( r_mask ( j ) ) result ( j ) = std::pow ( r_vector ( j ), linear_param );
        return result;
    }
};

template<class VECTOR_TYPE, typename STORAGE_TYPE>
struct vector_element_pow
{
    VECTOR_TYPE
    operator() ( VECTOR_TYPE& r_vector, STORAGE_TYPE linear_param )
    {
        VECTOR_TYPE result = r_vector;
        for ( unsigned j = 0; j < r_vector.size(); j++ )
            result ( j ) = std::pow ( r_vector ( j ), linear_param );
        return result;
    }
};


template<class VECTOR_TYPE, typename STORAGE_TYPE>
struct vector_element_exp
{
    VECTOR_TYPE
    operator() ( VECTOR_TYPE& r_vector, STORAGE_TYPE linear_param )
    {
        VECTOR_TYPE result = r_vector;
        for ( unsigned j = 0; j < r_vector.size(); j++ )
            r_vector ( j ) = std::exp ( linear_param * r_vector ( j ) );
        return result;
    }
};

template<class VECTOR_TYPE, typename STORAGE_TYPE >
struct vector_element_log
{
    VECTOR_TYPE
    operator() ( VECTOR_TYPE& r_vector, STORAGE_TYPE linear_param )
    {
        VECTOR_TYPE result = r_vector;
        for ( unsigned j = 0; j < r_vector.size(); j++ )
            result ( j ) = std::log ( linear_param * r_vector ( j ) );
        return result;
    }
};
template<class MATRIX_TYPE, typename STORAGE_TYPE>
struct matrix_element_pow
{
    MATRIX_TYPE
    operator() ( MATRIX_TYPE& r_matrix, STORAGE_TYPE linear_param )
    {
        MATRIX_TYPE result = r_matrix;
        for ( unsigned j = 0; j < r_matrix.size1(); j++ )
            for ( unsigned k = 0; k < r_matrix.size2(); k++ )
                result ( j, k ) = std::pow ( r_matrix ( j, k ), linear_param );
        return result;
    }
};

template<class MATRIX_TYPE, typename STORAGE_TYPE>
struct matrix_element_log
{

    MATRIX_TYPE
    operator() ( MATRIX_TYPE& r_matrix, STORAGE_TYPE linear_param = 1.0 )
    {
        MATRIX_TYPE result = r_matrix;
        for ( unsigned j = 0; j < r_matrix.size1(); j++ )
            for ( unsigned k = 0; k < r_matrix.size2(); k++ )
                result ( j, k ) = std::log ( linear_param * r_matrix ( j, k ) );
        return result;
    }
};
/// @todo review template template matrix definition
//template<template <class> class MATRIX_TYPE, typename STORAGE_TYPE >
template<class MATRIX_TYPE, typename STORAGE_TYPE >
struct matrix_element_exp
{

    MATRIX_TYPE//<STORAGE_TYPE>
    operator() ( const MATRIX_TYPE r_matrix, STORAGE_TYPE linear_param = 1.0 )
    {
        /*
        typedef typename MATRIX_TYPE ::iterator1 iterator1;
        typedef typename MATRIX_TYPE ::iterator2 iterator2;

        for ( iterator1 it1 = r_matrix.begin1(); it1 != r_matrix.end1(); it1++ )
            for ( iterator2 it2 = it1.begin(); it2 != it1.end(); it2++ )
            {
                // @debug
                std::cout << "Idx[" << it2.index1() << "," << it2.index2() << "]; r_matrix=" << r_matrix ( it2.index1(), it2.index2() ) 
                << "; exp(%)=" << std::exp ( r_matrix ( it2.index1(), it2.index2() ) * linear_param  ) << std::endl;
                r_matrix ( it2.index1(), it2.index2() ) = std::exp ( r_matrix ( it2.index1(), it2.index2() ) * linear_param  ); 
            }
        */
        
        //std::cout << "matrix_element_exp: " << r_matrix << std::endl;
        
        MATRIX_TYPE result = r_matrix;//(r_matrix.size1(), r_matrix.size2());
        for ( size_t j = 0; j < r_matrix.size1(); j++ )
            for ( size_t k = 0; k < r_matrix.size2(); k++ )
            {
                /// @todo add debug level messages
                //std::cout << "r_matrix(" << j << "," << k << "): " << r_matrix(j,k) << ", alpha: " << linear_param << std::endl;
                result ( j, k ) = std::exp ( linear_param * r_matrix ( j, k ) );
                //std::cout << "exp (r_matrix(" << j << "," << k << ") ): " << r_matrix(j,k) << std::endl;
            }
        return result;
    }
};


template<class MATRIX_TYPE, class SPARSE_MATRIX>
struct sparse_matrix_element_div
{
    SPARSE_MATRIX
    operator () ( MATRIX_TYPE& matrix1, SPARSE_MATRIX& matrix2 )
    {
        typedef typename SPARSE_MATRIX::iterator1 iterator1;
        typedef typename SPARSE_MATRIX::iterator2 iterator2;

	//SPARSE_MATRIX result(matrix2.size1(), matrix2.size2());
        for ( iterator1 it1 = matrix2.begin1(); it1 != matrix2.end1(); it1++ )
            for ( iterator2 it2 = it1.begin(); it2 != it1.end(); it2++ )
	    {
	      // @debug
	      // std::cout << "Idx[" << it2.index1() << "," << it2.index2() << "]; matrix1=" << matrix1 ( it2.index1(), it2.index2() ) << "; matrix2=" << *it2 << std::endl;
	      matrix2 ( it2.index1(), it2.index2() ) = matrix1 ( it2.index1(), it2.index2() ) / matrix2 ( it2.index1(), it2.index2() ); 
	    }
	return matrix2;
    }
};

template<typename MatrixExpresion, typename Operation>
MatrixExpresion
Component ( MatrixExpresion& rMatrixExpresion, float linear_param )
{
    return rMatrixExpresion = rMatrixExpresion.op ( linear_param );
}
//template<typename lineal_par, typename value_x, typename value_y>

extern matrix_element_exp        <matrix, storage_type>  matrix_element_exp_struct;
extern matrix_element_log        <matrix, storage_type>  matrix_element_log_struct;
extern matrix_element_pow        <matrix, storage_type>  matrix_element_pow_struct;
extern sparse_matrix_element_div <matrix, sparse_matrix> matrix_element_div_struct;

extern vector_element_exp     <vector&, storage_type> vector_element_exp_struct;
extern vector_element_log     <vector&, storage_type> vector_element_log_struct;
extern vector_element_pow     <vector&, storage_type> vector_element_pow_struct;
extern vector_element_pow_mask<vector&, storage_type> vector_element_pow_mask_struct;


matrix_op               matrix_exp = matrix_element_exp_struct;
matrix_op               matrix_log = matrix_element_log_struct;
matrix_op               matrix_pow = matrix_element_pow_struct;
sparse_matrix_op sparse_matrix_div = matrix_element_div_struct;

vector_op      vector_exp = vector_element_exp_struct;
vector_op      vector_log = vector_element_log_struct;
vector_op      vector_pow = vector_element_pow_struct;
vector_op_mask vector_pow_mask = vector_element_pow_mask_struct;




struct vector_sum
{
    template<class VectorType>
    typename VectorType::storage_type operator() ( const VectorType& vec )
    {
        return std::accumulate ( vec.begin(), vec.end(), 0.0 );
    }
};


struct function_definition
{
    idx_vector idx_1; /// first idx (row size mask)
    idx_vector idx_2; /// second idx (columns size mask)

    matrix* source_matrix;
    unsigned source_matrix_row;

    matrix* destination_matrix; // it always replace a zones matrix column
    unsigned destination_matrix_row;

    vector ( *op ) ( vector, matrix&, idx_vector&, idx_vector&, unsigned );

    template<class DATA_TYPE>
    void apply ( DATA_TYPE* data, matrix& m )
    {
        vector temp = op ( matrix_column ( *source_matrix, source_matrix_row ), m, idx_1, idx_2, data->n_real_estates );
        matrix_column ( *destination_matrix, destination_matrix_row ) = temp;
        //std::cout << "Endogenous result: " << matrix_column ( *destination_matrix, destination_matrix_row ) << std::endl;
    }
};

/** @brief Adds a vector elements by range
 ** Asumes given vector @param source of size z is a matrix(i,j) representation
 ** with size z = i x j. With the given size @param size = {i|j}, the function returns
 ** a new vector with the sum of the components on the specified size equivalent to add
 ** the rows or columns of the represented matrix.
 **
 ** @result = \sum_{i|j} source 
 **/
template <class VectorType>
VectorType
VectorRangeSum
( const VectorType& source, size_t size )
{
    size_t new_size = source.size() / size;
    VectorType result ( new_size );

    //typedef typename vector::const_iterator iterator;
    //for ( iterator it = source.begin(); it != source.end(); it++ )
    //    result ( it.index() ) =  ublas::sum ( ublas::subrange ( source, it.index() * size, ( it.index() + 1 ) * size ) ); 
    
    for ( size_t step = 0; step < new_size; step++ )
        result ( step ) = ublas::sum ( ublas::subrange ( source, step * size, ( step + 1 ) * size ) );
    return result;
}

/// @brief summatory function
/// Adds the given indexes of the specified dimensions the element by element product
vector SumDefinition ( vector var, matrix& pond, idx_vector& idx_1, idx_vector& idx_2, unsigned dimension )
{
    matrix outer_prod;
    ( idx_1.size() == var.size() ) ?
    outer_prod = ublas::outer_prod ( ublas::element_prod ( var, idx_1 ), ublas::element_prod ( scalar_vector ( pond.size2(), 1.0 ), idx_2 ) ) :
                 outer_prod = ublas::outer_prod ( ublas::element_prod ( scalar_vector ( pond.size1(), 1.0 ), idx_1 ), ublas::element_prod ( var, idx_2 ) );

    matrix product = ublas::element_prod ( outer_prod, pond );

    // should sum every row
    vector row_sum = zero_vector ( pond.size2() );
    for ( unsigned i = 0; i < product.size2(); i++ )
        row_sum ( i ) = ublas::sum ( matrix_column ( product, i ) );
    //std::transform(product.rbegin1(), product.rend1(), row_sum.begin(), );
    return VectorRangeSum( row_sum, dimension );
}

/// @brief mean summatory function
vector MeanSumDefinition ( vector var, matrix& pond, idx_vector& idx_1, idx_vector& idx_2, unsigned dimension )
{
    vector sum = SumDefinition ( var, pond, idx_1, idx_2, dimension );
    vector row_sum = SumDefinition ( scalar_vector ( var.size(), 1.0 ), pond, idx_1, idx_2, dimension );
    for ( unsigned i = 0; i<sum.size(); i++ )
        if ( sum ( i ) == 0 ) row_sum ( i ) = 1.0;
    return ublas::element_div ( sum, row_sum );
}


/// @todo review operated indexes on ln definitions
/// @brief lnsum function
vector LnSumDefinition ( vector var, matrix& pond, idx_vector& idx_1, idx_vector& idx_2, unsigned dimension )
{
    vector sum    = SumDefinition ( var, pond, idx_1, idx_2, dimension );
    vector ln_sum = zero_vector ( sum.size() );
    for ( unsigned i = 0; i < sum.size(); i++ )
        ln_sum ( i ) = (sum ( i ) == 0 )? 0.0: std::log ( sum ( i ) );
    return ln_sum;
}

/// @brief ln(mean summatory) functions
vector LnMeanSumDefinition ( vector var, matrix& pond, idx_vector& idx_1, idx_vector& idx_2, unsigned dimension )
{
    vector mean   = MeanSumDefinition ( var, pond, idx_1, idx_2, dimension );
    vector ln_sum = zero_vector ( mean.size() );
    for ( unsigned i = 0; i < mean.size(); i++ )
        ln_sum ( i ) = (mean ( i ) < 1)? 0.0: std::log ( mean ( i ) );         
    return ln_sum;
}


} //#namespace functions
/// @}
} //#namespace math
} //#namespace m2l
