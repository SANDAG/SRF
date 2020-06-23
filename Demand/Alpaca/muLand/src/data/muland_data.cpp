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

#include <data/muland_data.hpp>

muland::LandData* muland::LandData::mps_instance; //< data static instance 

/******************************************************************************/
/// @brief data initialization 
int
muland::LandData::Init( unsigned _h, unsigned _vi, unsigned _i, unsigned _m )
{
    /// Data can only be initialized once 
    if (is_initialized) return 1;

    is_initialized = true;

    // Model variables
    n_h  =  _h;
    n_vi = _vi;
    n_i  =  _i;
    n_m  =  _m;

    n_hi  = _h *  _i;
    n_hvi = _h * _vi;

    zero_h_vi.resize(_h, n_vi, false);
    zero_vi  .resize(n_vi);

    H_hvi.resize(_h, n_vi);
    b_hvi.resize(_h, n_vi);
    P_hvi.resize(_h, n_vi);
    r_vi .resize(n_vi);
    S_vi .resize(n_vi);
    b_h  .resize(_h);

    acc_matrix.resize(_h, _i);
    att_matrix.resize(_h, _i);
    bid_adjustment_matrix = sparse_matrix(_h, n_vi);
    subsidies_matrix      = sparse_matrix(_h, n_vi);
    rents_adjustment_vector.resize(n_vi);
 
    // Markets definitions
    m_idx.resize(_m);
    for (size_t market_iterator = 0; market_iterator < _m; market_iterator++)
      m_idx(market_iterator) = sparse_matrix(_h, n_vi);
    
    hxm_idx  = sparse_matrix(  _h, _m);
    vixm_idx = sparse_matrix(n_vi, _m);
    phi_hvi  = sparse_matrix(  _h, n_vi);
    ones_vi  = scalar_vector(n_vi, 1.0);
    ones_h   = scalar_vector(  _h, 1.0);

    return 0;
}

