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

#include <fstream>

#include <io/txt_datafile_reader.hpp>
#include <data/muland_data.hpp>

using namespace muland;

/********************************************************************/
template <typename VECTOR_TYPE>
void
txtDatafileReader::Tokenize
(const std::string& str, VECTOR_TYPE& tokens, const std::string& delimiters )
{
    // Skip delimiters at beginning.
    std::string::size_type lastPos = str.find_first_not_of(delimiters, 0);
    // Find first "non-delimiter".
    std::string::size_type pos = str.find_first_of(delimiters, lastPos);
    /* Skip delimiter - fix for consecutive delimiter */
    std::string::size_type delimiter_skipper = delimiters.size();
    std::string::size_type next;
    if (std::string::npos == pos && std::string::npos == lastPos)
        return;
    while (std::string::npos != next)
    {
        // Found a token, add it to the vector.
        tokens.push_back(str.substr(lastPos, pos - lastPos));
        // Skip delimiters.  Note the "not_of"
        next = str.find_first_of(delimiters, pos);
        lastPos = next + delimiter_skipper;
        // Find next "non-delimiter"
        pos = str.find_first_of(delimiters, lastPos);
    }
}

/********************************************************************/
template <typename MATRIX_TYPE>
int
txtDatafileReader::ReadMatrix
(MATRIX_TYPE rMatrix, std::ifstream& _file, unsigned lines)
{
    std::string buffer_;
    std::vector<std::string> tokens_;
    
    // first line of headers
    std::getline( _file, buffer_);
    Tokenize(buffer_, tokens_);
    // Get sure rMatrix dimensions fits data stream 
    unsigned columns_ = tokens_.size();
    rMatrix->resize(lines, columns_ +1); // +1 for index
    tokens_.clear();

    for (unsigned i = 0; i < lines; i++)
    {
        std::getline( _file, buffer_);
        Tokenize(buffer_, tokens_);
        rMatrix->at_element(i, 0) = i;
        for (unsigned j = 0; j < columns_; j++)
            rMatrix->at_element(i, j+1) = strtod(tokens_[j].c_str(), NULL);
        
        tokens_.clear();
    }
    return 0;
}
/********************************************************************/
template <typename MATRIX_TYPE>
int
txtDatafileReader::Parse
(MATRIX_TYPE _destination )//, unsigned& _rows)
{
    unsigned lines_ = -1; // first line of headers
    std::string source_path_ = this->mp_datafile->getPath(); 
    std::ifstream ifstream_( source_path_.c_str() );
    std::ifstream lines_counter_( source_path_.c_str() );
    
    while ( ! lines_counter_.eof() ) 
    {
        std::getline(lines_counter_, source_path_ );
        if ( source_path_.size() != 0 ) lines_++;
    } 
    // dump file into matrix 
    return ReadMatrix(_destination, ifstream_, lines_);
}

/********************************************************************/
int
txtDatafileReader::Parse()
{
    return Parse( this->mp_datafile->GetData() );
}
