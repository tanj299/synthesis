import React, { Component } from 'react';
import { render } from 'react-dom';
import { HashRouter, Route, Redirect } from 'react-router-dom';

//components 
import Nav from './components/Nav';
import Login from './components/Login';
import Register from './components/Register';
import About from './components/About';

//authorized
import Plants from './components/authorized/Plants';
import PlantInfo from './components/authorized/PlantInfo';
import Nav_ from './components/authorized/Nav_';

/* git subtree push --prefix frontend-new heroku master */

class App extends Component{
	constructor(){
		super();
		this.state = {
			authorized: false,
			email: ''
		};
	}

	render(){
		const { authorized, email } = this.state;
		const login = email => {
			this.setState({ authorized: true, email: email });
        };
        const logout = () => {
            this.setState({ authorized: false, email: '' });
        };
		return (
		<HashRouter>
			<Route exact path='/' render={ props => authorized ? <Nav_ logout={ logout } {...props} /> : <Nav {...props} /> } />
			<Route exact path='/login' render={ props => <Login login={login} {...props} /> } />
			<Route exact path='/about' render={ props => <About {...props} /> } />
			<Route exact path='/register' render={ props => <Register {...props } /> } /> 
            <Route render={ () => authorized ?
                                                ( <main>
                                                    <Redirect to='/user/plants' />
													<Route exact path='/user/plants' render={ props => <Plants {...props} email={email} /> } />
                                                  </main>
                                                )
                                                : ''
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



