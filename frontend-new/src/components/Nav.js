import React, {Component} from 'react';
import { Link } from 'react-router-dom';

const Nav = () => {
    return (
        <nav>
            <div className="leftnav">
                <Link to='/'>Home</Link>
                <Link to='/about'>About</Link>
            </div>
            <div className="rightnav">
                <Link to='/login'>Login</Link>
                <Link to='/register'>Register</Link>
            </div>
        </nav>
    );
};

export default Nav;