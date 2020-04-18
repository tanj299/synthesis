import React, { Component } from 'react';
import BackButton from './BackButton';

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
        const { login, history } = this.props;
        return (
            <div>
                <BackButton history={history} />
                <div className='form'>
                    <form onSubmit={ ev => {
                                ev.preventDefault();
                                login();
                            }
                        }
                        >
                        <input type='text' value={username} onChange={ ev => this.setState({ username: ev.target.value }) } />
                        <input type='password' value={password} onChange={ ev => this.setState({ password: ev.target.value }) } />
                        <input type='submit' value='Login' />
                    </form>
                </div>
            </div>
        );
    }
};
 
export default Login;