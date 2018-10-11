from django.test import TestCase
from .models import Profile, Image, Comment
# Create your tests here.


class ProfileTestClass(TestCase):
    #set up method
    def setUp(self):
        self.yvonne = Profile(username='yvonne')
    #testing instance

    def test_instance(self):
        self.assertTrue(isinstance(self.yvonne, Profile))
    #testing save method

    def test_save_method(self):
        self.yvonne.save_profile()
        profiles = Profile.objects.all()
        self.assertTrue(len(profiles) > 0)
    #testng for deleting method

    def test_delete_method(self):
        self.yvonne.save_profile()
        self.yvonne.delete_profile()
        profiles = Profile.objects.all()
        self.assertTrue(len(profiles) == 1)


class CommentTestClass(TestCase):
    #set up method
    def setUp(self):
        self.coments = Comment(description='comment')
    #testing instance

    def test_instance(self):
        self.assertTrue(isinstance(self.coments, Comment))
    #testing for savinng method

    def test_save_method(self):
        self.coments.save_comment()
        comments = Comment.objects.all()
        self.assertTrue(len(comments) > 0)
    #testng for deleting method

    def test_delete_method(self):
        self.coments.save_comment()
        self.coments.delete_comment()
        comments = Comment.objects.all()
        self.assertTrue(len(comments) == 1)


class ImageTestClass(TestCase):
    #set Up method
    def setUp(self):
        self.image = Image(image='cool')
    #test  instance

    def test_instance(self):
        self.assertTrue(isinstance(self.image, Image))
    #testing for saving method

    def test_save_method(self):
        self.image.save_image()
        image = Image.objects.all()
        self.assertTrue(len(image) > 0)
    #testing for deleting method

    def test_delete_method(self):
        self.image.save_image()
        self.image.delete_image()
        image = Image.objects.all()
        self.assertTrue(len(image) > 0)
    #testing for update caption

    def test_update_metod(self):
        self.image.save_image()
        self.image.update_caption()
        image = Image.objects.all()
        self.assertTrue(len(image) > 0)
