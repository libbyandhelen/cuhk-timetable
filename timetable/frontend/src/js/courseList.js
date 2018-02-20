import React from 'react';
import '../styles/courseList.css';

class CourseList extends React.Component{

    render(){
        const courseLabelList = [];
        const courseList = [];
        let credit = 0;
        this.props.selectedSections.map((selectedSection)=>{
            if(selectedSection.section.term === this.props.choosedTerm){
                const label = `${selectedSection.section.course.id} ${selectedSection.section.category}`;
                // const background = $('.'+selectedSection.section.course.id+selectedSection.section.category).css('background-color');
                selectedSection.section.course.color = selectedSection.bgcolor;
                if(courseLabelList.indexOf(label) === -1){
                    courseLabelList.push(label);
                    courseList.push(selectedSection.section.course)
                    credit = credit + selectedSection.section.course.units
                    // console.log(selectedSection.section.course.color)
                }
            }
        });
        // console.log(courseList)
        const listGroup = courseList.map((course, index)=>
            <CourseItem
                key={index}
                courseLabel={courseLabelList[index]}
                courseInfo={course}
                // units={this.props.units}
                // changeUnits={this.props.changeUnits}
                choosedTerm={this.props.choosedTerm}
                changeSections={this.props.changeSections}
                selectedSections={this.props.selectedSections}
                toggleSelectedSection={this.props.toggleSelectedSection}
                changeSiblings={this.props.changeSiblings}
                selectedSiblings={this.props.selectedSiblings}
            />

        );
        return(
            <div>
                <ul className="list-group">
                    {listGroup}
                </ul>
                <div className="units indie">Total Units: {credit}</div>
            </div>
        )
    }
}

class CourseItem extends React.Component{
    constructor(props){
        super(props);
        this.deleteSections = this.deleteSections.bind(this);
        this.handleClick = this.handleClick.bind(this);
        this.jumpCourse = this.jumpCourse.bind(this);
        this.clickColor = this.clickColor.bind(this);
        this.changeColor = this.changeColor.bind(this);
        this.afterChangeColor = this.afterChangeColor.bind(this);
        this.toggleEye = this.toggleEye.bind(this);
        this.state = {
            eyeClass: 'ion-eye-disabled'
        }
    }

    toggleEye(){
        this.setState((prevState, props)=>{
            if(prevState.eyeClass === 'ion-eye-disabled'){
                props.selectedSections.map((selectedSection)=>{
                    if(selectedSection.section.course.id === props.courseInfo.id && selectedSection.section.category === props.courseLabel.split(' ')[1]){
                        selectedSection.show = 0
                    }
                });
                props.toggleSelectedSection(props.selectedSections);

                props.selectedSiblings.map((selectedSibling)=>{
                    if(selectedSibling.course.id === props.courseInfo.id && selectedSibling.category === props.courseLabel.split(' ')[1]){
                        selectedSibling.show = 0
                    }
                });
                props.changeSiblings(props.selectedSiblings);
                return{
                    eyeClass:'ion-eye'
                }
            }
            else{
                props.selectedSections.map((selectedSection)=>{
                    if(selectedSection.section.course.id === props.courseInfo.id && selectedSection.section.category === props.courseLabel.split(' ')[1]){
                        selectedSection.show = 1
                    }
                });
                props.toggleSelectedSection(props.selectedSections);

                props.selectedSiblings.map((selectedSibling)=>{
                    if(selectedSibling.course.id === props.courseInfo.id && selectedSibling.category === props.courseLabel.split(' ')[1]){
                        selectedSibling.show = 1
                    }
                });
                props.changeSiblings(props.selectedSiblings);
                return{
                    eyeClass: 'ion-eye-disabled'
                }
            }
        })
    }

    changeColor(e){
        $('#color-panel-'+this.props.courseInfo.id+this.props.courseLabel.split(' ')[1]).removeClass('color-show').addClass('color-hide')
        const data = {
            course_id: this.props.courseInfo.id,
            category: this.props.courseLabel.split(' ')[1],
            term: this.props.choosedTerm,
            bg_color: e.target.style.backgroundColor,
            color: e.target.style.color
        };
        request(
            '/api/selectsections/color',
            'POST',
            data,
            this.afterChangeColor
        )
    }

