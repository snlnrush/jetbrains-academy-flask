Stage 4/4: Results & history

Description

In the final stage, we will create the history page and a page that shows the actual result of a comparison. From now on, users will be redirected to the specific page with the result instead of True or False. Users should also be able to check the previous matches and open them again.

Objectives

The first task is to create views for the history and result pages. The result page should display the regexp, text, and the result fields. The history page is an unordered list of all entries, with newer ones on top. To implement it, reverse every entry of the object list in the database. To access data in the template, use a Jinja Flask template with parameters. The same applies to the history page. Use the for tag in your history template to list every entry.

The second task is to change response from the previous stage to another function that will take us to the result page. For this, use a redirect function of Flask.

Your final task is to add a link to the result page inside every <li></li> tag pair in the template. Put result/id/ inside the href attribute, where id is the ID of the passed variable.

Example

Example 1: the localhost:8000/result/1/ page

<p>Regex: ^[a-z0-9_-]{3,16}$</p>
<p>Text: thrawn_66</p>
<p>True</p>
The localhost:8000/history/ page

<li><a href="/result/2/">[\d]{1,2}$</a></li>
<li><a href="/result/1/">^[a-z0-9_-]{3,16}$</a></li>