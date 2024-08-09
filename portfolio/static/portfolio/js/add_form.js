document.addEventListener('DOMContentLoaded', function () {
    let formContainer = document.querySelector("#form-container");
    let addButton = document.querySelector("#add-form");
    let totalForms = document.querySelector("#id_form-TOTAL_FORMS");
    let shareFormsContainer = document.querySelector("#share-forms-container");
    let templateForm = document.querySelector("#template-form");

    let formNum = shareFormsContainer.children.length;  // Current number of forms

    addButton.addEventListener('click', addForm);
    shareFormsContainer.addEventListener('click', function (e) {
        if (e.target && e.target.classList.contains('delete-form')) {
            e.preventDefault();
            deleteForm(e.target);
        }
    });
    function addForm(e) {
        e.preventDefault();

        if (!templateForm) {
            console.error('Template form not found.');
            return;
        }
        let formNum = parseInt(totalForms.value);
        let newForm = templateForm.cloneNode(true);
        let formRegex = /__prefix__/g;

        newForm.innerHTML = newForm.innerHTML.replace(formRegex, formNum);

        newForm.removeAttribute('style');
        newForm.removeAttribute('id');
        newForm.classList.add("share-form");

        newForm.querySelectorAll('input').forEach(input => input.value = '');
        newForm.querySelector('.delete-form').style.display = 'inline';

        shareFormsContainer.appendChild(newForm);
        formNum++;
        totalForms.setAttribute('value', `${formNum}`);

    }

    function deleteForm(deleteButton) {
        let formToDelete = deleteButton.closest('.share-form');
        formToDelete.remove();
        let formNum = parseInt(totalForms.value);
        formNum--;
        totalForms.setAttribute('value', `${formNum}`);
    }
});