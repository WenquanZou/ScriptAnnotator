import React, {Component} from 'react';
import {List, ListItem, ListItemText, Divider} from '@material-ui/core';

class Menu extends Component {
    render() {
        return (
            <List className="scrollable">
                {this.props.plays.map((play, key) => (
                    <div key={key}>
                        <ListItem button onClick={this.props.loadPlay(play)}>
                            <ListItemText primary={play}/>
                        </ListItem>
                        <Divider/>
                    </div>
                ))}
            </List>
        );
    }
}

export default Menu;