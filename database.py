from sqlalchemy import create_engine, text
import os

db_connection = os.environ['db_connection']
engine = create_engine(db_connection,
                       connect_args={
                          "ssl":{
                             "ssl_ca":"/etc/ssl/cert.pem"
                          }
                       })






def load_jobs_from_db():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM jobs"))
        jobs = []
        for row in result.all():
            jobs.append(row)
        return jobs

def load_job_from_db(id):
    with engine.connect() as conn:
        result = conn.execute(text('SELECT * FROM jobs WHERE id = :val'), {'val': id})
        row = result.first()

        if row:
            column_names = result.keys()
            job_dict = {column: getattr(row, column) for column in column_names}
            return job_dict
        else:
            return None


def add_application_to_db(job_id, data):
    with engine.connect() as conn:
        query = text("INSERT INTO applications (job_id, full_name, email, linkedin_url, education, work_experience, resume_url) values (:job_id, :full_name, :email, :linkedin_url, :education, :work_experience, :resume_url)")
        
        parameters = {
            'job_id': job_id,
            'full_name': data['full_name'],
            'email': data['email'],
            'linkedin_url': data['linkedin_url'],
            'education': data['education'],
            'work_experience': data['work_experience'],
            'resume_url': data['resume_url'],
        }

        try:
         conn.execute(query, parameters)
         conn.commit()  # Make sure to commit the changes
        except Exception as e:
         print(f"Error executing query: {e}")
