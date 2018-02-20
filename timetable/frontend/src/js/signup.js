import React from 'react';
import ReactDOM from 'react-dom';
import TopBar from './topBar.js';
import '../styles/signup.css';
import '../styles/base.css';
import '../styles/md.css';
import '../styles/ripple.css';

class SignupPage extends React.Component{
    constructor(props){
        super(props);
        this.state={
            form: <SignInForm />
        };
        this.signIn = this.signIn.bind(this);
        this.signUp = this.signUp.bind(this);
    }

    signIn(){
        this.setState({
            form: <SignInForm />
        })
    }

    signUp(){
        this.setState({
            form: <SignUpForm />
        })
    }
    render(){
        const root = document.getElementById('signup-page');
        const staticUrl = root.getAttribute('static-url');
        return(
            <div>
                <TopBar page="signup"/>
                <div className="signup-main">
                <div className="row row1">
                    <div className="rect-container">
                        <div id="decoration-rect1" className="dark-yellow"></div>
                    </div>
                </div>
                <div className="row row2">
                    <div className="rect-container">
                        <div id="decoration-rect2" className="dark-yellow"></div>
                    </div>
                    <div className="image-container"></div>
                    <div className="panel-container">
                        <div id="decoration-rect3" className="yellow"></div>
                    </div>
                </div>
                <div className="row row3">
                    <div className="rect-container">
                        <div id="decoration-rect4" className="dark-purple"></div>
                    </div>
                    <div className="image-container">
                        <img id="image" src={staticUrl+require('../images/library.png')}></img>
                    </div>
                    <div className="panel-container">
                        <div id="panel" className="yellow">
                            <div className="rkmd-btn btn-fab dark-purple indie ripple-effect" id="sign-up-button" onClick={this.signUp}>Sign Up</div>
                            <div className="rkmd-btn btn-fab dark-purple indie ripple-effect" id="sign-in-button" onClick={this.signIn}>Sign In</div>
                            {this.state.form}
                        </div>
                    </div>
                </div>
                <div className="row row4">
                    <div className="rect-container"></div>
                    <div className="image-container"></div>
                    <div className="panel-container">
                        <div id="decoration-rect5" className="dark-yellow"></div>
                    </div>
                </div>
                </div>
            </div>
        )
    }
}


class SignInForm extends  React.Component{
    constructor(props){
        super(props);
        this.state = {
            username: null,
            password: null,
            warningMsg: null,
            wrongClass: null,
        };
        this.handleInputChange = this.handleInputChange.bind(this);
        this.submit = this.submit.bind(this);
        this.afterSubmit = this.afterSubmit.bind(this)
    }

    handleInputChange(event){
        this.setState({
            [event.target.name]: event.target.value
        })
    }

    submit(){
        const data = {
            username: this.state.username,
            password: this.state.password
        };
        request('/api/user/login', 'POST', data, this.afterSubmit)
    }

    afterSubmit(data){
        if(data.code === 2004 || data.code === 2005){
            this.setState({
                warningMsg: "Wrong username or password",
                wrongClass: "wrong-input"
            })
        }
        else if(data.code !== 0){
            this.setState({
                warningMsg: data.msg,
                wrongClass: "wrong-input"
            })
        }
        else{
            window.location.href = '/timetable'
        }
    }

    render(){
        return(
            <div>
              <div className="indie form-title">User Sign In</div>
              <div className="md-group">
                <input
                    type="text"
                    className="md-input md-w-sign"
                    name="username"
                    onChange={this.handleInputChange}
                    required
                />
                <span className="md-highlight"></span>
                <span className="md-bar md-w-sign"></span>
                <label className="md-label">Username</label>
              </div>
              <div className="md-group">
                <input
                    type="password"
                    className={`md-input md-w-sign ${this.state.wrongClass}`}
                    name="password"
                    onChange={this.handleInputChange}
                    required
                />
                <span className="md-highlight"></span>
                <span className="md-bar md-w-sign"></span>
                <label className="md-label">Password</label>
                <div className="warning-msg">{this.state.warningMsg}</div>
              </div>
              <div className="rkmd-btn purple indie ripple-effect submit-button" onClick={this.submit}>Sign In</div>

            </div>
        )
    }
}

class SignUpForm extends React.Component{
    constructor(props){
        super(props);
        this.state = {
            username: "",
            password: "",
            warningMsg: null,
            wrongClass: null,
        };
        this.handleInputChange = this.handleInputChange.bind(this);
        this.submit = this.submit.bind(this);
        this.afterSubmit = this.afterSubmit.bind(this)
    }

    handleInputChange(event){
        this.setState({
            [event.target.name]: event.target.value
        })
    }

    submit(){
        if(this.state.username === "" || this.state.password === ""){
            this.setState({
                warningMsg: "the username and password should not be empty",
                wrongClass: "wrong-input",
            });
            return
        }
        const data = {
            username: this.state.username,
            password: this.state.password
        };
        request('/api/user/', 'POST', data, this.afterSubmit)
    }

    afterSubmit(data){
        if(data.code === 2002){
            this.setState({
                warningMsg: data.msg,
                wrongClass: "wrong-input",
            })
        }
        else if(data.code !== 0){
            console.error(data.msg)
        }
        else{
            window.location.href = '/timetable'
        }
    }
    render(){
        return(
            <div>
              <div className="indie form-title">User Sign Up</div>
              <div className="md-group">
                <input
                    type="text"
                    className="md-input md-w-sign"
                    name="username"
                    onChange={this.handleInputChange}
                    required
                />
                <span className="md-highlight"></span>
                <span className="md-bar md-w-sign"></span>
                <label className="md-label">Username</label>
              </div>
              <div className="md-group">
                <input
                    type="password"
                    className={`md-input md-w-sign ${this.state.wrongClass}`}
                    name="password"
                    onChange={this.handleInputChange}
                    required
                />
                <span className="md-highlight"></span>
                <span className="md-bar md-w-sign"></span>
                <label className="md-label">Password</label>
                <div className="warning-msg">{this.state.warningMsg}</div>
              </div>

              <div className="rkmd-btn purple indie ripple-effect submit-button" onClick={this.submit}>Sign Up</div>

            </div>
        )
    }
}

ReactDOM.render(<SignupPage/>, document.getElementById('signup-page'));