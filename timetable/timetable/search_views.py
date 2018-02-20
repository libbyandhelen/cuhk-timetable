from haystack.query import SearchQuerySet

from Course.models import Course
from Section.models import Section
from base.decorator import require_get
from base.error import Error
from base.response import error_response, response


@require_get
def auto_search(request):
    query = request.GET.get('q', None)
    if not query:
        return error_response(Error.NO_SEARCH_PARAMETER)

    qs = SearchQuerySet().models(Course)
    results = qs.auto_query(query)

    result_list = []
    for result in results:
        ret = Section.get_sections_by_course(result.object)
        if ret.error is not Error.OK:
            return error_response(ret.error)
        if not ret.body:
            continue

        result_list.append(result)
    sorted_results = sorted(result_list, key=lambda x: x.score, reverse=True)

    final_result = []
    for result in sorted_results:
        final_result.append(result.object.to_dict())

    return response(body=final_result)
