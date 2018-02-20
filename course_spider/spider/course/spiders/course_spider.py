import re

import scrapy

from course.items import CourseItem, SectionItem, MeetingItem, AssessmentItem, ComponentItem

from Course.models import Course, Component, Assessment
from Section.models import Section, Meeting
from base.error import Error


def extract_content(array):
    content = ''
    for i in array:
        content = content+i
    return content


class CourseSpider(scrapy.Spider):
    name = "course"
    course_counter = 0
    term_counter = 0
    section_counter = 0

    def __init__(self, alphanums=None, *args, **kwargs):
        super().__init__(**kwargs)
        self.alphanums = int(alphanums)

    def start_requests(self):
        return [scrapy.Request(
            url='https://cusis.cuhk.edu.hk/psc/public/EMPLOYEE/HRMS/c/COMMUNITY_ACCESS.SSS_BROWSE_CATLG.GBL',
            method="POST",
            callback=self.submit_alphanum
        )]

    def submit_alphanum(self, response):
        # navigate the appropriate alphabet
        alphanums = response.xpath("//span[@class='SSSAZLINK' or @class='SSSAZLINKHOVER']/a/attribute::id")[self.alphanums].extract()
        request = scrapy.FormRequest.from_response(
            response=response,
            formname='win0',
            formdata={
                'ICAction': alphanums
            },
            callback=self.expand_all,
        )
        yield request

    def expand_all(self, response):
        # print(response.meta['item'])
        # press the extract all button
        if response.xpath("//span[@class='SSSHYPERLINKBOLD']/a/text()").extract_first():
            request = scrapy.FormRequest.from_response(
                response=response,
                formname='win0',
                formdata={
                    'ICAction': 'DERIVED_SSS_BCC_SSS_EXPAND_ALL$76$'
                },
                callback=self.get_course_detail,
            )
            yield request

    def get_course_detail(self, response):
        # for each course, navigate to the course detail page
        courses = response.xpath("//a[@title='View Course Details']/attribute::name").extract()
        course_num = len(courses)
        # print(course_num)
        if self.course_counter >= course_num:
            return
        # try:
        request = scrapy.FormRequest.from_response(
            response=response,
            formname='win0',
            formdata={
                'ICAction': courses[self.course_counter]
            },
            callback=self.parse_course_detail
        )

        self.course_counter = self.course_counter + 1
        yield request
        # except IndexError:
        #     return

    def parse_course_detail(self, response):
        # store the course detail
        # course_code = None
        # course_name = None
        response = response.replace(body=response.body.replace(b'<br />', b'\n'))
        name = response.xpath("//span[@class='PALEVEL0SECONDARY']/text()").extract_first()
        try:
            course_code = name.split(" - ")[0]
            course_name = name.split(" - ")[1]
        except:
            course_code = name
            course_name = name
        print(course_code)
        career = response.xpath("//label[@for='SSR_CRSE_OFF_VW_ACAD_CAREER$0']/../../following-sibling::tr[1]/td/span[@class='PSDROPDOWNLIST_DISPONLY']/text()").extract_first() or ''
        try:
            units = float(response.xpath("//label[@for='DERIVED_CRSECAT_UNITS_RANGE$0']/../../following-sibling::tr[1]/td/span[@class='PSEDITBOX_DISPONLY']/text()").extract_first() or 0)
        except ValueError:
            units = 0
        grading_basis = response.xpath(
            "//label[@for='SSR_CRSE_OFF_VW_GRADING_BASIS$0']/../following-sibling::td[1]/span/text()").extract_first() or ''
        add_consent = response.xpath(
            "//label[@for='SSR_CRSE_OFF_VW_CONSENT$0']/../following-sibling::td[1]/span/text()").extract_first() or ''
        drop_consent = response.xpath(
            "//label[@for='SSR_CRSE_OFF_VW_SSR_DROP_CONSENT$0']/../following-sibling::td[1]/span/text()").extract_first() or ''
        enroll_requirement = response.xpath(
            "//label[@for='SSR_CRSE_OFF_VW_RQRMNT_GROUP$0']/../../following-sibling::tr[1]//span/text()").extract_first() or ''
        description = response.xpath(
            "//td[text()='Description']/../following-sibling::tr[1]//span/text()").extract_first() or ''
        saved_item = None

        ret = Course.get_course_by_code(course_code)
        # if course is not exist, create new course
        if ret.error is not Error.OK:
            course_item = CourseItem()
            course_item['course_code'] = course_code
            course_item['course_name'] = course_name
            course_item['career'] = career
            course_item['units'] = units
            course_item['grading_basis'] = grading_basis
            course_item['add_consent'] = add_consent
            course_item['drop_consent'] = drop_consent
            course_item['enroll_requirement'] = enroll_requirement
            course_item['description'] = description
            try:
                saved_item = course_item.save()
            except:
                pass
        # if course is exist, update the info
        else:
            course_item = ret.body
            course_item.course_code = course_code
            course_item.course_name = course_name
            course_item.career = career
            course_item.units = units
            course_item.grading_basis = grading_basis
            course_item.add_consent = add_consent
            course_item.drop_consent = drop_consent
            course_item.enroll_requirement = enroll_requirement
            course_item.description = description
            course_item.save()
            try:
                saved_item = course_item
            except:
                pass

            # delete all the assessment and components
            Component.delete_component_by_course(course_item)
            Assessment.delete_assessment_by_course(course_item)

        # course_item['course_code'] = course_code
        # course_item['course_name'] = course_name
        # course_item['career'] = response.xpath("//label[@for='SSR_CRSE_OFF_VW_ACAD_CAREER$0']/../../following-sibling::tr[1]/td/span[@class='PSDROPDOWNLIST_DISPONLY']/text()").extract_first()
        # try:
        #     course_item['units'] = float(response.xpath("//label[@for='DERIVED_CRSECAT_UNITS_RANGE$0']/../../following-sibling::tr[1]/td/span[@class='PSEDITBOX_DISPONLY']/text()").extract_first() or 0)
        # except ValueError:
        #     course_item['units'] = 0
        # course_item['grading_basis'] = response.xpath("//label[@for='SSR_CRSE_OFF_VW_GRADING_BASIS$0']/../following-sibling::td[1]/span/text()").extract_first()
        # course_item['add_consent'] = response.xpath("//label[@for='SSR_CRSE_OFF_VW_CONSENT$0']/../following-sibling::td[1]/span/text()").extract_first()
        # course_item['drop_consent'] = response.xpath("//label[@for='SSR_CRSE_OFF_VW_SSR_DROP_CONSENT$0']/../following-sibling::td[1]/span/text()").extract_first()
        # course_item['enroll_requirement'] = response.xpath("//label[@for='SSR_CRSE_OFF_VW_RQRMNT_GROUP$0']/../../following-sibling::tr[1]//span/text()").extract_first()
        # course_item['description'] = response.xpath("//td[text()='Description']/../following-sibling::tr[1]//span/text()").extract_first()
        #
        # saved_item = course_item.save()

        # save the component for later use
        components = response.xpath("//label[@for='SR_LBL_WRK_CRSE_COMPONENT_LBL$0']/../../preceding-sibling::tr[1]//span[@class='PSEDITBOX_DISPONLY']/text()").extract()

        request = scrapy.FormRequest.from_response(
            response=response,
            formname='win0',
            formdata={
                'ICAction': 'DERIVED_SAA_CRS_SSR_PB_GO'
            },
            callback=self.get_class_sections
        )
        self.term_counter = 0
        request.meta['item'] = saved_item
        request.meta['components'] = components
        yield request

    def get_class_sections(self, response):
        terms = response.xpath("//label[text()='Terms Offered']/../..//option/attribute::value").extract()
        term_num = len(terms)
        print(term_num)
        print(self.term_counter)

        # if all the terms are crawled, go to the course_outcome page
        if self.term_counter >= term_num:
            request = scrapy.FormRequest.from_response(
                response=response,
                formname='win0',
                formdata={
                    'ICAction': 'CU_DERIVED_CUR_CU_CRSE_OUT_BTN'
                },
                callback=self.parse_course_outcome
            )
            request.meta['item'] = response.meta['item']
            request.meta['components'] = response.meta['components']
            yield request
            # return

        # try:
        # navigate to all the terms
        else:
            request = scrapy.FormRequest.from_response(
                response=response,
                formname='win0',
                formdata={
                    'ICAction': 'DERIVED_SAA_CRS_SSR_PB_GO$92$',
                    'DERIVED_SAA_CRS_TERM_ALT': terms[self.term_counter]
                },
                callback=self.select_term
            )
            request.meta['term'] = terms[self.term_counter]
            request.meta['item'] = response.meta['item']
            request.meta['components'] = response.meta['components']
            self.term_counter = self.term_counter + 1
            yield request
        # except IndexError:
        #     request = scrapy.FormRequest.from_response(
        #         response=response,
        #         formname='win0',
        #         formdata={
        #             'ICAction': 'CU_DERIVED_CUR_CU_CRSE_OUT_BTN'
        #         },
        #         callback=self.parse_course_outcome
        #     )
        #     request.meta['item'] = response.meta['item']
        #     request.meta['components'] = response.meta['components']
        #     yield request
        # return

    def select_term(self, response):
        # press view all button
        term = response.meta['term']
        print(term)
        request = scrapy.FormRequest.from_response(
            response=response,
            formname='win0',
            formdata={
                'ICAction': 'CLASS_TBL_VW5$fviewall$0',
                'DERIVED_SAA_CRS_TERM_ALT': term
            },
            callback=self.show_all_sections
        )
        self.section_counter = 0
        request.meta['item'] = response.meta['item']
        request.meta['term'] = term
        request.meta['components'] = response.meta['components']
        yield request

    def show_all_sections(self, response):
        term = response.meta['term']
        sections = response.xpath("//a[@title='Class Details']/attribute::name").extract()
        section_num = len(sections)
        print('section num %d' % section_num)
        print(self.section_counter)
        # if all the sections are crawled, go to change another term
        if self.section_counter >= section_num:
            request = scrapy.FormRequest.from_response(
                response=response,
                formname='win0',
                formdata={
                    'ICAction': 'DERIVED_SAA_CRS_SSR_PB_GO$92$',
                    'DERIVED_SAA_CRS_TERM_ALT': term
                },
                callback=self.get_class_sections
            )
            request.meta['item'] = response.meta['item']
            request.meta['components'] = response.meta['components']
            yield request
            # return
        # try:
        # navigate to the section detail page
        else:
            request = scrapy.FormRequest.from_response(
                response=response,
                formname='win0',
                formdata={
                    'ICAction': sections[self.section_counter],
                    'DERIVED_SAA_CRS_TERM_ALT': term
                },
                callback=self.get_section_detail
            )
            request.meta['term'] = term
            request.meta['item'] = response.meta['item']
            request.meta['components'] = response.meta['components']
            self.section_counter = self.section_counter + 1
            yield request
        # except IndexError:
        #     request = scrapy.FormRequest.from_response(
        #         response=response,
        #         formname='win0',
        #         formdata={
        #             'ICAction': 'DERIVED_SAA_CRS_SSR_PB_GO$92$',
        #             'DERIVED_SAA_CRS_TERM_ALT': term
        #         },
        #         callback=self.get_class_sections
        #     )
        #     request.meta['item'] = response.meta['item']
        #     request.meta['components'] = response.meta['components']
        #     yield request
        #     # return

    def get_section_detail(self, response):
        course_item = response.meta['item']

        # extract section code and category
        response = response.replace(body=response.body.replace(b'<br />', b'\n'))
        title = response.xpath("//span[@class='PALEVEL0SECONDARY']/text()").extract_first()
        section_code = ''
        category = ''
        try:
            section_code = title.split('\xa0\xa0')[0].split(' - ')[1]
            if section_code.startswith('-'):
                category = '-'
            elif not re.search('\d+', section_code):
                category = section_code
            else:
                number_free_code = re.sub('\d+', '', section_code)
                category = number_free_code[:-1]
        except:
            pass

        # extract term and type
        title = response.xpath("//span[@class='SSSKEYTEXT']/text()").extract_first()
        term = ''
        type = ''
        try:
            term = title.split(' | ')[1]
            type = title.split(' | ')[2]
        except:
            pass

        # extract other info
        status = response.xpath("//img[@class='SSSIMAGECENTER']/attribute::alt").extract_first() or ''
        instruction_mode = response.xpath("//label[text()='Instruction Mode']/../../following-sibling::tr[1]//span/text()").extract_first() or ''
        try:
            instructor = response.xpath("//th[text()='Instructor']/../following-sibling::tr[1]//span/text()").extract()[2]
            wait_capacity = response.xpath("//label[text()='Wait List Capacity']/../../following-sibling::tr[1]//span/text()").extract()[1]
            wait_total = response.xpath("//label[text()='Wait List Total']/../../following-sibling::tr[1]//span/text()").extract()[1]
        except IndexError:
            instructor = ''
            wait_total = 0
            wait_capacity = 0
        language = response.xpath("//label[text()='Class Attributes']/../following-sibling::td[1]/span/text()").extract_first() or ''
        class_capacity = response.xpath("//label[text()='Class Capacity']/../../following-sibling::tr[1]//span[1]/text()").extract_first() or 0
        # wait_capacity = response.xpath("//label[text()='Wait List Capacity']/../../following-sibling::tr[1]//span/text()").extract()[1]
        enrollment_total = response.xpath("//label[text()='Enrollment Total']/../../following-sibling::tr[1]//span[1]/text()").extract_first() or 0
        # wait_total = response.xpath("//label[text()='Wait List Total']/../../following-sibling::tr[1]//span/text()").extract()[1]
        available_seat = response.xpath("//label[text()='Available Seats']/../../following-sibling::tr[1]//span/text()").extract_first() or 0
        # course = course_item
        # saved_section = section_item.save()

        ret = Section.get_sections_for_spider(course_item.course_code, term, section_code)
        # if there is no such section under this course, create a new section
        if ret.error is not Error.OK:
            section_item = SectionItem()
            section_item['section_code'] = section_code
            section_item['category'] = category
            section_item['term'] = term
            section_item['type'] = type
            section_item['status'] = status
            section_item['instruction_mode'] = instruction_mode
            section_item['instructor'] = instructor
            section_item['language'] = language
            section_item['class_capacity'] = class_capacity
            section_item['wait_capacity'] = wait_capacity
            section_item['enrollment_total'] = enrollment_total
            section_item['wait_total'] = wait_total
            section_item['available_seat'] = available_seat
            section_item['course'] = course_item
            saved_section = section_item.save()
        # is the section is already exist, update the info
        else:
            section_item = ret.body
            section_item.section_code = section_code
            section_item.category = category
            section_item.term = term
            section_item.type = type
            section_item.status = status
            section_item.instruction_mode = instruction_mode
            section_item.instructor = instructor
            section_item.language = language
            section_item.class_capacity = class_capacity
            section_item.wait_capacity = wait_capacity
            section_item.enrollment_total = enrollment_total
            section_item.wait_total = wait_total
            section_item.available_seat = available_seat
            section_item.course = course_item
            section_item.save()
            saved_section = section_item

            # delete all the meetings of this section
            ret = Meeting.delete_meetings_by_section(section_item)
            if ret.error is not Error.OK:
                print(ret.error)

        # section_item = SectionItem()
        # title = response.xpath("//span[@class='PALEVEL0SECONDARY']/text()").extract_first()
        # try:
        #     section_item['section_code'] = title.split('\xa0\xa0')[0].split(' - ')[1]
        #     if section_item['section_code'].startswith('-'):
        #         section_item['category'] = '-'
        #     elif not re.search('\d+',  section_item['section_code']):
        #         section_item['category'] = section_item['section_code']
        #     else:
        #         number_free_code = re.sub('\d+', '', section_item['section_code'])
        #         section_item['category'] = number_free_code[:-1]
        # except:
        #     pass

        # title = response.xpath("//span[@class='SSSKEYTEXT']/text()").extract_first()
        # try:
        #     section_item['term'] = title.split(' | ')[1]
        #     section_item['type'] = title.split(' | ')[2]
        # except:
        #     pass

        # section_item['status'] = response.xpath("//img[@class='SSSIMAGECENTER']/attribute::alt").extract_first()
        # section_item['instruction_mode'] = response.xpath("//label[text()='Instruction Mode']/../../following-sibling::tr[1]//span/text()").extract_first()
        # try:
        #     section_item['instructor'] = response.xpath("//th[text()='Instructor']/../following-sibling::tr[1]//span/text()").extract()[2]
        # except IndexError:
        #     section_item['instructor'] = ''
        # section_item['language'] = response.xpath("//label[text()='Class Attributes']/../following-sibling::td[1]/span/text()").extract_first()
        # section_item['class_capacity'] = response.xpath("//label[text()='Class Capacity']/../../following-sibling::tr[1]//span[1]/text()").extract_first()
        # section_item['wait_capacity'] = response.xpath("//label[text()='Wait List Capacity']/../../following-sibling::tr[1]//span/text()").extract()[1]
        # section_item['enrollment_total'] = response.xpath("//label[text()='Enrollment Total']/../../following-sibling::tr[1]//span[1]/text()").extract_first()
        # section_item['wait_total'] = response.xpath("//label[text()='Wait List Total']/../../following-sibling::tr[1]//span/text()").extract()[1]
        # section_item['available_seat'] = response.xpath("//label[text()='Available Seats']/../../following-sibling::tr[1]//span/text()").extract_first()
        # section_item['course'] = course_item
        # saved_section = section_item.save()

        response = response.replace(body=response.body.replace(b'<br />', b'\n'))
        meeting_info = response.xpath("//td[text()='Meeting Information']/../..//span[@class='PSLONGEDITBOX']/text()").extract()
        print(meeting_info)
        for i in range(len(meeting_info)//4):
            meeting_item = MeetingItem()
            try:
                meeting_item['day'] = meeting_info[4*i].split(' ')[0]
                meeting_item['start'] = meeting_info[4*i].split(' - ')[0].split(' ')[1]
                meeting_item['end'] = meeting_info[4*i].split(' - ')[1]
            except:
                meeting_item['day'] = 'TBA'
                meeting_item['start'] = 'TBA'
                meeting_item['end'] = 'TBA'

            meeting_item['room'] = meeting_info[4*i+1]
            meeting_item['meeting_dates'] = meeting_info[4*i+3]
            meeting_item['section'] = saved_section
            meeting_item.save()

        request = scrapy.FormRequest.from_response(
            response=response,
            formname='win0',
            formdata={
                'ICAction': 'CLASS_SRCH_WRK2_SSR_PB_CLOSE'
            },
            callback=self.show_all_sections
        )
        request.meta['item'] = response.meta['item']
        request.meta['term'] = response.meta['term']
        request.meta['components'] = response.meta['components']
        yield request

    def parse_course_outcome(self, response):
        response = response.replace(body=response.body.replace(b'<br />', b'\n'))
        course_item = response.meta['item']

        learning_outcome = response.xpath("//span[text()='Learning Outcome']/../../following-sibling::tr[1]//div/text()").extract() or ''
        course_syllabus = response.xpath("//span[text()='Course Syllabus']/../../following-sibling::tr[1]//div/text()").extract() or ''
        feedback = response.xpath("//span[text()='Feedback for Evaluation']/../../following-sibling::tr[1]//div/text()").extract() or ''
        required_reading = response.xpath("//span[text()='Required Readings']/../../following-sibling::tr[1]//div/text()").extract() or ''
        recommended_reading = response.xpath("//span[text()='Recommended Readings']/../../following-sibling::tr[1]//div/text()").extract() or ''
        course_item.update_info(
            extract_content(learning_outcome),
            extract_content(course_syllabus),
            extract_content(feedback),
            extract_content(required_reading),
            extract_content(recommended_reading),
        )

        assessment = response.xpath("//span[text()='Assessment Type']/../../following-sibling::tr[1]//span[@class='PSEDITBOX_DISPONLY']/text()").extract()
        print("assessment {}".format(assessment))
        for i in range(len(assessment)//2):
            if assessment[i*2] == '\\xa0' or assessment[i*2+1] == '\\xa0':
                continue

            assessment_item = AssessmentItem()
            assessment_item['type'] = assessment[i*2]
            assessment_item['percent'] = assessment[i*2+1]
            assessment_item['course'] = course_item

            assessment_item.save()

        components = response.meta['components']
        for i in range(len(components)//2):
            component_item = ComponentItem()
            component_item['name'] = components[i*2]
            component_item['note'] = components[i*2+1]
            component_item['course'] = course_item

            component_item.save()

        request = scrapy.FormRequest.from_response(
            response=response,
            formname='win0',
            formdata={
                'ICAction': 'DERIVED_SAA_CRS_RETURN_PB'
            },
            callback=self.get_course_detail
        )
        yield request

    def parse(self, response):
        pass
