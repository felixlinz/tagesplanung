from atoms import TourItem
import tkinter as tk

def test_tour_item():
    test_root = tk.Tk()
    test_root.title("Test TourItem")

    # Create an instance of TourItem for testing
    test_tour_item = TourItem(test_root, number=1, time="08:00", delete_callback=lambda number: print(f"Deleted Tour {number}"))
    test_tour_item.pack()

    test_root.mainloop()

# Call the test function
test_tour_item()