import React from 'react';
import '../styles/timetable.css';

class Timetable extends React.Component{
    constructor(props){
        super(props);

    }
    render(){
        let sectionList = [];
        // console.log(this.props.selectedSections)
        this.props.selectedSections.map((selectedSection)=>{
            if(selectedSection.section.term === this.props.choosedTerm){
                // console.log(selectedSection.bgcolor)

                selectedSection.section['bgcolor'] = selectedSection.bgcolor;
                selectedSection.section['color'] = selectedSection.color;
                if(selectedSection.show === 1){
                    sectionList.push(selectedSection.section)
                }
            }
        });
        // console.log(sectionList)

        const days = ['Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa', 'Su'];
        const dayCount = [0,0,0,0,0,0,0];
        const meetingOfDay = [[],[],[],[],[],[],[]];
        const times = ['8:30','9:30','10:30','11:30','12:30','13:30','14:30','15:30','16:30','17:30','18:30','19:30'];
        this.props.selectedSiblings.map((sibling)=>{
            if(sibling.show === 1){
                sectionList.push(sibling)
            }
        })
        // sectionList = sectionList.concat(this.props.selectedSiblings);
        // console.log(sectionList)
        sectionList.map((section)=>{
            section.meetings.map((meeting)=>{
                // dayCount[days.indexOf(meeting.day)]++
                let start = parseInt(meeting.start.split(':')[0]);
                let end = parseInt(meeting.end.split(':')[0]);
                if(meeting.start.indexOf("PM")!==-1){
                    if(start !== 12)
                        start = start + 12;
                    end = end + 12;
                }
                else if (meeting.end.indexOf("PM")!==-1 && end !== 12){
                    end = end + 12;
                }
                // const hash = section.course.id+section.category.charCodeAt(0)+section.category.length;
                // meeting.style = colorScheme[hash%colorScheme.length];
                meeting.style = {
                    backgroundColor: section.bgcolor,
                    color: section.color
                };
                try {
                    // console.log(meeting.day)
                    meetingOfDay[days.indexOf(meeting.day)].push({
                        // meeting: meeting,
                        start: start,
                        end: end
                    })
                    // console.log(colorScheme[hash%colorScheme.length])
                }
                catch(err){
                }
            })
        });
        // console.log(meetingOfDay)

        days.map((day, index)=>{
            meetingOfDay[index].map((meetingI)=>{
                let counter = 0;
                meetingOfDay[index].map((meetingJ)=>{
                    if(meetingJ.start>=meetingI.start && meetingJ.start<meetingI.end){
                        counter++;
                    }
                });
                // console.log(counter);
                if(counter>dayCount[index]){
                    dayCount[index] = counter
                }
            })
        })
        // console.log(dayCount)
        return(
            <table className="timetable table">
                <TableHeader
                    days={days}
                    dayCount={dayCount}
                />
                <TableBody
                    days={days}
                    times={times}
                    sectionList={sectionList}
                    dayCount={dayCount}
                    siblingSections={this.props.siblingSections}
                    changeSiblings={this.props.changeSiblings}
                    selectedSiblings={this.props.selectedSiblings}
                    changeTargetSection={this.props.changeTargetSection}
                    targetSection={this.props.targetSection}
                    changeSections={this.props.changeSections}
                />
            </table>
        )
    }
}

class TableHeader extends React.Component{
    constructor(props){
        super(props);

    }

    render(){
        const header = this.props.days.map((day, index)=>
            <th scope="col" key={day.toString()} colSpan={this.props.dayCount[index]}>{day}</th>
        );

        return(
            <thead>
                <tr className="table-header">
                    <th scope="row">Time</th>
                    {header}
                </tr>
            </thead>
        )
    }
}

class TableBody extends React.Component{
    constructor(props){
        super(props);
    }

    render(){
        const rows = this.props.times.map((time, index)=>{
            let meetingList = [];
            let dayNum = [0,0,0,0,0,0,0];
            this.props.sectionList.map((section)=>{
                section.meetings.map((meeting)=>{
                    let start = parseInt(meeting.start.split(':')[0]);
                    let end = parseInt(meeting.end.split(':')[0]);
                    let diff;
                    if(meeting.start.indexOf("PM")!==-1){
                        if(start !== 12)
                            start = start + 12;
                        end = end + 12;
                    }
                    else if (meeting.end.indexOf("PM")!==-1 && end !== 12){
                        end = end + 12;
                    }
                    diff = end-start;
                    // console.log(diff)

                    if(start === parseInt(time.split(':')[0])){
                        meetingList.push({
                            meeting: meeting,
                            section: section,
                            rowspan: diff,
                        });
                    }
                    if(parseInt(time.split(':')[0])<end && parseInt(time.split(':')[0])>=start){
                        dayNum[this.props.days.indexOf(meeting.day)]++
                    }
                })
            });
            return  <TableRow
                key={index}
                time={time.toString()}
                days={this.props.days}
                dayNum={dayNum}
                dayCount={this.props.dayCount}
                meetingList={meetingList}
                siblingSections={this.props.siblingSections}
                changeSiblings={this.props.changeSiblings}
                selectedSiblings={this.props.selectedSiblings}
                changeTargetSection={this.props.changeTargetSection}
                targetSection={this.props.targetSection}
                changeSections={this.props.changeSections}
            />
        });
        return(
            <tbody>
            {rows}
            </tbody>
        )
    }
}

