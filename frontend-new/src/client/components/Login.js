import React, { Component } from 'react';

class Login extends Component {
    constructor() {
        super();
        this.state = {
            username: 'test',
            password: 'test'
        };
    }

    render() {
        const { username, password } = this.state;
        const { login } = this.props;
        return (
            <form onSubmit={ ev => {
                        ev.preventDefault();
                        login();
                    }
                }>
                <input type='text' value={username} onChange={ ev => this.setState({ username: ev.target.value }) } />
                <input type='password' value={password} onChange={ ev => this.setState({ password: ev.target.value }) } />
                <button>Login</button>
            </form>
        );
    }
};
 
export default Login;