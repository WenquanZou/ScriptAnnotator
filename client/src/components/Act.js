import {Typography} from "@material-ui/core";
import React, {Component} from "react";
import Scene from "./Scene.js"

export default class Act extends Component {
    render () {
        return (
            <div>
                <Typography component='h3' variant='h3'>Act {this.props.act_num}</Typography>
                <div className="Act">
                    {this.props.scenes.map((scene, key) => (

                    <Scene key={key} act_num={scene.act_num} scene_num={scene.scene_num} content={scene.content}
                           recordStart={this.props.recordStart}
                           recordEnd={this.props.recordEnd}
                           onRightClick={this.props.onRightClick}/>
                ))}
                </div>
            </div>
        );
    }
}