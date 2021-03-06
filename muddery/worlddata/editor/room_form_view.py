
"""
This file checks user's edit actions and put changes into db.
"""

from django import http
from django.http import HttpResponseRedirect
from evennia.utils import logger
from muddery.worlddata.editor.form_view import FormView
from worlddata import forms


class RoomFormView(FormView):
    """
    This object deal with common forms and views.
    """
    def parse_request(self):
        """
        Parse request data.

        Returns:
            boolean: Parse success.
        """
        result = super(RoomFormView, self).parse_request()

        # Get template file's name.
        self.template_file = "room_form.html"

        return result

    def get_context(self):
        """
        Get render context.

        Returns:
            context
        """
        context = super(RoomFormView, self).get_context()
        
        area = self.request_data.get("location", None)
        if not area:
            area = self.request_data.get("_area", None)
        if area:
            context["area"] = area

        return context

    def quit_form(self):
        """
        Quit a form without saving.

        Returns:
            HttpResponse
        """
        self.parse_request()

        try:
            # Back to record list.
            # Parse list's url from the request path.
            pos = self.request.path.rfind("/")
            if pos > 0:
                url = self.request.path[:pos] + "/list.html"

                args = ""
                if self.page:
                    args += "_page=" + str(self.page)

                area = self.request_data.get("location", None)
                if not area:
                    area = self.request_data.get("_area", None)
                if area:
                    if args:
                        args += "&"
                    args += "_area=" + area

                if args:
                    url += "?" + args

                return HttpResponseRedirect(url)
        except Exception, e:
            logger.log_tracemsg("Quit form error: %s" % e)

        raise http.Http404
