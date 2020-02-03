import os

from icon_validator.rules.validator import KomandPluginValidator
from icon_validator.exceptions import ValidationException


class WorkflowScreenshotKeyValidator(KomandPluginValidator):

    def __init__(self):
        super().__init__()
        self.files_list = list()
        self.names_list = list()

    @staticmethod
    def validate_title(title):
        if title.endswith("."):
            raise ValidationException("Title ends with period when it should not.")
        if title[0].islower():
            # This plugin title is OK: minFraud
            # This plugin title is OK: ifconfig.co
            raise ValidationException("Title should not start with a lower case letter.")
        if title[0].isspace():
            raise ValidationException("Title should not start with a whitespace character.")
        if len(title.split()) > 7:
            raise ValidationException(f"Title is too long, 6 words or less: contains {str(len(title.split()))}")
        for word in title.split():
            if not title.startswith(word):
                if "The" == word:
                    raise ValidationException("Title contains a capitalized 'The' when it should not.")
                if "By" == word and not title.endswith("By"):
                    # This is OK: Order By
                    # This is NOT OK: Search By String
                    raise ValidationException("Title contains a capitalized 'By' when it should not.")
                if "From" == word:
                    raise ValidationException("Title contains a capitalized 'From' when it should not.")
                if "A" == word:
                    raise ValidationException("Title contains a capitalized 'A' when it should not.")
                if "An" == word:
                    raise ValidationException("Title contains a capitalized 'An' when it should not.")
                if "Of" == word and not title.endswith("Of"):
                    # This is OK: Member Of
                    # This is NOT OK: Type Of String
                    raise ValidationException("Title contains a capitalized 'Of' when it should not.")

    @staticmethod
    def validate_screenshot_titles(spec):
        screenshots = spec.spec_dictionary()["resources"]["screenshots"]
        titles_list = list()
        for screenshot in screenshots:
            try:
                titles_list.append(screenshot["title"])
            except KeyError:
                raise ValidationException("Each screenshot must have a 'title' key."
                                          f" {screenshot} is missing this key.")
        for item in titles_list:
            WorkflowScreenshotKeyValidator.validate_title(item)

    def validate_screenshots_keys_exist(self, spec):
        try:
            screenshots = spec.spec_dictionary()["resources"]["screenshots"]
        except KeyError:
            raise ValidationException("The screenshots key under the resources key dose not exist in the yaml."
                                      " please add this key.")
        if len(screenshots) == 0:
            raise ValidationException("There are no screenshots listed in the yaml."
                                      " At lest one screenshot must be listed.")

        for screenshot in screenshots:
            try:
                self.names_list.append(screenshot["name"])
            except KeyError:
                raise ValidationException("Each screenshot must have a 'name' key that coresposnds to the file name of the screenshot."
                                          f" {screenshot} is missing this key.")

    def validate_screenshot_files_exist(self, spec):
        directory = spec.directory
        try:
            for file_name in os.listdir(f"{directory}/screenshots"):
                self.files_list.append(file_name)
        except FileNotFoundError:
            raise ValidationException(f"The screenshots directory could not be found at: {directory}\n"
                                      "Please ensure that the screenshots directory exists.")
        if len(self.files_list) == 0:
            raise ValidationException("There are no files in the screenshots directory."
                                      " Please add at lest one screenshot.")
        for screenshot in self.files_list:
            if not screenshot.endswith(".png"):
                raise ValidationException(f"All screenshots must be .png files. {screenshot} is not a .png file")

    def validate_screenshot_files_and_keys_match(self):
        sorted_names = sorted(self.names_list)
        sorted_files = sorted(self.files_list)
        if not sorted_files == sorted_names:
            raise ValidationException("The screenshot files names and the screenshot names in the yaml do not match.")

    def validate(self, spec):
        self.validate_screenshots_keys_exist(spec)
        self.validate_screenshot_files_exist(spec)
        self.validate_screenshot_files_and_keys_match()
        WorkflowScreenshotKeyValidator.validate_screenshot_titles(spec)
