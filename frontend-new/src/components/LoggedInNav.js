import React, {Component} from 'react';
import { Link } from 'react-router-dom';

const LoggedInNav = () => {
    return (
        <nav>
            <div className="leftnav">
                <Link to='/'>Home</Link>
                <Link to='/about'>About</Link>
            </div>
            <div className="rightnav">
                <Link to='/account'>Account Info</Link>
                <a href='/' >Log out</a>
            </div>
        </nav>
    );
};

export default LoggedInNav;