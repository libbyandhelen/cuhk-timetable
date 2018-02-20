import React from 'react';
import ReactDOM from 'react-dom';
import TopBar from './topBar.js';
import '../styles/course.css';

class CoursePage extends React.Component{
    constructor(props){
        super(props);
        this.state = {
            course: null,
            assessments: [],
            components: [],
            sections: []
        };

        this.getCourse = this.getCourse.bind(this);
        this.getAssessments = this.getAssessments.bind(this);
        this.getComponents = this.getComponents.bind(this);
        this.getSections = this.getSections.bind(this);
    }
    componentDidMount(){
        const root = document.getElementById('course-page');
        const course_id = root.getAttribute('course');
        request(
            `/api/courses/${course_id}`,
            'GET',
            null,
            this.getCourse
        );
        request(
            `/api/courses/${course_id}/assessments`,
            'GET',
            null,
            this.getAssessments
        );
        request(
            `/api/courses/${course_id}/components`,
            'GET',
            null,
            this.getComponents
        );
        request(
            `api/courses/${course_id}/sections`,
            'GET',
            null,
            this.getSections
        )
    }

    getCourse(data){
        if(data.code !== 0)
            console.error(data.msg);
        else{
            this.setState({
                course: data.body
            });
        }
    }

    getAssessments(data){
        if(data.code !== 0)
            console.error(data.msg);
        else{
            this.setState({
                assessments: data.body
            })
        }
    }

    getComponents(data){
        if(data.code !== 0)
            console.error(data.msg);
        else{
            this.setState({
                components: data.body
            })
        }
    }

    getSections(data){
        if(data.code !== 0)
            console.error(data.msg);
        else{
            this.setState({
                sections: data.body
            })
        }
    }

    render(){
        // console.log(this.state)
        $('body').scrollspy({ target: '#list-example' })
        return(
            <div>
                <TopBar page="course"/>
                <div className="row">
                    <div className="content">
                        <div data-spy="scroll" data-target="#list-example" data-offset="0" className="scrollspy-example">
                          {/*<h2 id="list-item-1">{this.state.course && <p>{this.state.course.course_code} {this.state.course.course_name}</p>}</h2>*/}
                            {this.state.course && <p id="list-item-1" className="course-info-code">{this.state.course.course_code}</p>}
                            {this.state.course && <p className="course-info-name">{this.state.course.course_name}</p>}
                          <CourseDetails course={this.state.course}/>
                          <h4 id="list-item-2" className="sub-header">Course Components</h4>
                          <div className="divider"></div>
                          <CourseComponents components={this.state.components} />
                          <h4 id="list-item-3" className="sub-header">Course Assessments</h4>
                            <div className="divider"></div>
                          <CourseAssessments assessments={this.state.assessments} />
                          <h4 id="list-item-4" className="sub-header">Course Sections</h4>
                            <div className="divider"></div>
                          <CourseSections sections={this.state.sections} />
                        </div>
                    </div>
                    <div className="side-bar">
                        <div id="list-example" className="list-group nav-side-bar indie">
                          <a className="list-group-item nav-label list-group-item-action" href="#list-item-1">Course Details</a>
                          <a className="list-group-item nav-label list-group-item-action" href="#list-item-2">Course Components</a>
                          <a className="list-group-item nav-label list-group-item-action" href="#list-item-3">Course Assessments</a>
                          <a className="list-group-item nav-label list-group-item-action" href="#list-item-4">Course Sections</a>
                          {/*<a href="/timetable" type="button" className="btn btn-secondary">Back to Timetable</a>*/}
                        </div>

                    </div>
                </div>
            </div>
        )
    }
}

