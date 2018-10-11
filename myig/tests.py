from django.test import TestCase
from .models import Profile, Image, Comment
# Create your tests here.


class ProfileTestClass(TestCase):
    #set up method
    def setUp(self):
        self.ojijo = Profile(user = 'ojijo',user_name='yvonne',bio = 'this is true',profile_image = 'myilg/media/profiles/ujbi.jpg')
    #testing instance

    def test_instance(self):
        self.assertTrue(isinstance(self.ojijo, Profile))
    #testing save method

    def test_save_method(self):
        self.ojijo.save_profile()
        profiles = Profile.objects.all()
        self.assertTrue(len(profiles) > 0)
    #testng for deleting method

    def test_delete_method(self):
        self.ojijo.save_profile()
        self.ojijo.delete_profile()
        profiles = Profile.objects.all()
        self.assertTrue(len(profiles) == 1)


class CommentTestClass(TestCase):
    #set up method
    def setUp(self):
        self.commentIg = Comment(text='this made me cry', poster ='yvonne', posted_time = '12 minutes ago')
    #testing instance

    def test_instance(self):
        self.assertTrue(isinstance(self.commentIg, Comment))
    #testing for savinng method

    def test_save_method(self):
        self.commentIg.save_comment()
        comments = Comment.objects.all()
        self.assertTrue(len(comments) > 0)
    #testng for deleting method

    def test_delete_method(self):
        self.commentIg.save_comment()
        self.commentIg.delete_comment()
        comments = Comment.objects.all()
        self.assertTrue(len(comments) == 1)


class ImageTestClass(TestCase):
    #set Up method
    def setUp(self):
        self.image = Image(name = 'haron' ,image_caption= 'yeah', image='myig/media/images/uierh.jpg' ,profile = 'popopod',posted_time='32 minutes ago')
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
        images = Image.objects.all()
        self.assertTrue(len(image) > 0)
    #testing for update caption

    def test_update_metod(self):
        self.image.save_image()
        self.image.update_caption()
        images = Image.objects.all()
        self.assertTrue(len(image) > 0)
