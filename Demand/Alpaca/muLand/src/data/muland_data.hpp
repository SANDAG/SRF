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

#include <m2l/matrix/matrix_backend.hpp>

using namespace m2l::math;

namespace muland
{

class LandData
{
public:
    static LandData*
    GetInstance()
    {
        return (mps_instance == 0)? mps_instance = new LandData():  mps_instance;
    }

    // Execution constants 
    unsigned n_h;
    unsigned n_i;   ///< total number of zones (i)
    unsigned n_m;   ///< total number of markets (m) 
    unsigned n_hi;  ///< total combination of agents-zones 
    unsigned n_vi;  ///< total combination of real_estates-zones 
    unsigned n_hvi; ///< total combination of agents-real_estates-zones
    

    // data matrixes and vector used
    matrix H_hvi; // Location matrix H_hvi 
    matrix b_hvi; // Component b_hvi of bid 
    matrix P_hvi; // Probability P_hvi 
    vector r_vi; // rents r_vi
    vector r_mu_m; // mu definition for r_vi
    vector S_vi; // Supply S_vi
    vector b_h; // Component b_h of bid 

    matrix bids_fn;
    matrix rents_fn;
    
    matrix zones_matrix;
    matrix agents_matrix;
    matrix real_estate_matrix;
    matrix total_demand_matrix;
    matrix acc_matrix;
    matrix att_matrix;
    sparse_matrix phi_hvi;     // demand cutoff phi_hvi
    sparse_matrix bid_adjustment_matrix;
    sparse_matrix subsidies_matrix;
    vector rents_adjustment_vector;

    /// @todo idx must be on tools headers 
    m2l_vector<sparse_matrix> m_idx; // markets index
    sparse_matrix hxm_idx; // agents by markets index
    sparse_matrix vixm_idx; // realestates v,i by markets index

    /// @todo not part of data but a helper 
    zero_matrix   zero_h_vi;
    zero_vector   zero_vi;
    scalar_vector ones_vi;
    scalar_vector ones_h;
    
    /// Initialize data values 
    int
    Init( unsigned, unsigned, unsigned, unsigned );

private:
    LandData(): is_initialized(false) { }; /// Null constructor everything is done on Init 
    
    static LandData* mps_instance; // self static instance
    bool is_initialized; // true if data was initialized with default values

};


}


