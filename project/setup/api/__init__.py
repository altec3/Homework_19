from flask_restx import Api

api = Api(
    title='Lesson 19. Homework',
    description='Theme: Decorators and access control.',
    doc="/docs",
    validate=True
)
