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

#include <boost/config/no_tr1/complex.hpp>


#include <math/muland_algorithm.hpp>

/* Boost debug symbols */
#ifndef BOOST_UBLAS_DEBUG
#define BOOST_UBLAS_DEBUG
#endif


namespace muland
{
    
/** static members **/
LandData* MuLand::mp_data_;

int
MuLand::Execute()
{

    if ( Init() != 0 )
        return 2;

    /// bids initialization
    BidFn(mp_data_);
    /// Then we initialize the location probability
    LocationProbFn(mp_data_);

    LocationFn(mp_data_); /** First we obtain the initial location \f$ H_{hvi}^0 \f$ */

 
//    BhFn(mp_data_); /** Then we compute the bid component \f$ b_h^n \f$ */
    mp_data_->r_vi = RentsFn(mp_data_);


    std::cout << "Algorithm ended sucessfully\n" ;
    return 0;
}


int
MuLand::Init()
{
    mp_data_ = LandData::GetInstance();    
    return 0;
}
}//end namespace