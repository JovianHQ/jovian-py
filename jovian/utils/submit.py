from jovian.utils.api import _h
from jovian.utils.commit import commit
from jovian.utils.credentials import read_webapp_url
from jovian.utils.error import ApiError
from jovian.utils.logger import log
from jovian.utils.misc import urljoin
from jovian.utils.request import post, pretty
from jovian.utils.shared import _u

POST_API_URL = '/learn/course/{}/section/{}/make_submission'
ASSIGNMENT_PAGE_URL = '/learn/{}/assignment/{}'


def submit(course_slug=None, assignment_slug=None, notebook_url=None, **kawrgs):
    """ Performs jovian.commit and makes a assignment submission with the uploaded notebook.
    """
    if not course_slug or not assignment_slug:
        log("Missing Course Slug or Assignment Slug", error=True)

    nb_url = notebook_url if notebook_url else commit(**kawrgs)

    if nb_url:
        data = {
            'assignment_url': nb_url
        }
        auth_headers = _h()

        log('Submitting assignment....')
        post_url = POST_API_URL.format(course_slug, assignment_slug)
        res = post(url=_u(post_url),
                   json=data,
                   headers=auth_headers)

        if res.status_code == 200:
            assignment = res.json()['data'].get('assignment')
            if assignment:
                assignment = assignment.get('assignment_url')
            assignment_page_url = ASSIGNMENT_PAGE_URL.format(course_slug, assignment_slug)

            log('Submitted assignment - {}'.format(assignment))
            log('Verify your submission at {}'.format(urljoin(read_webapp_url(), assignment_page_url)))
        else:
            log('Jovian submit failed. {}'.format(pretty(res)), error=True)
