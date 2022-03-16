import Header from './components/header';
import ItemsList from "./components/items_list";
import DetailsDisplay from "./components/details_display";
import Footer from "./components/footer";
import './App.css';
import EstimateControls from "./components/estimate_controls";

import React from 'react';

class App extends React.Component{

    constructor(props) {
        super(props);
        this.state = {
            issues: [],
            issue_loading_state: "Loading...",
            selected_item_key: null
        }
        this.onSelectIssue = this.onSelectIssue.bind(this);
        this.setIssueEstimate = this.setIssueEstimate.bind(this);
        this.clearEstimates = this.clearEstimates.bind(this);
        this.reloadTasks = this.reloadTasks.bind(this);
    }

    reloadTasks(){
        this.reloadIssues()
    }

    onSelectIssue(key){
        this.setState({selected_item_key: key});
        console.log(key);
    }

    reloadIssues(){
        let host = document.location.port === '3000'?"http://localhost:8080":"";
        // document.title = "Relative estimator";
        fetch(host+"/api/issues")
            .then(response => response.json())
            .then((jsonData) => {
                this.setState({
                    issues: jsonData.items,
                    issue_loading_state: null
                });
            })
            .catch((error) => {
                this.setState({
                    issues: [],
                    issue_loading_state: "Loading items error! " + error
                });
            });
    }

    componentDidMount() {
        this.reloadIssues();
    }

    getSelectedIssue(){
        if(this.state.selected_item_key){
            return this.state.issues.find(element => element.key === this.state.selected_item_key);
        }
        return null;
    }

    getSelectedIssueIndex(){
        if(this.state.selected_item_key){
            return this.state.issues.findIndex(element => element.key === this.state.selected_item_key);
        }
        return null;
    }

    clearEstimates(){
        let issues =  this.state.issues.slice();
        issues.forEach(function(item, index){item.estimate = '';});
        this.setState({selected_item_key: this.state.selected_item_key,
        issues: issues});
    }

    setIssueEstimate(estimate){
        let itemIndex = this.getSelectedIssueIndex();
        let issues = this.state.issues.slice();
        issues[itemIndex].estimate = estimate;
        this.setState({issues: issues});
        this.onSelectIssue(this.state.selected_item_key);
    }

    render()
    {
        let selected_issue = this.getSelectedIssue();

        return (
        <div className="App">
            <header className="App-header">
                <Header/>
            </header>
            <div className="body">
                <EstimateControls
                    clearAction={this.clearEstimates}
                    estimateAction={this.setIssueEstimate}
                    reloadAction={this.reloadTasks}
                />
                <ItemsList
                    entities={this.state.issues}
                    state={this.state.issue_loading_state}
                    selectedKey={this.state.selected_item_key}
                    onSelect={this.onSelectIssue}
                />
                <DetailsDisplay
                    issue={selected_issue}
                />
            </div>
            <Footer />
        </div>
        );
    }
}

export default App;
