# Algorithmix.blog: A blogging site for technologists and software developers.

[![Project Demo](https://i.ytimg.com/vi/nXzZcE1BEfI/maxresdefault.jpg)](https://youtu.be/nXzZcE1BEfI)

Welcome to Algorithmix.blog! A blogging website for technologists and software developers, which is driven by dynamic, user-generated content in the form of posts. This project is the final project of the 'CS50s Web Programming with Python and JavaScript' course. It is structured like a compact social network, but tailored to the creation of long, dynamic posts, so called 'blog posts'. On this site, you are able to create posts privately, while customizing them until you are ready to release them into the wild by making them public, for others to discover, read and enjoy. Registered users who enjoyed reading one of your posts can give it a like to boost its popularity, or can add it to their list of favorite posts to remember them in the future. They can also comment on your posts to share opinions, and can also reply to other comments, thereby creating small threads of comments under your post. These comments can be liked too.

Algorithmixblog contains several ways of discovering new and interesting content created on the platform. The homepage shows three infinite scroll widgets, which sort the posts created by users based on 3 different categories: Top, Newest, and Most Active. These widgets show blog posts that are sorted based on their like count, comment count, date of creation, and more.
The discover page is an infinite scroll container of posts randomly sorted based on different attributes. The following feed page shows you the newest creations of those who you follow on the platform.

Blog posts represent the core of Algorithmix.blog, and have to offer the user a dynamic and expressive way to create content that users can enjoy. The text of a blog post is parsed as markdown content into HTML. Using the `python-markdown2` Python library and some enhancements on the front end using JavaScript, the site enables users to generate tables, images with links and captions, hidden links, nested quotes, spoiler quotes, (un)ordered lists, inline code, code blocks with syntax highlighting, and much more! This gives users lots of possibilities to design their posts. Blog posts can optionally have tags attached to them, which makes them easier to search on the search page, and can be used to indicate the topics that a post focuses on.

The user interface of Algorithmix.blog is designed to be modern and user-friendly. The CSS code base is specifically tailored for this site, with no CSS frameworks included, enabling a unique design for the entire site.
Mobile responsiveness is also an important part of the website's design, allowing all pages to look nice and readable on all common devices and screen sizes.

Nothing on the platform must be permanent, therefore users can edit their posts and comments, edit their details, follow and unfollow any user they discover, delete their posts and comments, or delete their entire account if needed.

## Distinctiveness and Complexity

This project is larger and more complex than previous projects, as it features more HTML templates, more CSS stylesheets and more complex JavaScript logic on the front end, as well as more Python code on the backend, with more sophisticated view functions in the Django-based backend code. It is a blogging platform, a concept which is not found in any other previous projects. Things like full mobile responsiveness, a custom logo and infinite scrolling for loading posts on certain pages were only added to this project, in order to make it stand out as a modern and dynamic web application, that can be hosted on the web to be used by an online community.


## How To Run The Application

This library requires the Python libraries `Django`, `python-markdown2` and `Pygments` to run. To install these, run `py -m pip install -r requirements.txt` (note that `py` refers to your computer's environment variable for Python 3, it might be called differently on your host machine) in the command line at `/capstone/`.
Running the website is easily achieved by running `py manage.py runserver` in the command line in the `/capstone/` directory. 


## Files

### HTML
The site uses 18 HTML files to represent the structure of all pages. 17 of them represent unique pages on the site.

`/capstone/template/algorithmixblog/`:

- `about.html`:
  - A small Django HTML template describing what awaits users on the site, and what it is used for.

- `layout.html`:
  - This is a Django HTML template that holds elements present on every page of the site, such as the site header with links, and the container into which all content of the other pages is inserted to.

- `index.html`:
  - The homepage of the site, which displays 3 controllable containers for blog post preview elements. These are infinite scroll containers that populate with new content as you scroll to ther bottom, which is achieved through the JavaScript code in `/capstone/static/algorithmixblog/index.js`.

- `discover.html`:
  - A template holding a large container for blog post preview elements, which are loaded as you scroll down the page using the JavaScript code in `/capstone/static/algorithmixblog/index.js`. 

- `favoriteblogposts.html`, `likedblogposts.html`, `followingfeed.html`:
  - These templates follow a similar structure, which is a container of blog post preview elements that can be paginated through using buttons.

- `followers.html`, `following.html`:
  - Two mostly identical templates that show widgets of the users followed by/following a specific user as you scroll down the page.

- `create.html`, `edit.html`:
  - Two very similar Django HTML templates that provide forms for creating and editing blog posts on the site.

- `noaccess.html`, `notfound.html`:
  - Two error templates which appear when certain `GET` request operations fail.

- `login.html`, `register.html`:
  - Two authentication templates used for gaining access to more features on the site by becoming a user.

- `search.html`:
  - A template providing a form to search for blog posts by name, text content, authors and tags.

- `userprofile.html`:
  - A template that shows user information on their profile on the site, as well as a form for editing user information.


### CSS
The site uses 2 CSS stylesheets to achieve a unique design and mobile responsiveness across all pages of the site.

`/capstone/static/algorithmixblog/`:

- `*.png`, `*.svg`:
  - These are some of the images and graphics used in the interface of the site.

- `styles.css`:
  - The core stylesheet of the site.

- `monokai.css`:
  - A stylesheet for code blocks that require syntax highlighting in user generated blog posts. Generated using the `Pygments` Python library.

### JavaScript
This site uses one large JavaScript file that operates on most sites of the page depending on the current URL.

`/capstone/static/algorithmixblog/`:

- `index.js`:
  - The main JavaScript file of the site. This is vanilla JavaScript that operates on most pages of the site, which is used for dynamic element class assignment, infinite scroll containers, custom hover behavior for elements, and more. It is also used for sending hidden requests to the backend for certain actions, e.g. liking a post.


### Python
The backend of this project is completely Python-based, using Django as the framework to interact with databases and process requests from the client side. Some files are generated by Django and unchanged, so they will be ignored here.

`/capstone/`:

- `admin.py`:
  - A small file for configuring Django's admin interface.

- `models.py`:
  - The file containing all custom models used in the backend of the site. Blog posts, their comments and their tags are represented by `BlogPost`, `BlogPostComment`, and `BlogPostTag` models respectively.
  - The `User` model has all the fields defined by Django for a website user, but it has some additions that allow for a user bio and follower/following relationship on the website.

- `urls.py`, `/capstone/capstone/urls.py`:
  - The structure of all URLs used in the project are defined here. Some URLs are API URLs, which are used implicitly on the client side using JavaScript. Each is linked to a view function defined in `views.py`.


- `views.py`:
  - The bridge between the hidden backend managed by Django and the front end of the website. Several view functions defined here validate request data and return the correct HTML and database data to the client. At least 4 different HTTP requests are processed by the view functions, which are `GET`, `POST`, `PUT` and `DELETE`.

- `/capstone/capstone/settings.py`:
  - Small tweaks occured to this file to register `algorithmixblog` as a Django application and to add the custom user model to Django's authentication system.

### Other
Other files created for this project.

`/capstone/`:

- `README.md`:
  - This Markdown file.

- `requirements.txt`:
  - A text file documenting the libraries required to run this project.