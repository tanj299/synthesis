import React, { Component } from 'react';
import axios from 'axios';

class PlantInfo extends Component {
    constructor() {
        super();
        this.state = {
            plant: {},
            requestsHistory: [],
            light: '',
            water: ''
        };
        this.waterPlant = this.waterPlant.bind(this);
        this.toggleLight = this.toggleLight.bind(this);
        this.showCamera = this.showCamera.bind(this);
    }

    async componentDidMount() {
        const id = this.props.plant.plant_id;
        const plant = (await axios.get(`/api/plants/${id}`)).data;
        const requestsHistory = (await axios.get(`/api/requests/${plant.plant_id}`)).data.reverse();
        console.log(plant);
        this.setState({ plant: plant, requestsHistory });
    }

    async waterPlant(ev) {
        ev.preventDefault();
        const { plant_id } = this.state.plant;
        await axios.post(`/api/requests/insert`, { plant_id, category: "water", waterthreshold: this.state.water });
        this.props.close();
    };

    async toggleLight(ev) {
        ev.preventDefault();
        const { plant_id } = this.state.plant;
        await axios.post('/api/requests/insert', { plant_id, category: "light", lightthreshold: this.state.light });
        this.props.close();
    };

    async showCamera(ev) {
        ev.preventDefault();
        const id = this.props.plant.plant_id;
        const plant = (await axios.get(`/api/plants/${id}`)).data;
        this.setState({ plant: plant });
    };

    render() {
        const { plant, requestsHistory, light, water } = this.state;
        const { close, remove } = this.props;
        const { waterPlant, toggleLight, showCamera } = this;
        return (
            <div id='more-information'>
                <div id='plant-left'>
                    <h1>{plant.plant_name}</h1>
                    <div id='plant-img'>
                        <img id='plant-img' src={plant.uri} />
                    </div>
                </div>
                <div>
                    <ul className='history'>
                        {
                            requestsHistory.length !== 0 ? requestsHistory.map((history, index) => <li key={ index }>
                                                                        <span>{ history.category } - </span><span>{ history.timestamp }</span>
                                                                    </li>)
                                                        : <h1>No Requests History</h1>
                        }
                    </ul>
                    <div id='remove'>
                        <button onClick={ () => {
                                remove(plant);
                                close();
                            }
                        }>Delete Plant</button>
                    </div>
                </div>
                <div id='plant-controls'>
                    <form onSubmit={ showCamera }>
                        <button>Get Most Recent Picture</button>
                    </form>
                    <form onSubmit={ toggleLight }>
                        <input type='number' placeholder='Light threshold' value={ light } onChange={ ev => this.setState({ light: ev.target.value }) } /><button>Light</button>
                    </form>
                    <form onSubmit={ waterPlant }>
                        <input type='number' placeholder='Water threshold' value={ water } onChange={ ev => this.setState({ water: ev.target.value }) } /><button>Water</button>
                    </form>
                </div>
            </div>
        );
    }
};

export default PlantInfo;