
class Error:
    """Error class"""
    NO_SEARCH_PARAMETER = 2012
    SECTION_ALREADY_SELECTED = 2011
    SELECT_SECTION_NOT_EXIST = 2010
    USER_SECTION_NOT_MATCH = 2009
    NOT_YOUR_SECTIONS = 2008
    SECTION_NOT_BELONG_TO_COURSE = 2007
    SECTION_NOT_EXIST = 2006
    USER_NOT_EXIST = 2005
    WRONG_PASSWORD = 2004
    ERROR_CREATE_USER = 2003
    EXIST_USERNAME = 2002
    ERROR_CREATE_SELECTSECTION = 2001
    COURSE_NOT_EXIST = 2000

    REQUIRE_ADMIN = 1006
    STRANGE = 1005
    ERROR_METHOD = 1004
    REQUIRE_LOGIN = 1003
    REQUIRE_JSON = 1002
    REQUIRE_PARAM = 1001
    NOT_FOUND_ERROR = 1000
    OK = 0

    ERROR_TUPLE = (
        (NO_SEARCH_PARAMETER, "Please supply the search parameter"),
        (SECTION_ALREADY_SELECTED, "the section is already selected"),
        (SELECT_SECTION_NOT_EXIST, "the SelectSection does not exist"),
        (USER_SECTION_NOT_MATCH, "User and the Section does not Match"),
        (NOT_YOUR_SECTIONS, "You Cannot Get Sections Not Belong to You"),
        (SECTION_NOT_BELONG_TO_COURSE, "Section not Belong to the Course"),
        (SECTION_NOT_EXIST, "Section Not Exist"),
        (USER_NOT_EXIST, "User not exist"),
        (WRONG_PASSWORD, "Wrong Password"),
        (ERROR_CREATE_USER, "Error Creating User"),
        (EXIST_USERNAME, "Username already exists"),
        (ERROR_CREATE_SELECTSECTION, "Error Creating Select Section"),
        (COURSE_NOT_EXIST, "Course Not Exist"),

        (REQUIRE_ADMIN, "Require Admin"),
        (ERROR_METHOD, 'Error HTTP Request Method'),
        (REQUIRE_LOGIN, "Require Login"),
        (REQUIRE_JSON, "Require JSON"),
        (REQUIRE_PARAM, "Require Parameter: "),
        (NOT_FOUND_ERROR, "Error Not Exist"),
        (OK, "ok"),
    )