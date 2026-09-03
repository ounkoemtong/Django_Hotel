from app.rooms.models import Amenity, Room, RoomType
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Seed the database with Amenities, RoomTypes, and Rooms"

    def handle(self, *args, **options):
        self.stdout.write("Starting room data seeding...")

        # ១. បង្កើត Amenities មូលដ្ឋាន
        amenities_data = [
            {"name": "High-Speed WiFi", "icon": "fa-wifi"},
            {"name": "Air Conditioning", "icon": "fa-snowflake"},
            {"name": "Jacuzzi", "icon": "fa-hot-tub"},
            {"name": "Smart TV", "icon": "fa-tv"},
            {"name": "Balcony View", "icon": "fa-mountain"},
            {"name": "Mini Bar", "icon": "fa-wine-glass"},
        ]

        amenity_objs = {}
        for item in amenities_data:
            obj, _ = Amenity.objects.get_or_create(
                name=item["name"], defaults={"icon": item["icon"]}
            )
            amenity_objs[item["name"]] = obj

        self.stdout.write(
            self.style.SUCCESS(f"Created {len(amenity_objs)} Amenities.")
        )

        # ២. បង្កើត Room Types
        room_types_data = [
            {
                "name": "Standard Single",
                "description": "Cozy single room ideal for solo travelers on a budget.",
                "base_price": 25.00,
                "capacity": 1,
                "amenities": ["High-Speed WiFi", "Air Conditioning", "Smart TV"],
            },
            {
                "name": "Deluxe Double",
                "description": "Spacious room with king bed and city views.",
                "base_price": 50.00,
                "capacity": 2,
                "amenities": [
                    "High-Speed WiFi",
                    "Air Conditioning",
                    "Smart TV",
                    "Balcony View",
                    "Mini Bar",
                ],
            },
            {
                "name": "Presidential Suite",
                "description": "Luxury suite with private Jacuzzi and top-tier amenities.",
                "base_price": 120.00,
                "capacity": 4,
                "amenities": [
                    "High-Speed WiFi",
                    "Air Conditioning",
                    "Smart TV",
                    "Balcony View",
                    "Jacuzzi",
                    "Mini Bar",
                ],
            },
        ]

        room_type_objs = {}
        for rt_data in room_types_data:
            rt, _ = RoomType.objects.get_or_create(
                name=rt_data["name"],
                defaults={
                    "description": rt_data["description"],
                    "base_price": rt_data["base_price"],
                    "capacity": rt_data["capacity"],
                },
            )
            # ភ្ជាប់ ManyToMany Amenities ទៅកាន់ RoomType
            assigned_amenities = [
                amenity_objs[a_name] for a_name in rt_data["amenities"]
            ]
            rt.amenities.set(assigned_amenities)
            room_type_objs[rt.name] = rt

        self.stdout.write(
            self.style.SUCCESS(f"Created {len(room_type_objs)} Room Types.")
        )

        # ៣. បង្កើត Rooms ជាក់ស្តែង (ឧ. បន្ទប់ជាន់ទី ១ ដល់ទី ៣)
        room_counter = 0
        room_setup = [
            # ជាន់ទី ១ (Standard Rooms: 101 - 105)
            {"type": "Standard Single", "prefix": 100, "count": 5},
            # ជាន់ទី ២ (Deluxe Rooms: 201 - 204)
            {"type": "Deluxe Double", "prefix": 200, "count": 4},
            # ជាន់ទី ៣ (Suites: 301 - 302)
            {"type": "Presidential Suite", "prefix": 300, "count": 2},
        ]

        for setup in room_setup:
            rt_instance = room_type_objs[setup["type"]]
            for i in range(1, setup["count"] + 1):
                room_num = str(setup["prefix"] + i)
                _, created = Room.objects.get_or_create(
                    room_number=room_num,
                    defaults={
                        "room_type": rt_instance,
                        "status": Room.RoomStatus.AVAILABLE,
                    },
                )
                if created:
                    room_counter += 1

        self.stdout.write(
            self.style.SUCCESS(f"Successfully created {room_counter} physical Rooms!")
        )