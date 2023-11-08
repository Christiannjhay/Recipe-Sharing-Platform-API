from flask import Flask, request, jsonify
from sqlalchemy import ForeignKey, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Text


#Headers: Content-Type: application/json
# Define the Flask app
app = Flask(__name__)

# Define the MSSQL database connection details
Server = 'Desktop-DA0V9'  # The hostname or IP address of your MSSQL server
Database = 'RecipeSharing'
Driver = 'ODBC Driver 17 for SQL Server'

# Create a SQLAlchemy engine
Database_Con = f'mssql://@{Server}/{Database}?driver={Driver}'
engine = create_engine(Database_Con)

# Create a Session class for database interactions
Session = sessionmaker(bind=engine)

# Define a Recipe model
Base = declarative_base()

# Define a Ratings model
class Ratings(Base):
    __tablename__ = 'Ratings'

    RatingID = Column(Integer, primary_key=True)
    RecipeID = Column(Integer, ForeignKey('Recipes.RecipeID'), nullable=False)
    RatingValue = Column(Integer, nullable=False, name='RatingValue')

# Create the database table for Ratings
Base.metadata.create_all(engine)

# API endpoint to rate a specific recipe
@app.route('/recipes/<int:recipe_id>/ratings', methods=['POST'])
def rate_recipe(recipe_id):
    data = request.get_json()
    
    rating = data.get('rating')

    # Check if the specified recipe exists
    session = Session()
    recipe = session.query(Recipes).filter_by(RecipeID=recipe_id).first()

    if not recipe:
        session.close()
        return jsonify({"message": "Recipe not found"}), 404

    # Check if the rating is within the valid range (1-5)
    if not (1 <= rating <= 5):
        session.close()
        return jsonify({"message": "Invalid rating. Please provide a rating between 1 and 5"}), 400

    # Create a new Rating object and associate it with the recipe
    new_rating = Ratings(RecipeID=recipe_id, RatingValue=rating)

    # Add the new rating to the database
    session.add(new_rating)
    session.commit()
    session.close()

    return jsonify({"message": "Rating added successfully"})

# Define a Comment model
class Comments(Base):
    __tablename__ = 'Comments'

    CommentID = Column(Integer, primary_key=True)
    RecipeID = Column(Integer, ForeignKey('Recipes.RecipeID'), nullable=False)
    CommentText = Column(Text, nullable=False, name='CommentText')
    
# Create the database table for Comments
Base.metadata.create_all(engine)

# API endpoint to add a comment to a specific recipe
@app.route('/recipes/<int:recipe_id>/comments', methods=['POST'])
def add_comment(recipe_id):
    data = request.get_json()
    
    comment_text = data.get('comment_text')

    # Check if the specified recipe exists
    session = Session()
    recipe = session.query(Recipes).filter_by(RecipeID=recipe_id).first()

    if not recipe:
        session.close()
        return jsonify({"message": "Recipe not found"}), 404

    # Create a new Comment object and associate it with the recipe
    new_comment = Comments(RecipeID=recipe_id, CommentText=comment_text)

    # Add the new comment to the database
    session.add(new_comment)
    session.commit()
    session.close()

    return jsonify({"message": "Comment added successfully"})


#RECIPES
class Recipes(Base):
    __tablename__ = 'Recipes'

    RecipeID = Column(Integer, primary_key=True)
    Name = Column(String(100), nullable=False, name='Name')
    Ingredients = Column(String(500), nullable=False, name='Ingredients')
    Steps = Column(Text, nullable=False, name='Steps')
    PreparationTime = Column(Integer, nullable=False, name='PreparationTime')

# Create the database table
Base.metadata.create_all(engine)

# API endpoint to add a new recipe
@app.route('/recipes', methods=['POST'])
def add_recipe():
    data = request.get_json()
    
    name = data.get('name')
    ingredients = data.get('ingredients')
    steps = data.get('steps')
    prep_time = data.get('prep_time')

    # Create a new Recipe object
    new_recipe = Recipes(Name=name, Ingredients=ingredients, Steps=steps, PreparationTime=prep_time)

    # Add the new recipe to the database
    session = Session()
    session.add(new_recipe)
    session.commit()
    session.close()

    return jsonify({"message": "Recipe added successfully"})

if __name__ == '__main__':
    app.run(debug=True)

