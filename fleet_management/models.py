from django.db import models

class Vehicle(models.Model):
    # Vehicle Types
    MATATU = 'Matatu'
    BUS = 'Bus'
    VEHICLE_TYPES = [
        (MATATU, 'Matatu'),
        (BUS, 'Bus'),
    ]

    # Primary Status (The Big Filter)
    ACTIVE = 'Active'
    UNROADWORTHY = 'Unroadworthy'
    STATUS_CHOICES = [
        (ACTIVE, 'Active'),
        (UNROADWORTHY, 'Unroadworthy'),
    ]

    # Sub-Status for Unroadworthy Vehicles
    # "Fixed" means ready to move to Active. "Fixer-Upper" means broken.
    FIXED = 'Fixed'
    FIXER_UPPER = 'Fixer-Upper'
    SUB_STATUS_CHOICES = [
        (FIXED, 'Fixed'),
        (FIXER_UPPER, 'Fixer-Upper'),
    ]
    
    # Fields
    number_plate = models.CharField(max_length=15, unique=True)
    vehicle_type = models.CharField(max_length=10, choices=VEHICLE_TYPES)
    
    # Revenue (KES)
    revenue = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    # Status
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default=ACTIVE)
    
    # Only applicable if status is Unroadworthy
    unroadworthy_sub_status = models.CharField(
        max_length=15, 
        choices=SUB_STATUS_CHOICES, 
        null=True, 
        blank=True
    )

    # Condition Report / Assessment Report
    # This contains the keywords like "Engine", "Tires", "Interior"
    condition_report = models.TextField(blank=True, help_text="Detailed assessment of the vehicle condition.")

    # Specific Flags for Active Vehicles (to help with filtering)
    driver_assigned = models.BooleanField(default=True)
    license_expired = models.BooleanField(default=False)
    maintenance_due = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.number_plate} - {self.status}"