import React from 'react';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faArrowCircleLeft } from '@fortawesome/free-solid-svg-icons';

const BackButton = ({ history }) => {
    return (
        <FontAwesomeIcon icon={ faArrowCircleLeft } size='6x' 
            onClick={ () => {
                history.goBack() 
            }} 
            className='back'
        />
    );
};

export default BackButton;