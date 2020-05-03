import React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faArrowCircleLeft } from '@fortawesome/free-solid-svg-icons';

const BackButton = ({ history, time }) => {
    return (
        <FontAwesomeIcon icon={ faArrowCircleLeft } size='6x' 
            onClick={ () => {
                setTimeout( () => {
                    // if(history.location.pathname.slice(1) === 'login' || history.location.pathname.slice(1) === 'register') history.push('/')
                    // else history.goBack()
                    history.push('/');
                }, time);
            }} 
            className='back'
        />
    );
};

export default BackButton;