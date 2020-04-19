import React, { Component } from 'react';
import BackButton from './BackButton';

import LoginRegisterNav from './LoginRegisterNav';

class Register extends Component {
    constructor() {
        super();
        this.state = {
            username: 'test',
            password: 'test',
            email: 'test@gmail.com',
            closed: false
        };
    }

    render() {
        const { username, password, email, closed } = this.state;
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
                                login();
                            }
                        }
                        >
                        <LoginRegisterNav history={history} close={close} />
                        <h1 className='loginh1'>Register</h1>
                        <input type='text' value={username} onChange={ ev => this.setState({ username: ev.target.value }) } />
                        <input type='email' value={email} onChange={ ev => this.setState({ email: ev.target.value }) } />
                        <input type='password' value={password} onChange={ ev => this.setState({ password: ev.target.value }) } />
                        <input type='submit' value='Register' />
                    </form>
                </div>
            </div>
        );
    }
};
 
export default Register;