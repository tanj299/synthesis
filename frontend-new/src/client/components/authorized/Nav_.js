import React from 'react';
import { Link } from 'react-router-dom';

const Nav_ = props => {
    const { logout } = props;
    return (
        <nav>
            <Link className='title' to='/'>Synthesis</Link>
            <Link to='/about'>About</Link>
            <Link to='/user/plants'>My Plants</Link>
            <Link to='/' onClick={ () => logout() }>Log out</Link>
        </nav>
    );
};

export default Nav_;