import React from 'react';
import Popup from "reactjs-popup";
import PlantInfo from './PlantInfo';
import moment from 'moment';

const PlantCard = props => {
    const { plant, remove, email } = props;
    const date = moment(plant.date_created).format('MM-DD-YYYY');
    return (
        <div id='plant-card'>
            <Popup modal trigger={
                <h1 id={`${plant.species}-image`}>{`${plant.plant_name[0].toUpperCase()}${plant.plant_name.substring(1, plant.plant_name.length)}`}</h1>
            }>
                { close => <PlantInfo plant={ plant } close={ close } remove={ remove } email={ email } /> }
            </Popup>

            <div id='plant-info'>
                <h1>Plant Information</h1>
                <h2>Species: { plant.species }</h2>
                <h2>User email: { plant.user_email }</h2>
                <h2>Date created: { date } </h2>
                <h2>Water threshold: { plant.water_threshold }</h2>
                <h2>Light threshold: { plant.light_threshold }</h2>
            </div>
        </div>
    );  
};

export default PlantCard;