import React from 'react';

import './issue_item.css';

class IssueItem extends React.Component{

    render() {
        return (
            <div
                    className={this.props.isSelected?"issueItem selected":"issueItem"}
                    onClick={() => { this.props.onSelect(this.props.issueKey)}}
                >
                <span className="summaryField">
                    {this.props.summary}
                </span>:
                <span className="sPField">
                    {this.props.sp}
                </span>
                <span>{this.props.estimate}</span>
            </div>
        );
    }
}


export default IssueItem;