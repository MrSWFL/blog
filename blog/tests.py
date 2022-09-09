# blog/tests.py
from django.contrib.auth import get_user_model
from django.test import TestCase 
from django.urls import reverse

from .models import Post

# -CONSTANTS -----
# -- HTTP status codes   See: developer.mozilla.org/en-US/docs/Web/HTTP/Status
SUCCESS = 200       # 200: OK
REDIRECT = 302     # 302: REDIRECT
FAILURE = 404       # 404: Page Not Found

# -- User details
u_username = "testuser"
u_email = "test@email.com"
u_password = "secret"

# -- Post details
p_title = "Little Miss Muffet..."
p_body = "Sweet, warm, curvy"
p_author = "The big bad wolf"
p_upd_title = "The meaning of Life"
p_upd_body = "Endless BS about contemplating my navel."

# -- URL details
u_post_list_url = "/"
u_post_detail_url = "/post/1/"
u_bad_post_detail_url = "/post/99999/"

# -- URL/Template details
t_base_content = "<!-- templates/base.html -->"

u_home_name = "home"
t_home_filename = "home.html"
t_home_content = "<!-- templates/home.html -->"

u_post_name = "post_detail"
t_post_filename = "post_detail.html"
t_post_content = "<!-- templates/post_detail.html -->"

class BlogTests(TestCase):
    # -- SETUP -----
    @classmethod
    def setUpTestData(cls):
        # Create a user
        cls.user = get_user_model().objects.create_user(
                username = u_username,
                email = u_email,
                password = u_password
            )
    
        # [M] Create a Post
        cls.post = Post.objects.create(
            title = p_title,
            body = p_body,
            author = cls.user
        )

    #-- Test Post Creation -----
    def test_post_model(self):
        # User tests
        self.assertEqual(self.post.author.username, u_username)

        # [M] Post model tests
        self.assertEqual(str(self.post), p_title)
        self.assertEqual(self.post.title, p_title)
        self.assertEqual(self.post.body, p_body)
        
        # [U] URL tests - Doest the URL of the post matched the expected URL?
        self.assertEqual(self.post.get_absolute_url(), u_post_detail_url)

        # [T] Are we using the correct Base Template?


    # [U] Test that the URL exists for List View
    def test_url_exists_at_correct_location_listview(self):
        r = self.client.get(u_post_list_url)
        self.assertEqual(r.status_code, SUCCESS)


    # [U] Test that the URL exists for Detail View
    def test_url_exists_at_correct_location_detailview(self):
        r = self.client.get(u_post_detail_url)
        
        self.assertEqual(r.status_code, SUCCESS)


    # [U,T] Test"path name"; Template contents; Template filename
    def test_post_listview(self):
        r = self.client.get(reverse(u_home_name))

        self.assertEqual(r.status_code, SUCCESS)
        self.assertContains(r, t_home_content)
        self.assertTemplateUsed(r, t_home_filename)

    # [U,T] Test"path name" URL; Template contents; Template filename
    def test_post_detailview(self):
        r = self.client.get(reverse(u_post_name, kwargs={"pk" : self.post.pk}))
        bad_r = self.client.get(u_bad_post_detail_url)  # Do a "negative" test

        self.assertEqual(r.status_code, SUCCESS)
        self.assertEqual(bad_r.status_code, FAILURE)
        self.assertContains(r, t_post_content)
        self.assertTemplateUsed(r, t_post_filename)

    # [V, U, T] Test BlogCreateView
    def test_post_createview(self):
        r = self.client.post(
            reverse("post_new"),
            {
                "title" : p_title,
                "body" : p_body,
                "author" : self.user.id,
            },
        )

        self.assertEqual(r.status_code, REDIRECT)
        self.assertEqual(Post.objects.last().title, p_title)
        self.assertEqual(Post.objects.last().body, p_body)

    # [V, U, T] Test BlogUpdateView
    def test_post_updateview(self):
        r = self.client.post(
            reverse("post_edit", args="1"),
            {
                "title" : p_upd_title,
                "body" : p_upd_body,
            },
        )

        self.assertEqual(r.status_code, REDIRECT)
        self.assertEqual(Post.objects.last().title, p_upd_title)
        self.assertEqual(Post.objects.last().body, p_upd_body)


    # [V, U, T] Test BlogDeleteView
    def test_post_deleteview(self):
        r = self.client.post(reverse("post_delete", args="1"))

        self.assertEqual(r.status_code, REDIRECT)
    