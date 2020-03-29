import React from 'react';
import { Link } from 'react-router-dom';

const PlantCard = props => {
    const { plant } = props;
    return (
        <div id='plant-card'>
            <Link to={`/user/plants/${plant.plant_id}`} id={`${plant.name}-image`}>{plant.name}</Link>
        </div>
    );  
};

export default PlantCard;