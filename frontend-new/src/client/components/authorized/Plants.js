import React, { Component } from 'react';
import axios from 'axios';

import PlantCard from './PlantCard';
import BackButton from '../BackButton';

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
        const { history } = this.props;
        return (
            <div>
                <BackButton history={history} />
                <div id='all-plants'>
                    {
                        plants.map(plant => <PlantCard key={ plant.plant_id } plant={ plant } /> )
                    }
                </div>
            </div>
        );
    }
};
 
export default Plants;