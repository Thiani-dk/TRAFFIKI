import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Vehicle {
  id: number;
  number_plate: string;
  vehicle_type: string;
  revenue: number;
  status: 'Active' | 'Unroadworthy';
  unroadworthy_sub_status?: 'Fixed' | 'Fixer-Upper';
  condition_report: string;
  driver_assigned: boolean;
  license_expired: boolean;
  maintenance_due: boolean;
}

@Injectable({
  providedIn: 'root'
})
export class VehicleService {
  private apiUrl = 'http://127.0.0.1:8000/api'; 

  constructor(private http: HttpClient) { }

  getAllVehicles(): Observable<Vehicle[]> {
    return this.http.get<Vehicle[]>(`${this.apiUrl}/vehicles/`);
  }

  simulateImport(): Observable<any> {
    return this.http.post(`${this.apiUrl}/simulate/`, {});
  }

  moveToActive(id: number): Observable<any> {
    return this.http.post(`${this.apiUrl}/move-active/${id}/`, {});
  }

  // UPDATED: Used to move Active -> Unroadworthy
  writeOff(id: number): Observable<any> {
    return this.http.post(`${this.apiUrl}/write-off/${id}/`, {});
  }

  // Used for permanent deletion (Garage)
  deleteVehicle(id: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/delete/${id}/`);
  }


  downloadReport(): Observable<Blob> {
    // We must specify { responseType: 'blob' } so Angular knows it's a file
    return this.http.get(`${this.apiUrl}/download-report/`, { responseType: 'blob' });
  }
}
