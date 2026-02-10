import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
import { VehicleService, Vehicle } from './services/vehicle'; 

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, FormsModule, HttpClientModule],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class AppComponent implements OnInit {
  
  // Data Containers
  allVehicles: Vehicle[] = [];
  activeVehicles: Vehicle[] = [];
  unroadworthyVehicles: Vehicle[] = [];
  
  // Search Engine
  searchText: string = '';
  searchError: string = '';
  validKeywords = ['MAINTENANCE', 'LICENSE', 'INTERIOR', 'DRIVER', 'ENGINE', 'TIRE', 'BRAKE', 'SUSPENSION'];

  // Stats
  repairCount: number = 0; // REPLACES REVENUE
  unroadworthyCount: number = 0;
  activeCount: number = 0;

  constructor(private vehicleService: VehicleService) {}

  ngOnInit() {
    this.loadData();
  }

  loadData() {
    this.vehicleService.getAllVehicles().subscribe((data) => {
      this.allVehicles = data;
      this.processVehicles();
    });
  }

  processVehicles() {
    // 1. Reset Arrays
    this.activeVehicles = [];
    this.unroadworthyVehicles = [];
    this.repairCount = 0;

    // 2. Sort Data
    this.allVehicles.forEach(v => {
      if (v.status === 'Active') {
        this.activeVehicles.push(v);
      } else {
        this.unroadworthyVehicles.push(v);
        // Count Fixer-Uppers
        if (v.unroadworthy_sub_status === 'Fixer-Upper') {
          this.repairCount++;
        }
      }
    });

    // 3. Update Counts
    this.activeCount = this.activeVehicles.length;
    this.unroadworthyCount = this.unroadworthyVehicles.length;
  }

  // --- GETTERS FOR LOGIC ---
  
  // Returns true if there are ANY cars marked 'Fixed' in the garage
  get hasFixedCars(): boolean {
    return this.unroadworthyVehicles.some(v => v.unroadworthy_sub_status === 'Fixed');
  }

  // Returns true if there are cars that need fixing
  get hasBrokenCars(): boolean {
    return this.unroadworthyVehicles.some(v => v.unroadworthy_sub_status === 'Fixer-Upper');
  }

  // --- ACTIONS ---

  onSimulate() {
    if(confirm("⚠ WARNING: This will WIPE the database and generate 200 new vehicles. Continue?")) {
      this.vehicleService.simulateImport().subscribe(() => {
        this.loadData();
        alert("Simulation Complete: 200 Vehicles Imported.");
      });
    }
  }

  // INSTANT UPDATE: Move Unroadworthy -> Active
  moveToActive(id: number) {
    const car = this.allVehicles.find(v => v.id === id);
    if (!car) return;

    // Local Update (Instant)
    car.status = 'Active';
    car.unroadworthy_sub_status = 'Fixed'; // Clears the bad status locally
    this.processVehicles(); 

    // Backend Update
    this.vehicleService.moveToActive(id).subscribe({
      error: () => {
        alert("Sync Error: Could not move vehicle.");
        this.loadData(); // Revert
      }
    });
  }

  // INSTANT UPDATE: Active -> Unroadworthy (The new "Write Off" Logic)
  onWriteOff(id: number) {
    if(!confirm("Report Critical Failure? This will move the vehicle to Unroadworthy.")) return;

    const car = this.allVehicles.find(v => v.id === id);
    if (!car) return;

    // Local Update
    car.status = 'Unroadworthy';
    car.unroadworthy_sub_status = 'Fixer-Upper';
    car.condition_report = "CRITICAL FAILURE REPORTED";
    this.processVehicles();

    // Backend Update
    this.vehicleService.writeOff(id).subscribe({
      error: () => { 
        alert("Sync Error");
        this.loadData(); 
      }
    });
  }

  // Permanent Delete (For the Garage)
  permanentDelete(id: number) {
    if(confirm("⚠ PERMANENTLY SCRAP VEHICLE? This cannot be undone.")) {
      // Local Update
      this.allVehicles = this.allVehicles.filter(v => v.id !== id);
      this.processVehicles();

      // Backend Update
      this.vehicleService.deleteVehicle(id).subscribe();
    }
  }

  downloadGarageReport() {
    // Logic Check: Don't download if empty
    if (!this.hasBrokenCars) {
      alert("No broken vehicles to report!");
      return;
    }

    this.vehicleService.downloadReport().subscribe((blob) => {
      const link = document.createElement('a');
      link.href = window.URL.createObjectURL(blob);
      link.download = `Sacco_Garage_Report_${new Date().toISOString().slice(0,10)}.csv`;
      link.click();
    });
  }

  // --- SEARCH ENGINE ---

  get filteredActiveVehicles() {
    if (!this.searchText) {
      this.searchError = '';
      return this.activeVehicles;
    }

    const term = this.searchText.toUpperCase().trim();
    const isKeywordSearch = this.validKeywords.some(k => term.includes(k));
    const isPlateSearch = term.startsWith('K');

    if (!isPlateSearch && !isKeywordSearch && term.length > 3) {
      this.searchError = `Keyword '${term}' not recognized.`;
      return [];
    } else {
      this.searchError = '';
    }

    return this.activeVehicles.filter(v => {
      const matchPlate = v.number_plate.includes(term);
      const matchCondition = v.condition_report.toUpperCase().includes(term);
      return matchPlate || matchCondition;
    });
  }
}