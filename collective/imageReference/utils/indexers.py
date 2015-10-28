
from plone.indexer.decorator import indexer
from ..imageReference import IImageReference

@indexer(IImageReference)
def reproductionData_identification_reproductionType(object, **kw):
    try:
        if hasattr(object, 'reproductionData_identification_reproductionType'):
            return object.reproductionData_identification_reproductionType
        else:
            return []
    except:
        return []

@indexer(IImageReference)
def reproductionData_identification_technique(object, **kw):
    try:
        if hasattr(object, 'reproductionData_identification_technique'):
            return object.reproductionData_identification_technique
        else:
            return []
    except:
        return []

@indexer(IImageReference)
def reproductionData_identification_location(object, **kw):
    try:
        if hasattr(object, 'reproductionData_identification_location'):
            return object.reproductionData_identification_location
        else:
            return []
    except:
        return []

@indexer(IImageReference)
def reproductionData_descriptiveElements_subject(object, **kw):
    try:
        if hasattr(object, 'reproductionData_descriptiveElements_subject'):
            return object.reproductionData_descriptiveElements_subject
        else:
            return []
    except:
        return []


@indexer(IImageReference)
def reproductionData_descriptiveElements_coverage(object, **kw):
    try:
        if hasattr(object, 'reproductionData_descriptiveElements_coverage'):
            return object.reproductionData_descriptiveElements_coverage
        else:
            return []
    except:
        return []





        
