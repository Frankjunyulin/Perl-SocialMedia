# Simple-Social-Media
It is a social media(website), which is written by Perl cgi, html and css.

Here is just the part that I finished.

1.Display User Information & Posts
The starting-point script you've been given (see below) displays user information in raw form and does not display their image or posts.
Your web site should display user information in nicely formatted HTML with appropriate accompanying text. It should display the user's image if there is one.
Private information such e-mail, password, lat, long and courses should not be displayed.
The user's posts should be displayed in reverse chronological order.

2.Interface
Your web site must generate nicely formatted convenient-to-use web pages including appropriate navigation facilities and instructions for naive users. Although this is not a graphic design exercise you should produce pages with a common and somewhat distinctive look-and-feel. You may find CSS useful for this.
As part of your personal design you may change the name of the website to something other than matelook but the primary CGI script has to be matelook.cgi.

3.Mate list
When a matelook page is shown a list of the names of that user's mates should be displayed.
The list should include a thumbnail image of the mate (if they have a profile image).
Clicking on the image and/or name should take you to that matelook page.


4.Search for Names
Your web site should provide searching for a user whose name containing a specified substring. Search results should include the matching name and a thumbnail image. Clicking on the image and/or name should take you to that matelook page.

5.Logging In & Out
Users should have to login to use matelook.
Their password should be checked when they attempt to log in.
Users should also be able to logout.

6.Displaying Posts
When a user logs in they should see their recent posts, any posts from their mates and any posts which contain their zid in the post, comments or replies.
Comments and replies should be shown appropriately with posts.
When displaying posts zids should be replaced with a link to the user's matelook page. The link text should be the user's full name.

7.Making Posts
Users should be able to make posts.

8.Searching Posts
It should be possible to search for posts containing particular words.
Commenting on Post and replying to Comments (Level 2)
When viewing a post, it should be possible to click on a link and create a comment on that post. When viewing a comment , it should be possible to click on a link and create a reply to that comment.

9.Mate/Unmate Users
A user should be able to add & delete users from their mate list.
Pagination of Posts & Search Results (Level 3)
When searching for users or posts and when viewing posts the users be shown the first n (e.g n == 16) results. They should be able then view the next n and the next n and so on.

10.User Account Creation
Your web site should allow users to create accounts with a zid, password and e-mail address. You should of course check that an account for this zid does not exist already. It should be compulsory that a valid e-mail-address is associated with an account but the e-mail address need not be a UNSW address.
You should confirm e-mail address are valid and owned by the matelook user creating the account by e-mailing them a link necessary to complete account creation.
I expect (and recommend) most students to use the data format of the data set you've been supplied. If so for a new user you would need create a directory named with their zid and then add a appropriate user.txt containing their details.


11.Profile Text
A matelook user should be able to add to some text to their details , probably describing their interests, which is displayed with their user details.
