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

//#include <m2l/math/functions.hpp>

namespace muland
{
 // using namespace m2l::math;
/// @addtogroup land
/// @{
/// land use model definitions
    /** 
     ** Computation of bid component according to definition
     ** \f[ b_h^n = - \ln (\sum_{vi} \frac{S_{vi} \phi_{hvi} \exp(b_{hvi})}{ \sum_{g} H_g \phi_{gvi} \exp(b_g^{n-1} + b_{gvi}) } ) \f]
     **/
    template<class DATA>
    int
    BhFn(DATA*);
    /// Evaluates de functional definition of bids
    /// \f[ b_{hvi} = \phi_{hvi}^e (b_{hvi}^{function\_def} + b_{hvi}^{adjustments} + subsidies_{hvi}) \f]
    /// With:
    /// \f[ b_{hvi}^{function\_def} = \alpha x_{[h|hi|vi]}^{\beta} y_{[h|hi|vi]}^{\gamma} \f]
    template<class DATA>
    int
    BidFn(DATA*);
    /// Evaluates the constant bid value to relate with rents level
    /// \f[ b_level = \overline{r} - \sum_{v \in R, i} \frac{S_{vi}\bigl[ \frac{1}{\mu} \ln \sum_g H_g \phi_{gvi} \exp^{ [\mu(b_g + b_{gvi}) ] } + b_{vi} \bigr] }{\sum_{h \in R} H_h} - \frac{\gamma}{\mu} \f]
    template<class DATA>
    storage_type
    B_LevelFx(DATA*);
    /** Evaluates location according to definition
     * \f[ H_{hvi} = S_{vi} \wedge P_{hvi} \f]*/
    template<class DATA> 
    matrix
    LocationFn(DATA*);
        /** Location probabilty is computed as follows:
     ** \f[ P_{h/vi} = \Biggl\lbrace \begin{matrix}
      0 & h \notin \Omega_{vi} \\
      \frac{\phi_{hvi}H_h\exp(\mu B_{hvi})}{\sum_{g \in \Omega_{gvi}} \phi_{gvi} H_g \exp(\mu B_{gvi})}  & h \in \Omega_{vi}
      \end{matrix} \f]
     **/
    template<class DATA>
    int
    LocationProbFn(DATA*);
    /** Costs are defined per simulation basis following the next structure:
     ** \f[ costs_{vi} = \sum \alpha X^{\beta} Y^\gamma \f]
     **/
    template<class DATA>
    vector
    CostsFn(DATA*);
    /** Rents are computed according to definition:
     ** \f[ r_{vi} = r_{vi}^{[logsum]} + r_{vi}^{[functional_def]} + r_{vi}^{[adjustment]} \f] 
     ** \f[ r_{vi}^{logsum} = \frac{1}{\mu_m}(\ln(\sum_{g \in A_m} H_g \phi_{gvi} \exp (\mu_m B_{gvi}) ) + \gamma  ) \forall (v,i) \in R_m, \forall m\f]
     ** \f[ r_{vi}^{functional\_def} = \alpha  x^\beta  y^\gamma \forall vi \in R_m \f]
     **/
    template<class DATA>
    vector
    RentsFn(DATA*);
    /** Computes the supply as defined on equation:
     ** \f[ S_{vi} = So_{vi} ( 1 - k_{vi} ) + ( \sum_{h \in A_m} H_h - \sum_{vi \in R_m} So_{vi} ( 1 - k_{vi} ) ) \f]
     **/
    template<class DATA>
    vector
    SupplyFn(DATA*);
    /** Moves the rents by a constant according to the simulation parameters given to retrieve real rents 
     ** It also modifies the results according to the new rents.
     **/
    template<class DATA>
    int
    RelativeToAbsoluteRents(DATA*);
/// @}
} //namespace 
