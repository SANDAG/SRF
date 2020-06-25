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

/// @brief Writer interface for a Datafile.
/// Interface to store the processed data from the Matrices
/// and Vectors into several file formats.


#pragma once

#include <m2l/io/datafile.hpp>

namespace m2l
{
namespace io
{


class DatafileWriter
{
public:
    /// Default constructor 
    DatafileWriter
    ( const Datafile& _r_file )
    {
        mp_datafile_reference = _r_file.GetSelfPointer();
    }

    DatafileWriter
    ( const std::string& _r_file, Datafile::TYPES _type, Datafile::FORMAT _format = Datafile::OTHER ) :
        mp_datafile_reference ( new Datafile ( _r_file, _type, _format, Datafile::OUTPUT ) )
    { }

    /// Copy constructor.
    /// @param from The value to copy to this object
    DatafileWriter
    ( const DatafileWriter& _r_from )
    {
        mp_datafile_reference = _r_from.mp_datafile_reference;
    }

    /// Destructor.
    virtual
    ~DatafileWriter
    ( void )
    {
        Close();
    }

    /// Close the Datafile and releases resources
    virtual void
    Close()
    {
        mp_datafile_reference.reset();
    }
    /// Writes into the represented file.
    /// @param rBuffer string buffer to be stored.
    /// @returns 0 if succed. -1 if error
    virtual unsigned Save() = 0;
protected:
    io::Datafile::const_datafile_ptr mp_datafile_reference;
private:
};

} //namespace io
} //namespace LandUseModel
