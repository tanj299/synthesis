import React from 'react';

import BackButton from './BackButton';

const About = ({ history }) => {
    return (
        <div>
            <BackButton history={history} />
            <h1>grrrr this is the about page</h1>
        </div>
    );
};

export default About;