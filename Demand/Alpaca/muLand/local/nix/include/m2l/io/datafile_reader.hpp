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

#include <m2l/io/datafile.hpp>

namespace m2l
{
namespace io
{
/// @brief Reader-Parser interface for a Datafile.
/// Reads and parse a datafile.
class DatafileReader
{
public:
    /// Default constructor 
    DatafileReader
    ( const_datafile_ptr _r_file )
    {
        mp_datafile = _r_file;
    }

    DatafileReader
    ( const Datafile& _r_file )
    {
        mp_datafile = _r_file.GetSelfPointer();
    }
    /// Copy constructor.
    /// @param from The value to copy to this object.
    DatafileReader ( const DatafileReader& _r_from )
    {
        mp_datafile = _r_from.mp_datafile;
    }

    /// Destructor
    virtual
    ~DatafileReader ( void )
    {
        Close();
    }

    /// Close the Datafile and releases resources
    virtual void
    Close()
    {
        mp_datafile.reset();
    }
    /// @brief Reads and parse
    /// Parses the datafile writing the contents on given @param Data
    /// @param Data network data representation
    /// @returns 0 if success
    virtual int
    Parse() = 0;
protected:
    Datafile::const_datafile_ptr mp_datafile; /// Datafile readed 
private:
};

} //namespace io
} //namespace LandUseModel
