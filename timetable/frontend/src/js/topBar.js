import React from 'react';
import '../styles/base.css';
import '../styles/topBar.css';
import '../styles/ripple.css';

class TopBar extends React.Component{
    constructor(props){
        super(props);
        this.logOut = this.logOut.bind(this);
    }

    logOut(){
        request("/api/user/logout", 'POST', null, this.afterLogOut)
    }

    afterLogOut(data){
        if(data.code !== 0){
            console.error(data.msg)
        }
        else{
            window.location.href = '/signup'
        }
    }
   handleClick(){
        window.location.href = '/timetable'
   }
    render(){
        return(
            <nav className="navbar navbar-expand-lg sticky-top purple my-navbar">
                <div className="prj-title indie" onClick={this.handleClick}>CU Timetable</div>
                {this.props.page === "timetable" &&
                <button className="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNavDropdown"
                        aria-controls="navbarNavDropdown" aria-expanded="false" aria-label="Toggle navigation">
                    <span className="navbar-toggler-icon"></span>
                </button>
                }
                {this.props.page === "timetable" &&
                <div className="collapse navbar-collapse" id="navbarNavDropdown">
                    <ul className="navbar-nav">
                        <TermDropdown
                            terms={this.props.terms}
                            choosedTerm={this.props.choosedTerm}
                            changeTerm={this.props.changeTerm}
                        />
                    </ul>
                </div>
                }
                {(this.props.page === "timetable" || this.props.page === "course") &&
                <div className="indie logout-button" onClick={this.logOut}>Log Out</div>
                }
            </nav>
        )
    }
}

class TermDropdown extends React.Component{
    render(){
        const termList = this.props.terms.map((term, index)=>
            <TermDropdownItem term={term} key={index+1} changeTerm={this.props.changeTerm}/>
        );

        return(
          <li className="drop nav-item dropdown">
            <div className="nav-link dropdown-toggle term-info" href="#" id="navbarDropdownMenuLink" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                {this.props.choosedTerm}
            </div>
              <ul>
            <li className="dropdown-menu  term-dropdown" aria-labelledby="navbarDropdownMenuLink">
                {termList}
            </li>
              </ul>
          </li>
        )
    }
}

class TermDropdownItem extends React.Component{
    constructor(props){
        super(props);
        this.handleClick = this.handleClick.bind(this);
    }

    handleClick(){
        this.props.changeTerm(this.props.term)
    }

    render(){
        return(
            <a className="dropdown-item" href="#" onClick={this.handleClick}>{this.props.term}</a>
        )
    }
}

export default TopBar;