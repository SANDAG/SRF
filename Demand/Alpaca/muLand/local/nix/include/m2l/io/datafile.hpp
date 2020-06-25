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
/* SYSTEM INCLUDES */
#include <string>
/* PROJECT INCLUDES */
#include <boost/filesystem.hpp>
#include <boost/filesystem/fstream.hpp>
#include <boost/enable_shared_from_this.hpp>
/* LOCAL INCLUDES */
#include <m2l/io/datafile_exception.hpp>
#include <m2l/matrix/matrix_backend.hpp>

/* FORWARD REFERENCES */

/// @brief Proyect root namespace
namespace m2l
{
namespace io
{
/// @addtogroup io
/// @{
/// Input-Output definitions
namespace fs = boost::filesystem;

#define BOOST_FILESYSTEM_NO_DEPRECATED

/// @brief Handles a file on the filesystem
/// Abstraction of a file on the filesystem.
/// @todo should have a matrix template representation of the data parsed.
class Datafile: public boost::enable_shared_from_this<Datafile>
{
public:
    typedef boost::shared_ptr<Datafile> datafile_ptr;
    typedef boost::shared_ptr<Datafile const> const_datafile_ptr;

    // datafile access type
    enum MODE
    {
        INPUT,
        OUTPUT
    };
    // datafile supported formats
    enum FORMAT
    {
        XML,
        DBF,
        TXT,
        PATH
    };
    
    // datafile supported types
    enum TYPES
    {
        AGENTS, // agents definition and data
        REAL_ESTATES, // realestates definition and data
        ZONES, // zones definition and data
        ACCESS_ATTRACTION, // access and attraction definition and data
        DEMAND, // total demand by agents type
        FIXED_SUPPLY, // fixed supply by zone
        SUBSIDES,
        // cutoffs definitions
        DEMAND_EXOGENOUS_CUTOFF,
        // model functions definitions
        BID_FUNCTION,
        RENT_FUNCTION,
        // model functions adjustment
        BID_ADJUSTMENT,
        RENT_ADJUSTMENT,
        // model output files
        BIDS,
        BH_BID_COMPONENT,
        LOCATION,
        LOCATION_PROBABILITY,
        RENTS,
        SUPPLY,
        // undefined
        OTHER
    };

    /* Constructor
     * Creates a new Datafile representation.
     * @param rPath boost path to an existent file.
     */
    Datafile() throw ( DatafileException )
    {
        m_path = fs::system_complete ( fs::current_path() );
	m_format = PATH;
	m_mode = INPUT;
//	mp_self = boost::const_pointer_cast<Datafile>(shared_from_this());
	mp_data = math::matrix_ptr(new math::matrix());

	// this should never happen 
        if ( !fs::exists ( m_path ) )
            throw DatafileException ( DatafileException::FILE_NOT_EXISTS, m_path.generic_string<std::string>() );
    }

    /* Constructor
     * Creates a new Datafile representation.
     * @param rPath boost path to an existent file.
     */
    Datafile ( const fs::path& rPath, TYPES type, FORMAT format = Datafile::DBF, MODE mode = INPUT ) throw ( DatafileException )
    {
      std::cout<<"New(1) datafile: "<<rPath.generic_string<std::string>()<<std::endl;
      
        m_type = type;
        m_format = format;
        m_mode = mode;
//	mp_self = boost::const_pointer_cast<Datafile>(shared_from_this());
        mp_data.reset( new math::matrix() );
        if ( m_mode == OUTPUT ) m_path = fs::system_complete ( rPath );
        else
        {
            fs::exists ( fs::system_complete ( rPath ) ) ? m_path = fs::system_complete ( rPath )
                    : throw DatafileException ( DatafileException::FILE_NOT_EXISTS, rPath.generic_string<std::string>() );
        }
    }
    /** Constructor
     * Creates a new Datafile representation.
     * @param rPath string representation of the existent file.
     */
    Datafile ( const std::string& rPath, TYPES type, FORMAT format, MODE mode = INPUT ) throw ( DatafileException )
    {
            std::cout<<"New(2) datafile: "<<rPath<<std::endl;

        m_type = type;
        m_format = format;
        m_mode = mode;
//	mp_self = boost::const_pointer_cast<Datafile>(shared_from_this());
        mp_data.reset(new math::matrix());

        if ( m_mode == OUTPUT ) m_path = fs::system_complete ( fs::path ( rPath ) );
        else
        {
            fs::exists ( fs::system_complete ( rPath ) ) ? m_path = fs::system_complete ( fs::path ( rPath ) )
                    : throw DatafileException ( DatafileException::FILE_NOT_EXISTS, rPath );
        }
    }
    /** Copy constructor.
     *
     * @param rFrom The value to copy to this object.
     */
    Datafile ( const Datafile& r_datafile )
    {
            std::cout<<"Copy datafile: "<<r_datafile.getPath()<<std::endl;

        m_type = r_datafile.m_type;
        m_format = r_datafile.m_format;
        m_mode = r_datafile.m_mode;
        m_path = r_datafile.m_path;
//	mp_self = r_datafile.mp_self;
        mp_data = r_datafile.mp_data;
    }
    /// Default destructor 
    ~Datafile() { mp_data->clear(); }

    /// Gets the file name
    /// @return the name of the file
    std::string
    getFileName() const
    {
        return m_path.filename().generic_string<std::string>();
    }
    /// Gets the path to the file
    /// @return the path to the file
    std::string
    getParent() const throw ( DatafileException )
    {
        if ( !m_path.has_parent_path() )
            throw DatafileException ( DatafileException::NULL_PARENT );
        return m_path.parent_path().string();
    }
    /// Gets full path to file
    /// @return the path including the file name
    std::string
    getPath() const
    {
        return m_path.generic_string<std::string>();
    }
    /// Create directory
    bool
    create_directory()
    {
        fs::is_directory ( m_path.parent_path() ) ? fs::create_directory ( m_path ) : throw DatafileException ( DatafileException::FILE_NOT_EXISTS );
        return true;
    }
    /// Pointer to matrix data representation of datafile parsed
    math::matrix_ptr
    GetData() const
    {
        return mp_data;
    }
    /// Pointer to self instance    
    const_datafile_ptr
    GetSelfPointer() const
    {
        return boost::const_pointer_cast<Datafile>(shared_from_this());
    }
protected:

private:  
    fs::path m_path;   //< datafile represented
    TYPES    m_type;   //< datafile type
    FORMAT   m_format; //< datafile format
    MODE     m_mode;   //< datafile mode

    math::matrix_ptr mp_data; //< Pointer to matrix data representation of datafile
  
};//end class

typedef boost::shared_ptr<Datafile> datafile_ptr; //< Datafile pointer redifinition on namespace
typedef boost::shared_ptr<Datafile const> const_datafile_ptr; //< Datafile const pointer redifinition on namespace

} /// @} //namespace io
} //namespace LandUseModel
