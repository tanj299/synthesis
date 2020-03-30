import React from 'react';
import { Link } from 'react-router-dom';

const Nav = props => {
    return (
        <nav>
            <Link className='title' to='/'>Synthesis</Link>
            <Link to='/about'>About</Link>
            <Link to='/login'>Login</Link>
            <Link to='/register'>Register</Link>
        </nav>
    );
};

export default Nav;