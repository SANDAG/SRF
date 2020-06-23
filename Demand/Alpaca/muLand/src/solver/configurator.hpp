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

#include<string>

#include <m2l/io/datafile.hpp>


using namespace m2l;

namespace muland
{
/**
 * @brief Runtime Configuration.
 *
 *
 * Store the current configuration on runtime for an execution
 * of the program.
 *
 **/

class configurator
{
public:
    /// Returns an instance of configurator. It should only be called once.
    static configurator*
    GetInstance ( std::string );

    /// It should only be called when already initialized with some path
    static configurator*
    GetInstance();

    /// Output files 
    int
    save();

    // Input files
    io::Datafile::datafile_ptr mp_access_attraction;
    io::Datafile::datafile_ptr mp_agents;
    io::Datafile::datafile_ptr mp_real_estates;
    io::Datafile::datafile_ptr mp_zones;

    io::Datafile::datafile_ptr mp_bid_function;
    io::Datafile::datafile_ptr mp_rent_function;

    io::Datafile::datafile_ptr mp_bid_adjustment;
    io::Datafile::datafile_ptr mp_rent_adjustment;

    io::Datafile::datafile_ptr mp_demand;
    io::Datafile::datafile_ptr mp_supply;
    io::Datafile::datafile_ptr mp_subsidies;

    io::Datafile::datafile_ptr mp_demand_exogenous_cutoff;

    // output files
    io::Datafile::datafile_ptr mp_b_hvi;
    io::Datafile::datafile_ptr mp_b_h;
    io::Datafile::datafile_ptr mp_H_hvi;
    io::Datafile::datafile_ptr mp_Prob_hvi;
    io::Datafile::datafile_ptr mp_r_vi;
    io::Datafile::datafile_ptr mp_S_vi;
    
private:
    configurator
    ( std::string simfile );
    ~configurator() { delete mps_instance; }
    static configurator*       mps_instance;

};
} // end namespace


// kate: indent-mode cstyle; indent-width 4; replace-tabs on; 
