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

#include <string>

#include <m2l/io/datafile_reader.hpp>

namespace muland
{

/** @brief Raw text reader.
 *
 * Reads a Datafile formated in raw text.
 * Gets the initial state of the city network and feed the
 * algorithm.
 */
class txtDatafileReader : public m2l::io::DatafileReader
{
public:
    /** Default constructor.
     * @param rDatafile data file to parse */
    txtDatafileReader( m2l::io::Datafile::datafile_ptr rDatafile): DatafileReader(rDatafile) { };
    /** Copy constructor.
     * @param rFrom The value to copy to this object.
     */
    txtDatafileReader(const txtDatafileReader& rFrom): DatafileReader(*rFrom.mp_datafile) { };
    /// Destructor
    virtual ~txtDatafileReader( void ){ };

    /** Parse the raw text file
     * @return 0 if success
     */
    int
    Parse();

private:    
    /// Tokenizer helper function
    /// @return VECTOR_TYPE with tokens
    template<typename VECTOR_TYPE>
    void
    Tokenize(const std::string&, VECTOR_TYPE&, const std::string& delimeters = ";" );
    /// Read matrix helper
    template <typename MATRIX_TYPE>
    int
    ReadMatrix(MATRIX_TYPE, std::ifstream&, unsigned);
    /// Parser 
    template<typename MATRIX_TYPE>
    int
    Parse ( MATRIX_TYPE );//, unsigned& );

};

} //end namespace 
