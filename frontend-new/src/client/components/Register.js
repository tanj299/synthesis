import React from 'react';

import BackButton from './BackButton';

const Register = ({ history }) => {
    return (
        <div>
            <BackButton history={history} />
            <h1>grrrr this is the register page</h1>
        </div>
    );
};

export default Register;