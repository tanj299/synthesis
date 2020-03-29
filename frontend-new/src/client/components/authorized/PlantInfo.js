import React, { Component } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';

class PlantInfo extends Component {
    constructor() {
        super();
        this.state = {
            plant: {}
        };
    }

    async componentDidMount() {
        const id = this.props.match.params.id;
        const plant = (await axios.get(`/api/plants/${id}`)).data;
        this.setState({ plant: plant });
    }

    render() {
        const { plant } = this.state;
        return (
            <div>
                <Link to='/user/plants'>Back to plants</Link>
                <h1>{plant.plant_id}</h1>
                <h1>{plant.humidity_level}</h1>
                <h1>{plant.light_intensity}</h1>
                <h1>{plant.moisture_level}</h1>
            </div>
        );
    }
};

export default PlantInfo;