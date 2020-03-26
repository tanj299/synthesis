import React, {Component} from 'react';

class Login extends Component { 
    constructor() {
        super();
        this.state = {
            username: 'test',
            password: 'test'
        };
    }
    render() {
        const { login } = this.props;
        const { username, password } = this.state;
        return (
            <div className="form">
                <form className='loginform' onSubmit={ () => login() } >
                    <input type="text" value={ username } onChange={ ev => this.setState({ username: ev.target.value }) } />
                    <input type="password" value={ password } onChange={ ev => this.setState({ password: ev.target.value }) } />
                    <button>Login</button>
                </form>
            </div>
        );
    }
};

export default Login