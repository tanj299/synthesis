import React, { Component } from 'react';

class Nav extends Component {
    constructor() {
        super();
        this.state = {
            clicked: false
        };
    }

    render() {
        const { clicked } = this.state;
        const { history } = this.props;

        return (
            <div className='homepagediv'>
                <nav className='text-focus-in'>
                    <div className="buttons">
                        {/* <div>
                            <a onClick={ () => {
                                    // this.setState({clicked: true });
                                }} 
                                className={clicked ? 'text-blur-out home' : 'home'}>
                                <span>HOMEPAGE</span>
                            </a>
                        </div> */}

                        {/* <div>
                            <a onClick={ () => {
                                    this.setState({clicked: true });
                                    setTimeout(() => history.push('/about'), 700);
                                }} 
                                className={clicked ? 'text-blur-out about' : 'about'}>
                                <span>ABOUT</span>
                            </a>
                        </div> */}

                        <div>
                            <a onClick={ () => {
                                    this.setState({clicked: true });
                                    setTimeout(() => history.push('/login'), 700);
                                }}
                                className={clicked ? 'text-blur-out login' : 'login'}>
                                <span>LOGIN</span>
                            </a>
                        </div>

                        <div>
                            <a onClick={ () => {
                                    this.setState({clicked: true });
                                    setTimeout(() => history.push('/register'), 700);
                                }} 
                                className={clicked ? 'text-blur-out register' : 'register'}>
                                <span>REGISTER</span>
                            </a>
                        </div>
                    </div>
                </nav>
                <h1 className={clicked ? 'title slide-out-blurred-bottom register' : 'title slide-in-blurred-bottom'}>Synthesis: The Automated Garden</h1>
            </div>
        );
    }
};

export default Nav;