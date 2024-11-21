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
    Click Button  Valitse
    Input Text    author    bot
    Input Text    title     testing
    Input Text    booktitle testing
    Input Text    year      2024
    Click Button  Create
    Page Should Contain  testing : written by bot


