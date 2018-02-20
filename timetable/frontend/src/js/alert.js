import React from 'react'
import '../styles/alert.css'

class Alert extends React.Component{
    constructor(props){
        super(props)
        this.handleClick = this.handleClick.bind(this);
        this.handleMouseOver = this.handleMouseOver.bind(this)
    }
    handleClick(){
        this.props.changeWarnState({
            className: 'warn-hide',
            warnMsg: null
        })
        // this.setState({
        //     className: "animated fadeOut"
        // })
    }
    handleMouseOver(){
        // if(this.props.warnState.className === "animated fadeOut"){
        //     console.log('nono')
        //     this.props.changeWarnState({
        //         className: 'warn-hide',
        //         warnMsg: null
        //     })
        // }
        // if(this.state.className === "animated fadeOut"){
        //     this.setState({
        //         className: "warn-hide"
        //     })
        // }
    }
    render(){
        return(
            <div id="warning" className={this.props.warnState.className} onMouseOver={this.handleMouseOver}>
                <div className="background"></div>
                <div className="alert-dialog">
                    <div className="error-msg">{this.props.warnState.warnMsg}</div>
                    <div className="error-btn" onClick={this.handleClick}>OK</div>
                </div>
            </div>
        )
    }
}
export default Alert