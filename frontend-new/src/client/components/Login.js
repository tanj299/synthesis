import React, { Component } from 'react';
import BackButton from './BackButton';

import LoginRegisterNav from './LoginRegisterNav';

class Login extends Component {
    constructor() {
        super();
        this.state = {
            username: 'janesmith@gmail.com',
            password: 'test',
            closed: false
        };
    }

    render() {
        const { username, password, closed } = this.state;
        const { login, history } = this.props;

        const close = () => {
            this.setState({ closed: true });
        }

        return (
            <div className='loginpage'>
                <div className='backbutton' onClick={ () => this.setState({ closed: true }) } >
                    <BackButton time='500' history={history} />
                </div>
                <div className={closed ? 'form slide-out-right' : 'slide-in-right form'}>
                    <form onSubmit={ ev => {
                                ev.preventDefault();
                                login(username);
                            }
                        }
                        >
                        <LoginRegisterNav history={history} close={close}/>
                        <h1 className='loginh1'>Login</h1>
                        <input type='text' placeholder='Username' value={username} onChange={ ev => this.setState({ username: ev.target.value }) } />
                        <input type='password' placeholder='Password' value={password} onChange={ ev => this.setState({ password: ev.target.value }) } />
                        <button className='button'><span>Login</span></button>
                    </form>
                </div>
            </div>
        );
    }
};
 
export default Login;