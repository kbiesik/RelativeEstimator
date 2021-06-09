import './tag.css';

function Tag(props){
        return (
            <span className="tag" >{props.label}</span>
        );
}

export default  Tag;