import React, { Component } from 'react';
import axios from 'axios';

class PlantInfo extends Component {
    constructor() {
        super();
        this.state = {
            plant: {}
        };
    }

    async componentDidMount() {
        const id = this.props.plant.plant_id;
        const plant = (await axios.get(`/api/plants/${id}`)).data;
        this.setState({ plant: plant });
    }

    render() {
        const { plant } = this.state;
        return (
            <div id='more-information'>
                <div id='plant-left'>
                    <h1>{plant.plant_name}</h1>
                    <div id='plant-img'>
                        <p>No image yet</p>
                    </div>
                </div>
                <div id='remove'>
                    <button>Delete Plant</button>
                </div>
                <div id='plant-controls'>
                    <button>Water</button>
                    <br/>
                    <button>Fan</button>
                    <br/>
                    <button>Camera</button>
                    <br/>
                    <button>Water threshold</button><input type='number' />
                    <br/>
                    <button>Light threshold</button><input type='number' />
                </div>
            </div>
        );
    }
};

export default PlantInfo;