import boto
import StringIO
import urllib2
import re
from boto.s3.key import Key
from db import User, Project

AWS_ACCESS_KEY = ''
AWS_SECRET_KEY = ''
BUCKET_NAME = ''
RE_GET_FILE = re.compile('(.*)(.com)/(.*)/(.*)/(/*)')

def upload_file(url, user):
    try:
        # S3 Save
        conn = boto.connect_s3(AWS_ACCESS_KEY, AWS_SECRET_KEY)
        bucket = conn.get_bucket(BUCKET_NAME)
        k = Key(bucket)
        k.key = RE_GET_FILE.match(url).group(5)
        file_object = urllib2.urlopen(url)
        fp = StringIO.StringIO(file_object.read())
        k.set_contents_from_file(fp)
        k.make_public()
        # Save S3 url to user
        url_to_save = 'https://s3-us-west-2.amazonaws.com/'+ BUCKET_NAME + '/' + k.key

        project = Project.create(url=url_to_save, project_user_id=user.user_id, status='pre')
        if not user.team_id:
            user.project_id = project.proj_id
            user.save()
        else:
            project.team_id = user.team_id
            project.save()
            users = User.update(project_id=project.proj_id).where(User.team_id == user.team_id)
            users.execute()

        return True
    except:
        return False
