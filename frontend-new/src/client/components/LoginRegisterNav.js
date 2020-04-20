import React, { Component } from 'react';

class LoginRegisterNav extends Component {
    constructor() {
        super();
        this.state = {
            closed: false
        };
    }

    render() {
        const { history, close } = this.props;
        return (
            <nav className='loginregisternav'>
               <a   className={ history.location.pathname.slice(1) === 'login' ? 'highlight hlhover' : 'hlhover' }
                    onClick={ () => {
                        if(history.location.pathname.slice(1) !== 'login') {
                            close();
                            setTimeout( () => {
                                history.push('/login');
                            }, 500 )
                        }
                    }
                }
                >
                Login</a>
                <a  className={ history.location.pathname.slice(1) === 'register' ? 'highlight hlhover' : 'hlhover' }
                    onClick={ () => {
                        if(history.location.pathname.slice(1) !== 'register') {
                            close();
                            setTimeout( () => {
                                history.push('/register');
                            }, 500 )
                        }
                    }
                }
                >
                Register</a>
            </nav>
        );
    }
};

export default LoginRegisterNav;