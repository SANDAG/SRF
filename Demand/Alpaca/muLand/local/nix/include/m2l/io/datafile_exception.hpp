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

#include <exception>
#include <string>
#include <iostream>

namespace m2l
{
namespace io
{
/// Especifies exceptions for Datafile
class DatafileException : public std::exception
{
public:
    /// Errors enumeration
    enum ERROR_CODES
    {
        FILE_NOT_EXISTS, NULL_PARENT
    };

    /// Exception constructor
    DatafileException ( ERROR_CODES _error, std::string _param = "" ) :
        std::exception(), m_param ( _param ), m_error_code ( _error )
    {
        switch ( _error )
        {
        case FILE_NOT_EXISTS:
            std::cerr << "Datafile must exists: " + _param << std::endl;
            break;
        case NULL_PARENT:
            std::cerr << "Datafile has not parent directory\n";
            break;
        default:
            std::cerr << "Unexpected error ocurred on Datafile\n";
        }
    }

    ~DatafileException() throw() {};

    const char * what() const throw()
    {
        return "Exception on datafile\n";
    }

private:
    std::string m_param;
    int m_error_code;

};
}
}
// kate: indent-mode cstyle; indent-width 4; replace-tabs on; 
