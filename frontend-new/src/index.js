import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import { HashRouter, Route, Redirect, Link } from 'react-router-dom';
import Nav from './components/Nav';
import LoggedInNav from './components/LoggedInNav';
import About from './components/About';
import Login from './components/Login';
import Plants from './components/Plants';
import PlantInfo from './components/PlantInfo';

class App extends Component { 
    constructor() {
        super();
        this.state = {
            authenticated: false
        };
    }

    render() {
        const { authenticated } = this.state;

        const login = () => {
            this.setState({ authenticated: true });
        };

        const logout = () => {
            this.setState({ authenticated: false });
        };

        return (
            <HashRouter>
                <Route path='/' render={ () => authenticated ? <LoggedInNav logout={ logout } /> : <Nav /> } />
                <Route exact path='/' render={ () => <h1>Homepage</h1> } />
                <Route exact path='/about' component={ About } />
                <Route exact path='/login' render={ () => <Login login={ login } /> } />
                <Route exact path='/register' render={ () => <h1>We will probably never use this</h1> } />

                <Route render={ () => ( authenticated ? (<main>
                                                            <Redirect to='/user/plants' />
                                                            <Route exact path='/user/plants' 
                                                             render={ () => < Plants /> } />  
                                                        </main>) 
                                                        : <Redirect to='/login' /> )} />

                <Route exact path='/user/account' render={ () => <h1>Account info</h1> } />
                <Route path='/user/plants/:id' component={ PlantInfo } />
            </HashRouter>
        );
    }
};

const root = document.querySelector('#root');
ReactDOM.render(<App />, root);