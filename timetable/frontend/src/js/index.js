import React from 'react';
import ReactDOM from 'react-dom';
import Timetable from './timetable.js';
import TopBar from './topBar.js';
import CourseList from './courseList.js';
import SearchBar from './searchBar.js'
import Alert from './alert.js';
import '../styles/base.css';

class HomePage extends React.Component{
    constructor(props){
        super(props);
        this.state={
            choosedTerm: null,
            terms: [],
            selectedSections: [],
            siblingSections: [],
            selectedSiblings: [],
            targetSection: null,
            warnState: {
                className: 'warn-hide',
                warnMsg: null,
            },
        };
        this.changeTerm = this.changeTerm.bind(this);
        this.getTerms = this.getTerms.bind(this);

        this.getSelectedSections = this.getSelectedSections.bind(this);
        this.getSiblingSections = this.getSiblingSections.bind(this);
        this.changeSections = this.changeSections.bind(this);
        this.changeSiblings = this.changeSiblings.bind(this);

        this.changeTargetSection = this.changeTargetSection.bind(this);

        this.changeWarnState = this.changeWarnState.bind(this)

        this.toggleSelectedSection = this.toggleSelectedSection.bind(this)
    }

    toggleSelectedSection(selectedSections){
        this.setState({
            selectedSections: selectedSections
        })
    }

    changeWarnState(warnState){
        this.setState({
            warnState:warnState
        })
    }

    getTerms(data){
        if(data.code !== 0)
                console.error(data.msg);
        else{
            this.setState({
                choosedTerm: data.body[0],
                terms: data.body
            })
        }
    }

    getSelectedSections(data){
        if(data.code !== 0)
            console.error(data.msg);
        else{
            data.body.map((section)=>{
                section.show = 1
            });
            this.setState({
                selectedSections: data.body
            });

            this.state.selectedSections.map((selectedSection)=>{
                const data={
                    category: selectedSection.section.category,
                    term: selectedSection.section.term,
                    type: selectedSection.section.type,
                    section_id: selectedSection.section.id
                };
                request(
                    `/api/courses/${selectedSection.section.course.id}/sections`,
                    'POST',
                    data,
                    this.getSiblingSections
                )
            })
        }
    }

    getSiblingSections(data){
        if(data.code !== 0)
            console.error(data.msg);
        else{
            this.setState((prevState)=>{
                return {
                    siblingSections: prevState.siblingSections.concat(data.body)
                }
            })
        }
    }

    changeSiblings(siblings){
        this.setState({
            selectedSiblings: siblings
        })
    }

    changeTargetSection(target){
        this.setState({
            targetSection: target
        })
    }

    changeSections(){
        request('/api/selectsections/', 'GET', null, this.getSelectedSections)
        this.setState({
            selectedSiblings: [],
            siblingSections: []
        })
    }

    componentDidMount(){
        request('/api/courses/terms', 'GET', null, this.getTerms);
        request('/api/selectsections/', 'GET', null, this.getSelectedSections)
    }

    changeTerm(term){
        this.setState({
            choosedTerm: term,
            // selectedSiblings: []
        });
        this.changeSections()
    }

    render(){
        const root = document.getElementById('root');
        const staticUrl = root.getAttribute('static-url');
        const colStyleLeft = {
            backgroundImage: 'url('+staticUrl+'images/sakula.png)'
        };
        const colStyleRight = {
            backgroundImage: 'url('+staticUrl+'images/sakula2.png)'
        };
        return(
            <div className="main">
                <Alert
                    warnState={this.state.warnState}
                    changeWarnState={this.changeWarnState}
                />
                <TopBar
                    terms={this.state.terms}
                    choosedTerm={this.state.choosedTerm}
                    changeTerm={this.changeTerm}
                    page="timetable"
                />

                    <div className="row">
                        <div className="col1" style={colStyleLeft}>
                            <SearchBar
                                changeSections={this.changeSections}
                                staticUrl={staticUrl}
                                warnState={this.state.warnState}
                                changeWarnState={this.changeWarnState}
                            />
                        </div>
                        <div className="col2">
                            <Timetable
                                choosedTerm={this.state.choosedTerm}
                                selectedSections={this.state.selectedSections}
                                changeSections={this.changeSections}
                                siblingSections={this.state.siblingSections}
                                selectedSiblings={this.state.selectedSiblings}
                                changeSiblings={this.changeSiblings}
                                changeTargetSection={this.changeTargetSection}
                                targetSection={this.state.targetSection}
                            />
                        </div>
                        <div className="col3" style={colStyleRight}>
                            <CourseList
                                selectedSections={this.state.selectedSections}
                                choosedTerm={this.state.choosedTerm}
                                changeSections={this.changeSections}
                                toggleSelectedSection={this.toggleSelectedSection}
                                changeSiblings={this.changeSiblings}
                                selectedSiblings={this.state.selectedSiblings}
                            />
                        </div>
                    </div>
            </div>
        )
    }
}

ReactDOM.render(<HomePage/>, document.getElementById('root'));