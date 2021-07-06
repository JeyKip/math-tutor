(function ($) {
    const INTEGER_SELECTOR = ".field-integer_correct_answer";
    const DECIMAL_SELECTOR = ".field-decimal_correct_answer";
    const BOOLEAN_SELECTOR = ".field-boolean_correct_answer";
    const TEXT_SELECTOR = ".field-text_correct_answer";
    const OPTIONS_LIST_SELECTOR = "#options-group";
    const TYPE_SELECTOR = "#id_type";

    const SINGLE_CHOICE_MODE = "single";
    const MULTIPLE_CHOICE_MODE = "multiple";

    subscribeToQuestionTypeChangedEvent();
    turnOnCorrectAnswerSection();
    assignRequiredClassToCorrectAnswerLabels();

    function subscribeToQuestionTypeChangedEvent() {
        $(TYPE_SELECTOR).on("change", function (event) {
            turnOnCorrectAnswerSection();
            unselectOptions();
        });
    }

    function turnOnCorrectAnswerSection() {
        hideCorrectAnswerSections();

        if (currentTypeIsInteger()) {
            showElement(INTEGER_SELECTOR);
        } else if (currentTypeIsDecimal()) {
            showElement(DECIMAL_SELECTOR);
        } else if (currentTypeIsBoolean()) {
            showElement(BOOLEAN_SELECTOR);
        } else if (currentTypeIsText()) {
            showElement(TEXT_SELECTOR);
        } else if (currentTypeIsSingleChoice()) {
            showElement(OPTIONS_LIST_SELECTOR);
            changeOptionsListToSingleSelect();
        } else if (currentTypeIsMultipleChoice()) {
            showElement(OPTIONS_LIST_SELECTOR);
            changeOptionsListToMultipleSelect();
        }
    }

    function currentTypeIsInteger() {
        return getSelectedType() === "Integer";
    }

    function currentTypeIsDecimal() {
        return getSelectedType() === "Decimal";
    }

    function currentTypeIsBoolean() {
        return getSelectedType() === "Boolean";
    }

    function currentTypeIsText() {
        return getSelectedType() === "Text";
    }

    function currentTypeIsSingleChoice() {
        return getSelectedType() === "Single Choice";
    }

    function currentTypeIsMultipleChoice() {
        return getSelectedType() === "Multiple Choice";
    }

    function unselectOptions() {
        if (currentTypeIsMultipleChoice()) {
            getInputsFromOptionsList("checkbox").prop("checked", false);
        }
        if (currentTypeIsSingleChoice()) {
            getInputsFromOptionsList("radio").prop("checked", false);
        }
    }

    function hideCorrectAnswerSections() {
        hideElements([
            INTEGER_SELECTOR,
            DECIMAL_SELECTOR,
            BOOLEAN_SELECTOR,
            TEXT_SELECTOR,
            OPTIONS_LIST_SELECTOR
        ]);
    }

    function hideElements(elements) {
        for (let i = 0; i < elements.length; i++) {
            hideElement(elements[i]);
        }
    }

    function hideElement(el) {
        $(el).addClass("hidden");
    }

    function showElement(el) {
        $(el).removeClass("hidden");
    }

    function changeOptionsListToSingleSelect() {
        if (setCurrentModeOfOptionsList(SINGLE_CHOICE_MODE)) {
            changeCheckboxesToRadioButtons();
        }
    }

    function setCurrentModeOfOptionsList(mode) {
        const currentMode = getCurrentModeOfOptionsList();

        if (currentMode === mode) {
            return false;
        }

        $(OPTIONS_LIST_SELECTOR).data("mode", mode);
        return true;
    }

    function getCurrentModeOfOptionsList() {
        return $(OPTIONS_LIST_SELECTOR).data("mode") || MULTIPLE_CHOICE_MODE;
    }

    function changeCheckboxesToRadioButtons() {
        const checkboxes = getInputsFromOptionsList("checkbox");

        for (let i = 0; i < checkboxes.length; i++) {
            changeCheckboxToRadioButton(checkboxes[i]);
        }
    }

    function changeCheckboxToRadioButton(checkbox) {
        const $checkbox = $(checkbox);

        $checkbox.attr("type", "radio");
        $checkbox.off("change")
            .on("change", radioChangedEventHandler);
    }

    function radioChangedEventHandler(event) {
        const $inputs = getInputsFromOptionsList("radio");

        for (let i = 0; i < $inputs.length; i++) {
            const input = $inputs[i];

            if (input !== event.target) {
                $(input).prop("checked", false);
            }
        }
    }

    function getInputsFromOptionsList(type) {
        return $(OPTIONS_LIST_SELECTOR).find(`tr.form-row .field-is_correct input[type=${type}]`);
    }

    function changeOptionsListToMultipleSelect() {
        if (setCurrentModeOfOptionsList(MULTIPLE_CHOICE_MODE)) {
            changeRadioButtonsToCheckboxes();
        }
    }

    function changeRadioButtonsToCheckboxes() {
        const radioButtons = getInputsFromOptionsList("radio");

        for (let i = 0; i < radioButtons.length; i++) {
            changeRadioButtonToCheckbox(radioButtons[i]);
        }
    }

    function changeRadioButtonToCheckbox(radio) {
        $(radio).attr("type", "checkbox");
    }

    function getSelectedType() {
        return $(TYPE_SELECTOR).val();
    }

    function assignRequiredClassToCorrectAnswerLabels() {
        $(`${INTEGER_SELECTOR} label`).addClass("required");
        $(`${DECIMAL_SELECTOR} label`).addClass("required");
        $(`${BOOLEAN_SELECTOR} label`).addClass("required");
        $(`${TEXT_SELECTOR} label`).addClass("required");
    }
})(django.jQuery);