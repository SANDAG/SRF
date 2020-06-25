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
#include <m2l/math/functions.hpp>

#include <math/muland_tools.hpp>
#include <math/muland_functions.hpp>
#include <data/muland_data.hpp>

namespace muland
{
  /** Evaluates location according to definition
 * \f[ H_{hvi} = S_{vi} \wedge P_{hvi} \f]*/
template<class DATA>
matrix
LocationFn(DATA* mp_data_)
{
    matrix S_hvi = ublas::outer_prod ( mp_data_->ones_h, mp_data_->S_vi ); /// \f$ S_{vi} \f$ dimension conversion as \f$ S_{hvi} = 1_{h} \wedge S_{vi} \f$
    /// New location \f$  H_{hvi} = S_{hvi} P_{hvi} \f$ 
    mp_data_->H_hvi = ublas::element_prod ( S_hvi, mp_data_->P_hvi );
    return mp_data_->H_hvi;
}

/// @brief Computes location probability matrix
template<class DATA>
int
LocationProbFn(DATA* mp_data_)
{
    /** First we obtain the total bid as \f$ B\_hvi = b_{hvi} + b_h \wedge 1_{vi} \f$ */
    matrix B_hvi_ = mp_data_->b_hvi + ublas::outer_prod ( mp_data_->b_h, mp_data_->ones_vi );
    /** Then we calculate \f$  Hh\_phi\_exp\_B\_hvi = H_h \wedge 1_{vi} \phi_{hvi} \exp(B_{hvi}) \f$ */
    B_hvi_ = functions::matrix_exp ( B_hvi_, 1.0 );

    matrix Hh_phi_exp_B_hvi_ =
        ublas::element_prod ( ublas::outer_prod ( matrix_column ( mp_data_->total_demand_matrix, 2 ), mp_data_->ones_vi ),
                              ublas::element_prod ( mp_data_->phi_hvi, B_hvi_ ) );
    /** Then for each market \f$ m \f$ */
    mp_data_->P_hvi = mp_data_->zero_h_vi; /* reset probability */
    for ( unsigned m = 0; m < mp_data_->n_m; m++ )
    {
        /** \f[ Hh\_phi\_exp\_B\_hvi\_by\_m = H_h \phi_{hvi} \exp(B_{hvi}) \ h \in \Omega_{vi} \f] */
        matrix Hh_phi_exp_B_hvi_by_m_ = ublas::element_prod ( Hh_phi_exp_B_hvi_, mp_data_->m_idx ( m ) );
        for ( unsigned j = 0; j < mp_data_->n_vi; j++ )
        {
            /** \f[ sum\_by\_h = \sum_{g \in \Omega_{vi}} H_g \phi_{gvi}  \exp(B_{gvi}) \f] */
            double sum_by_h_ = ublas::sum ( matrix_column ( Hh_phi_exp_B_hvi_by_m_, j ) );
            /* If sum_by_h_ != 0 then evaluate probability else zero */
            if ( sum_by_h_ ) matrix_column ( Hh_phi_exp_B_hvi_by_m_, j ) /= sum_by_h_;
        }
        /** Finally \f[ P\_hvi = \frac {H_h \phi_{hvi} \exp(B_{hvi})}{\sum_{g \in \Omega_{vi}} H_g \phi_{gvi}  \exp(B_{gvi})} h \in \Omega_{vi} \f] */
        mp_data_->P_hvi = mp_data_->P_hvi + Hh_phi_exp_B_hvi_by_m_;
    }

    return 0;
}

/// @brief Bid computation \f$ b_{hvi} \f$
template<class DATA>
int
BidFn(DATA* mp_data_)
{
    mp_data_->b_hvi = mp_data_->zero_h_vi; // bid must be reseted before adding
    /// First we iterate over the bid function definition \f[ b_{hvi}^{function\_def} = \alpha  x^\beta  y^\gamma \forall h \in H_m \f]
    for ( unsigned i = 0; i < mp_data_->bids_fn.size1(); i++ )
    {
        /// Get the agents involved in the bidding definition \f$ \forall h \in H_m \f$
        unsigned market = mp_data_->bids_fn ( i,1 );

        vector h_m_idx  = ublas::matrix_column<sparse_matrix> ( mp_data_->hxm_idx, market-1 ); //market definitions start in 1 but idx in 0
        vector vi_m_idx = ublas::matrix_column<sparse_matrix> ( mp_data_->vixm_idx, market-1 ); //market definitions start in 1 but idx in 0
        /// Get the agents bidding in the aggregated category
        unsigned h_aggregated = mp_data_->bids_fn ( i,2 );
        /// Then evaluate for each agent his bid definition \f$ b_{hvi} = \alpha x_{vi}^\beta y_{vi}^\gamma \forall vi \in R_m \f$
        for ( unsigned h = 0; h < h_m_idx.size(); h++ )
        {
            // unsigned h = idx::findH(mp_data_->agents_matrix(h_m, 1)); // should be a reverse key search for generalization
            if ( h_m_idx ( h ) == 1 )
                if ( mp_data_->agents_matrix ( h,3 ) == h_aggregated ) // is a bidder
                {
                    // Build function definition
                    /// Notice that x,y can be of any dimensions h,v,i. Then we must repeat values to normalize as vi dimension vector
                    /// First we get x
                    vector x_h = vector ( mp_data_->n_vi );
                    if ( mp_data_->bids_fn ( i,5 ) != 0 ) // x_h in agents
                        x_h = vi_m_idx * mp_data_->agents_matrix ( h, mp_data_->bids_fn ( i,5 ) );
                    else if ( mp_data_->bids_fn ( i,6 ) !=0 ) // x_vi in real estates
                        x_h = ublas::element_prod ( matrix_column ( mp_data_->real_estate_matrix, mp_data_->bids_fn ( i,6 ) ),
                                                    vi_m_idx );
                    else if ( mp_data_->bids_fn ( i,7 ) != 0 ) // x_hi in accessibility-attraction
                    {
                        ( mp_data_->bids_fn ( i,7 ) == 3 ) ?
                        x_h = matrix_row ( mp_data_->acc_matrix,h ) :
                              x_h = matrix_row ( mp_data_->att_matrix,h );

                        x_h = ublas::element_prod ( FixDimensions ( x_h, mp_data_->n_i, mp_data_->n_vi ),
                                                    vi_m_idx );
                    }
                    else if ( mp_data_->bids_fn ( i,8 ) != 0 ) // x_i in zones
                    {
                        x_h = matrix_column ( mp_data_->zones_matrix, mp_data_->bids_fn ( i,8 ) );
                        x_h = ublas::element_prod ( FixDimensions ( x_h, mp_data_->n_i, mp_data_->n_vi ),
                                                    vi_m_idx );
                    }
                    ( mp_data_->bids_fn ( i,9 ) < 0 ) ?
                    x_h = functions::vector_pow_mask ( x_h, mp_data_->bids_fn ( i,9 ), vi_m_idx ) :
                    x_h = functions::vector_pow ( x_h, mp_data_->bids_fn ( i,9 ) );

                    /// Then we get y
                    vector y_h = vector ( mp_data_->n_vi );
                    if ( mp_data_->bids_fn ( i,10 ) != 0 ) // y_h in agents
                        y_h = vi_m_idx * mp_data_->agents_matrix ( h, mp_data_->bids_fn ( i,10 ) );
                    else if ( mp_data_->bids_fn ( i,11 ) !=0 ) // y_vi in real estates
                        y_h = ublas::element_prod ( matrix_column ( mp_data_->real_estate_matrix, mp_data_->bids_fn ( i,11 ) ),
                                                    vi_m_idx );
                    else if ( mp_data_->bids_fn ( i,12 ) != 0 ) // y_hi in accessibility-attraction
                    {
                        ( mp_data_->bids_fn ( i,12 ) == 3 ) ?
                        y_h = matrix_row ( mp_data_->acc_matrix,h ) :
                              y_h = matrix_row ( mp_data_->att_matrix,h );
                        y_h = ublas::element_prod ( FixDimensions ( y_h, mp_data_->n_i, mp_data_->n_vi ),
                                                    vi_m_idx );
                    }
                    else if ( mp_data_->bids_fn ( i,13 ) != 0 ) // y_i in zones
                    {
                        y_h = matrix_column ( mp_data_->zones_matrix, mp_data_->bids_fn ( i,13 ) );
                        y_h = ublas::element_prod ( FixDimensions ( y_h, mp_data_->n_i, mp_data_->n_vi ),
                                                    vi_m_idx );
                    }
                    else // y not used
                    {
                        y_h = mp_data_->ones_vi;
                    }
                    ( mp_data_->bids_fn ( i,14 ) < 0 ) ?
                    y_h = functions::vector_pow_mask ( y_h, mp_data_->bids_fn ( i,14 ), vi_m_idx ) :
                    y_h = functions::vector_pow ( y_h, mp_data_->bids_fn ( i,14 ) );

                    /// Lastly we evaluate \f$ b_{hvi} = \alpha x^\beta y^\gamma \f$
                    matrix_row ( mp_data_->b_hvi, h ) = matrix_row ( mp_data_->b_hvi, h ) +
                                                        mp_data_->bids_fn ( i,4 ) * ublas::element_prod ( x_h, y_h );
                }// is a bidder
        }// h in market
    }// bid definitions
    /// Finally we add subsidies-taxes to bid definitions and apply exogenous phi to resulting bids
    /// \f[ b_{hvi} = \phi_{hvi}^e (b_{hvi}^{function\_def} + subsidies_{hvi} + bid^{adjustments}) \f]
    mp_data_->b_hvi = mp_data_->b_hvi + mp_data_->bid_adjustment_matrix + mp_data_->subsidies_matrix;
    // Everything went allright return exit code 0
    return 0;

}

/** @brief Rents function computation
 **/
template<class DATA>
vector
RentsFn(DATA* mp_data_)
{
    /// First we reset rents to zero \f$ rents = 0_{vi} \f$
    mp_data_->r_vi = mp_data_->zero_vi; // rents must be reseted before adding

    /// Then rents function definitions are evaluated
    /// First we iterate over the rents function definition \f[ r_{vi} = \alpha  x^\beta  y^\gamma \forall vi \in R_m \f]
    for ( unsigned i = 0; i < mp_data_->rents_fn.size1(); i++ )
    {
        unsigned market = mp_data_->rents_fn ( i,1 ) -1;
        vector vixm_idx = ublas::matrix_column<sparse_matrix> ( mp_data_->vixm_idx, market );
        mp_data_->r_mu_m ( market ) = mp_data_->rents_fn ( i,3 );
        /// Then evaluate each rent definition \f$ r_{vi} = \alpha x_{vi}^\beta y_{vi}^\gamma \forall vi \in R_m \f$
        // Build function definition
        /// Notice that x,y can be of any dimensions v,i. Then we must repeat values to normalize as vi dimension vector
        /// First we get x
        vector x = mp_data_->ones_vi;
        if ( mp_data_->rents_fn ( i,5 ) !=0 ) // x_vi in real estates
            x = ublas::element_prod ( matrix_column ( mp_data_->real_estate_matrix, mp_data_->rents_fn ( i,5 ) ), vixm_idx );
        else if ( mp_data_->rents_fn ( i,6 ) != 0 ) // x_i in zones
        {
            x = matrix_column ( mp_data_->zones_matrix, mp_data_->rents_fn ( i,6 ) );
            x = FixDimensions ( x, mp_data_->n_i, mp_data_->n_vi );
            x = ublas::element_prod ( x, vixm_idx );
        }

        ( mp_data_->rents_fn ( i,7 ) < 0 ) ?
        x = functions::vector_pow_mask ( x, mp_data_->rents_fn ( i,7 ), vixm_idx ) :
            x = functions::vector_pow ( x, mp_data_->rents_fn ( i,7 ) );

        /// Then we get y
        vector y = mp_data_->ones_vi;
        if ( mp_data_->rents_fn ( i,8 ) !=0 ) // y_vi in real estates
            y = ublas::element_prod ( matrix_column ( mp_data_->real_estate_matrix, mp_data_->rents_fn ( i,8 ) ), vixm_idx );
        else if ( mp_data_->rents_fn ( i,9 ) != 0 ) // y_i in zones
        {
            y = matrix_column ( mp_data_->zones_matrix, mp_data_->rents_fn ( i,9 ) );
            y = FixDimensions ( y, mp_data_->n_i, mp_data_->n_vi );
            y = ublas::element_prod ( y, vixm_idx );
        }

        ( mp_data_->rents_fn ( i,10 ) < 0 ) ?
        y = functions::vector_pow_mask ( y, mp_data_->rents_fn ( i,10 ), vixm_idx ) :
            y = functions::vector_pow ( y, mp_data_->rents_fn ( i,10 ) );

        /// Lastly we evaluate \f$ r_{vi} = \alpha x^\beta y^\gamma \f$
        mp_data_->r_vi = mp_data_->r_vi + mp_data_->rents_fn ( i,4 ) * ublas::element_prod ( x, y );
    }    
    /// Then we compute logsum expression
    vector rent_logsum = mp_data_->zero_vi;
    /// \f[ H\_phi\_exp\_B = H_h \wedge 1_{vi} \cdot \phi_{hvi} \cdot \exp (b_{hvi} + b_h \wedge 1_{vi})\f]
    matrix H_h_ = ublas::outer_prod ( matrix_column ( mp_data_->total_demand_matrix, 2 ), mp_data_->ones_vi );
    matrix B_hvi_ = mp_data_->b_hvi + ublas::outer_prod ( mp_data_->b_h, mp_data_->ones_vi );
    matrix exp_B_hvi_ = functions::matrix_exp ( B_hvi_, 1 );
    matrix H_phi_exp_B_ = ublas::element_prod ( H_h_, ublas::element_prod ( mp_data_->phi_hvi, exp_B_hvi_ ) );
   
    /// Then we apply sum by market to get
    /// \f[ sum\_H\_phi\_exp\_B\_by\_m =
    ///          \sum_g H_g \wedge 1_{vi} \cdot \phi_{gvi} \cdot \exp (b_{gvi} + b_g \wedge 1_{vi}) \forall h \in A_m, vi \in R_m \f]
    matrix sum_H_phi_exp_B_by_m_ ( mp_data_->n_vi, mp_data_->n_m );
    for ( unsigned m = 0; m < mp_data_->n_m; m++ )
    {
        matrix sum_by_m_ = ublas::element_prod ( H_phi_exp_B_, mp_data_->m_idx ( m ) );
        for ( unsigned vi =0; vi < mp_data_->n_vi; vi++ )
            sum_H_phi_exp_B_by_m_ ( vi, m ) = ublas::sum ( matrix_column ( sum_by_m_, vi ) );
    }
    
    /// Then we compute the logsum rent component
    /// \f[ r_{vi}^{logsum} = \frac{1_{vi}}{\mu_{vi}} \cdot
    ///    (\ln (\sum_g H_g \wedge 1_{vi} \cdot \phi_{gvi} \cdot \exp (b_{gvi} + b_g \wedge 1_{vi}) ) + \gamma ) \forall (v,i) \in R_m\f]
    for ( unsigned m = 0; m < mp_data_->n_m; m++ )
        for ( unsigned vi = 0; vi < mp_data_->n_vi; vi++ )
            if ( mp_data_->vixm_idx ( vi, m ) == 1 && mp_data_->r_mu_m(m) ) // evaluates only if selected vi is active in market and there is a mu definition for the market
	        rent_logsum ( vi ) = rent_logsum ( vi )
                                     + 1/mp_data_->r_mu_m ( m ) * ( std::log ( sum_H_phi_exp_B_by_m_ ( vi, m ) ) ); 
              
    /// Then we add to get the final rents \f$ r_{vi} = r_{vi}^{[logsum]} + r_{vi}^{[function]} + r_{vi}^{[adjustment]} \f$
    mp_data_->r_vi = rent_logsum + mp_data_->r_vi + mp_data_->rents_adjustment_vector;
    return mp_data_->r_vi;
}


// explicit instantiation
template int BidFn(LandData*);
template matrix LocationFn(LandData*);
template int LocationProbFn(LandData*);
template vector RentsFn(LandData*);

}//namespaceland

