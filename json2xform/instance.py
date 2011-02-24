from xform_manager.utils import parse_xform_instance


class SurveyInstance(object):
    def __init__(self, survey_object, **kwargs):
        self._survey = survey_object
        self.kwargs = kwargs #not sure what might be passed to this

        #does the survey object provide a way to get the key dicts?
        self._keys = [c.get_name() for c in self._survey._children]
        
        # get xpaths
        #  - prep for xpaths.
        self._survey.xml()
        self._xpaths = self._survey._xpath.values()
        
        #see "answers(self):" below for explanation of this dict
        self._answers = {}
        self._orphan_answers = {}
        
        #do we want to use keys or xpaths?
        #do we want to leave empty spaces where answers haven't been given?
        #                --i think this could be useful
        for x in self._xpaths:
            self._answers[x] = None
    
    def keys(self):
        return self._keys
    
    def xpaths(self):
        #originally thought of having this method get the xpath stuff
        #but survey doesn't like when xml() is called multiple times.
        return self._xpaths

    def answer(self, xpath=None, name=None, value=None):
        if name is not None:
            _xpath = self._survey._xpath.get(name, None)
        elif xpath is not None:
            _xpath = xpath
        else:
            raise Exception("Xpath or name must be given")
        
        if _xpath is not None:
            self._answers[_xpath] = value
        else:
            self._orphan_answers[name] = value

    def answers(self):
        """
        This returns "_answers", which is a dict with the key-value
        responses for this given instance. This could be pumped to xml
        or returned as a dict for maximum convenience (i.e. testing.)
        """
        return self._answers
        
    def import_from_xml(self, xml_string_or_filename):
        import os.path
        if os.path.isfile(xml_string_or_filename):
            xml_str = open(xml_string_or_filename).read()
        else:
            xml_str = xml_string_or_filename
        key_val_dict = parse_xform_instance(xml_str)
        for k, v in key_val_dict.items():
            self.answer(name=k, value=v)
        
    def __unicode__(self):
        orphan_count = len(self._orphan_answers.keys())
        placed_count = len(self._answers.keys())
        answer_count = orphan_count + placed_count
        return "<Instance (%d answers: %d placed. %d orphans)>" % (answer_count, placed_count, orphan_count)