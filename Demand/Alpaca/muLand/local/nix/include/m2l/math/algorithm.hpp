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

#include <m2l/matrix/matrix_backend.hpp>

namespace m2l
{
namespace math
{

/// @brief Algorithm abstraction
/// Implemented algorithms should be derived from this class.
/// - Includes generic functions definitions
/// - Includes matrix backend defintions
class Algorithm
{
public:
    typedef boost::shared_ptr<Algorithm> algorithm_ptr; //< Algorithm shared pointer 
    typedef boost::shared_ptr<Algorithm const> const_algorithm_ptr;

    /// @brief Solution algorithm
    /// Main algorithm logic implementation
    virtual int
    Execute() = 0;
protected:
    /// @brief Initialize values for excecution
    /// Main algorithm previous initializations needed
    virtual int
    Init() = 0;
    
    /// @brief Generic destructor 
    ~Algorithm() {};
    ///	FunctionImpl mFunction;  ** Replaced by direct boost 
}; // class Algorithm

typedef boost::shared_ptr<Algorithm> algorithm_ptr; //< Algorithm pointer redifinition for convenience
typedef boost::shared_ptr<Algorithm const> const_algorithm_ptr; //< Algorithm const pointer redifition for convenience

algorithm_ptr Algorithm();

}// namespace math
}// namespace m2l
