class TourAssigner:
    """
    Assign requested tours to drivers (Stammfahrer preferred, else backup pool).
    Backup pool = non-requested Stammfahrer + Springer + Abrufer.
    """

    def __init__(self, sorted_data: dict):
        self.data = sorted_data
        self.assignments = []
        self.unassigned = []

    def assign_tours(self, requested_tours: list[int]) -> dict:
        assignments = []
        assigned_names = set()

        requested_tour_strs = {str(t).strip() for t in requested_tours}

        stammfahrer = self.data.get("Stammfahrer", [])
        springer    = self.data.get("Springer", [])
        abrufer     = self.data.get("Abrufer", [])

        # Split Stammfahrer into those whose tour is requested vs. free
        matched_stammfahrer = [
            p for p in stammfahrer
            if str(p.get("Stammtour")).strip() in requested_tour_strs
        ]
        free_stammfahrer = [
            p for p in stammfahrer
            if str(p.get("Stammtour")).strip() not in requested_tour_strs
        ]

        # Combine all backups into one common pool
        backup_pool = free_stammfahrer + springer + abrufer

        # Assign tours
        for tour in requested_tours:
            tour_str = str(tour).strip()

            # Try to find matching Stammfahrer
            match = next(
                (
                    p for p in matched_stammfahrer
                    if str(p.get("Stammtour")).strip() == tour_str
                    and p["Name"] not in assigned_names
                ),
                None
            )

            if match:
                driver_name = match["Name"]
                assigned_names.add(driver_name)
            else:
                # Otherwise take any unused person from backup pool
                backup = next(
                    (p for p in backup_pool if p["Name"] not in assigned_names),
                    None
                )
                if backup:
                    driver_name = backup["Name"]
                    assigned_names.add(driver_name)
                else:
                    driver_name = None  # nobody left

            assignments.append({
                "tour": tour,
                "driver": driver_name
            })

        # Determine leftovers (unassigned from backup + unused matched)
        eligible_people = [
            p["Name"] for p in (matched_stammfahrer + backup_pool)
        ]
        self.unassigned = [
            name for name in eligible_people if name not in assigned_names
        ]

        # Add the fixed categories (unchanged)
        other_categories = {}
        for key in [
            "Frühdienst",
            "Spätdienst",
            "Innendienst",
            "Firmen",
            "Einweisung",
            "Dienstfrei",
        ]:
            other_categories[key] = [p["Name"] for p in self.data.get(key, [])]

        # Final result
        result = {
            "assignments": assignments,
            **other_categories,
            "unassigned": self.unassigned,
        }

        self.assignments = assignments
        return result
