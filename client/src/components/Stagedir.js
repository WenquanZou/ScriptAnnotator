import React, {Component} from "react";

export default class Stagedir extends Component{
    render () {
        return (
            <p className="stagedir">
                {this.props.dir}
            </p>
        );
    }
}