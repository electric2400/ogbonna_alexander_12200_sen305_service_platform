from django.test import TestCase
from django.core.exceptions import ValidationError
from .models import Category, ServiceRequest


class ServiceRequestValidationTest(TestCase):

    def setUp(self):
        self.category = Category.objects.create(
            name="Electrical",
            description="Electrical maintenance"
        )

    def test_resolved_request_requires_resolution_date(self):
        request = ServiceRequest(
            title="Broken light",
            description="The classroom light is not working",
            category=self.category,
            status="RESOLVED",
            resolution_summary="Light repaired"
        )

        with self.assertRaises(ValidationError):
            request.full_clean()

    def test_resolved_request_requires_summary(self):
        from django.utils import timezone

        request = ServiceRequest(
            title="Broken fan",
            description="The classroom fan is not working",
            category=self.category,
            status="RESOLVED",
            resolved_at=timezone.now(),
            resolution_summary=""
        )

        with self.assertRaises(ValidationError):
            request.full_clean()