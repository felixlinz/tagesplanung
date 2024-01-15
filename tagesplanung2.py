from gui2 import Application, Page
from styles import set_styles  # Import this if you have a separate styles.py

# Set up styles


# If you have a separate styles.py
# from styles import set_styles
# Set up styles
# set_styles()

# Create and run the application
app = Application()

# Add pages (You can create custom pages by subclassing Page)
app.add_page(Page, 'Page 1')
app.add_page(Page, 'Page 2')

# Show the initial page
app.show_page('Page 1')

app.mainloop()
