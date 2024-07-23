# ETL_Project_Draft

### Step-by-Step Setup

1. **Clone the Repository**: Clone the project repository to your local machine.

    ```bash
    git clone <repository_url>
    cd ETL_Project
    ```

2. **Create and Activate Conda Environment**: Create and activate a new conda environment.

    ```bash
   
    conda activate dev environment
    conda install flask pymongo python-dotenv flask-cors seaborn matplotlib pandas
    ```

3. **Install Dependencies**: Install the required Python packages using `pip`.

    ```bash
    pip install -r requirements.txt
    ```

4. **Set Up Environment Variables**: Create a `.env` file in the `flask_app` directory and add your MongoDB connection string.

    ```env
    MONGO_URI=mongodb://localhost:27017/national_parks_db
    ```

5. **Run the Application**: Use the following command to start the Flask application.

    ```bash
    flask run
    ```