class TableRow extends React.Component{
    constructor(props){
        super(props);
    }

    render(){
        // console.log(this.props.meetingList);
        // dayCount: in this day, how many meetings are clash together
        // dayNum: in this day and at this time, how many meetings are clash together
        const meetings = [];
        this.props.days.map((day, index)=>{
            // console.log(this.props.dayCount[index])
            // console.log(this.props.dayNum[index])
            let count = this.props.dayCount[index]
            if(count === 0)
                count = count+1
            count = count-this.props.dayNum[index];
            this.props.meetingList.map((meeting)=>{
                if(meeting.meeting.day === day){
                    meetings.push(meeting)
                    // flag = 1
                    // count = count-1
                }
            })
            for(let i = 0;i<count;i++){
                meetings.push(null)
            }
        })
        // console.log(meetings)

        const sections = meetings.map((meeting, index)=>
            <SectionBlock
                key={index}
                meeting={meeting}
                siblingSections={this.props.siblingSections}
                changeSiblings={this.props.changeSiblings}
                selectedSiblings={this.props.selectedSiblings}
                changeTargetSection={this.props.changeTargetSection}
                targetSection={this.props.targetSection}
                changeSections={this.props.changeSections}
            />
        )

        return(
            <tr>
                <th scope="row" className="time">{this.props.time}</th>
                {sections}
            </tr>
        )
    }
}

class SectionBlock extends React.Component{
    constructor(props){
        super(props);
        this.state = {
            showSiblings: true
        }
        this.handleClick = this.handleClick.bind(this)
        this.deleteTargetSection = this.deleteTargetSection.bind(this);
        this.createSelectSection = this.createSelectSection.bind(this)
    }

    handleClick(){
        // console.log(this.props.siblingSections)
        let flag = 0
        this.props.selectedSiblings.map((selectedSibling)=>{
            if(this.props.meeting.section.id === selectedSibling.id){
                flag = 1;
            }
        });
        // if the meeting belongs to a section already been selected
        if(flag === 0){
            const siblingList = []
            this.props.siblingSections.map((sibling)=>{
                if(sibling.self_id === this.props.meeting.section.id){
                    sibling.sibling.bgcolor = this.props.meeting.meeting.style.backgroundColor;
                    sibling.sibling.color = this.props.meeting.meeting.style.color;
                    sibling.sibling.show = 1;
                    siblingList.push(sibling.sibling)
                }
            })
            // console.log(siblingList)
            if(siblingList.length === 0)
                return;
            if(this.props.targetSection === null || this.props.targetSection !== this.props.meeting.section.id){
                this.props.changeSiblings(siblingList);
                this.props.changeTargetSection(this.props.meeting.section.id)
            }
            else{
                request(
                    `/api/selectsections/${this.props.targetSection}`,
                    'DELETE',
                    null,
                    this.deleteTargetSection
                )
            }
        }
        else{
            request(
                `/api/selectsections/${this.props.targetSection}`,
                'DELETE',
                null,
                this.deleteTargetSection
            )
        }
    }
    deleteTargetSection(data){
        if(data.code !== 0){
            console.error(data.msg)
        }
        else{
            // console.log(this.props)
            const postData = {
                bg_color: this.props.meeting.meeting.style.backgroundColor,
                color: this.props.meeting.meeting.style.color
            };
            request(
                `api/selectsections/${this.props.meeting.section.id}`,
                'POST',
                postData,
                this.createSelectSection
            )
        }
    }

    createSelectSection(data){
        if(data.code !== 0){
            console.error(data.msg)
        }
        else{
            this.props.changeSections();
            this.props.changeTargetSection(null)
        }
    }
    render(){
        // console.log(this.props.meeting && this.props.meeting.meeting.style)
        let statusClass = null;
        if(this.props.meeting){
            if(this.props.meeting.section.status === 'Open')
                statusClass='ion-record open';
            else if(this.props.meeting.section.status === 'Closed')
                statusClass='ion-stop closed';
            else
                statusClass = 'ion-android-warning waiting';
        }
        return(
            <td rowSpan={this.props.meeting && this.props.meeting.rowspan}
                style={this.props.meeting && this.props.meeting.meeting.style}
                className={this.props.meeting && 'block '+this.props.meeting.section.course.id+this.props.meeting.section.category}>
                {this.props.meeting &&
                <div className={`section-block ${this.props.meeting.section.course.id}${this.props.meeting.section.category} block-show`} onClick={this.handleClick}>
                    <p className="block-content code indie">{this.props.meeting.section.course.course_code}</p>
                    <p className="block-content sub">Section {this.props.meeting.section.section_code}</p>
                    <p className="block-content sub"><span className={statusClass}></span> {this.props.meeting.section.status}</p>
                    <p className="block-content sub">{this.props.meeting.section.type}</p>
                    <p className="block-content sub">{this.props.meeting.meeting.day}</p>
                    <p className="block-content sub">{this.props.meeting.meeting.start} - {this.props.meeting.meeting.end}</p>
                </div>
                }
            </td>
        )
    }
}

export default Timetable;