import React, {Component} from 'react';
import axios from 'axios';

class Plants extends Component {
    constructor() {
        super();
        this.state = { 
            plants: []
        };
    };

    async componentDidMount() {
        const getPlants = (await axios.get('/api/plantsdata')).data;
        this.setState({plants: getPlants});
    }
    
    async componentDidUpdate(prev) {
        if(prev !== this.props) {
            const getPlants = (await axios.get('/api/plantsdata')).data;
            this.setState({plants: getPlants});
        }
    }

    render() {
        const { plants } = this.state;
        const categories = plants.reduce((endresult, item) => endresult.includes(item.category) ? endresult : [...endresult, item.category], []);
        
        return (
            <div id="listofcategories">
                {
                    categories.map(category => {
                        return (
                            <div id="category" key={category}>
                                <h1>{`${category[0].toUpperCase()}${category.substring(1, category.length)}`}</h1>
                                <div id="plants">
                                    {
                                        plants.map(plant => {
                                            return plant.category === category ?
                                                (
                                                    <a style={{backgroundImage: `url(${plant.photo})`}} href={`/#/user/plants/${plant.id}`} id="plantnode" key={plant.id}>
                                                        <p id="plantname">
                                                            {plant.name}
                                                        </p>
                                                        <p>
                                                            Water level: {plant.waterLevel}
                                                        </p>
                                                    </a>

                                                )
                                                : null
                                        })
                                    }
                                </div>
                            </div>
                        )
                    })
                }
            </div>
        );
    }
};

export default Plants;