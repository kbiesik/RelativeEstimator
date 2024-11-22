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
                return a.calc_sp - b.calc_sp;
            });

            return (
                <div id="ItemsList">
                {
                    items_list.map((entity) => {
                        return (
                            <IssueItem
                                key={entity.key}
                                isSelected = {entity.key===this.props.selectedKey}
                                labels={entity.labels}
                                issueKey={entity.key}
                                summary={entity.summary}
                                no_of_active_sprints={entity.no_of_active_sprints}
                                calc_sp={entity.calc_sp}
                                sph={entity.sph}
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