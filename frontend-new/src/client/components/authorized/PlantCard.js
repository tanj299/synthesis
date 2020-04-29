import React from 'react';
import Popup from "reactjs-popup";
import PlantInfo from './PlantInfo';

const PlantCard = props => {
    const { plant } = props;
    return (
        <div id='plant-card'>
            <Popup modal trigger={
                <h1 id={`${plant.species}-image`}>{`${plant.plant_name[0].toUpperCase()}${plant.plant_name.substring(1, plant.plant_name.length)}`}</h1>
            }>
                <PlantInfo plant={ plant } />
            </Popup>


            <div id='plant-info'>
                <h1>Plant Information</h1>
                <h2>Species: { plant.species }</h2>
                <h2>User email: { plant.user_email }</h2>
                <h2>Date created: { plant.date_created } </h2>
            </div>
        </div>
    );  
};

export default PlantCard;