import React, { Component } from 'react';
import Form from './Form';
import Plants from './Plants';

class App extends Component { 
    constructor() {
        super();
        this.state = {

        };
    }
    render() {
        return (
            <main>
                <Form/>
                <Plants />
            </main>
        );
    }
};

export default App;