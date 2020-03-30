import React, { Component } from 'react';
import axios from 'axios';

import PlantCard from './PlantCard';

class Plants extends Component {
    constructor() {
        super();
        this.state = {
            plants: []
        };
    }

    async componentDidMount() {
        const data = (await axios.get('/api/plants')).data;
        this.setState({ plants: data });
    }

    render() {
        const { plants } = this.state;
        return (
            <div id='all-plants'>
                {
                    plants.map(plant => <PlantCard key={ plant.plant_id } plant={ plant } /> )
                }
            </div>
        );
    }
};
 
export default Plants;