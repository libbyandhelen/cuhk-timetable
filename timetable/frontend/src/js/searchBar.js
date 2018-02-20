import React from 'react';

import '../styles/base.css';
import '../styles/searchBar.css';
import '../styles/ripple.css';
import '../styles/searchBox.css';

class SearchBar extends React.Component{
    constructor(props){
        super(props);
        this.state = {
            searchResults: [],
        };
        this.handleChange = this.handleChange.bind(this);
        this.getSearchResults = this.getSearchResults.bind(this);
    }
    handleChange(event){
        let query_param = event.target.value.split(' ').join('+');

        request(`/search/?q=${query_param}`, 'GET', null, this.getSearchResults);
    }

    getSearchResults(data){
        if(data.code !== 0){
            console.log(data.msg)
        }
        else{
            this.setState({
                searchResults: data.body
            })
        }
    }

    render(){
        return(
            <div>
                <div className="search-input">
                    <input type="text" onChange={this.handleChange}/>
                    <span className="highlight"></span>
                    <span className="bar"></span>
                    <span className="ion-search"></span>
                </div>
                <SearchResultList
                    searchResults={this.state.searchResults}
                    // selectedSections={this.props.selectedSections}
                    changeSections={this.props.changeSections}
                    warnState={this.props.warnState}
                    changeWarnState={this.props.changeWarnState}
                />
            </div>
        )
    }
}

class SearchResultList extends React.Component{
    render(){
        const listGroup = this.props.searchResults.map((course=>
                <SearchResultCourseItem
                    key={course.id}
                    course={course}
                    // selectedSections={this.props.selectedSections}
                    changeSections={this.props.changeSections}
                    warnState={this.props.warnState}
                    changeWarnState={this.props.changeWarnState}
                />
        ));

        return(
            <div id="accordion" role="tablist">
                {listGroup}
            </div>
        )
    }
}

class SearchResultCourseItem extends React.Component{
    constructor(props){
        super(props);
    }
    jumpCourse(){
        window.location.href = `/courses/${this.props.course.id}`
    }
    handleClick(){
        $('.term-list').removeClass('shown').addClass('not-shown');
    }
    render(){
        const href = `#${this.props.course.id}`;
        return(
          <div className="my-card">
            <div className="accordion-header" role="tab" id="headingOne" onClick={this.handleClick}>
              <div className="mb-0">
                <div className="collapsed" data-toggle="collapse" href={href} role="button" aria-expanded="false" aria-controls={this.props.course.id}>
                    {/*<div className="row">*/}
                        {/*<div className="icon-col">*/}
                            {/*<div className="info-button">*/}
                                {/*<a href={`/courses/${this.props.course.id}`} className="ion-ios-information-outline search-info-btn" ></a>*/}
                            {/*</div>*/}
                        {/*</div>*/}
                        {/*<div className="code-title">*/}
                            <a href={`/courses/${this.props.course.id}`} className="class-code indie">{this.props.course.course_code}</a>
                            <p className="class-name">{this.props.course.course_name}</p>
                        {/*</div>*/}
                    {/*</div>*/}
                </div>
              </div>
            </div>

            <div id={this.props.course.id} className="collapse" role="tabpanel" aria-labelledby="headingOne" data-parent="#accordion">
              <div className="card-body accordion-body">
                  <SearchResultSectionList
                      courseId={this.props.course.id}
                      // selectedSections={this.props.selectedSections}
                      changeSections={this.props.changeSections}
                      warnState={this.props.warnState}
                      changeWarnState={this.props.changeWarnState}
                  />
              </div>
            </div>
          </div>
        )
    }
}

class SearchResultSectionList extends React.Component{
    constructor(props){
        super(props);
        this.state = {
            categories: [],
            categoryTerm: {}
        };
        this.getSections = this.getSections.bind(this)
    }

