from flask_restx.reqparse import RequestParser

page_parser: RequestParser = RequestParser()
page_parser.add_argument(name='page', type=int, location='args', required=False, default=1)

movie_filter_and_page_parser: RequestParser = page_parser.copy()
movie_filter_and_page_parser.add_argument(name='director_id', type=str, location='args', required=False)
movie_filter_and_page_parser.add_argument(name='genre_id', type=str, location='args', required=False)
movie_filter_and_page_parser.add_argument(name='year', type=int, location='args', required=False)

auth_parser: RequestParser = RequestParser()
auth_parser.add_argument(name='username', type=str, location='json', required=True, nullable=False)
auth_parser.add_argument(name='password', type=str, location='json', required=True, nullable=False)

refresh_auth_parser: RequestParser = RequestParser()
refresh_auth_parser.add_argument(name="refresh_token", type=str, required=True, nullable=False)
