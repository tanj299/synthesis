import React, { Component } from 'react';
import axios from 'axios';

class PlantInfo extends Component {
    constructor() {
        super();
        this.state = {
            plant: {}
        };
        this.waterPlant = this.waterPlant.bind(this);
        this.toggleLight = this.toggleLight.bind(this);
        this.showCamera = this.showCamera.bind(this);
    }

    async componentDidMount() {
        const id = this.props.plant.plant_id;
        const plant = (await axios.get(`/api/plants/${id}`)).data;
        this.setState({ plant: plant });
    }

    async waterPlant(ev) {
        ev.preventDefault();
        await axios.post('/api/requests', { });
        this.props.close();
    };

    async toggleLight(ev) {
        ev.preventDefault();
        await axios.post('/api/requests', { });
        this.props.close();
    };

    async showCamera(ev) {
        ev.preventDefault();
        await axios.post('/api/requests', { });
        this.props.close();
    };

    render() {
        const { plant } = this.state;
        const { close, remove } = this.props;
        const { waterPlant, toggleLight, showCamera } = this;
        return (
            <div id='more-information'>
                <div id='plant-left'>
                    <h1>{plant.plant_name}</h1>
                    <div id='plant-img'>
                        <p>No image yet</p>
                    </div>
                </div>
                <div id='remove'>
                    <button onClick={ () => {
                            remove(plant);
                            close();
                        }
                    }>Delete Plant</button>
                </div>
                <div id='plant-controls'>
                    <form onSubmit={ toggleLight }>
                        <button>Light</button>
                    </form>
                    <form onSubmit={ showCamera }>
                        <button>Camera</button>
                    </form>
                    <form onSubmit={ waterPlant }>
                        <input type='number' placeholder='Water threshold' /><button>Water</button>
                    </form>
                </div>
            </div>
        );
    }
};

export default PlantInfo;