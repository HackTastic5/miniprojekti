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
    Input Text  author  bot
    Input Text    title    testing
    Click Button  Create
    Page Should Contain  testing : written by bot


