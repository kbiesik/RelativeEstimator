import React from 'react';
import './details_display.css';
import TagList from "./tag_list";


class DetailsDisplay extends React.Component{
    render()
    {
        if (!this.props.issue){
            return null;
        }
        const description = this.props.issue?this.props.issue.description:"";
        const time = this.props.issue.time?this.props.issue.time.toFixed(1)+" h":"N/A"

        let sptime = 'NA';
        if(this.props.issue.sp && this.props.issue.time){
            sptime = (this.props.issue.sp/this.props.issue.time).toFixed(3);
        }

        return (
            <div id="DetailsDisplay">
                    <h2>{ this.props.issue.summary } ({this.props.issue.key})</h2>
                    <ul>
                    <li>Story points: { this.props.issue.sp?this.props.issue.sp:"N/A" }</li>
                    <li>Time: { time }</li>
                    <li>SP/h: {sptime}</li>
                    </ul>
                <h3>Description:</h3>
                <div dangerouslySetInnerHTML={{__html: description}}></div>
            </div>
        );
    }
}

export default  DetailsDisplay;
