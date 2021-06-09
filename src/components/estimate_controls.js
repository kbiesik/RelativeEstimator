import React from 'react';
import './estimate_controls.css';


class EstimateControls extends React.Component{
    render()
    {
        return (
            <div id="EstimateControls">
                <span>
                <a href="#" onClick={() =>{ this.props.clearAction(); return false;}}>Clear all rates</a>,
                Rate this task as <a href="#" onClick={() => {this.props.estimateAction("v"); return false;}}>smaller</a>|
                <a href="#" onClick={() => {this.props.estimateAction("~"); return false;}}>same</a>|
                <a href="#" onClick={() => {this.props.estimateAction("^"); return false;}}>bigger</a> then your.
                </span>
            </div>
        )
    }
}

export default  EstimateControls;