import './tag_list.css';
import Tag from "./tag";


function TagList(props){

    if (!props.tags || props.tags.length === 0){
        return false;
    }

    return (
        <div className="tags">
            <h3>{ props.children }</h3>
            <div id="itemTags">
            {
                props.tags.map( (item) => {
                    return (< Tag label={item} />)
                }
                )
            }
            </div>
        </div>
    );
}

export default TagList