class CourseDetails extends React.Component{
    render(){
        const learning_outcome = this.props.course && this.props.course.learning_outcome
            .split('\\n\\n').join('').split('(\'').join('').split('\',)').join('')
            .split('\\r\\n').map((text, index)=>
                <div key={index}>{text.split('\\').join('')}</div>
            )
        const feedback = this.props.course && this.props.course.feedback
            .split('\\n\\n').join('').split('(\'').join('').split('\',)').join('')
            .split('\\r\\n').map((text, index)=>
                <div key={index}>{text.split('\\').join('')}</div>
            )
        const required_reading = this.props.course && this.props.course.required_reading
            .split('\\n\\n').join('').split('(\'').join('').split('\',)').join('')
            .split('\\r\\n').map((text, index)=>
                <div key={index}>{text.split('\\').join('')}</div>
            )
        const recommended_reading = this.props.course && this.props.course.recommended_reading
            .split('\\n\\n').join('').split('(\'').join('').split('\',)').join('')
            .split('\\r\\n').map((text, index)=>
                <div key={index}>{text.split('\\').join('')}</div>
            )
        const course_syllabus = this.props.course && this.props.course.course_syllabus
            .split('\\n\\n').join('').split('(\'').join('').split('\',)').join('')
            .split('\\r\\n').map((text, index)=>
                <div key={index}>{text.split('\\').join('')}</div>
            )


        // const course_syllabus = this.props.course && this.props.course.course_syllabus.split('\\n\\n').join('').split('\\r\\n').join('\r\n')
        // const feedback = this.props.course && this.props.course.feedback.split('\\n\\n').join('').split('\\r\\n').join('\n')
        // const required_reading = this.props.course && this.props.course.required_reading.split('\\n\\n').join('').split('\\r\\n').join('\n')
        // const recommended_reading = this.props.course && this.props.course.recommended_reading.split('\\n\\n').join('').split('\\r\\n').join('\n')
        // console.log(learning_outcome)
        return(
            <div>
                {this.props.course &&
                <div>
                    <div>{this.props.course.units} Units • {this.props.course.career} • {this.props.course.grading_basis}</div>
                    {/*<p>career: {this.props.course.career}</p>*/}
                    {/*<p>grading basis: {this.props.course.grading_basis}</p>*/}
                    <div className="divider"></div>
                    <div className="row">
                        <div className="col-md-7">
                            {this.props.course.description}
                        </div>
                        <div className="col-md-5">
                            <p><span className="little-title">Add Consent</span><br /> {this.props.course.add_consent}</p>
                            <p><span className="little-title">Drop Consent</span><br /> {this.props.course.drop_consent}</p>
                            <p><span className="little-title">Enroll Requirements</span><br />{this.props.course.enroll_requirement}</p>
                        </div>
                    </div>
                    {/*<p>add consent: {this.props.course.add_consent}</p>*/}
                    {/*<p>drop consent: {this.props.course.drop_consent}</p>*/}
                    {/*<p>enroll requirements: {this.props.course.enroll_requirements}</p>*/}
                    {/*<p>description: {this.props.course.description}</p>*/}
                    <div className="more-info">
                        <div className="content-paragraph"><span className="little-title white-space-wrap">Learning Outcome</span><br /> {learning_outcome}</div>
                        <div className="content-paragraph"><span className="little-title white-space-wrap">Course Syllabus</span><br /> {course_syllabus}</div>
                        <div className="content-paragraph"><span className="little-title white-space-wrap">Feedback</span><br /> {feedback}</div>
                        <div className="content-paragraph"><span className="little-title white-space-wrap">Required Reading</span><br />{required_reading}</div>
                        <div className="content-paragraph"><span className="little-title white-space-wrap">Recommended Reading</span><br /> {recommended_reading}</div>
                    </div>
                </div>
                }
            </div>
        )
    }
}

class CourseComponents extends React.Component{
    render(){
        const rows = this.props.components.map((component, index)=>
            <tr key={index}>
              <th scope="row">{index+1}</th>
              <td>{component.name}</td>
              <td>{component.note}</td>
            </tr>
        );
        return(
            <table className="table info-table">
              <tbody>
                {rows}
              </tbody>
            </table>
        )
    }
}

