import React, { Component } from 'react';
import ReactDOM from 'react-dom';
import { HashRouter, Route, Redirect, Link } from 'react-router-dom';
import Nav from './components/Nav';
// import LoggedInNav from './components/LoggedInNav';
import About from './components/About';
import Login from './components/Login';
import Plants from './components/Plants';
import PlantInfo from './components/PlantInfo';

class App extends Component { 
    constructor() {
        super();
        this.state = {

        };
    }

    render() {
        return (
            <HashRouter>
                <Nav />
                <Route exact path='/' render={ () => <h1>Homepage</h1> } />
                <Route exact path='/about' component={ About } />
                <Route exact path='/login' component={ Login } />
                <Route exact path='/register' render={ () => <h1>We will probably never use this</h1> } />

                <Route exact path='/user/plants' component={ Plants } />
                <Route exact path='/user/account' render={ () => <h1>Account info</h1> } />
                <Route path='/user/plants/:id' component={ PlantInfo } />
            </HashRouter>
        );
    }
};

const root = document.querySelector('#root');
ReactDOM.render(<App />, root);