from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Vehicle
from .serializers import VehicleSerializer
import random
import string
import csv
from django.http import HttpResponse
from datetime import datetime

# --- HELPER FUNCTIONS ---

def generate_number_plate():
    """Generates a random plate like KBA 123C"""
    letters = ''.join(random.choices(string.ascii_uppercase, k=3)) 
    numbers = ''.join(random.choices(string.digits, k=3))         
    last_letter = random.choice(string.ascii_uppercase)           
    return f"K{letters[1:]} {numbers}{last_letter}"

def generate_condition_report(status, sub_status=None):
    """Generates a condition report based on keywords."""
    if status == Vehicle.UNROADWORTHY:
        if sub_status == Vehicle.FIXED:
            return random.choice([
                "Engine overhaul complete. Ready for inspection.",
                "Brake system repaired. Fixed.",
                "Windshield replaced. Fixed.",
                "Transmission rebuilt. Fixed."
            ])
        else: # Fixer-Upper
            return random.choice([
                "Catastrophic engine failure. Needs replacement.",
                "Chassis cracked. Severe damage.",
                "Gearbox missing. Fixer-Upper.",
                "Written off after collision."
            ])
    
    # Active Vehicles - Random Issues
    issues = [
        "MAINTENANCE: Oil change due.",
        "MAINTENANCE: Brake pads worn.",
        "LICENSE: Expired last week.",
        "LICENSE: TLB renewal needed.",
        "INTERIOR: Seats torn in back row.",
        "INTERIOR: Audio system wiring faulty.",
        "DRIVER: Assigned driver off-duty.",
        "DRIVER: No driver assigned for night shift.",
        "Good condition. No issues.",
        "Good condition. Recently serviced."
    ]
    return random.choice(issues)

# --- API VIEWS ---

@api_view(['GET'])
def get_all_vehicles(request):
    """Returns all vehicles currently in the system."""
    vehicles = Vehicle.objects.all()
    serializer = VehicleSerializer(vehicles, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def simulate_import(request):
    # 1. Wipe existing data
    Vehicle.objects.all().delete()
    new_vehicles = []
    
    # 2. Generate 15 Fixed (Unroadworthy but ready to move)
    for _ in range(15): 
        plate = generate_number_plate()
        new_vehicles.append(Vehicle(
            number_plate=plate,
            vehicle_type=random.choice([Vehicle.MATATU, Vehicle.BUS]),
            revenue=0,
            status=Vehicle.UNROADWORTHY,
            unroadworthy_sub_status=Vehicle.FIXED,
            condition_report=generate_condition_report(Vehicle.UNROADWORTHY, Vehicle.FIXED)
        ))
        
    # 3. Generate 35 Fixer-Uppers (The broken ones)
    for _ in range(35): 
        plate = generate_number_plate()
        new_vehicles.append(Vehicle(
            number_plate=plate,
            vehicle_type=random.choice([Vehicle.MATATU, Vehicle.BUS]),
            revenue=0,
            status=Vehicle.UNROADWORTHY,
            unroadworthy_sub_status=Vehicle.FIXER_UPPER,
            condition_report=generate_condition_report(Vehicle.UNROADWORTHY, Vehicle.FIXER_UPPER)
        ))

    # 4. Generate 150 Active Vehicles
    for _ in range(150):
        plate = generate_number_plate()
        report = generate_condition_report(Vehicle.ACTIVE)
        m_due = "MAINTENANCE" in report
        l_exp = "LICENSE" in report
        
        new_vehicles.append(Vehicle(
            number_plate=plate,
            vehicle_type=random.choice([Vehicle.MATATU, Vehicle.BUS]),
            revenue=random.randint(5000, 45000), 
            status=Vehicle.ACTIVE,
            unroadworthy_sub_status=None,
            condition_report=report,
            maintenance_due=m_due,
            license_expired=l_exp
        ))

    Vehicle.objects.bulk_create(new_vehicles)
    return Response({"message": "Simulation Complete. 200 Vehicles Imported.", "count": 200})

@api_view(['POST'])
def move_to_active(request, pk):
    """Moves a Fixed vehicle to Active status."""
    try:
        vehicle = Vehicle.objects.get(pk=pk)
        if vehicle.status == Vehicle.UNROADWORTHY and vehicle.unroadworthy_sub_status == Vehicle.FIXED:
            vehicle.status = Vehicle.ACTIVE
            vehicle.unroadworthy_sub_status = None
            vehicle.condition_report = "Recently moved from Unroadworthy. Monitoring required."
            vehicle.save()
            return Response({"status": "success", "message": "Vehicle moved to Active"})
        return Response({"status": "error", "message": "Vehicle not eligible for move"}, status=400)
    except Vehicle.DoesNotExist:
        return Response(status=404)

@api_view(['DELETE'])
def delete_vehicle(request, pk):
    """Deletes a vehicle (Written Off)."""
    try:
        vehicle = Vehicle.objects.get(pk=pk)
        vehicle.delete()
        return Response({"status": "success", "message": "Vehicle written off"})
    except Vehicle.DoesNotExist:
        return Response(status=404)

@api_view(['POST'])
def write_off_vehicle(request, pk):
    vehicle = get_object_or_404(Vehicle, pk=pk)
    vehicle.status = 'Unroadworthy'
    vehicle.unroadworthy_sub_status = 'Fixer-Upper'
    vehicle.condition_report = "Written off: Critical failure detected."
    vehicle.save()
    return Response(VehicleSerializer(vehicle).data)

@api_view(['GET'])
def download_garage_report(request):
    """
    Generates a CSV report of all Unroadworthy vehicles
    with estimated repair costs.
    """
    # 1. Setup the CSV Response
    response = HttpResponse(content_type='text/csv')
    filename = f"Garage_Report_{datetime.now().strftime('%Y-%m-%d')}.csv"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    writer = csv.writer(response)
    
    # 2. Write Header Row
    writer.writerow(['ID', 'Plate Number', 'Type', 'Status', 'Condition Report', 'Est. Repair Cost (KES)'])

    # 3. Get Data
    vehicles = Vehicle.objects.filter(status=Vehicle.UNROADWORTHY)
    
    total_cost = 0

    for v in vehicles:
        # Calculate Estimated Cost based on keywords
        cost = 0
        report_upper = v.condition_report.upper()
        
        if "ENGINE" in report_upper: cost = 150000
        elif "TRANSMISSION" in report_upper: cost = 85000
        elif "BRAKE" in report_upper: cost = 25000
        elif "WINDSHIELD" in report_upper: cost = 15000
        elif "CHASSIS" in report_upper: cost = 200000
        elif "GEARBOX" in report_upper: cost = 90000
        else: cost = 10000 # Minor fix
        
        total_cost += cost

        # Write Row
        writer.writerow([
            v.id, 
            v.number_plate, 
            v.vehicle_type, 
            v.unroadworthy_sub_status, 
            v.condition_report, 
            cost
        ])

    # 4. Write Footer (Total)
    writer.writerow([])
    writer.writerow(['', '', '', '', 'TOTAL BUDGET REQUIRED:', total_cost])

    return response