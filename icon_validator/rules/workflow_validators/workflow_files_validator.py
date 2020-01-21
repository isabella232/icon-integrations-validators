import os

from icon_validator.rules.validator import KomandPluginValidator
from icon_validator.exceptions import ValidationException


class WorkflowFilesValidator(KomandPluginValidator):

    def validate(self, spec):
        d = spec.directory

        if not os.path.isfile('{}/{}'.format(d, 'workflow.spec.yaml')):
            raise ValidationException('File workflow.spec.yaml does not exist in: ', d)
        if not os.path.isfile('{}/{}'.format(d, 'help.md')):
            raise ValidationException('File help.md does not exist in: ', d)
        if not os.path.isfile('{}/{}'.format(d, 'extension.png')):
            raise ValidationException('File extension.png does not exist in: ', d)
        # TODO check for .icon file
