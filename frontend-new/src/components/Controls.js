import React, {Component} from 'react';

const Controls = () => {
    return (
        <div className="controls">
            <h3>Controls for garden</h3>
            <div className="slidecontainer">
                <input type="range" min="1" max="100" value="50" class="slider" id="myRange" />
            </div>
            <div className="slidecontainer">
                <input type="range" min="1" max="100" value="50" class="slider" id="myRange" />
            </div>
            <div className="slidecontainer">
                <input type="range" min="1" max="100" value="50" class="slider" id="myRange" />
            </div>
            <div className="slidecontainer">
                <input type="range" min="1" max="100" value="50" class="slider" id="myRange" />
            </div>
        </div>
    );
};

export default Controls