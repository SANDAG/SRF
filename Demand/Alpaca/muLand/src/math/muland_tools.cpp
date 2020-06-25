/*******************************************************************************
 *            Micro Land (mu-land) - Land Use Model 
 *                     Copyright 2016 by
 *
 *          Felipe Saavedra C. (fsaavedr@dcc.uchile.cl)
 *
 *
 *  This file is part of Micro Land (mu-land)
 *
 *  Mu-Land is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  Mu-Land is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with Mu-Land.  If not, see <http://www.gnu.org/licenses/>.
 *
 ******************************************************************************/

#include <math/muland_tools.hpp>


    
// static definitions 
idx::h_idx_map  idx::h_idx;
idx::v_idx_map  idx::v_idx;
idx::i_idx_map  idx::i_idx;
idx::vi_idx_map idx::vi_idx;

/// @brief Generic indexation function
int
idx::IdxGen
( matrix& source, vector& to_index, std::map<std::pair<unsigned, unsigned>, unsigned>& idx )
{
    unsigned index = 0;
    std::pair<std::map<std::pair<unsigned, unsigned>, unsigned>::iterator,bool> ret;
    std::map<std::pair<unsigned, unsigned>, unsigned>::iterator iterator;

    for ( unsigned i = 0; i < source.size1(); i++ )
    {
        vector key_aux = to_index;
        for ( unsigned j=0; j< to_index.size(); j++ )
            key_aux ( j ) = source ( i,to_index ( j ) );
        //std::cout << "Row(" << i << ") - key: " << key_aux << std::endl;
        std::pair<unsigned, unsigned> key ( key_aux ( 0 ), key_aux ( 1 ) );
        ret = idx.insert ( std::pair<std::pair<unsigned, unsigned>, unsigned> ( key, index ) );
        if ( ret.second ) index++;
    }    
    return 0;
}

int
idx::hIdxGen
( matrix& rAgentsMatrix, h_idx_map& rIdx )
{
    for ( unsigned j = 0; j < rAgentsMatrix.size1(); j++ )
    {
        unsigned h_ = rAgentsMatrix ( j, 1 );
        unsigned idx_ = rAgentsMatrix ( j, 0 );
        //std::cout << "Inserting: " << h_ << "," << idx_ << std::endl;
        //unsigned m_ = rAgentsMatrix(j, 2);
        rIdx.left.insert ( h_idx_map::left_map::value_type ( h_, idx_ ) );
        //rHxmIdx.insert(hxm_idx_map::value_type(idx_, m_));
    }

    return 0;
}
int
idx::iIdxGen
( matrix& rZonesMatrix, i_idx_map& rIdx )
{
    for ( unsigned j = 0; j < rZonesMatrix.size1(); j++ )
    {
	unsigned idx_ = rZonesMatrix ( j, 0 );
        unsigned i_ = rZonesMatrix ( j, 1 );
        rIdx.left.insert ( i_idx_map::left_map::value_type ( i_, idx_ ) );
    }
    return 0;
}
int
idx::vIdxGen
( matrix& rRealEstate, v_idx_map& rIdx )
{
    for ( unsigned j = 0; j < rRealEstate.size1(); j++ )
    {
	unsigned idx_ = rRealEstate ( j, 0 );
        unsigned v_ = rRealEstate ( j, 1 ); 
        rIdx.left.insert ( v_idx_map::left_map::value_type ( v_, idx_ ) );
    }
    return 0;
}
int
idx::viIdxGen
( matrix& rRealEstateMatrix, vi_idx_map& rIdx )
{
    for ( unsigned j = 0; j < rRealEstateMatrix.size1(); j++ )
    {
        unsigned idx_ = rRealEstateMatrix ( j, 0 );
	unsigned v_ = rRealEstateMatrix ( j, 1 );
        unsigned i_ = rRealEstateMatrix ( j, 2 );

        rIdx.left.insert ( vi_idx_map::left_map::value_type ( vi ( v_, i_ ), idx_ ) );
    }
    return 0;
}

vector
FixDimensions
( vector& source, unsigned dim_i, unsigned dim_f )
{
    vector ret ( dim_f );
    unsigned step = std::floor ( dim_f / dim_i );

    for ( unsigned i = 0; i < dim_i; i++ )
        ublas::subrange ( ret, i * step, ( i + 1 ) * step ) = scalar_vector ( step, source ( i ) );
    return ( ret );
}

unsigned int
idx::findH ( const unsigned int h, h_idx_map& rIdx)
{
    h_idx_map::left_iterator i_ = rIdx.left.find ( h );
    return ( i_ == rIdx.left.end() ) ? -1 : i_->second;
}
unsigned int
idx::reverseFindH ( const unsigned int key, h_idx_map& r_idx)
{
    h_idx_map::right_iterator i_ = r_idx.right.find ( key );
    return ( i_ == r_idx.right.end() ) ? -1 : i_->second;
}
unsigned int
idx::findI ( const unsigned int i, i_idx_map& rIdx )
{
    i_idx_map::left_iterator i_ = rIdx.left.find ( i );
    return ( i_ == rIdx.left.end() ) ? -1 : i_->second;
}
unsigned int
idx::reverseFindI ( const unsigned int key, i_idx_map& r_idx )
{
    i_idx_map::right_iterator i_ = r_idx.right.find ( key );
    return ( i_ == r_idx.right.end() ) ? -1 : i_->second;
}
unsigned int
idx::findVi ( const vi vi, vi_idx_map& rIdx )
{
    vi_idx_map::left_iterator i_ = rIdx.left.find ( vi );
    return ( i_ == rIdx.left.end() ) ? -1 : i_->second;
}
idx::vi
idx::reverseFindVi ( const unsigned int key, vi_idx_map& r_idx )
{
    vi_idx_map::right_iterator i_ = r_idx.right.find ( key );
    return ( i_ == r_idx.right.end() ) ? vi(-1,-1) : i_->second;
}
unsigned int
idx::findVi ( unsigned int v, unsigned int i )
{
    return findVi ( vi ( v, i ) );
}