    afterChangeColor(data){
        if(data.code !== 0){
            console.error(data.msg)
        }
        else{
            this.props.changeSections()
        }
    }

    clickColor(){
        // console.log('#color-panel-'+this.props.courseInfo.course_code+this.props.courseLabel.split(' ')[1])
        const flag = $('#color-panel-'+this.props.courseInfo.id+this.props.courseLabel.split(' ')[1]).attr('class').split(' ')[1]
        if(flag === 'color-hide'){
            $('.color-panel').removeClass('color-show').addClass('color-hide');
            $('#color-panel-'+this.props.courseInfo.id+this.props.courseLabel.split(' ')[1]).removeClass('color-hide').addClass('color-show')
        }
        else{
            $('#color-panel-'+this.props.courseInfo.id+this.props.courseLabel.split(' ')[1]).removeClass('color-show').addClass('color-hide')
        }

    }

    jumpCourse(){
        window.location.href = `/courses/${this.props.courseInfo.id}`
    }

    handleClick(){
        const courseId = this.props.courseLabel.split(' ')[0];
        const category = this.props.courseLabel.split(' ')[1];
        const data = {
            course_id: courseId,
            category: category,
            term: this.props.choosedTerm
        };
        request(
            '/api/selectsections/', 'DELETE', data, this.deleteSections
        )
    }

    deleteSections(data){
        if(data.code !== 0)
            console.error(data.msg);
        else{
            this.props.changeSections()
        }
    }

    render(){
        const colorRow1 = [
            {
                bgcolor: '#C33C54',
                color: 'white'
            },
            {
                bgcolor: '#4F000B',
                color: 'white'
            },
            {
                bgcolor: '#E4C1F9',
                color: 'black'
            },
            {
                bgcolor: '#E06C9F',
                color: 'white'
            }
        ];
        const colorRow2 = [
            {
                bgcolor: '#F49E4C',
                color: 'black'
            },
            {
                bgcolor: '#ABE07D',
                color: 'black'
            },
            {
                bgcolor: '#596869',
                color: 'white'
            },
            {
                bgcolor: '#5A1659',
                color: 'white'
            }
        ];
        const row1 = colorRow1.map((ele, index)=>
            <td key={index} style={{backgroundColor: ele.bgcolor, color: ele.color}} className="color-grid" onClick={this.changeColor}></td>
        )
        const row2 = colorRow2.map((ele, index)=>
            <td key={index} style={{backgroundColor: ele.bgcolor, color: ele.color}} className="color-grid" onClick={this.changeColor}></td>
        )
        const style = {
            color: this.props.courseInfo.color
        };
        return(
            <li className="list-group-item course-list-item yellow">
                <div>
                    <div className="course-list-row">
                        <div className="color-col">
                            <div style={style}>
                                <span className="ion-stop color-icon" onClick={this.clickColor}></span>
                            </div>
                            <div className="color-panel color-hide" id={`color-panel-${this.props.courseInfo.id}${this.props.courseLabel.split(' ')[1]}`}>
                                <table className="color-table">
                                    <tbody>
                                        <tr>
                                            {row1}
                                        </tr>
                                        <tr>
                                            {row2}
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                        <div className="name-col" onClick={this.jumpCourse}>
                            <p className="course-code indie">
                                {this.props.courseInfo.course_code}
                            </p>
                        </div>
                        <div className="delete-btn-col">
                            <div className="icons">
                                <span onClick={this.handleClick} className="ion-trash-a"></span>
                            </div>
                        </div>
                        <div className="info-btn-col">
                            <div className="icons">
                                {/*<span onClick={this.jumpCourse} className="ion-information-circled"></span>*/}
                                <span className={this.state.eyeClass} onClick={this.toggleEye}></span>
                            </div>
                        </div>
                    </div>
                    <p className="course-name">
                        {this.props.courseInfo.course_name}
                    </p>
                    <p className="section">
                        Section {this.props.courseLabel.split(' ')[1]} | {this.props.courseInfo.units} Units
                    </p>
                </div>
            </li>
        )
    }
}

export default CourseList