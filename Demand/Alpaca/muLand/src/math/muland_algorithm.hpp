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

#include <m2l/math/algorithm.hpp>

#include <data/muland_data.hpp>
#include <math/muland_functions.hpp>
#include <math/muland_tools.hpp>


namespace muland
{

class MuLand: public m2l::math::Algorithm
{
public:
    /// @brief Land Use Equilibrium main algorithm 
    virtual int
    Execute();
    /// @brief Generic destructor
    ~MuLand()
    {
        /// @todo data instances should have deleter
        //delete mp_data_; 
    }
protected:
    /// @brief Initialize values for excecution 
    int
    Init();
private:
    /// @brief Load the network and simulation values 
    int
    Load();
    /// Functions used by Equilibrium 
    static muland::LandData* mp_data_;
};

} 
