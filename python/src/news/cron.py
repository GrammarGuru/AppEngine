import webapp2

from google.appengine.api import taskqueue


class NewsCron(webapp2.RequestHandler):
    def get(self):
        queue = taskqueue.Queue(name='default')
        task = taskqueue.Task(
            url='/newscrawler',
            target='worker')

        rpc = queue.add_async(task)
        task = rpc.get_result()

        return self.response.write(
            'Task {} enqueued, ETA {}.'.format(task.name, task.eta))