# Feedback

The following is a log of all feedback recieved from peers.

From: Shane Miller    
Content reviewed: README and ERD    
Date: 15/12/2024
    
    Is the main purpose of the app clear?
    It apears to be simple to understand, but i have a question about other exercises besides weights... like treadmill or such. Or is the focus on Weights Training?

    Are all the entities understandable? 
    All enterties are understandable, but could be expanded upon. goal could have a target date for the goal for example.. and you could include optional data for distance and time for things like cycling and running etc. depending on how complex you want to get.

    Especially how the 'goal' entity works?
    At the moment with Weight Training focus the goal makes sense, I feel if the goal was updated based off of exercises completed it would be more functional. You could tie this into a workout completed or failed attribute in workout i think.. and then make a route to update goals. 

Action required: 
- I've already stated that the API will focus on weight training only, cardio and body weight exercises will be implemented in the future.
- Will include target date for goal.
- Make goal status dynamic if goal is achieved to change itself. (Maybe a future implementation depending on time)


From: Evan Meehan
Content reviewed: Workout.py (model and controller)
Date: 19/12/2024    
    
    **Strengths:**

    ***Database Design:***
    - The Workout model has a clear structure with appropriate relationships (user and workout_exercises).

    - The use of ```ForeignKey and cascade="all, delete"``` ensures proper data integrity and cascading deletion.

    ***Validation:***
    - The custom validation methods in WorkoutSchema for workout_date and duration are thoughtful and ensure data correctness.
    - The use of Marshmallow's Regexp validator for name ensures user input constraints.

    ***Serialisation:***
    - ```fields.Nested``` for ```user``` and ```workout_exercises``` maintains modularity by linking schemas instead of duplicating fields.

    **Areas For Improvement:**

    ***Field Specifications:***
    - Adding ```nullable=False``` constraints to fields like ```workout_date``` and ```duration``` ensures consistency between the database schema and the validation logic.

    ***Error Messages:***
    - Improve error messages for validation to provide clearer guidance, e.g., include examples or valid formats for users.

    ***Code Comments:***
    - Add comments explaining the purpose of relationships and validations to make the code more maintainable for others (or your future self).

    ***Imports:***
    - You are importing Length but not using it. Remove unused imports to keep the code clean.

    ***Testing Considerations:***
    - Ensure unit tests validate all edge cases, such as invalid dates, excessively long durations, and invalid characters in name. 

Action required:
- Improve error messages to include example inputs
- Add code comments for documentation purposes
- Remove unnecessary imports eg. Length when not used
- More testing considerations.