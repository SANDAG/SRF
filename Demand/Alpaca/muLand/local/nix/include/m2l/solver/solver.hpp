/*******************************************************************************
 *          Math Library Maker (M^2L), a math framework
 *                     Copyright 2010 by
 *
 *          Felipe Saavedra C. (fsaavedr@dcc.uchile.cl)
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
 ******************************************************************************/

#pragma once

namespace m2l
{
namespace solver
{

/**
 * @brief Main logic bridge between the components
 *
 * Given the Input Data, sets the specific components previously
 * configured by the user, and initialized them to execute the
 * selected Algorithm module and stores the results.
 *
 **/
class Solver
{
public:
    typedef int status;

    /// @returns the unique instance of solver s
    static Solver*
    GetInstance()
    {
        return ( Solver::mpsInstance == 0 ) ?
               Solver::mpsInstance = new Solver() :
        Solver::mpsInstance;
    }
    /// Executes Algorithm
    /// @returns 0 if succeded
    status
    Solve() ;
private:
    status m_status;

    Solver()
    {
        m_status = 0;
    };
    ~Solver()
    {
        delete mpsInstance;
    };
    /// Initialize the selected components specified by user for the current execution
    status
    Init();
    /// Finalize saving the status and outputs of the excecution
    status
    Close();

    static Solver* mpsInstance; ///< Unique instance of Solver

};
}
}
// kate: indent-mode cstyle; indent-width 4; replace-tabs on; 
