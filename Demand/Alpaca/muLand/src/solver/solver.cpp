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


#include <math/muland_algorithm.hpp>
#include <solver/configurator.hpp> 

#include <m2l/solver/solver.hpp>

using namespace m2l::solver;
using namespace m2l;
using namespace muland;


// static members 
Solver* Solver::mpsInstance = NULL; ///< Unique instance of Solver 

Solver::status
Solver::Init()
{
    std::cout << "Initializing values for execution ...";
    
    muland::LandData* data = muland::LandData::GetInstance();
    configurator* configurator = configurator::GetInstance();
    
    unsigned h = configurator->mp_agents->GetData()->size1();
    unsigned vi = configurator->mp_real_estates->GetData()->size1();
    unsigned i  = configurator->mp_zones->GetData()->size1();
    unsigned m  = configurator->mp_agents->GetData()->at_element( h -1, 2 );
    data->Init( h, vi, i, m);

    data->zones_matrix  = *configurator->mp_zones->GetData(); //data->zones_matrix_file;
    data->agents_matrix = *configurator->mp_agents->GetData(); //data->agents_matrix_file;
    data->real_estate_matrix  = *configurator->mp_real_estates->GetData(); //data->real_estate_matrix_file;
    data->total_demand_matrix = *configurator->mp_demand->GetData(); //data->total_demand_matrix_file;
    data->bids_fn  = *configurator->mp_bid_function->GetData();
    data->rents_fn = *configurator->mp_rent_function->GetData();
    
    /// First we genereate our index hashes 
    idx::viIdxGen ( data->real_estate_matrix );
    idx::vIdxGen  ( data->real_estate_matrix );
    idx::hIdxGen  ( data->agents_matrix );
    idx::iIdxGen  ( data->zones_matrix );
    idx::MarketIdxGen ( data );


    data->H_hvi  = data->zero_h_vi;
    data->b_hvi  = data->zero_h_vi;
    data->r_vi   = data->zero_vi;
    data->r_mu_m = zero_vector ( m );
    data->P_hvi  = data->zero_h_vi;
    data->b_h    = zero_vector ( h );

    // Sparce matrix generation
    matrix phi_matrix_file = *configurator->mp_demand_exogenous_cutoff->GetData();    
    for ( unsigned j = 0; j < phi_matrix_file.size1(); j++ )
        if ( phi_matrix_file ( j, 4 ) ) 
            data->phi_hvi ( idx::findH ( phi_matrix_file ( j, 1 ) ), idx::findVi ( phi_matrix_file ( j, 2 ), phi_matrix_file ( j, 3 ) ) ) = phi_matrix_file ( j, 4 );
    matrix bid_adjustment_matrix_file = *configurator->mp_bid_adjustment->GetData();    
    for ( unsigned j = 0; j < bid_adjustment_matrix_file.size1(); j++ )
        if ( bid_adjustment_matrix_file ( j, 4 ) ) 
            data->bid_adjustment_matrix ( idx::findH ( bid_adjustment_matrix_file ( j, 1 ) ), idx::findVi ( bid_adjustment_matrix_file ( j, 2 ), bid_adjustment_matrix_file ( j, 3 ) ) ) = bid_adjustment_matrix_file ( j, 4 );
    matrix subsidies_matrix_file = *configurator->mp_subsidies->GetData();    
    for ( unsigned j = 0; j < subsidies_matrix_file.size1(); j++ )
        if ( subsidies_matrix_file ( j, 4 ) ) 
            data->subsidies_matrix ( idx::findH ( subsidies_matrix_file ( j, 1 ) ), idx::findVi ( subsidies_matrix_file ( j, 2 ), subsidies_matrix_file ( j, 3 ) ) ) = subsidies_matrix_file ( j, 4 );

    matrix acc_att_matrix_file = *configurator->mp_access_attraction->GetData();     
    for ( unsigned j = 0; j < acc_att_matrix_file.size1(); j++ )
        data->acc_matrix ( idx::findH ( acc_att_matrix_file ( j, 1 ) ), idx::findI ( acc_att_matrix_file ( j, 2 ) ) ) = acc_att_matrix_file ( j, 3 );
    for ( unsigned j = 0; j < acc_att_matrix_file.size1(); j++ )
        data->att_matrix ( idx::findH ( acc_att_matrix_file ( j, 1 ) ), idx::findI ( acc_att_matrix_file ( j, 2 ) ) ) = acc_att_matrix_file ( j, 4 );

    matrix rent_adjustment = *configurator->mp_rent_adjustment->GetData();
    data->rents_adjustment_vector = matrix_column ( rent_adjustment, 3 );
    matrix supply = *configurator->mp_supply->GetData();
    data->S_vi = matrix_column ( supply , 3 );

    return m_status;
}

Solver::status
Solver::Close()
{
    std::cout << "Finishing execution. Saving files\n" ;
    return configurator::GetInstance()->save();        
}

Solver::status
Solver::Solve()
{
    math::algorithm_ptr model_solver = algorithm_ptr( new muland::MuLand() );

    m_status = Init();        
    m_status = model_solver->Execute();
    m_status = Close();
    
    return m_status;
}
