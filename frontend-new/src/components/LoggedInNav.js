import React, {Component} from 'react';
import { Link } from 'react-router-dom';

const LoggedInNav = props => {
    const { logout } = props;
    return (
        <nav>
            <div className="leftnav">
                <Link to='/'>Home</Link>
                <Link to='/about'>About</Link>
            </div>
            <div className="rightnav">
                <Link to='/user/plants'>My Plants</Link>
                <a href='/' onClick={ () => logout() } >Log out</a>
            </div>
        </nav>
    );
};

export default LoggedInNav;