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

#include <solver/configurator.hpp>
#include <m2l/solver/solver.hpp>

using namespace muland;

int
main ( int argc, char *argv[] )
{
    if ( argc != 2 )
    {
        std::cout << "usage: " << argv[0] <<" <path to simulation>\n";
        exit ( -1 );
    }
    else configurator::GetInstance ( ( std::string ) argv[1] ); /// configurator initialized

    /// excecute solver
    return ( ::m2l::solver::Solver::GetInstance()->Solve() );
}

// kate: indent-mode cstyle; indent-width 4; replace-tabs on; 
