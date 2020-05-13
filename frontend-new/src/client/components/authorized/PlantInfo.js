import React, { Component } from 'react';
import axios from 'axios';

class PlantInfo extends Component {
    constructor() {
        super();
        this.state = {
            plant: {},
            requestsHistory: [],
            logs: [],
            light: 0,
            water: 0,
            name: '',
            species: '',
            email: '',
            port: '',
            position: ''
        };
        this.waterPlant = this.waterPlant.bind(this);
        this.toggleLight = this.toggleLight.bind(this);
        this.showCamera = this.showCamera.bind(this);
        this.submit = this.submit.bind(this);
    }

    async componentDidMount() {
        const id = this.props.plant.plant_id;
        const plant = (await axios.get(`/api/plants/${id}`)).data;
        const requestsHistory = (await axios.get(`/api/requests/${plant.plant_id}`)).data;
        const logs = (await axios.get(`/api/logs/${id}`)).data.reverse();
        this.setState({ logs, plant, requestsHistory: requestsHistory[requestsHistory.length - 1], light: plant.light_threshold, water: plant.water_threshold, name: plant.plant_name, species: plant.species, email: plant.user_email, port: plant.serial_port, position: plant.position });
    }

    async componentDidUpdate(prev) {
        if(prev !== this.props) {
            const id = this.props.plant.plant_id;
            const plant = (await axios.get(`/api/plants/${id}`)).data;
            const requestsHistory = (await axios.get(`/api/requests/${plant.plant_id}`)).data;
            this.setState({ plant: plant, requestsHistory: requestsHistory[requestsHistory.length - 1] });
            console.log(this.state.requestsHistory);
        }
    };

    async waterPlant(ev) {
        ev.preventDefault();
        const { plant_id } = this.state.plant;
        await axios.post(`/api/requests/insert`, { plant_id, category: "water" });
        this.props.close();
    };

    async toggleLight(ev) {
        ev.preventDefault();
        const { plant_id } = this.state.plant;
        await axios.post('/api/requests/insert', { plant_id, category: "light" });
        this.props.close();
    };

    async showCamera(ev) {
        ev.preventDefault();
        const { plant_id } = this.state.plant;
        await axios.post('/api/requests/insert', { plant_id, category: "picture" });
        this.setState({ plant: plant });
    };

    async submit(ev) {
        ev.preventDefault();
        const { light, water, name, species, email, port, position } = this.state;
        const { curr_photo, date_created, uri } = this.state.plant
        const plant = (await axios.put('/api/requests/edit', { id: this.state.plant.plant_id, light, water, name, species, email, port, position, curr_photo, date_created, uri })).data[1]
        console.log(plant);
        this.setState({ plant: plant });
        this.props.close();
    }
        
    render() {
        const { plant, requestsHistory, light, water, name, species, email, port, position, logs } = this.state;
        const { close, remove } = this.props;
        const { waterPlant, toggleLight, showCamera, submit } = this;
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
                    <div>
                    {
                        requestsHistory.length !== 0 ? <div><h1>Most Recent Request</h1><span>{ requestsHistory.category } - </span><span>{ requestsHistory.timestamp }</span></div>
                                                        : <h1>No requests have been made yet</h1>
                    }
                    </div>
                    {
                        logs.length !== 0 ? logs.map(log => {
                                                        return (
                                                            <li key={log.timestamp}>
                                                                <h2>{log.timestamp}</h2>
                                                                <div>Light: {log.light_status === 0 ? 'off' : 'on'}</div>
                                                                <div>Light level: {log.light}</div>
                                                                <div>Water level: {log.water_level === 0 ? 'Good' : 'Empty'}</div>
                                                                <div>Soil moisture: {log.soil_moisture}</div>
                                                                <div>Soil temperature: {log.soil_temp} ˚F</div>
                                                                <div>Temperature: {log.temp} ˚F</div>
                                                                <div>Humidity: {log.humidity}</div>
                                                            </li>
                                                        )
                                                    })
                                            : <h1>No logs</h1>
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
                        <button>Toggle Light</button>
                    </form>
                    <form onSubmit={ waterPlant }>
                        <button>Water</button>
                    </form>
                    <div className="edit">
                        <form onSubmit={ submit }>
                            <div><label>Name</label><br/><input onChange={ ev => this.setState({ name: ev.target.value }) }value={name}/></div>
                            <div><label>Species</label><br/><input onChange={ ev => this.setState({ species: ev.target.value }) }value={species}/></div>
                            <div><label>Email</label><br/><input onChange={ ev => this.setState({ email: ev.target.value }) }value={email}/></div>
                            <div><label>Serial Port</label><br/><input onChange={ ev => this.setState({ port: ev.target.value }) }value={port}/></div>
                            <div><label>Position</label><br/><input onChange={ ev => this.setState({ position: ev.target.value }) }value={position}/></div>
                            <div><label>Water Threshold</label><br/><input type='number' onChange={ ev => this.setState({ water: ev.target.value }) }value={water}/></div>
                            <div><label>Light Threshold</label><br/><input type='number' onChange={ ev => this.setState({ light: ev.target.value }) }value={light}/></div>
                            <button>Edit</button>
                        </form>
                    </div>
                </div>
            </div>
        );
    }
};

export default PlantInfo;