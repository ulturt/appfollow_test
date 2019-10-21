# appfollow_test
Test task for Python developer

Parser of posts from https://news.ycombinator.com/

### Running

Requirements: docker, docker-compose

1. Clone the repository and enter the directory:

    `git clone https://github.com/ulturt/appfollow_test.git && cd appfollow_test`

2. Run docker-compose:

    `docker-compose up`

3. And visit:

    `http://localhost:5000/posts`
    
### Services

#### scraper
The service parses the posts and store them in the database (MongoDB). Parsing is performed periodically (every 30 minutes) and on demand.

#### api 
Flask web app with one endpoint `posts/` that returns parsed data from database. An endpoint can also sort and paginate data. Example:
`curl -X GET http://localhost:8000/posts?offset=10&limit=10`

For parsing on demand use `action=parse` in query params. Example:

`curl -X GET http://localhost:8000/posts?action=parse`
