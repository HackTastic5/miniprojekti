*** Settings ***
Resource  resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset Citations

*** Test Cases ***
Sorting by author works
    Go To  ${HOME_URL}
    Select From List By Value  citation_type  article
    Click Button  Select
    Input Text  author  first author
    Input Text  title  first title
    Input Text  journal  first journal
    Input Text  year  2023
    Click Button  Create
    Page Should Contain  first title by first author
    Select From List By Value  citation_type  article
    Click Button  Select
    Input Text  author  second author
    Input Text  title  second title
    Input Text  journal  second journal
    Input Text  year  2024
    Click Button  Create
    Page Should Contain  second title by second author
    Click Button  Author
    @{authors}  Get WebElements  xpath=//ul[@id="citation-list"]/li/p[strong[text()="Author:"]]
    ${author_texts}  Evaluate  [author.text.split("Author:")[-1].strip() for author in @{authors}]
    ${sorted_authors}  Evaluate  sorted(${author_texts})
    Should Be Equal As Strings  ${author_texts}  ${sorted_authors}

Sorting by title works
    Go To  ${HOME_URL}
    Select From List By Value  citation_type  article
    Click Button  Select
    Input Text  author  first author
    Input Text  title  first title
    Input Text  journal  first journal
    Input Text  year  2023
    Click Button  Create
    Page Should Contain  first title by first author
    Select From List By Value  citation_type  article
    Click Button  Select
    Input Text  author  second author
    Input Text  title  second title
    Input Text  journal  second journal
    Input Text  year  2024
    Click Button  Create
    Page Should Contain  second title by second author
    Click Button  Title
    @{titles}  Get WebElements  xpath=//ul[@id="citation-list"]/li/p[strong[text()="Title:"]]
    ${title_texts}  Evaluate  [title.text.split("Title:")[-1].strip() for title in @{titles}]
    ${sorted_titles}  Evaluate  sorted(${title_texts})
    Should Be Equal As Strings  ${title_texts}  ${sorted_titles}

Sorting by year works
    Go To  ${HOME_URL}
    Select From List By Value  citation_type  article
    Click Button  Select
    Input Text  author  first author
    Input Text  title  first title
    Input Text  journal  first journal
    Input Text  year  2023
    Click Button  Create
    Page Should Contain  first title by first author
    Select From List By Value  citation_type  article
    Click Button  Select
    Input Text  author  second author
    Input Text  title  second title
    Input Text  journal  second journal
    Input Text  year  2024
    Click Button  Create
    Page Should Contain  second title by second author
    Click Button  Year
    @{years}  Get WebElements  xpath=//ul[@id="citation-list"]/li/p[strong[text()="Year:"]]
    ${year_texts}  Evaluate  [int(year.text.split("Year:")[-1].strip()) for year in @{years}]
    ${sorted_years}  Evaluate  sorted(${year_texts})
    Should Be Equal As Strings  ${year_texts}  ${sorted_years}

Sorting in descending order works
    Go To  ${HOME_URL}
    Select From List By Value  citation_type  article
    Click Button  Select
    Input Text  author  first author
    Input Text  title  first title
    Input Text  journal  first journal
    Input Text  year  2023
    Click Button  Create
    Page Should Contain  first title by first author
    Select From List By Value  citation_type  article
    Click Button  Select
    Input Text  author  second author
    Input Text  title  second title
    Input Text  journal  second journal
    Input Text  year  2024
    Click Button  Create
    Page Should Contain  second title by second author
    Click Element  xpath=//input[@name="desc"]
    Click Button  Author
    @{authors}  Get WebElements  xpath=//ul[@id="citation-list"]/li/p[strong[text()="Author:"]]
    ${author_texts}  Evaluate  [author.text.split("Author:")[-1].strip() for author in @{authors}]
    ${sorted_authors}  Evaluate  sorted(${author_texts}, reverse=True)
    Should Be Equal As Strings  ${author_texts}  ${sorted_authors}
