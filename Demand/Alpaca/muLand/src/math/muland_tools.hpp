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

#pragma once

#include <boost/bimap.hpp>
#include <m2l/matrix/matrix_backend.hpp>

using namespace m2l::math;

/// @addtogroup idx
/// @{
/// generic index definitions
namespace idx
{

/// @todo indexes should have a generic definition and properties (struct definition)
//map index definitions
typedef boost::bimap<unsigned int, unsigned int> h_idx_map; // agents (h) index map
typedef boost::bimap<unsigned int, unsigned int> hxm_idx_map; // agents by market index map
typedef boost::bimap<unsigned int, unsigned int> v_idx_map; // real estates (v) index map
typedef boost::bimap<unsigned int, unsigned int> i_idx_map; // zones (i) index map
typedef std::pair<unsigned int, unsigned int> vi; // vi pair definition
typedef boost::bimap<vi, unsigned int> vi_idx_map; // vi pair index map
typedef boost::bimap<vi, unsigned int> vixm_idx_map; // vi by market index map

// indexes 
extern  h_idx_map  h_idx;
extern  v_idx_map  v_idx;
extern  i_idx_map  i_idx;
extern vi_idx_map vi_idx;

/// Generic idx generation
/// Creates a map from the @param source matrix, using @param to_index as a column indicator
/// And storage the values on @param idx map
int
IdxGen ( matrix& source, vector& to_index, std::map<std::pair<unsigned int, unsigned int>,unsigned int>& idx );

int
hIdxGen ( matrix& rAgentsMatrix, h_idx_map& rIdx = h_idx );
int
iIdxGen ( matrix& rZonesMatrix, i_idx_map& rIdx = i_idx );
int
vIdxGen ( matrix& , v_idx_map& rIdx = v_idx );
int
viIdxGen ( matrix& rRealEstateMatrix, vi_idx_map& rIdx = vi_idx );

unsigned int
findH ( const unsigned int h, h_idx_map& rIdx = h_idx );
unsigned int
reverseFindH ( const unsigned int key, h_idx_map& r_idx = h_idx );
unsigned int
findI ( const unsigned int i, i_idx_map& rIdx = i_idx );
unsigned int
reverseFindI ( const unsigned int key, i_idx_map& r_idx = i_idx );

unsigned int
findVi ( const vi vi, vi_idx_map& rIdx = vi_idx );
vi
reverseFindVi ( const unsigned int key, vi_idx_map& r_idx = vi_idx );
unsigned int
findVi ( unsigned int v, unsigned int i );

template<class DataType>
int
MarketIdxGen ( DataType* pData )
{
    for ( unsigned int vi = 0; vi < pData->n_vi; vi++ )
        for ( unsigned int h = 0; h < pData->n_h; h++ )
        {
            if ( pData->agents_matrix ( h, 2 ) == pData->real_estate_matrix ( vi, 3 ) )
                pData->m_idx ( pData->agents_matrix ( h, 2 ) - 1 ) ( h, vi ) = 1;

            pData->hxm_idx ( h, pData->agents_matrix ( h, 2 ) -1 ) = 1;
            pData->vixm_idx ( vi, pData->real_estate_matrix ( vi, 3 ) -1 ) = 1;

        }
    return 0;
}

}// namespace idx
///@}

vector
FixDimensions ( vector&, unsigned int, unsigned int );