class CourseAssessments extends React.Component{
    render(){
        const rows = this.props.assessments.map((assessment, index)=>
            <tr key={index}>
                <th scope="row">{index+1}</th>
                <td>{assessment.type}</td>
                <td>{assessment.percent}%</td>
            </tr>
        );
        return(
            <table className="table info-table">
                <tbody>
                {rows}
                </tbody>
            </table>
        )
    }
}

class CourseSections extends React.Component{
    render(){
        const sections = {};
        this.props.sections.map((section)=>{
            if(sections.hasOwnProperty(section.category)){
                sections[section.category].push(section)
            }
            else{
                sections[section.category] = []
                sections[section.category].push(section)
            }
        });
        // console.log(sections)
        const sectionCategories = Object.entries(sections).map(([key, value], index)=>
            <SectionCategory category={key} sections={value} key={index}/>
        );
        // console.log(sectionCategories)
        return(
            <div>
                {sectionCategories}
            </div>
        )
    }
}

class SectionCategory extends React.Component{
    render(){
        // console.log(this.props.category);
        // console.log(this.props.sections)
        const sectionList = this.props.sections.map((section, index)=>
            <SectionItem key={index} section={section} />
        );
        return(
            <div>
                <h4>Section {this.props.category}</h4>
                {sectionList}
            </div>
        )
    }
}

class SectionItem extends React.Component{
    render(){
        const meetingList = this.props.section.meetings.map((meeting, index)=>
            <MeetingItem key={index} meeting={meeting} />
        );
        let statusClass = null;
        if(this.props.section.status === 'Open')
            statusClass='ion-record open';
        else if(this.props.section.status === 'Closed')
            statusClass='ion-stop closed';
        else
            statusClass = 'ion-android-warning waiting';
        // console.log(this.props.section.instructor.split(','))
        const instructor = this.props.section.instructor.split(',').map((prof, index)=> {
                // console.log(prof)
                return <span key={index}>{prof} <br /></span>
            }
        )
        return(
            <div className="section-card">
                <div className="section-code">{this.props.section.section_code}</div>
                <div className="divider"></div>
                <p> <span className={statusClass}></span> {this.props.section.status} • {this.props.section.type} •  {this.props.section.term}</p>
                <div className="row">
                    <div className="col-md-6">
                        {/*<h4>class details</h4>*/}
                        <p><span className="little-title">Instructor</span><br /> {instructor}</p>
                        <p><span className="little-title">Instruction mode</span><br /> {this.props.section.instruction_mode}</p>
                        <p><span className="little-title">Language</span><br /> {this.props.section.language}</p>
                        <p><span className="little-title">Class capacity</span><br /> {this.props.section.class_capacity}</p>
                    </div>
                    <div className="col-md-6">
                        {/*<h4>class availability</h4>*/}
                        <p><span className="little-title">Enrollment total</span><br /> {this.props.section.enrollment_total}</p>
                        <p><span className="little-title">Available seat</span><br /> {this.props.section.available_seat}</p>
                        <p><span className="little-title">Wait capacity</span><br /> {this.props.section.wait_capacity}</p>
                        <p><span className="little-title">Wait total</span><br /> {this.props.section.wait_total}</p>
                    </div>
                </div>
                {/*<h4>meeting information</h4>*/}
                <table className="table info-table">
                  <thead>
                    <tr>
                      <th scope="col">Weekday</th>
                      <th scope="col">Start Time</th>
                      <th scope="col">End Time</th>
                      <th scope="col">Room</th>
                      <th scope="col">Meeting Dates</th>
                    </tr>
                  </thead>
                  <tbody>
                    {meetingList}
                  </tbody>
                </table>
            </div>
        )
    }
}

class MeetingItem extends React.Component{
    render(){
        return(
            <tr>
              <td>{this.props.meeting.day}</td>
              <td>{this.props.meeting.start}</td>
              <td>{this.props.meeting.end}</td>
              <td>{this.props.meeting.room}</td>
              <td>{this.props.meeting.meeting_dates}</td>
            </tr>
        )
    }
}

ReactDOM.render(<CoursePage/>, document.getElementById('course-page'));