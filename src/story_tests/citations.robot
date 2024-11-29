*** Settings ***
Resource  resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset Citations

*** Test Cases ***
Loads at start
    Go To  ${HOME_URL}
    Title Should Be  Citation app


After adding a citation, there is one
    Go To  ${HOME_URL}
    Select From List By Value  citation_type  inproceedings
    Click Button  Select
    Input Text  author  author
    Input Text  title   testing
    Input Text  booktitle   testing
    Input Text  year    2024
    Click Button  Create
    Page Should Contain  testing by author

Type selection works
    Go To  ${HOME_URL}
    Select From List By Value  citation_type  article
    Click Button  Select
    Input Text  author  author2
    Input Text  title   testing
    Input Text  journal   testing
    Input Text  year    2024
    Click Button  Create
    Page Should Contain  testing by author2

Deletion works
    Go To  ${HOME_URL}
    Select From List By Value  citation_type  article
    Click Button  Select
    Input Text  author  author2
    Input Text  title   testing
    Input Text  journal   testing
    Input Text  year    2024
    Click Button  Create
    Page Should Contain  testing by author2
    Click Button  Delete
    Page Should Not Contain    testing by author2

Deletion works when there are multiple delete buttons
    Go To  ${HOME_URL}
    Select From List By Value  citation_type  article
    Click Button  Select
    Input Text  author  author
    Input Text  title   testing
    Input Text  journal   testing
    Input Text  year    2024
    Click Button  Create
    Page Should Contain  testing by author
    Select From List By Value  citation_type  article
    Click Button  Select
    Input Text  author  another author
    Input Text  title   testing again
    Input Text  journal   testing again
    Input Text  year    2024
    Click Button  Create
    Page Should Contain  testing again by another author
    Click Button  //span[contains(text(), 'testing again by another author')]/../form/input[@value='Delete']
    Page Should Contain  testing by author
    Page Should Not Contain  testing again by another author

Editing works
    Go To  ${HOME_URL}
    Select From List By Value  citation_type  article
    Click Button  Select
    Input Text  author  author
    Input Text  title   testing
    Input Text  journal   testing
    Input Text  year    2024
    Click Button  Create
    Page Should Contain  testing by author
    Click Button  Edit
    Input Text  author  another author
    Input Text  title   testing again
    Click Button  Submit
    Page Should Contain  testing again by another author

Editing works when there are multiple edit buttons
    Go To  ${HOME_URL}
    Select From List By Value  citation_type  article
    Click Button  Select
    Input Text  author  author
    Input Text  title   testing
    Input Text  journal   testing
    Input Text  year    2024
    Click Button  Create
    Page Should Contain  testing by author
    Select From List By Value  citation_type  article
    Click Button  Select
    Input Text  author  another author
    Input Text  title   testing again
    Input Text  journal   testing again
    Input Text  year    2024
    Click Button  Create
    Page Should Contain  testing again by another author
    Click Button  //span[contains(text(), 'testing again by another author')]/../form/input[@value='Edit']
    Input Text  author  some author
    Click Button  Submit
    Page Should Contain  testing by author
    Page Should Contain  testing again by some author

Filtering works
    Go To  ${HOME_URL}
    Select From List By Value  citation_type  article
    Click Button  Select
    Input Text  author  author1
    Input Text  title   found
    Input Text  journal   testing
    Input Text  year    2024
    Click Button  Create
    Page Should Contain  found by author1
    Select From List By Value  citation_type  article
    Click Button  Select
    Input Text  author  author2
    Input Text  title   filtered
    Input Text  journal   testing
    Input Text  year    2024
    Click Button  Create
    Page Should Contain  filtered by author2
    Element Should Be Visible  found
    Element Should Be Visible  filtered
    Input Text  filter  found
    Element Should Be Visible  found
    Element Should Not Be Visible  filtered

DOI search works
    Go To  ${HOME_URL}
    Input Text  doi  10.1126/science.169.3946.635
    Click Button  DOI-search
    Page Should Contain  Enter a new citation
    Textfield Value Should Be  author  Frank, Henry S.
