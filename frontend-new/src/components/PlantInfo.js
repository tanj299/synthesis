import React, {Component} from 'react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import Controls from './Controls';

class PlantInfo extends Component {
    constructor() {
        super();
        this.state = {
            data: []
        };
    }

    async componentDidMount() {
        const id = this.props.match.params.id;
        this.setState({data: (await axios.get(`/api/plantsdata/${id}`)).data });
    }

    render() {
        const { data } = this.state;
        return (
            <main>
                <Link to='/user/plants'>Go back</Link>
                <h1>More Info</h1>
                <h3>Category: {data.category}</h3>
                <h3>Name: {data.name}</h3>
                <h3>Water level: {data.waterLevel}</h3>
                <Controls />
            </main>
        );
    }
};

export default PlantInfo;