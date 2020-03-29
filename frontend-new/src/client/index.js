import React, { Component } from 'react';
import { render } from 'react-dom';
import { HashRouter, Route, Redirect } from 'react-router-dom';

//components 
import Nav from './components/Nav';
import Login from './components/Login';

//authorized
import Plants from './components/authorized/Plants';
import PlantInfo from './components/authorized/PlantInfo';
import Nav_ from './components/authorized/Nav_';

class App extends Component{
	constructor(){
		super();
		this.state = {
			authorized: false
		};
	}
	componentDidMount(){

	}
	render(){
		const { authorized } = this.state;
		const login = () => {
			this.setState({ authorized: true });
        };
        const logout = () => {
            this.setState({ authorized: false });
        };
		return (
		<HashRouter>
			<Route path='/' render={ () => authorized ? <Nav_ logout={ logout } /> : <Nav /> } />
			<Route exact path='/login' render={ () => <Login login={ login } /> } />
            <Route render={ () => authorized ?
                                                ( <main>
                                                    <Redirect to='/user/plants' />
													<Route exact path='/user/plants' render={ () => <Plants /> } />
                                                  </main>
                                                )
                                                : <Redirect to='/login' /> 
                                                } />
			<Route exact path='/user/plants/:id' render={ props => authorized ? 
																		  ( <main>
																				<PlantInfo {...props} />
																			</main>
																		  )
																		  : <Redirect to='/login' />
																		  } />
		</HashRouter>
		);
	}
};

const root = document.querySelector('#root');
render(<App />, root);



