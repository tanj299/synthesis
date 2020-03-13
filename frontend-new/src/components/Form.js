import React, { Component } from 'react';
import axios from 'axios';

class Form extends Component {
    constructor() {
        super();
        this.state = {
            category: '',
            name: '',
            photo: ''
        };
    }
    render() {
        const { category, name, photo } = this.state;
        return (
            <form onSubmit={ async(ev) => {
                ev.preventDefault();
                await axios.post('/api/plantsdata', {category: category, name: name, photo: photo});
            } }>
                <input type="text" placeholder="Category" value={ category } onChange={(ev) => this.setState({category: ev.target.value})}/>
                <input type="text" placeholder="Name of your plant" value={ name } onChange={(ev) => this.setState({name: ev.target.value})}/>
                <input type="text" placeholder="Link of photo" value={ photo } onChange={(ev) => this.setState({photo: ev.target.value})}/>
                <button disabled={ category === '' || name === '' || photo === '' }>Create</button>
            </form>
        )
    }
};

export default Form;