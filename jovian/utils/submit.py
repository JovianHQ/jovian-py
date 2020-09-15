from jovian.utils.api import _h
from jovian.utils.commit import commit
from jovian.utils.credentials import read_webapp_url
from jovian.utils.error import ApiError
from jovian.utils.logger import log
from jovian.utils.misc import urljoin
from jovian.utils.request import post, pretty
from jovian.utils.shared import _u

POST_API_URL = '/learn/course/{}/section/{}/make_submission'
POST_API_URL_SHORT_SLUG = '/learn/course/section/{}/make_submission'
ASSIGNMENT_PAGE_URL = '/learn/{}/assignment/{}'


def submit(assignment=None, assignment_short_slug=None, notebook_url=None, **kwargs):
    """ Performs jovian.commit and makes a assignment submission with the uploaded notebook.
    """
    if not assignment and not assignment_short_slug:
        log("Please provide assignment or assignment_short_slug argument", error=True)
        return

    if assignment:
        course_slug, assignment_slug = assignment.split("/")
        post_url = POST_API_URL.format(course_slug, assignment_slug)

    if assignment_short_slug:
        post_url = POST_API_URL_SHORT_SLUG.format(assignment_short_slug)

    nb_url = notebook_url if notebook_url else commit(**kwargs)

    if nb_url:
        data = {
            'assignment_url': nb_url
        }
        auth_headers = _h()

        log('Submitting assignment..')
        res = post(url=_u(post_url),
                   json=data,
                   headers=auth_headers)

        if res.status_code == 200:
            data = res.json()['data']
            course_slug = data.get('course_slug')
            assignment_slug = data.get('section_slug')

            assignment_page_url = ASSIGNMENT_PAGE_URL.format(course_slug, assignment_slug)
            log('Verify your submission at {}'.format(urljoin(read_webapp_url(), assignment_page_url)))
        else:
            log('Jovian submit failed. {}'.format(pretty(res)), error=True)
