import React from 'react';
import IssueItem from './issue_item';
import './items_list.css'

class ItemsList extends React.Component {

    render() {
        if (this.props.state !== null){
            return (
                <div id="ItemsList">
                    <p>{this.props.state}</p>
                </div>
            )
        } else {
            let items_list = this.props.entities.slice();
            items_list.sort(function(a,b){
                return a.sp - b.sp;
            });

            return (
                <div id="ItemsList">
                {
                    items_list.map((entity) => {
                        return (
                            <IssueItem
                                key={entity.key}
                                isSelected = {entity.key===this.props.selectedKey}
                                issueKey={entity.key}
                                summary={entity.summary}
                                sp={entity.sp}
                                description={entity.description}
                                onSelect={this.props.onSelect}
                                estimate={entity.estimate}
                            />
                        );
                    })
                }
                </div>
            );
        }
    }
};


export default ItemsList;