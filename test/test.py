import base64
import datetime
import json
import hashlib
import logging
import magic
import os
import re
import requests
import sys
import time
import unittest

from urlparse import urlparse
from StringIO import StringIO
from PIL import Image

from flask_login import current_user
from flask import session
from werkzeug.security import generate_password_hash

logging.basicConfig(level=logging.INFO)

BASE_PATH = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(BASE_PATH, "files")
PROJECT_PATH = os.path.dirname(BASE_PATH)
sys.path.append(PROJECT_PATH)

os.environ["CONFIG_PATH"] = "pasta.config.TestConfig"

from pasta import models, database
from pasta import pasta as app

sha256sum = lambda x: hashlib.sha256(x).hexdigest()
mime_type = lambda x: magic.Magic(mime=True).from_buffer(x)

def create_testuser(username, password):
    try:
        user = models.User(
            username = username,
            password = generate_password_hash(password)
        )
        database.session.add(user)
        database.session.commit()
        return True
    except Exception:
        return False

class PastaTests(unittest.TestCase):

    def setUp(self):
        """
        pre-test preparation
        """
        # zeroize session state
        self.client = app.test_client()
        database.create_all()

        # create test user
        create_testuser("testuser", "testpass")

    def _login(self, username, password):
        """
        (client context) login helper
        """
        data = { "username": username, "password": password }
        response = self.client.post("/login", data=data)
        return response

    def _logout(self):
        """
        (client context) logout helper
        """
        self.client.get("/logout")

    def tearDown(self):
        """
        post-test cleanup
        """
        self._logout()
        database.session.close()
        database.drop_all()

    def test_signup_cleartext_password_check(self):
        """ check password stored is not in cleartext """
        result = models.User.query.filter_by(username="testuser").first()
        self.assertNotEqual(result.password, "testpass")

    def test_signup_duplicate_no_overwrite(self):
        """ check user not overwritten during duplicate signup """
        result = models.User.query.filter_by(username="testuser").first()
        old_pass = result.password

        # create same user with diff pass
        data = { "username": "testuser", "password": "new", "confirm": "new" }
        response = self.client.post("/signup", data=data)
        results = models.User.query.filter_by(username="testuser")
        new_pass = results.first().password

        self.assertEqual(results.count(), 1)
        self.assertEqual(old_pass, new_pass)

    def test_login_authentication_good(self):
        """ check login pass has is_authenticated flag set to True """
        with self.client:
            self._login("testuser", "testpass")
            self.assertTrue(current_user.is_authenticated)
            self.assertEqual(current_user.username, "testuser")
            self._logout()

    def test_login_authentication_bad(self):
        """ check login fail has is_authenticated flag set to False """
        with self.client:
            self._login("fakeuser", "fakepass")
            self.assertFalse(current_user.is_authenticated)
            self._logout()

    def test_image_file_type_upload_good(self):
        """ check upload of supported image file types """
        test_files = [ "abc-a.jpg", "abc-d.png", "abc-g.gif" ]

        for test_file in test_files:
            with open(os.path.join(FILE_PATH, test_file), "rb") as fp:
                data = fp.read()

            with self.client:
                sha256 = sha256sum(data)
                s = StringIO(data)
                files = { "fileToUpload": (s, test_file) }

                # login and upload file
                self._login("testuser", "testpass")
                resp = self.client.post("/upload", data=files)
                self.assertEqual(resp.status_code, 200)

                # query database for successful upload
                image = (
                    models.Image.query
                    .filter_by(user_id=current_user.id)
                    .filter_by(sha256=sha256)
                    .filter_by(caption=test_file)
                ).first()
                self.assertIsNotNone(image)

    def test_image_file_type_upload_bad(self):
        """ check upload of unsupported image file type """
        with open("/bin/ls", "rb") as fp:
            data = fp.read()

        # upload elf binary
        with self.client:
            sha256 = sha256sum(data)
            s = StringIO(data)
            files = { "fileToUpload": (s, "fake-a.jpg") }
            self._login("testuser", "testpass")
            resp = self.client.post("/upload", data=files)
            self.assertEqual(resp.status_code, 200)

            image = (
                models.Image.query
                .filter_by(user_id=current_user.id)
                .filter_by(sha256=sha256)
                .filter_by(caption="fake-a.jpg")
            ).first()
            self.assertIsNone(image)

    def test_missing_user_login_enumeration(self):
        """ check for user enumeration via login timing """

        # good user - good pass
        t1 = time.time()
        self._login("testuser", "testpass")
        t2 = time.time()
        a = t2 - t1

        # good user - bad pass
        t1 = time.time()
        self._login("testuser", "testpast")
        t2 = time.time()
        b = t2 - t1

        # bad user
        t1 = time.time()
        self._login("fakeuser", "fakepass")
        t2 = time.time()
        c = t2 - t1

        avg = (a + b + c)/3

        # average time between all login attempts should be close-ish
        self.assertTrue((avg-0.01) < b < (avg+0.01))
        self.assertTrue((avg-0.01) < c < (avg+0.01))

    def test_server_parameter_response(self):
        """ check for http server parameter in response """
        resp = self.client.get("/")
        for param in resp.headers:
            try:
                k, v = param
                if k == "Server":
                    self.assertEqual(v, "Server")
            except ValueError:
                pass

    def test_unauthenticated_access_control(self):
        """ check for unauthenticated access to pages """
        endpoints = [
            "/logout",
            "/",
            "/1",
            "/image/view/1",
            "/image/edit/1",
            "/upload"
        ]
        for endpoint in endpoints:
            with self.client:
                resp = self.client.get(endpoint)
                self.assertTrue(resp.location.startswith("http://localhost/login"))

    def test_authenticated_access_control(self):
        """ check for access to other user content """
        # create user/pass
        create_testuser("realuser", "realpass")

        # upload file for testuser
        with open(os.path.join(FILE_PATH, "abc-a.jpg"), "rb") as fp:
            data = fp.read()
        a_sha256 = sha256sum(data)
        s = StringIO(data)
        f = { "fileToUpload": (s, "abc-a.jpg") }
        with self.client:
            self._login("testuser", "testpass")
            self.client.post("/upload", data=f)
            self._logout()

        # upload files for realuser
        with open(os.path.join(FILE_PATH, "abc-b.jpg"), "rb") as fp:
            data = fp.read()
        b_sha256 = sha256sum(data)
        s = StringIO(data)
        f = { "fileToUpload": (s, "abc-b.jpg") }
        with self.client:
            self._login("realuser", "realpass")
            self.client.post("/upload", data=f)
            self._logout()

        # testuser should not be able to access realuser image
        with self.client:
            self._login("testuser", "testpass")
            resp = self.client.get("/image/edit/" + b_sha256)
            self.assertEquals(resp.location, "http://localhost/")
            self._logout()

        # realuser should not be able to access testuser image
        with self.client:
            self._login("realuser", "realpass")
            resp = self.client.get("/image/edit/" + a_sha256)
            self.assertEquals(resp.location, "http://localhost/")
            self._logout()

    def test_image_caption_escaped(self):
        """ check for simple image caption rendering """
        # upload file for testuser
        with open(os.path.join(FILE_PATH, "abc-a.jpg"), "rb") as fp:
            data = fp.read()
        a_sha256 = sha256sum(data)
        s = StringIO(data)
        bad = "<script>alert(1);</script>"
        f = { "fileToUpload": (s, "AAAAA"+bad+"AAAAA") }
        with self.client:
            self._login("testuser", "testpass")
            self.client.post("/upload", data=f)
            resp = self.client.get("/image/edit/" + a_sha256)
            self.assertFalse(bad in resp.data)

    def test_image_max_file_size_5mb(self):
        """ check for upload of large file sizes """
        with open(os.path.join(FILE_PATH, "5mb.jpg"), "rb") as fp:
            data = fp.read()
        s = StringIO(data)
        f = { "fileToUpload": (s, "large.jpg") }
        with self.client:
            self._login("testuser", "testpass")
            resp = self.client.post("/upload", data=f)
            self.assertEqual(resp.status_code, 413)

    def test_unsupported_http_methods(self):
        """ check for use of unsupported http methods """
        bad_methods = [ "PUT", "DELETE", "TRACE", "CONNECT", "PATCH", "FAKE" ]

        # create login session
        url = "http://localhost:8080"
        session = requests.session()
        data = { "username": "testuser", "password": "testpass" }
        session.post(url + "/login", data=data)

        # cycle through invalid methods and expect code 405
        for method in bad_methods:
            req = requests.Request(method, url + "/")
            pre = session.prepare_request(req)
            resp = session.send(pre)
            self.assertEqual(resp.status_code, 405)
        session.close()


if __name__ == "__main__":
    unittest.main()
