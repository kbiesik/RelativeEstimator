import React from 'react';

import './issue_item.css';
import TagList from "./tag_list";

class IssueItem extends React.Component{

    render() {
        return (
            <div
                    className={this.props.isSelected?"issueItem selected":"issueItem"}
                    onClick={() => { this.props.onSelect(this.props.issueKey)}}
                >
                <span className="labelsField">
                    <TagList tags={ this.props.labels }></TagList>
                </span>
                <span className="summaryField">
                    {this.props.summary}
                </span>:
                <span className="sPField">
                    {this.props.sp}
                </span>
                <span className="calcSpField">
                    {this.props.calc_sp}
                </span>
                <span className="sph">
                    {this.props.sph.toFixed(3)}
                </span>
                <span className="no_of_sprints">
                    {this.props.no_of_active_sprints}
                </span>
                <span>{this.props.estimate}</span>
            </div>
        );
    }
}


export default IssueItem;