import React, { Component } from 'react';
import axios from 'axios';
import Popup from "reactjs-popup";

import PlantCard from './PlantCard';
import BackButton from '../BackButton';

class Plants extends Component {
    constructor() {
        super();
        this.state = {
            plants: [],
            plant_name: '',
            species: '',
            user_email: '',
            uri: '',
            curr_photo: ''
        };
        this.addPlant = this.addPlant.bind(this);
        this.remove = this.remove.bind(this);
    }

    async componentDidMount() {
        const data = (await axios.get('/api/plants')).data;
        this.setState({ plants: data });
    }

    async addPlant(ev) {
        ev.preventDefault();
        const { plant_name, species, user_email, uri, curr_photo } = this.state;
        const newPlant = (await axios.post('/api/plants', { plant_name, species, user_email, uri, curr_photo })).data;
        this.setState({ plants: [...this.state.plants, newPlant], plant_name: '', species: '', user_email: '', uri: '', curr_photo: ''});
    };


    async remove(removeplant) {
        this.setState({ plants: this.state.plants.filter(plant => plant.plant_id !== removeplant.plant_id) });
        await axios.delete(`/api/plants/${removeplant.plant_id}`);
    }

    render() {
        const { plants, plant_name, species, user_email, uri, curr_photo } = this.state;
        const { history } = this.props;
        const { addPlant, remove } = this;
        return (
            <div className='plants-page'>
                <div id='all-plants'>
                    <div className='backbuttons'>
                        <BackButton history={history} />
                        {/* <Popup modal trigger={
                                <button className='add'>Add new plant</button>
                            }>
                            {close => {
                                return <div className='formadd'>
                                    <form 
                                    className='addform'
                                    onSubmit={ ev => {
                                        addPlant(ev);
                                        close();
                                    }}>
                                        <div><input type='text' placeholder='Plant Name' value={ plant_name } onChange={ ev => this.setState({ plant_name: ev.target.value }) } /></div>
                                        <div><input type='text' placeholder='Species' value={ species } onChange={ ev => this.setState({ species: ev.target.value }) } /></div>
                                        <div><input type='text' placeholder='User Email' value={ user_email } onChange={ ev => this.setState({ user_email: ev.target.value }) } /></div>
                                        <div><input type='text' placeholder='URI' value={ uri } onChange={ ev => this.setState({ uri: ev.target.value }) } /></div>
                                        <div><input type='text' placeholder='Photo' value={ curr_photo } onChange={ ev => this.setState({ curr_photo: ev.target.value }) } /></div>
                                        <div><input type='submit' value='Add Plant' /></div>
                                </form> 
                            </div>
                            }}
                        </Popup> */}
                    </div>
                    <div>
                    {
                        plants.map(plant => <PlantCard key={ plant.plant_id } plant={ plant } remove={ remove } /> )
                    }   
                    </div>
                </div>
            </div>
        );
    }
};
 
export default Plants;