class TourAssigner:
    """
    Assign requested tours to drivers (Stammfahrer preferred, else backup pool).
    Backup pool = non-requested Stammfahrer + Springer + Abrufer.
    Uses EmployeeTaskLogManager for experience-based suggestions.
    """

    def __init__(self, sorted_data: dict, task_log_manager=None):
        """
        Args:
            sorted_data (dict): grouped employee data from sort_workers()
            task_log_manager (EmployeeTaskLogManager, optional): experience tracker
        """
        self.data = sorted_data
        self.task_log_manager = task_log_manager
        self.assignments = []
        self.unassigned = []

    def assign_tours(self, requested_tours: list[int]) -> dict:
        assignments = []
        assigned_names = set()

        requested_tour_strs = {str(t).strip() for t in requested_tours}

        stammfahrer = self.data.get("Stammfahrer", [])
        springer    = self.data.get("Springer", [])
        abrufer     = self.data.get("Abrufer", [])

        # Stammfahrer who have their tour requested vs. free
        matched_stammfahrer = [
            p for p in stammfahrer
            if str(p.get("Stammtour")).strip() in requested_tour_strs
        ]
        free_stammfahrer = [
            p for p in stammfahrer
            if str(p.get("Stammtour")).strip() not in requested_tour_strs
        ]

        # Combine all backups
        backup_pool = free_stammfahrer + springer + abrufer

        # 🎯 Assign tours
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
                # No Stammfahrer → look for the best backup
                driver_name = self._select_best_backup(backup_pool, assigned_names, tour_str)
                if driver_name:
                    assigned_names.add(driver_name)

            assignments.append({
                "tour": tour,
                "driver": driver_name or None
            })

        # Determine leftovers (unused backups)
        eligible_people = [p["Name"] for p in (matched_stammfahrer + backup_pool)]
        self.unassigned = [n for n in eligible_people if n not in assigned_names]

        # Non-tour categories for the API response
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

        return {
            "assignments": assignments,
            **other_categories,
            "unassigned": self.unassigned,
        }

    def _select_best_backup(self, backup_pool, assigned_names, tour_str) -> str | None:
        """
        Selects the most experienced available backup for a tour.
        Uses EmployeeTaskLogManager if available, else falls back to first-come.
        """
        available = [p for p in backup_pool if p["Name"] not in assigned_names]
        if not available:
            return None

        if self.task_log_manager:
            # Get top drivers for this tour from the log
            top_from_log = self.task_log_manager.get_top_employees_for_task(tour_str)
            top_names = [name for name, _ in top_from_log]

            # Prefer available backups who appear in the top list
            for preferred in top_names:
                match = next((p for p in available if p["Name"] == preferred), None)
                if match:
                    return match["Name"]

        # fallback: pick first available if no experience data
        return available[0]["Name"] if available else None
