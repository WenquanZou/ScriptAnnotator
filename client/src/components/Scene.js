import React, {Component} from "react";
import {Typography} from "@material-ui/core";
import Stagedir from "./Stagedir.js"
import Speech from "./Speech.js"

export default class Scene extends Component {
    render() {
        return (
            <div>
                <Typography variant='h4'>Scene {this.props.scene_num}</Typography>
                <div className="Scene">
                    {this.props.content.map((line, key) => {
                        if (line.type === 'stagedir')
                            return <Stagedir key={key} dir={line.dir}/>;
                        else
                            return <Speech key={key} publicKey={key} speaker={line.speaker} content={line.content}
                                           onRightClick={this.props.onRightClick}
                                           recordStart={this.props.recordStart}
                                           recordEnd={this.props.recordEnd}
                            />
                    })}
                </div>
            </div>
        );
    }
}