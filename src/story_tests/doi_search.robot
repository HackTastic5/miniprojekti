*** Settings ***
Resource  resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset Citations

*** Test Cases ***
DOI search finds bibtex fields and fills form
    Go To  ${HOME_URL}
    Input Text  doi  10.1126/science.169.3946.635
    Click Button  Search
    Page Should Contain  Enter a new citation
    Page Should Not Contain  No results found for specified DOI
    Textfield Value Should Be  author  Frank, Henry S.

DOI search shows error message when resource not found
    Go To  ${HOME_URL}
    Input Text  doi  10.1001/1234
    Click Button  Search
    Page Should Contain  No results found for specified DOI
    Page Should Not Contain  Enter a new citation
