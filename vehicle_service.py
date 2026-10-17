"""Manage vehicle service bookings and persist them as JSON records."""

import hashlib
import json
import shutil
from datetime import date
from pathlib import Path

SERVICE_RATES = {
    "Oil Change": 1500,
    "Wheel Alignment": 800,
    "General": 2500,
    "Brake Check": 1200,
}
service_records = {}


def add_service(vehicle_number, service_type="General", history=None):
    """Add a service booking and return this call's updated history."""
    if not isinstance(vehicle_number, str) or not vehicle_number.strip():
        raise ValueError("vehicle_number must be a non-empty string")
    if service_type not in SERVICE_RATES:
        raise ValueError(f"Unsupported service type: {service_type}")

    if history is None:
        history = []

    entry = {
        "type": service_type,
        "cost": SERVICE_RATES[service_type],
        "date": date.today().isoformat(),
    }
    service_records.setdefault(vehicle_number, []).append(entry)
    history.append(vehicle_number)
    return history


def cancel_service(vehicle_number, service_type):
    """Cancel matching jobs for a vehicle and report whether one existed."""
    try:
        jobs = service_records[vehicle_number]
    except KeyError:
        print(f"No records for {vehicle_number}")
        return False

    remaining = [job for job in jobs if job["type"] != service_type]
    service_records[vehicle_number] = remaining
    return len(remaining) < len(jobs)


def get_total_cost(vehicle_number):
    """Return the combined cost of all jobs booked for a vehicle."""
    return sum(job["cost"] for job in service_records.get(vehicle_number, []))


def job_card_id(vehicle_number):
    """Return a stable, non-security identifier for a vehicle's job card."""
    digest = hashlib.md5(vehicle_number.encode(), usedforsecurity=False)
    return digest.hexdigest()[:8]


def busiest_vehicle():
    """Return the vehicle with the most jobs, or None when none exist."""
    return max(
        service_records,
        key=lambda vehicle: len(service_records[vehicle]),
        default=None,
    )


def save_records(file_name="services.json"):
    """Write all service records to a UTF-8 encoded JSON file."""
    with open(file_name, "w", encoding="utf-8") as file_handle:
        json.dump(service_records, file_handle, indent=2)


def load_records(file_name="services.json"):
    """Load and return service records from a UTF-8 encoded JSON file."""
    with open(file_name, encoding="utf-8") as file_handle:
        return json.load(file_handle)


def backup_records(folder, source_file="services.json"):
    """Copy the service records file into an existing backup folder."""
    destination = Path(folder) / Path(source_file).name
    return shutil.copy2(source_file, destination)


def main():
    """Run a short demonstration of the vehicle service workflow."""
    add_service("KA01AB1234", "Oil Change")
    add_service("KA01AB1234", "Wheel Alignment")
    add_service("KA05XY9876")
    add_service("KA03MN4455", "Brake Check")
    cancel_service("KA05XY9876", "Brake Check")
    cancel_service("KA09ZZ0001", "General")
    cancel_service("KA03MN4455", "Brake Check")
    print("Total for KA01AB1234:", get_total_cost("KA01AB1234"))
    print("Total for KA05XY9876:", get_total_cost("KA05XY9876"))
    print("Job card for KA01AB1234:", job_card_id("KA01AB1234"))
    save_records()
    loaded = load_records()
    print(
        "Vehicles on file:",
        len(loaded),
        "| busiest vehicle:",
        busiest_vehicle(),
    )


if __name__ == "__main__":
    main()