    getSections(data){
        if(data.code!==0){
            console.log(data.msg)
        }
        else{
            const categoryList = [];
            const categoryTerm = {};

            data.body.map((section)=>{
                if(categoryList.indexOf(section.category) === -1)
                    categoryList.push(section.category);

                let category = section.category;
                try{
                    if(categoryTerm[category].indexOf(section.term) === -1)
                        categoryTerm[category].push(section.term)
                }
                catch(err){
                    categoryTerm[category] = [];
                    categoryTerm[category].push(section.term)
                }
            });
            this.setState({
                categories: categoryList,
                categoryTerm: categoryTerm
            })
        }
    }

    componentDidMount(){
        request(`/api/courses/${this.props.courseId}/sections`, "GET", null, this.getSections)
    }

    render(){
        const listGroup = this.state.categories.map((category, index)=>
            <SearchResultSectionItem
                key={index}
                category={category}
                courseId={this.props.courseId}
                terms={this.state.categoryTerm[category]}
                // selectedSections={this.props.selectedSections}
                changeSections={this.props.changeSections}
                warnState={this.props.warnState}
                changeWarnState={this.props.changeWarnState}
            />
        );

        return(
            <ul className="list-group section-list-group">
                {listGroup}
            </ul>
        )
    }
}

class SearchResultSectionItem extends React.Component{
    constructor(props){
        super(props);
        this.handleClick = this.handleClick.bind(this);
    }

    handleClick(){
        const flag = $('#term-list-'+ this.props.courseId+this.props.category).attr('class').split(' ')[1];
        if(flag === 'not-shown'){
            $('.term-list').removeClass('shown').addClass('not-shown');
            $('#term-list-'+ this.props.courseId+this.props.category).removeClass('not-shown').addClass('shown')
        }
        else{
            $('#term-list-'+ this.props.courseId+this.props.category).removeClass('shown').addClass('not-shown')
        }
    }
    render(){
        const termList = this.props.terms.map((term, index)=>
            <TermItem
                key={index}
                term={term}
                category={this.props.category}
                courseId={this.props.courseId}
                // selectedSections={this.props.selectedSections}
                changeSections={this.props.changeSections}
                warnState={this.props.warnState}
                changeWarnState={this.props.changeWarnState}
            />
        );
        return(
            <li className="category-list">
                <div className="row">
                    <div className="category">
                        Section: {this.props.category}
                    </div>
                    <div className="icon-col">
                        <div id={this.props.courseId+this.props.category} className="info-button"  data-toggle="popover" data-placement="right">
                            <i className="ion-android-add-circle" onClick={this.handleClick}></i>
                        </div>
                    </div>
                </div>

                <div id={`term-list-${this.props.courseId}${this.props.category}`} className={`term-list not-shown`}>
                  <ul className="list-group">
                      {termList}
                  </ul>
                </div>
            </li>
        )
    }
}

class TermItem extends React.Component{
    constructor(props){
        super(props);
        this.handleClick = this.handleClick.bind(this);
        this.selectSections = this.selectSections.bind(this);
    }

    handleClick(){
        const data = {
            course_id: this.props.courseId,
            category: this.props.category,
            term: this.props.term
        };
        request('/api/selectsections/', 'POST', data, this.selectSections);
        $('#term-list-'+ this.props.courseId+this.props.category).removeClass('shown').addClass('not-shown')
    }

    selectSections(data){
        if(data.code === 2011){
            this.props.changeWarnState({
                className: 'warn-show',
                warnMsg: data.msg
            });
        }
        else if(data.code !== 0){
            console.error(data.msg);
        }
        else{
            // console.log(data.body);
            // record whether there is a meeting is TBA
            let flag = 0;
            data.body.map((section)=>{
                section.section.meetings.map((meeting)=>{
                    if(meeting.day === 'TBA' || meeting.start === 'TBA' || meeting.end === 'TBA'){
                        flag = 1;
                        console.log(meeting)
                    }
                })
            });
            if(flag === 1){
                this.props.changeWarnState({
                    className: 'warn-show',
                    warnMsg: 'some meetings in this section are TBA'
                });
            }
            this.props.changeSections();
        }
    }
    render(){
        return(
            <li className="term-item" onClick={this.handleClick}>
                {this.props.term}
            </li>
        )
    }
}

export default SearchBar

