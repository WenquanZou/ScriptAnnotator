import React, {Component} from "react";
import Stagedir from "./Stagedir";
import Card from "@material-ui/core/Card";
import Grid from "@material-ui/core/Grid";
import Divider from "@material-ui/core/Divider";

export default class Speech extends Component {
    render() {
        return (
            <div className="speech">
                <span className="speaker">{this.props.speaker}</span>
                {this.props.content
                    .map((line, key) => {
                        if (line.type === "stagedir") {
                            return <Stagedir key={key} dir={line.dir}/>
                        } else {
                            return (
                                <Card key={key} className="line"
                                      onMouseDown={this.props.recordStart(line.line_num, this.props.speaker, this.props.publicKey)}
                                      onMouseUp={this.props.recordEnd(line.line_num, this.props.speaker, this.props.publicKey)}
                                      onContextMenu={
                                          this.props.onRightClick(line.line_num, this.props.speaker, line.text)
                                      }>
                                    {line.text}<span className="annotation">{line.annotation}</span>
                                </Card>

                            )
                        }
                    })
                }
            </div>
        );
    }
}