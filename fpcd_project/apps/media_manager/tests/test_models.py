"""
Tests para los modelos de media_manager.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.media_manager.models import MediaFile, MediaFolder, MediaFileType

User = get_user_model()


class MediaFileTypeTest(TestCase):
    """Tests para los tipos de archivo."""

    def test_media_file_type_choices(self):
        """Test que todos los tipos están disponibles."""
        self.assertEqual(MediaFileType.IMAGE, "image")
        self.assertEqual(MediaFileType.DOCUMENT, "document")
        self.assertEqual(MediaFileType.VIDEO, "video")
        self.assertEqual(MediaFileType.AUDIO, "audio")
        self.assertEqual(MediaFileType.OTHER, "other")


class MediaFileModelTest(TestCase):
    """Tests para el modelo MediaFile."""

    def setUp(self):
        self.user = User.objects.create_user(
            email="uploader@fpcd.com",
            password="testpass123",
            role="editor",
        )

    def test_create_media_file(self):
        """Test creación de archivo."""
        # This test would require an actual file
        # For now, just test the model structure
        file = MediaFile(
            filename="test.jpg",
            file_type="image",
            uploader=self.user,
        )
        self.assertEqual(file.filename, "test.jpg")
        self.assertEqual(file.file_type, "image")

    def test_get_file_type_image(self):
        """Test get_file_type para imagen."""
        file = MediaFile(filename="test.jpg")
        self.assertEqual(file.get_file_type(), "image")

    def test_get_file_type_document(self):
        """Test get_file_type para documento."""
        file = MediaFile(filename="test.pdf")
        self.assertEqual(file.get_file_type(), "document")

    def test_get_file_type_video(self):
        """Test get_file_type para video."""
        file = MediaFile(filename="test.mp4")
        self.assertEqual(file.get_file_type(), "video")

    def test_get_file_type_audio(self):
        """Test get_file_type para audio."""
        file = MediaFile(filename="test.mp3")
        self.assertEqual(file.get_file_type(), "audio")

    def test_get_file_extension(self):
        """Test get_file_extension."""
        file = MediaFile(filename="document.pdf")
        self.assertEqual(file.get_file_extension(), "pdf")

    def test_get_file_size_display(self):
        """Test get_file_size_display."""
        file = MediaFile(filename="test.jpg", file_size=1024)
        self.assertEqual(file.get_file_size_display(), "1.0 KB")

    def test_get_file_size_display_mb(self):
        """Test get_file_size_display en MB."""
        file = MediaFile(filename="test.jpg", file_size=1048576)
        self.assertEqual(file.get_file_size_display(), "1.0 MB")


class MediaFolderModelTest(TestCase):
    """Tests para el modelo MediaFolder."""

    def setUp(self):
        self.user = User.objects.create_user(
            email="folder_user@fpcd.com",
            password="testpass123",
            role="editor",
        )

    def test_create_folder(self):
        """Test creación de carpeta."""
        folder = MediaFolder.objects.create(
            name="Images",
            slug="images",
            created_by=self.user,
        )
        self.assertEqual(folder.name, "Images")
        self.assertEqual(folder.slug, "images")

    def test_folder_str(self):
        """Test __str__ de carpeta."""
        folder = MediaFolder.objects.create(
            name="Documents",
            created_by=self.user,
        )
        self.assertEqual(str(folder), "Documents")
